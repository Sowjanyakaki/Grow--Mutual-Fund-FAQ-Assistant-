import schedule
import time
import subprocess
from datetime import datetime
import pytz
import os
import sys

def run_ingestion():
    ist_time = datetime.now(pytz.timezone('Asia/Kolkata'))
    print(f"[{ist_time.strftime('%Y-%m-%d %H:%M:%S')}] Starting scheduled data ingestion...")
    
    # Run the ingestion script using the same python interpreter
    try:
        subprocess.run([sys.executable, "ingest.py"], check=True)
        print(f"[{datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')}] Ingestion completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running ingestion script: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    print("Initializing Mutual Fund FAQ Scheduler...")
    
    # Schedule the job to run daily at 10:00 AM IST
    schedule.every().day.at("10:00", "Asia/Kolkata").do(run_ingestion)
    
    print("Scheduler started. The ingestion script will run daily at 10:00 AM IST.")
    print("Press Ctrl+C to exit.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1) # Sleep for a second to prevent high CPU usage
    except KeyboardInterrupt:
        print("\nScheduler stopped manually.")
