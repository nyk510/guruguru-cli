import json
import os

home = os.path.expanduser('~')
config_dir = os.path.join(home, '.guruguru')
os.makedirs(config_dir, exist_ok=True)

BASE_URL = os.getenv('GURUGURU_BASE_URL', 'https://api.guruguru.science/')


class Config:
    @property
    def config_path(self):
        return os.path.join(config_dir, 'config.json')

    @property
    def exist_token(self):
        return os.path.exists(self.config_path)

    def load(self) -> dict:
        with open(self.config_path, 'r') as f:
            data = json.load(f)
        return data

    def save(self, config: dict) -> str:
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return self.config_path

    @property
    def data(self):
        if not os.path.exists(self.config_path):
            return None
        _data = self.load()
        return _data

    def get_token(self):
        if self.data is not None: return self.data.get('token', None)
        return None


config = Config()
