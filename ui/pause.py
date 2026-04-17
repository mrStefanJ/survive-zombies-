# ==============================
# ui/pause
# ==============================
import pygame
from data.settings import WIDTH, HEIGHT

class Pause:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Arial", 50)

    def draw(self):
        screen = self.game.screen
        options = self.game.pause_options
        selected = self.game.pause_selected

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = self.font.render("PAUSED", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - 100, 150))

        for i, option in enumerate(options):
            color = (200, 200, 200)
            if i == selected:
                color = (255, 200, 0)

            text = self.font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - 80, 250 + i * 80))