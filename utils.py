import os
import json
from discord import Webhook, RequestsWebhookAdapter

discord_webhook_url = ""

root_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(root_dir, 'config.json')

def update_config(data):
    with open(config_path, 'w') as f:
        json.dump(data, f)


def read_config():
    with open(config_path, 'r') as f:
        configs = json.load(f)
    
    return configs


def send_message_to_discord(message):
    """ Send message to discord webhook """
    print("Sending message to discord: {}".format(message))
    print(message)
    webhook = Webhook.from_url(discord_webhook_url, adapter=RequestsWebhookAdapter())
    webhook.send(message)
