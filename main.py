import time
import schedule
import fetch_data
from fetch_data import fetch_data
from preprocess_data import preprocess_csv, preprocess_json
from datetime import datetime

def main():
    global api_calls
    if 'api_calls' not in globals():
        api_calls = 0
    fetch_data()
    preprocess_json()
    preprocess_csv()

    # Print validation
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print("Data processed successfully on: ", formatted_datetime)
    print("API calls: ", api_calls)
    print("--")
    print("\ndsadasd")
    api_calls+=1

schedule.every(5).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)