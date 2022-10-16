import os
import json
from discord import Webhook
from discord_webhook import DiscordWebhook
from time import sleep

discord_webhook_url = ""

root_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(root_dir, 'src/config.json')

def update_config(data):
    with open(config_path, 'w') as f:
        json.dump(data, f)


def read_config():
    with open(config_path, 'r') as f:
        configs = json.load(f)
    
    return configs


def send_message_to_discord(message):
    webhook = DiscordWebhook(url=discord_webhook_url, content=message)
    response = webhook.execute()

def edit_webhook_message(message):
    webhook = DiscordWebhook(url=discord_webhook_url, content='')
    sent_webhook = webhook.execute()
    webhook.content = 'After Edit'
    sleep(10)
    sent_webhook = webhook.edit(sent_webhook)
