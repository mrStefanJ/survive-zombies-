import json

FILE = "data/save.json"

def load_data():
    try:
        with open("save.json", "r") as f:
            data = json.load(f)
    except:
        data = {}

    # DEFAULTS
    data.setdefault("coins", 0)
    data.setdefault("owned_skins", ["Green Skin"])
    data.setdefault("selected_skin", "Green Skin")
    data.setdefault("leaderboard", [])
    data.setdefault("highscore", 0)

    return data

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)