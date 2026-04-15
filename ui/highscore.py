# =========================
# FILE: ui/highscore.py
# =========================
import pygame
from core.game_state import GameState

class Highscore:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 25)
        self.key_pressed = False

        self.options = ["Back"]
        self.selected = 0

    def enter(self):
        self.key_pressed = True

    def handle_event(self, event):
        pass

    def select_option(self):
        if self.options[self.selected] == "Back":
            self.game.change_state(GameState.MENU)  # koristi fade

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and not self.key_pressed:
            self.selected = (self.selected - 1) % len(self.options)
            self.key_pressed = True

        elif keys[pygame.K_DOWN] and not self.key_pressed:
            self.selected = (self.selected + 1) % len(self.options)
            self.key_pressed = True

        elif keys[pygame.K_RETURN] and not self.key_pressed:
            self.select_option()
            self.key_pressed = True

        if not any(keys):
            self.key_pressed = False

    def draw(self, screen):
        screen.fill((50, 0, 0))

        title = self.font.render("HIGHSCORES", True, (255, 255, 0))
        screen.blit(title, (100, 50))

        leaderboard = self.game.data.get("leaderboard", [])

        if not leaderboard:
            no_data = self.small_font.render("No scores yet", True, (200, 200, 200))
            screen.blit(no_data, (100, 150))
        else:
            for i, entry in enumerate(leaderboard):
                name = entry["name"]
                score = entry["score"]

                text = self.font.render(
                    f"{i + 1}. {name} - {score}",
                    True,
                    (255, 255, 255)
                )
                screen.blit(text, (100, 150 + i * 50))

        # BACK dugme
        for i, option in enumerate(self.options):
            color = (255, 255, 255)
            if i == self.selected:
                color = (255, 200, 0)

            text = self.font.render(option, True, color)
            screen.blit(text, (100, 400 + i * 60))