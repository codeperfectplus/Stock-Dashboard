import os
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

discord_webhook_url = "https://discord.com/api/webhooks/832610199613210646/WuPRjWtvLe3NFAqyUqXtkC_l5irBQcor-XKBLv5IvZ1-p2F8R0q7Y3MepckZNbVy4AO9"

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
    """ Send message to discord """
    webhook = DiscordWebhook(url=discord_webhook_url, username="Stock Bot")
    embed = DiscordEmbed(title='Stock Dashboard Alert', description=message, color='03b2f8')
    embed.set_author(name='Stock Bot', url='https://github.com/Py-Contributors/Stock-Dashboard')
    webhook.add_embed(embed)
    webhook.execute()

