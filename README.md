# Stock Dashboard

Dashboard to track the stock market and send notifications when the stock price is above or below a certain threshold.

Data for stocks is scrapped from [Google Finance](https://www.google.com/finance/).

## How to use

### for sending stock alert in discord channel

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python stock_alert.py 
```

### for running dashboard

```bash
python dashboard.py
```

## Dashboard Table

![Dashboard Table](/images/sample.png)

# Dashboard Graph

![Dashboard Graph](/images/sample2.png)


- Update the webhook url in the utils.py, webhook url can be found in the discord channel.
- Update the config.json with your favorite stocks and thresholds.

## Upcoming features



## Why this project?

to track your favorite stocks in one click and send notifications when the stock price is above or below a certain threshold and to keep update yourself with the stock market without any hassle. 

## Author

- [Deepak Raj](https://github.com/codeperfectplus)
