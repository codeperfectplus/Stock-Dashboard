import time
import pytz
import datetime
from fetch_data import fetch_data
from utils import read_config, update_config, send_message_to_discord

IST = pytz.timezone('Asia/Kolkata')

current_time = datetime.datetime.now(IST).strftime('%H:%M:%S')

def check_alert(config):
    stock_data = fetch_data(config['stock'])
    print('Checking alert for {}'.format(config['stock']))
    # update csv
    with open('data/stock.csv', 'a') as f:
        f.write('{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
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
            stock_data['current_price'] - stock_data['previous_close'],
            config['watch']
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
        send_message_to_discord(message)
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
        send_message_to_discord(message)
        print("Max Price updated to {}".format(config['max_price']))

def main():
    configs = read_config()
    for config in configs:
        check_alert(config)
    update_config(configs)

if __name__ == '__main__':
    while True:
        if current_time > '08:55:00' and current_time < '15:30:00':
            main()
            time.sleep(30)
        else:
            print('Market is closed')
            time.sleep(300)