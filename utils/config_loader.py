import yaml
import json

def load_config():
    with open('config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config