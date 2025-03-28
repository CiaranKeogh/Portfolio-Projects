"""
Main entry point for the Drug Tariff Master application.

This script provides a CLI interface to run different components
of the Drug Tariff Master application.
"""
import sys
import argparse
from pathlib import Path

# Add the current directory to the path to allow imports from the project
sys.path.insert(0, str(Path(__file__).resolve().parent))

import download_dmd
from utils import setup_logger

# Set up logger
logger = setup_logger("main", "main.log")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Drug Tariff Master - dm+d data processing tool"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Download command
    download_parser = subparsers.add_parser("download", help="Download dm+d files")
    
    # Future commands will be added here
    # setup_db_parser = subparsers.add_parser("setup-db", help="Set up the database")
    # load_parser = subparsers.add_parser("load", help="Load data into the database")
    # search_parser = subparsers.add_parser("search", help="Search the database")
    # search_parser.add_argument("term", help="Search term")
    
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    
    if args.command == "download":
        logger.info("Running download command")
        return download_dmd.main()
    # elif args.command == "setup-db":
    #     logger.info("Running setup-db command")
    #     return setup_database.main()
    # elif args.command == "load":
    #     logger.info("Running load command")
    #     return load_data.main()
    # elif args.command == "search":
    #     logger.info("Running search command")
    #     return search_dmd.main([args.term])
    else:
        logger.error(f"Unknown command: {args.command}")
        print("Available commands: download")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 