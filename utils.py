import json
from discord import Webhook, RequestsWebhookAdapter

discord_webhook_url = "https://discord.com/api/webhooks/940522536557498368/un_14JP-n7T6haQzIhsDB9Dfj_XjWB_2wYFK6oD-opeC-ZfRhgH29_LSbWnNGnOzGi5B"

def update_config(data):
    with open('config.json', 'w') as f:
        json.dump(data, f)


def read_config():
    with open('config.json', 'r') as f:
        configs = json.load(f)
    
    return configs


def send_meeage_to_discord(message):
    """ Send message to discord webhook """
    webhook = Webhook.from_url(discord_webhook_url, adapter=RequestsWebhookAdapter())
    webhook.send(message)