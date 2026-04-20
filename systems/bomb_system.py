import pygame

class BombSystem:
    def __init__(self, game):
        self.game = game
        self.bombs = []

        self.max_bombs = 5
        self.current_bombs = 5

        self.bomb_cooldown = 2.0
        self.bomb_timer = 0

        self.explosion_time = 3

    def throw(self, pos):
        self.bombs.append({
            "pos": pos,
            "timer": self.explosion_time
        })

    def update(self, dt):
        # recharge
        if self.current_bombs < self.max_bombs:
            self.bomb_timer += dt

            if self.bomb_timer >= self.bomb_cooldown:
                self.current_bombs += 1
                self.bomb_timer = 0

        # update bombs
        for bomb in self.bombs[:]:
            bomb["timer"] -= dt

            if bomb["timer"] <= 0:
                self.game.explode(bomb["pos"])
                self.bombs.remove(bomb)

    def draw(self, screen):
        for bomb in self.bombs:
            x, y = int(bomb["pos"][0]), int(bomb["pos"][1])

            pygame.draw.circle(screen, (255, 100, 0), (x, y), 15)

            time_left = max(0, int(bomb["timer"]) + 1)
            text = self.game.bomb_font.render(str(time_left), True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=(x, y)))

    def reset(self):
        self.bombs.clear()
        self.current_bombs = self.max_bombs
        self.bomb_timer = 0