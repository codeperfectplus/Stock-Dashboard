import json
from discord import Webhook, RequestsWebhookAdapter

discord_webhook_url = "https://discord.com/api/webhooks/946623261708550144/DDMYbeTMk2nA4l-4iG2WlqkXlAVbmuwK_6oIV1fndRyeA8lmPmXl8WJU_pmPGUXRO9lj"

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
