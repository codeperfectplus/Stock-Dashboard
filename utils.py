import json

def update_config(data):
    with open('config.json', 'w') as f:
        json.dump(data, f)


def read_config():
    with open('config.json', 'r') as f:
        configs = json.load(f)
    
    return configs