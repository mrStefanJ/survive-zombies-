import pygame
from core.game_state import GameState
from ui.helper import UIHelper


class Controls:
    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.font = pygame.font.SysFont("Arial", 30)
        self.small_font = pygame.font.SysFont("Arial", 25)

        self.key_pressed = False
        self.time = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.change_state(GameState.MENU)

    def update(self):
        self.time += 0.05

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            if not self.key_pressed:
                self.game.change_state(GameState.MENU)
                self.key_pressed = True
        else:
            self.key_pressed = False

    def enter(self):
        self.key_pressed = True  # blokira prvi ENTER

    def draw(self, screen):
        screen.fill((18, 18, 22))
        w, h = screen.get_size()

        # =========================
        # TITLE (ANIMATED)
        # =========================
        UIHelper.draw_title(
            screen,
            "CONTROLS",
            self.title_font,
            self.time,
            y=90
        )

        # =========================
        # PANEL
        # =========================
        panel_x = w // 2 - 300
        panel_y = 180
        panel_w = 600
        panel_h = 320

        pygame.draw.rect(screen, (28, 28, 35), (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(screen, (60, 60, 80), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=12)

        controls = [
            "W / A / S / D   - Movement",
            "SPACE           - Throw Bomb",
            "ESC             - Pause",
            "ENTER           - Select"
        ]

        for i, text in enumerate(controls):
            render = self.font.render(text, True, (220, 220, 220))
            screen.blit(render, (panel_x + 40, panel_y + 50 + i * 50))

        # =========================
        # BACK BUTTON
        # =========================
        pygame.draw.rect(
            screen,
            (40, 40, 50),
            (panel_x + 200, panel_y + panel_h - 60, 200, 40),
            border_radius=8
        )

        text = self.font.render("BACK", True, (0, 255, 200))
        text_rect = text.get_rect(center=(panel_x + panel_w // 2, panel_y + panel_h - 40))
        screen.blit(text, text_rect)