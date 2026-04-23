import pygame
import math
import sys
from core.game_state import GameState


class Menu:
    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.SysFont("Arial", 70, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 25)
        self.font = pygame.font.SysFont("Arial", 40)

        self.options = ["Play", "Shop", "Highscore", "Settings", "Controls", "Exit"]
        self.selected = 0

        self.key_pressed = False

        self.time = 0

    def handle_event(self, event):
        pass  # koristimo continuous input kao settings

    def enter(self):
        self.selected = 0
        self.key_pressed = True

    def update(self):
        keys = pygame.key.get_pressed()

        self.time += 0.05

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

    def select_option(self):
        option = self.options[self.selected]

        if option == "Play":
            self.game.reset()
            self.game.change_state(GameState.PLAYING)

        elif option == "Shop":
            self.game.change_state(GameState.SHOP)

        elif option == "Highscore":
            self.game.change_state(GameState.HIGHSCORE)

        elif option == "Controls":
            self.game.change_state(GameState.CONTROLS)

        elif option == "Settings":
            self.game.change_state(GameState.SETTINGS)

        elif option == "Exit":
            pygame.quit()
            sys.exit(0)

    def draw(self, screen):
        screen.fill((18, 18, 22))

        w, h = screen.get_size()

        # =========================
        # TITLE
        # =========================
        scale = 1 + math.sin(self.time) * 0.05

        title_surface = self.title_font.render("ZOMBIE SURVIVE", True, (0, 255, 200))
        title_surface = pygame.transform.rotozoom(title_surface, 0, scale)

        title_rect = title_surface.get_rect(center=(w // 2, 90))

        # shadow
        shadow = self.title_font.render("ZOMBIE SURVIVE", True, (0, 80, 60))
        shadow = pygame.transform.rotozoom(shadow, 0, scale)
        screen.blit(shadow, (title_rect.x + 5, title_rect.y + 5))

        # glow
        glow = self.title_font.render("ZOMBIE SURVIVE", True, (0, 180, 120))
        glow = pygame.transform.rotozoom(glow, 0, scale)
        screen.blit(glow, (title_rect.x - 2, title_rect.y - 2))

        # main
        screen.blit(title_surface, title_rect)

        subtitle = self.subtitle_font.render(
            "Survive as long as you can...", True, (160, 160, 160)
        )
        subtitle_rect = subtitle.get_rect(center=(w // 2, 130))
        screen.blit(subtitle, subtitle_rect)

        # =========================
        # PANEL (kao settings)
        # =========================
        panel_x = w // 2 - 200
        panel_y = 180
        panel_w = 400
        panel_h = 350

        pygame.draw.rect(screen, (28, 28, 35), (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(screen, (60, 60, 80), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=12)

        # =========================
        # OPTIONS (cards kao settings)
        # =========================
        for i, option in enumerate(self.options):
            y = panel_y + 40 + i * 50

            is_selected = (i == self.selected)

            bg_color = (40, 40, 50) if is_selected else (28, 28, 35)
            text_color = (0, 255, 200) if is_selected else (220, 220, 220)

            pygame.draw.rect(
                screen,
                bg_color,
                (panel_x + 20, y - 10, panel_w - 40, 45),
                border_radius=8
            )

            text = self.font.render(option, True, text_color)
            screen.blit(text, (panel_x + 40, y - 10))

        # =========================
        # HINT
        # =========================
        hint = self.subtitle_font.render(
            "↑ ↓ navigate | ENTER select", True, (120, 120, 120)
        )
        hint_rect = hint.get_rect(center=(w // 2, h - 40))
        screen.blit(hint, hint_rect)