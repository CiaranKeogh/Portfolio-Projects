"""
Main entry point for the Drug Tariff Master application.

This script provides a CLI interface to run different components
of the Drug Tariff Master application.
"""
import sys
import argparse
from pathlib import Path

from drug_tariff_master import download_dmd
from drug_tariff_master import setup_database
from drug_tariff_master import load_data
from drug_tariff_master.utils import setup_logger

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
    
    # Setup database command
    setup_db_parser = subparsers.add_parser("setup-db", help="Set up the database")
    
    # Load data command
    load_parser = subparsers.add_parser("load", help="Load data into the database")
    
    # Future commands will be added here
    # search_parser = subparsers.add_parser("search", help="Search the database")
    # search_parser.add_argument("term", help="Search term")
    
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    
    if args.command == "download":
        logger.info("Running download command")
        return download_dmd.main()
    elif args.command == "setup-db":
        logger.info("Running setup-db command")
        return setup_database.main()
    elif args.command == "load":
        logger.info("Running load command")
        return load_data.main()
    # elif args.command == "search":
    #     logger.info("Running search command")
    #     return search_dmd.main([args.term])
    else:
        logger.error(f"Unknown command: {args.command}")
        print("Available commands: download, setup-db, load")
        return 1


def cli_entry_point():
    """Entry point for CLI when installed as a package."""
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main()) 