# settings.py -- Centralized settings loader for Fermentation Chamber Project

print("E ========== START IMPORT 'settings.py'                   ========== E")

import ujson

# Load config.json to get the local settings file name
try:
    with open("config.json", "r") as f:
        config = ujson.load(f)
    LOCAL_SETTINGS_FILE = config.get("LOCAL_SETTINGS_FILE", "fermenter_settings.ujson")
except Exception as e:
    print("[WARNING] Could not load config.json:", e)
    LOCAL_SETTINGS_FILE = "fermenter_settings.ujson"

_settings = {}


# Load settings from the local settings file
def load():
    global _settings
    try:
        with open(LOCAL_SETTINGS_FILE, "r") as f:
            _settings = ujson.load(f)
    except Exception as e:
        print("[ERROR] Could not load local settings:", e)
        _settings = {}


# Get a value from settings
def get(key, default=None):
    return _settings.get(key, default)


# Get all settings as a dict
def all():
    return _settings


# Optionally, provide structured access for cold/warm/other settings


def cold_settings():
    # Collect keys ending with '_cold' and strip the suffix for easier access
    return {
        k.replace("_cold", ""): v for k, v in _settings.items() if k.endswith("_cold")
    }


def warm_settings():
    # Collect keys ending with '_warm' and strip the suffix for easier access
    return {
        k.replace("_warm", ""): v for k, v in _settings.items() if k.endswith("_warm")
    }


def other_settings():
    # Example: everything else
    return {k: v for k, v in _settings.items() if "_cold" not in k and "_warm" not in k}


# Load settings once at import
def _init():
    load()


_init()

print("E ==========   END IMPORT 'settings.py'                   ========== E")
