import json
import os

SAVE_DIR = "data"
FILE = os.path.join(SAVE_DIR, "save.json")


def load_data():
    os.makedirs(SAVE_DIR, exist_ok=True)

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}

    # DEFAULTS
    data.setdefault("coins", 0)
    data.setdefault("owned_skins", ["Green Skin"])
    data.setdefault("selected_skin", "Green Skin")
    data.setdefault("leaderboard", [])
    data.setdefault("highscore", 0)
    data.setdefault("sound", True)

    return data


def save_data(data):
    os.makedirs(SAVE_DIR, exist_ok=True)

    temp_file = FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(data, f, indent=4)

    os.replace(temp_file, FILE)  # atomic save