# =========================
# FILE: ui/game_over.py
# =========================
import pygame
from core.game_state import GameState

class GameOver:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Arial", 40)

    def handle_event(self, event):
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            self.game.reset()
            self.game.state = GameState.PLAYING
        if keys[pygame.K_n]:
            self.game.state = GameState.MENU

    def draw(self, screen):
        screen.fill((0,0,0))
        text = f"Survived: {int(self.game.time_survived)}s"
        screen.blit(self.font.render(text, True, (255,255,255)), (100,100))
        screen.blit(self.font.render("Play again? Y/N", True, (255,255,255)), (100,150))