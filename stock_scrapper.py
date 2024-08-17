import os
from logging import root, shutdown
import time
import shutil
import pytz
import datetime
from src.fetch_data import fetch_data
from src.utils import read_config, update_config, root_dir

IST = pytz.timezone('Asia/Kolkata')


def check_alert(config):
    stock_data = fetch_data(config['symbol'])
    print('Checking alert for {}'.format(config['symbol']))
    # update csv
    difference = stock_data['current_price'] - stock_data['previous_close']
    difference_percentage = (difference / stock_data['previous_close']) * 100
    with open(os.path.join(root_dir, 'data/stock.csv'), 'a') as f:
        f.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
            config['stock_name'],
            stock_data['previous_close'],
            stock_data['current_price'],
            stock_data['day_min'],
            stock_data['day_max'],
            stock_data['year_min'],
            stock_data['year_max'],
            config['min_price'],
            config['max_price'],
            stock_data['date_time'],
            difference,
            difference_percentage,
            config['buy'],
            config['market'],
            config['currency']
            ))
        
    if stock_data['current_price'] < config['min_price']:
        difference = config['min_price'] - stock_data['current_price']
        difference = round(difference, 2)
        message = ':small_red_triangle_down: __**{}**__ \nCurrent Value: {}\nMin threshold: {}\ndifference: {}'.format(
                            config['stock_name'], 
                            stock_data['current_price'],
                            config['min_price'], 
                            difference)
        config['min_price'] = stock_data['current_price']
        #send_message_to_discord(message)
        print("Min Price updated to {}".format(config['min_price']))

    if stock_data['current_price'] > config['max_price']:
        difference = stock_data['current_price'] - config['max_price']
        difference = round(difference, 2)
        message = ':arrow_up_small: __**{}**__ \nCurrent Value: {}\nMax threshold: {}\ndifference: {}'.format(
                            config['stock_name'], 
                            stock_data['current_price'],
                            config['max_price'], 
                            difference)
        
        config['max_price'] = stock_data['current_price']
        #send_message_to_discord(message)
        print("Max Price updated to {}".format(config['max_price']))

def check_overall():
    symbols = {'BSE SENSEX': 'SENSEX:INDEXBOM', 'NIFTY 50': 'NIFTY_50:INDEXNSE'}
    for stock_name, symbol in symbols.items():
        stock_data = fetch_data(symbol)
        print('Checking alert for {}'.format(symbol))
        differnce = stock_data['current_price'] - stock_data['previous_close']
        differnce_percentage = (differnce / stock_data['previous_close']) * 100
        with open(os.path.join(root_dir, 'data/market.csv'), 'a') as f:
            f.write('{},{},{},{},{},{},{},{},{},{}\n'.format(
                stock_name,
                stock_data['previous_close'],
                stock_data['current_price'],
                stock_data['day_min'],
                stock_data['day_max'],
                stock_data['year_min'],
                stock_data['year_max'],
                stock_data['date_time'],
                differnce,
                differnce_percentage
                )) 

def main():
    configs = read_config()
    for config in configs:
        check_alert(config)
    update_config(configs)


def print_time_left(minutes_left, print_time_delay=1):
    seconds_left = minutes_left * 60
    while seconds_left > 0:
        print("Remaining time: {} mins".format(round(seconds_left / 60, 2)), end='\r')
        time.sleep(print_time_delay)
        seconds_left -= print_time_delay
        minutes_left -= print_time_delay / 60

import datetime
import time

# Function to print the time left in a countdown
def print_time_left(minutes_left):
    for minute in range(int(minutes_left), 0, -1):
        print(f'Market will open in {minute} minutes')
        time.sleep(60)

# Main function
def market_monitor():
    IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))  # Define the IST timezone
    market_open_time = datetime.time(9, 0, 0)   # Market opens at 09:00:00
    market_close_time = datetime.time(15, 30, 0)  # Market closes at 15:30:00

    while True:
        current_time = datetime.datetime.now(IST).time()
        current_day = datetime.datetime.now(IST).strftime('%A')

        if current_day in ['Saturday', 'Sunday']:
            check_overall()
            main()
            print('Market is closed')
            print('Market will open on Monday at 09:00 AM')
            time.sleep(1200)
            continue

        if current_time < market_open_time:
            time_until_open = (datetime.datetime.combine(datetime.date.today(), market_open_time) - 
                               datetime.datetime.now(IST)).total_seconds() / 60
            print('Market is closed')
            print(f'Market will open in {int(time_until_open)} minutes')
            print_time_left(time_until_open)
            continue

        elif current_time > market_close_time:
            print('Market is closed')
            print('Market will open tomorrow at 09:00 AM')
            time_until_open = (datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), market_open_time) - 
                               datetime.datetime.now(IST)).total_seconds() / 60
            print_time_left(time_until_open)
            continue

        else:
            print('Market is open')
            check_overall()
            main()
            time.sleep(20)  # Sleep for 20 seconds before checking again

if __name__ == '__main__':
    market_monitor()
