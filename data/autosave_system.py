import time
from data.save_system import save_data


class AutoSaveSystem:
    def __init__(self, game, interval=10):
        self.game = game
        self.interval = interval
        self.timer = 0

    def update(self, dt):
        self.timer += dt

        if self.timer >= self.interval:
            self.save()
            self.timer = 0

    def save(self):
        save_data(self.game.data)
        print("💾 Autosaved")