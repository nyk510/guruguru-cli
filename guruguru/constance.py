import json
import os

home = os.environ['HOME']
config_dir = os.path.join(home, '.guruguru')
os.makedirs(config_dir, exist_ok=True)

BASE_URL = os.getenv('GURUGURU_BASE_URL', 'https://api.guruguru.ml/')


class Config(object):

    @property
    def config_path(self):
        return os.path.join(config_dir, 'config.json')

    def load(self):
        with open(self.config_path, 'r') as f:
            data = json.load(f)
        return data

    def save(self, config: dict):
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f'Save config to {self.config_path}')


config = Config()
