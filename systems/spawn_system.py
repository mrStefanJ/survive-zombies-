# =========================
# FILE: systems/spawn_system.py
# =========================
class SpawnSystem:
    def __init__(self, zombie_manager):
        self.zombie_manager = zombie_manager
        self.last_spawn = 0

    def update(self, time_survived):
        if time_survived - self.last_spawn >= 3:
            self.zombie_manager.add_zombie(time_survived)
            self.last_spawn = time_survived