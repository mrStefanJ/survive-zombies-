import json

FILE = "data/save.json"

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "highscore": 0,
            "coins": 0,
            "unlocked_skins": ["default"],
            "selected_skin": "default"
        }

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)