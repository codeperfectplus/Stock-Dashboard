import pytz
import datetime

IST = pytz.timezone('Asia/Kolkata')

current_time = datetime.datetime.now(IST).strftime('%H:%M:%S')

current_time = "09:39:00"
current_time = datetime.datetime.strptime(current_time, '%H:%M:%S')
if current_time > '09:00:00' and current_time < '15:30:00':
    print('Market is open')