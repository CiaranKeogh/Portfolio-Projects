import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pathlib import Path

from .trud_client import TRUDClient
from ..config.config import RAW_DATA_DIR

logger = logging.getLogger(__name__)

class DownloadManager:
    """Manages the scheduling and execution of TRUD file downloads"""
    
    def __init__(self, trud_client=None):
        """Initialize the download manager
        
        Args:
            trud_client (TRUDClient, optional): The TRUD API client. Creates a new one if not provided.
        """
        self.trud_client = trud_client or TRUDClient()
        self.scheduler = BackgroundScheduler()
        
    def start_scheduler(self):
        """Start the background scheduler for regular downloads"""
        if not self.scheduler.running:
            # Schedule downloads every Monday at 02:00 UTC
            self.scheduler.add_job(
                self.download_all_files,
                trigger=CronTrigger(day_of_week='mon', hour=2, minute=0),
                id='trud_weekly_download',
                replace_existing=True
            )
            self.scheduler.start()
            logger.info("Download scheduler started. Next run: Monday at 02:00 UTC")
        else:
            logger.warning("Scheduler is already running")
    
    def stop_scheduler(self):
        """Stop the background scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Download scheduler stopped")
        else:
            logger.warning("Scheduler is not running")
    
    def download_all_files(self):
        """Download all required TRUD files
        
        Returns:
            dict: Dictionary mapping file types to download success status
        """
        logger.info("Starting scheduled download of all TRUD files")
        results = self.trud_client.download_all_files(RAW_DATA_DIR)
        
        # Log results
        success_count = sum(1 for success in results.values() if success)
        logger.info(f"Downloaded {success_count}/{len(results)} files successfully")
        
        for file_type, success in results.items():
            if not success:
                logger.error(f"Failed to download {file_type}")
        
        return results
    
    def download_file_now(self, file_type):
        """Download a specific file immediately
        
        Args:
            file_type (str): The type of file to download (e.g., 'vmp', 'vmpp')
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        from ..config.config import TRUD_DOWNLOAD_ITEMS
        
        if file_type not in TRUD_DOWNLOAD_ITEMS:
            logger.error(f"Unknown file type: {file_type}")
            return False
        
        file_info = TRUD_DOWNLOAD_ITEMS[file_type]
        file_path = RAW_DATA_DIR / file_info["name"]
        
        logger.info(f"Starting immediate download of {file_type}")
        return self.trud_client.download_file(file_info["file_id"], file_path) 