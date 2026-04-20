import pygame
from core.game_state import GameState
from ui.helper import UIHelper


class Highscore:
    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.font = pygame.font.SysFont("Arial", 35)
        self.small_font = pygame.font.SysFont("Arial", 25)

        self.options = ["Back"]
        self.selected = 0
        self.key_pressed = False

        self.time = 0

    def enter(self):
        self.key_pressed = True

    def handle_event(self, event):
        pass

    def update(self):
        self.time += 0.05
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN] and not self.key_pressed:
            self.game.change_state(GameState.MENU)
            self.key_pressed = True

        if not any(keys):
            self.key_pressed = False

    def draw(self, screen):
        screen.fill((18, 18, 22))
        w, h = screen.get_size()

        # =========================
        # TITLE (ANIMATED)
        # =========================
        UIHelper.draw_title(
            screen,
            "HIGHSCORE",
            self.title_font,
            self.time,
            y=90
        )

        # =========================
        # PANEL
        # =========================
        panel_x = w // 2 - 250
        panel_y = 180
        panel_w = 500
        panel_h = 300

        pygame.draw.rect(screen, (28, 28, 35), (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(screen, (60, 60, 80), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=12)

        leaderboard = self.game.data.get("leaderboard", [])

        if not leaderboard:
            text = self.small_font.render("No scores yet", True, (140, 140, 140))
            screen.blit(text, (panel_x + 20, panel_y + 60))
        else:
            for i, entry in enumerate(leaderboard):
                name = entry.get("name", "YOU")
                score = entry.get("score", 0)

                text = f"{i+1}. {name} - {score}"
                render = self.font.render(text, True, (220, 220, 220))

                screen.blit(render, (panel_x + 40, panel_y + 40 + i * 45))

        # =========================
        # BACK BUTTON
        # =========================
        pygame.draw.rect(
            screen,
            (40, 40, 50),
            (panel_x + 150, panel_y + panel_h - 60, 200, 40),
            border_radius=8
        )

        text = self.font.render("BACK", True, (0, 255, 200))
        text_rect = text.get_rect(center=(panel_x + panel_w // 2, panel_y + panel_h - 40))
        screen.blit(text, text_rect)