import pytz
import datetime

IST = pytz.timezone('Asia/Kolkata')
date = datetime.datetime.now(IST).strftime("%Y-%m-%d")

min_date = date + " 09:00:00"
max_date = date + " 16:00:00"
