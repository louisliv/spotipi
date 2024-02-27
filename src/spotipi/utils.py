from typing import Dict, Any
import json

CONFIG_JSON_FILE = "config.json"
SETTINGS_JSON_FILE = "settings.json"

class Config:
    def __init__(self):
        self.path = CONFIG_JSON_FILE
        
    def read(self) -> Dict[str, Any]:
        with open(self.path) as json_file:
            data = json.load(json_file)
            return data
        
    @property
    def reading_mode(self):
        return self.read().get("reading_mode")
    
    def set_reading_mode(self, reading_mode):
        data = {}
        data["reading_mode"] = reading_mode
        with open(self.path, "w") as json_file:
            json.dump(data, json_file)
            
    def get_value(self, key):
        return self.read().get(key)
    
    def set_value(self, key, value):
        data = self.read()
        data[key] = value
        with open(self.path, "w") as json_file:
            json.dump(data, json_file)
            
    def set_all(self, settings_to_set: Dict[str, Any]):
        data = self.read()
        for key, value in settings_to_set.items():
            data[key] = value
        with open(self.path, "w") as json_file:
            json.dump(data, json_file)
            
class Settings(Config):
    def __init__(self):
        self.path = SETTINGS_JSON_FILE


def convert_redis_to_bool(redis_value: str) -> bool:
    if redis_value == "True":
        return True
    return False
