# coding: utf-8
import time

from fetch_data import fetch_data
from utils import read_config, update_config, send_meeage_to_discord


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

    print('Current Price: {}'.format(stock_data['current_price']))
    print('Min Threshold: {} | Max Threshold: {}'.format(config['min_price'], config['max_price']))
    print('Day Up: {} | Down: {}'.format(stock_data['day_min'], stock_data['day_max']))
    print('-'*50)
        
    difference = config['min_price']- stock_data['current_price']
    if stock_data['current_price'] < config['min_price']:
        message = '{} is currently down at: {}, min threshold: {}, difference: {}'.format(
                            config['stock_name'], 
                            stock_data['current_price'],
                            config['min_price'], 
                            difference)
        config['min_price'] = stock_data['current_price']
        send_meeage_to_discord(message)
        print(message)
        print("Min Price updated to {}".format(config['min_price']))
    if stock_data['current_price'] > config['max_price']:
        difference = stock_data['current_price']- config['max_price']
        message = '{} is currently Up at: {}, max threshold: {}, difference: {}'.format(
                            config['stock_name'], 
                            stock_data['current_price'],
                            config['max_price'], 
                            difference)
        
        config['max_price'] = stock_data['current_price']
        send_meeage_to_discord(message)
        print(message)
        print("Max Price updated to {}".format(config['max_price']))

def main():
    configs = read_config()
    for config in configs:
        print("Checking {}".format(config['stock_name']), end='\n')
        check_alert(config)
    update_config(configs)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(60)