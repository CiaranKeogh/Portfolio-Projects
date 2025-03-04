"""
Scheduler module for Drug Tariff Master.
This module handles scheduled tasks like automatic data updates.
"""
import logging
import signal
import time
from datetime import datetime
from threading import Event, Thread

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

import config

# Set up logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger('scheduler')

# Create a stop event for graceful shutdown
stop_event = Event()


def signal_handler(signum, frame):
    """
    Handle termination signals for graceful shutdown.
    
    Args:
        signum: Signal number
        frame: Current stack frame
    """
    logger.info(f"Received signal {signum}. Initiating shutdown...")
    stop_event.set()


def start_scheduler(job_function):
    """
    Start the background scheduler for periodic updates.
    
    Args:
        job_function: The function to call on schedule
        
    Returns:
        None
    """
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("Starting scheduler")
    
    # Parse the CRON expression from config
    cron_parts = config.DOWNLOAD_CRON.split()
    if len(cron_parts) != 5:
        logger.error(f"Invalid CRON expression: {config.DOWNLOAD_CRON}")
        return
    
    minute, hour, day, month, day_of_week = cron_parts
    
    # Create scheduler
    scheduler = BackgroundScheduler()
    
    # Add job
    trigger = CronTrigger(
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week
    )
    
    scheduler.add_job(
        job_function,
        trigger=trigger,
        id='update_job',
        name='Drug Tariff Data Update',
        max_instances=1,
        coalesce=True
    )
    
    # Start the scheduler
    scheduler.start()
    logger.info(f"Scheduler started. Next run at: {scheduler.get_job('update_job').next_run_time}")
    
    # Calculate and log the next run time in human-readable format
    next_run = scheduler.get_job('update_job').next_run_time
    now = datetime.now()
    delta = next_run - now
    
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    time_str = ""
    if days > 0:
        time_str += f"{days} days, "
    if hours > 0:
        time_str += f"{hours} hours, "
    time_str += f"{minutes} minutes from now"
    
    print(f"Next scheduled update: {next_run.strftime('%Y-%m-%d %H:%M:%S')} ({time_str})")
    
    try:
        # Keep the main thread alive
        while not stop_event.is_set():
            time.sleep(1)
            
    except (KeyboardInterrupt, SystemExit):
        logger.info("Received shutdown signal")
    
    finally:
        # Shutdown scheduler
        logger.info("Shutting down scheduler")
        scheduler.shutdown()
        print("Scheduler stopped.")


def run_once_then_schedule(job_function, cron_expression=None):
    """
    Run a job immediately, then schedule it to run periodically.
    
    Args:
        job_function: The function to call
        cron_expression: Optional custom cron expression, uses config default if not provided
        
    Returns:
        None
    """
    # Run immediately
    print("Running initial update...")
    job_function()
    
    # Then schedule
    start_scheduler(job_function)


if __name__ == "__main__":
    # Test the scheduler with a dummy job
    def dummy_job():
        print(f"Dummy job executed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("Dummy job executed")
    
    print("Testing scheduler with dummy job (Ctrl+C to stop)")
    start_scheduler(dummy_job) 