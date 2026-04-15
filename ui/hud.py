# =========================
# FILE: ui/hud.py
# =========================
import pygame

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 30)

    def draw(self, screen, time_survived, highscore):
        screen.blit(self.font.render(f"Time: {int(time_survived)}", True, (255, 255, 255)), (10, 10))
        screen.blit(self.font.render(f"Highscore: {highscore}", True, (255, 255, 0)), (10, 40))