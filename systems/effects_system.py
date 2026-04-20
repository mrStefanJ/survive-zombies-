class EffectsSystem:
    def __init__(self, game):
        self.game = game
        self.explosions = []
        self.particles = []

    def reset(self):
        self.explosions.clear()
        self.particles.clear()

    def update(self, dt):
        pass

    def draw(self, screen, offset_x, offset_y):
        pass