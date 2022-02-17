import json
from discord import Webhook, RequestsWebhookAdapter

discord_webhook_url = "https://discord.com/api/webhooks/940876122122485760/JdzaPVTIcdaQiKCFcP-f5MbRUW5BGpuAKCcNuJVNucSMBmcr4qPNp3IaGCJQnm6MJJbR"

def update_config(data):
    with open('config.json', 'w') as f:
        json.dump(data, f)


def read_config():
    with open('config.json', 'r') as f:
        configs = json.load(f)
    
    return configs


def send_message_to_discord(message):
    """ Send message to discord webhook """
    print("Sending message to discord: {}".format(message))
    print(message)
    webhook = Webhook.from_url(discord_webhook_url, adapter=RequestsWebhookAdapter())
    webhook.send(message)
