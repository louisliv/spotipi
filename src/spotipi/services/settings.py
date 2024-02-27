from typing import Dict, Any

from spotipi.utils import Settings


def get_all_settings() -> Dict[str, Any]:
    settings = Settings()
    return settings.read()


def get_setting(key: str) -> Any:
    settings = Settings()
    return settings.get_value(key)


def set_setting(key: str, value: Any) -> Dict[str, Any]:
    settings = Settings()
    settings.set_value(key, value)
    return settings.read()


def set_all_settings(settings_to_set: Dict[str, Any]) -> Dict[str, Any]:
    settings = Settings()
    settings.set_all(settings_to_set)
    return settings.read()
