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

        self.options = ["Toggle Music", "Select Skin", "Back"]
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
        self.time += 0.05

        current_owned = self.game.data.get("owned_skins", ["Green Skin"])
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
            if self.selected == 1 and self.skins:
                self.skin_index = (self.skin_index - 1) % len(self.skins)
            self.key_pressed = True

        elif keys[pygame.K_RIGHT] and not self.key_pressed:
            if self.selected == 1 and self.skins:
                self.skin_index = (self.skin_index + 1) % len(self.skins)
            self.key_pressed = True

        elif keys[pygame.K_RETURN] and not self.key_pressed:
            self.select_option()
            self.key_pressed = True

        if not any(keys):
            self.key_pressed = False

    # =========================
    # SKINS
    # =========================
    def refresh_skins(self):
        self.skins = self.game.data.get("owned_skins", ["Green Skin"])
        self.selected_skin = self.game.data.get("selected_skin", "Green Skin")

        if self.selected_skin not in self.skins:
            self.selected_skin = "Green Skin"
            self.game.data["selected_skin"] = "Green Skin"

        self.skin_index = self.skins.index(self.selected_skin)

    # =========================
    # ACTIONS
    # =========================
    def select_option(self):
        option = self.options[self.selected]

        # -------------------------
        # TOGGLE MUSIC (FIXED)
        # -------------------------
        if option == "Toggle Music":
            current = self.game.data.get("music", True)
            new_state = not current

            self.game.data["music"] = new_state

            if new_state:
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()

        # -------------------------
        # SELECT SKIN
        # -------------------------
        elif option == "Select Skin":
            if self.skins:
                chosen = self.skins[self.skin_index]
                self.game.data["selected_skin"] = chosen
                self.selected_skin = chosen
                self.refresh_skins()

        # -------------------------
        # BACK
        # -------------------------
        elif option == "Back":
            self.game.state = GameState.MENU

        save_data(self.game.data)

    # =========================
    # DRAW
    # =========================
    def draw(self, screen):
        screen.fill((18, 18, 22))
        w, h = screen.get_size()

        # TITLE
        UIHelper.draw_title(
            screen,
            "SETTINGS",
            self.title_font,
            self.time,
            y=90
        )

        # LEFT PANEL
        panel_x, panel_y = 80, 140
        panel_w, panel_h = 320, 250

        pygame.draw.rect(screen, (28, 28, 35), (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(screen, (60, 60, 80), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=12)

        for i, option in enumerate(self.options):
            y = panel_y + 30 + i * 70
            is_selected = (i == self.selected)

            bg = (40, 40, 50) if is_selected else (28, 28, 35)
            color = (0, 255, 200) if is_selected else (220, 220, 220)

            pygame.draw.rect(
                screen,
                bg,
                (panel_x + 15, y - 20, panel_w - 30, 50),
                border_radius=8
            )

            text = self.font.render(option, True, color)
            screen.blit(text, (panel_x + 30, y - 15))

        # RIGHT PANEL
        panel_x, panel_y = 450, 140
        panel_w, panel_h = 360, 320

        pygame.draw.rect(screen, (28, 28, 35), (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(screen, (60, 60, 80), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=12)

        selected_option = self.options[self.selected]

        # -------------------------
        # MUSIC UI
        # -------------------------
        if selected_option == "Toggle Music":
            header = self.small_font.render("MUSIC SETTINGS", True, (255, 220, 0))
            screen.blit(header, (panel_x + 20, panel_y + 15))

            is_on = self.game.data.get("music", True)

            status = "ON" if is_on else "OFF"
            color = (0, 255, 120) if is_on else (255, 80, 80)

            pygame.draw.rect(
                screen,
                (45, 45, 60),
                (panel_x + 40, panel_y + 100, panel_w - 80, 100),
                border_radius=12
            )

            text = self.font.render(status, True, color)
            screen.blit(text, text.get_rect(center=(panel_x + panel_w // 2, panel_y + 150)))

            hint = self.small_font.render("Press ENTER to toggle", True, (140, 140, 140))
            screen.blit(hint, hint.get_rect(center=(panel_x + panel_w // 2, panel_y + 230)))

        # -------------------------
        # SKINS UI
        # -------------------------
        elif selected_option == "Select Skin":
            header = self.small_font.render("OWNED SKINS", True, (255, 220, 0))
            screen.blit(header, (panel_x + 20, panel_y + 15))

            if not self.skins:
                empty = self.small_font.render("No skins owned", True, (120, 120, 120))
                screen.blit(empty, (panel_x + 20, panel_y + 80))
            else:
                for i, skin in enumerate(self.skins):
                    y = panel_y + 60 + i * 60

                    selected = (i == self.skin_index and self.selected == 1)
                    active = (skin == self.selected_skin)

                    color = (70, 70, 95) if selected else (45, 45, 60)

                    pygame.draw.rect(
                        screen,
                        color,
                        (panel_x + 20, y - 15, panel_w - 40, 45),
                        border_radius=10
                    )

                    dot = (0, 255, 120) if active else (120, 120, 120)
                    pygame.draw.circle(screen, dot, (panel_x + 35, y + 7), 6)

                    txt_color = (255, 220, 120) if selected else (255, 255, 255)
                    text = self.small_font.render(skin, True, txt_color)
                    screen.blit(text, (panel_x + 55, y))

        # -------------------------
        # BACK UI
        # -------------------------
        elif selected_option == "Back":
            text = self.small_font.render("Return to main menu", True, (140, 140, 140))
            screen.blit(text, text.get_rect(center=(panel_x + panel_w // 2, panel_y + panel_h // 2)))

        # HINT
        hint = self.small_font.render("↑ ↓ navigate | ← → skins | ENTER select", True, (120, 120, 120))
        screen.blit(hint, hint.get_rect(center=(w // 2, h - 40)))