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

if __name__ == '__main__':
    while True:
        market_open_timing = '09:00:00'
        market_close_timing = '15:30:00'
        current_time = datetime.datetime.now(IST).strftime('%H:%M:%S')
        current_day = datetime.datetime.now(IST).strftime('%A')
        if current_day in ['Saturday', 'Sunday']:
            print('Market is closed')
            print('Market will open on Monday at {}'.format(market_open_timing))
            time.sleep(300)
            continue

        elif current_time < market_open_timing or current_time > market_close_timing:
            print('Market is closed')
            differnce = datetime.datetime.strptime(market_open_timing, '%H:%M:%S') - datetime.datetime.strptime(current_time, '%H:%M:%S')
            differnce = differnce.total_seconds()/60
            print('Market will open in {} minutes'.format(differnce))
            # start a timer and print in the reverse order
            print_time_left(differnce)
            continue
        else:
            check_overall()
            main()
            time.sleep(20)
