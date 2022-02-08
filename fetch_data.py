import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

base_url = "https://www.google.com/finance/quote/"

def fetch_data(stock):
    final_url = base_url + stock
    data = {}
    html_data = requests.get(final_url).text
    soup = BeautifulSoup(html_data, "html.parser")
    data["title"] = soup.title.string

    current_price = soup.find('div', class_='YMlKec fxKbKc').text
    current_price = re.findall('\d+\.\d+', current_price)
    data['current_price'] = float(current_price[0])

    sidebar_data = soup.find('div', 'eYanAe').text
    sidebar_data = re.findall('\d+\.\d+', sidebar_data)
    sidebar_data = [float(data) for data in sidebar_data]

    data['previous_close'] = sidebar_data[0]
    data['day_min'] = sidebar_data[1]
    data['day_max'] = sidebar_data[2]
    data['year_min'] = sidebar_data[3]
    data['year_max'] = sidebar_data[4]
    data['market_cap'] = sidebar_data[5]
    data['date_time'] = datetime.now()
    
    return data