# =========================
# FILE: data/highscore.py
# =========================
import json

FILE = "data/save.json"

def load_highscore():
    try:
        with open(FILE, "r") as f:
            return json.load(f).get("highscore", 0)
    except:
        return 0


def save_highscore(score):
    with open(FILE, "w") as f:
        json.dump({"highscore": score}, f)