# =========================
# FILE: systems/spawn_system.py
# =========================
class SpawnSystem:
    def __init__(self, game, zombie_manager):
        self.game = game
        self.zombie_manager = zombie_manager
        self.last_spawn = 0

    def update(self, time_survived):
        if time_survived - self.last_spawn >= 3:

            margin = 50

            import random
            side = random.choice(["top", "bottom", "left", "right"])

            if side == "top":
                x = random.randint(0, self.game.world_width)
                y = -margin
            elif side == "bottom":
                x = random.randint(0, self.game.world_width)
                y = self.game.world_height + margin
            elif side == "left":
                x = -margin
                y = random.randint(0, self.game.world_height)
            else:
                x = self.game.world_width + margin
                y = random.randint(0, self.game.world_height)

            # 🔥 prosledi poziciju
            self.zombie_manager.add_zombie((x, y), time_survived)

            self.last_spawn = time_survived