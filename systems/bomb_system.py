import pygame
from helper.utils import resource_path

class BombSystem:
    def __init__(self, game):
        self.game = game

        self.max_bombs = 5
        self.current_bombs = 5

        self.bomb_cooldown = 4.0
        self.fuse_time = 3.0
        self.bomb_timer = 0

        self.bombs = []
        self.explosion_time = 3
        # sound
        self.tick_sound = pygame.mixer.Sound(
            resource_path("assets/sounds/tick.wav")
        )
        self.tick_channel = pygame.mixer.Channel(5)

        self.last_tick_stage = -1

    def throw(self, pos):
        if self.current_bombs <= 0:
            return

        self.bombs.append({
            "pos": pos,
            "timer": 3.0,
            "tick_stage": 0
        })

        self.current_bombs -= 1

    def update(self, dt):
        for bomb in self.bombs[:]:
            bomb["timer"] -= dt
            t = bomb["timer"]

            # =========================
            # STAGE DETECTION
            # =========================
            if t > 2.0:
                stage = 0
            elif t > 1.0:
                stage = 1
            elif t > 0.5:
                stage = 2
            else:
                stage = 3

            bomb["tick_stage"] = stage

            # =========================
            # AUDIO TICK SYSTEM
            # =========================
            if stage != self.last_tick_stage and stage > 0:
                self.tick_channel.play(self.tick_sound)

                # ubrzavanje tick-a
                self.tick_sound.set_volume(0.2)

                self.last_tick_stage = stage

            # =========================
            # EXPLOSION
            # =========================
            if t <= 0:
                self.game.explode(bomb["pos"])
                self.bombs.remove(bomb)

        # 🔥 REGEN SISTEM
        if self.current_bombs < self.max_bombs:
            self.bomb_timer += dt

            if self.bomb_timer >= self.bomb_cooldown:
                self.current_bombs += 1
                self.bomb_timer = 0

    def draw(self, screen):
        for bomb in self.bombs:
            x, y = bomb["pos"]
            t = bomb["timer"]

            # =========================
            # COLOR PULSE
            # =========================
            intensity = max(0, 255 - int(t * 80))
            color = (255, intensity, 0)

            radius = 15 + int((3 - t) * 3)

            pygame.draw.circle(screen, color, (x, y), radius)

            # timer text
            text = self.game.bomb_font.render(str(max(0, int(t) + 1)), True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=(x, y)))

    def reset(self):
        self.current_bombs = self.max_bombs
        self.bombs.clear()
        self.bomb_timer = 0