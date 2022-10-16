#!/bin/bash

touch /app/data/stock.csv
touch /app/data/market.csv

cd /app

nohup python3 stock_scrapper.py &
tail -100f nohup.out
