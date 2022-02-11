# coding: utf-8
import time
import pytz
from datetime import datetime
from fetch_data import fetch_data
from utils import read_config, update_config, send_meeage_to_discord

IST = pytz.timezone('Asia/Kolkata')

current_time = datetime.now(IST).strftime('%H:%M:%S')


def check_alert(config):
    stock_data = fetch_data(config['stock'])
    # update csv
    with open('data/stock.csv', 'a') as f:
        f.write('{},{},{},{},{},{},{},{},{}\n'.format(
            config['stock_name'],
            stock_data['previous_close'],
            stock_data['current_price'],
            stock_data['day_min'],
            stock_data['day_max'],
            config['min_price'],
            config['max_price'],
            stock_data['date_time'],
            stock_data['current_price'] - stock_data['previous_close']
            ))
        
    if stock_data['current_price'] < config['min_price']:
        difference = config['min_price'] - stock_data['current_price']
        difference = round(difference, 2)
        message = ':red_circle: {} is currently down at: {}, min threshold: {}, difference: {}'.format(
                            config['stock_name'], 
                            stock_data['current_price'],
                            config['min_price'], 
                            difference)
        config['min_price'] = stock_data['current_price']
        send_meeage_to_discord(message)
        print("Min Price updated to {}".format(config['min_price']))

    if stock_data['current_price'] > config['max_price']:
        difference = stock_data['current_price'] - config['max_price']
        difference = round(difference, 2)
        message = ':green_circle: {} is currently Up at: {}, max threshold: {}, difference: {}'.format(
                            config['stock_name'], 
                            stock_data['current_price'],
                            config['max_price'], 
                            difference)
        
        config['max_price'] = stock_data['current_price']
        send_meeage_to_discord(message)
        print("Max Price updated to {}".format(config['max_price']))

def main():
    print('Updating Config... {}'.format(current_time), end='\r')
    configs = read_config()
    for config in configs:
        check_alert(config)
    update_config(configs)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(60)