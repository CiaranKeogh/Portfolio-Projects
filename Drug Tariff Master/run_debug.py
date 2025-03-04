"""
Debug script for Drug Tariff Master web application
"""
import os
import sys
import traceback

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Attempting to import required modules...")
    
    import config
    print("✓ Imported config")
    
    import database
    print("✓ Imported database")
    
    import search
    print("✓ Imported search")
    
    import trud
    print("✓ Imported trud")
    
    import web_app
    print("✓ Imported web_app")
    
    # Check if data directory exists
    print(f"\nChecking data directory: {config.DATA_DIR}")
    if not os.path.exists(config.DATA_DIR):
        os.makedirs(config.DATA_DIR, exist_ok=True)
        print(f"Created data directory: {config.DATA_DIR}")
    else:
        print(f"✓ Data directory exists: {config.DATA_DIR}")
    
    # Check if database file exists
    db_path = os.path.join(config.DATA_DIR, 'dmd_data.db')
    print(f"Checking database file: {db_path}")
    if not os.path.exists(db_path):
        print(f"⚠ Database file does not exist. Will initialize database.")
        database.initialize_database()
        print(f"✓ Database initialized: {db_path}")
    else:
        print(f"✓ Database file exists: {db_path}")
    
    # Initialize the web server
    print("\nStarting web server...")
    print("Web interface will be available at http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    
    web_app.run_web_app(debug=True)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nTraceback:")
    traceback.print_exc()
    print("\nPlease fix the above error and try again.") 