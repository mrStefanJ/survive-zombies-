# =========================
# FILE: ui/settings.py
# =========================
import pygame
from core.game_state import GameState
from data.save_system import save_data
from ui.helper import UIHelper

class Settings:
    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 25)

        self.options = ["Toggle Sound", "Select Skin", "Back"]
        self.selected = 0
        self.key_pressed = False

        self.skin_index = 0

        self.time = 0

        self.refresh_skins()

    def enter(self):
        self.key_pressed = True

    def handle_event(self, event):
        pass

    def update(self):
        current_owned = self.game.data.get("owned_skins", ["Green Skin"])
        self.time += 0.05

        if current_owned != self.skins:
            self.refresh_skins()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and not self.key_pressed:
            self.selected = (self.selected - 1) % len(self.options)
            self.key_pressed = True

        elif keys[pygame.K_DOWN] and not self.key_pressed:
            self.selected = (self.selected + 1) % len(self.options)
            self.key_pressed = True

        elif keys[pygame.K_LEFT] and not self.key_pressed:
            if self.selected == 1:  # skin row
                if self.skins:
                    self.skin_index = (self.skin_index - 1) % len(self.skins)
            self.key_pressed = True

        elif keys[pygame.K_RIGHT] and not self.key_pressed:
            if self.selected == 1:
                if self.skins:
                    self.skin_index = (self.skin_index + 1) % len(self.skins)
            self.key_pressed = True

        elif keys[pygame.K_RETURN] and not self.key_pressed:
            self.select_option()
            self.key_pressed = True

        if not any(keys):
            self.key_pressed = False

    def refresh_skins(self):
        self.skins = self.game.data.get("owned_skins", ["Green Skin"])
        self.selected_skin = self.game.data.get("selected_skin", "Green Skin")

        if self.selected_skin not in self.skins:
            self.selected_skin = "Green Skin"
            self.game.data["selected_skin"] = "Green Skin"

        self.skin_index = self.skins.index(self.selected_skin)

    def select_option(self):
        option = self.options[self.selected]

        if option == "Toggle Sound":
            new_state = not self.game.data.get("sound", True)
            self.game.data["sound"] = new_state

            if new_state:
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()

        elif option == "Select Skin":
            if self.skins:
                chosen = self.skins[self.skin_index]

                self.game.data["selected_skin"] = chosen

                # sync local state
                self.selected_skin = chosen
                self.refresh_skins()

        elif option == "Back":
            self.game.state = GameState.MENU

        # ALWAYS SAVE AFTER CHANGE
        save_data(self.game.data)

    def draw(self, screen):
        screen.fill((18, 18, 22))

        w, h = screen.get_size()

        # =========================
        # TITLE
        # =========================
        UIHelper.draw_title(
            screen,
            "SETTINGS",
            self.title_font,
            self.time,
            y=90
        )

        # =========================
        # LEFT PANEL (OPTIONS)
        # =========================
        panel_x = 80
        panel_y = 140
        panel_w = 320
        panel_h = 250

        pygame.draw.rect(screen, (28, 28, 35), (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(screen, (60, 60, 80), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=12)

        for i, option in enumerate(self.options):
            y = panel_y + 30 + i * 70

            is_selected = (i == self.selected)

            bg_color = (40, 40, 50) if is_selected else (28, 28, 35)
            text_color = (0, 255, 200) if is_selected else (220, 220, 220)

            pygame.draw.rect(
                screen,
                bg_color,
                (panel_x + 15, y - 20, panel_w - 30, 50),
                border_radius=8
            )

            text = self.font.render(option, True, text_color)
            screen.blit(text, (panel_x + 30, y - 15))

        # =========================
        # RIGHT PANEL (DYNAMIC)
        # =========================
        panel_x = 450
        panel_y = 140
        panel_w = 360
        panel_h = 320

        pygame.draw.rect(screen, (28, 28, 35), (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(screen, (60, 60, 80), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=12)

        selected_option = self.options[self.selected]

        # =========================
        # TOGGLE SOUND PANEL
        # =========================
        if selected_option == "Toggle Sound":
            header = self.small_font.render("SOUND SETTINGS", True, (255, 220, 0))
            screen.blit(header, (panel_x + 20, panel_y + 15))

            is_on = self.game.data.get("sound", True)

            status_text = "ON" if is_on else "OFF"
            status_color = (0, 255, 120) if is_on else (255, 80, 80)

            # big toggle box
            pygame.draw.rect(
                screen,
                (45, 45, 60),
                (panel_x + 40, panel_y + 100, panel_w - 80, 100),
                border_radius=12
            )

            status_render = self.font.render(status_text, True, status_color)
            status_rect = status_render.get_rect(center=(panel_x + panel_w // 2, panel_y + 150))
            screen.blit(status_render, status_rect)

            hint = self.small_font.render("Press ENTER to toggle", True, (140, 140, 140))
            hint_rect = hint.get_rect(center=(panel_x + panel_w // 2, panel_y + 230))
            screen.blit(hint, hint_rect)


        # =========================
        # SKIN PANEL
        # =========================
        elif selected_option == "Select Skin":
            header = self.small_font.render("OWNED SKINS", True, (255, 220, 0))
            screen.blit(header, (panel_x + 20, panel_y + 15))

            if not self.skins:
                empty = self.small_font.render("No skins owned", True, (120, 120, 120))
                screen.blit(empty, (panel_x + 20, panel_y + 80))
            else:
                for i, skin in enumerate(self.skins):
                    y = panel_y + 60 + i * 60

                    is_selected = (i == self.skin_index and self.selected == 1)
                    is_active = (skin == self.selected_skin)

                    card_color = (45, 45, 60)
                    if is_selected:
                        card_color = (70, 70, 95)

                    pygame.draw.rect(
                        screen,
                        card_color,
                        (panel_x + 20, y - 15, panel_w - 40, 45),
                        border_radius=10
                    )

                    # active indicator
                    dot_color = (0, 255, 120) if is_active else (120, 120, 120)
                    pygame.draw.circle(screen, dot_color, (panel_x + 35, y + 7), 6)

                    text_color = (255, 255, 255)
                    if is_selected:
                        text_color = (255, 220, 120)

                    text = self.small_font.render(skin, True, text_color)
                    screen.blit(text, (panel_x + 55, y))


        # =========================
        # BACK PANEL (optional)
        # =========================
        elif selected_option == "Back":
            text = self.small_font.render("Return to main menu", True, (140, 140, 140))
            text_rect = text.get_rect(center=(panel_x + panel_w // 2, panel_y + panel_h // 2))
            screen.blit(text, text_rect)

        # =========================
        # HINT
        # =========================
        hint = self.small_font.render("↑ ↓ navigate | ← → skins | ENTER select", True, (120, 120, 120))
        hint_rect = hint.get_rect(center=(w // 2, h - 40))
        screen.blit(hint, hint_rect)