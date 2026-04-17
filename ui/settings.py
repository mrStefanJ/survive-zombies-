# =========================
# FILE: ui/settings.py
# =========================
import pygame
from core.game_state import GameState
from data.save_system import save_data

class Settings:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 25)

        self.options = ["Toggle Sound", "Select Skin", "Back"]
        self.selected = 0
        self.key_pressed = False

        self.skin_index = 0
        self.key_pressed = False

        self.refresh_skins()

    def enter(self):
        self.key_pressed = True

    def handle_event(self, event):
        pass

    def update(self):
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
            self.game.data["sound"] = not self.game.data.get("sound", True)

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
        title = self.font.render("SETTINGS", True, (0, 220, 220))
        title_rect = title.get_rect(center=(w // 2, 70))
        screen.blit(title, title_rect)

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
        # RIGHT PANEL (SKINS)
        # =========================
        skin_x = 450
        skin_y = 140
        skin_w = 360
        skin_h = 320

        pygame.draw.rect(screen, (28, 28, 35), (skin_x, skin_y, skin_w, skin_h), border_radius=12)
        pygame.draw.rect(screen, (60, 60, 80), (skin_x, skin_y, skin_w, skin_h), 2, border_radius=12)

        header = self.small_font.render("OWNED SKINS", True, (255, 220, 0))
        screen.blit(header, (skin_x + 20, skin_y + 15))

        # no skins fallback
        if not self.skins:
            empty = self.small_font.render("No skins owned", True, (120, 120, 120))
            screen.blit(empty, (skin_x + 20, skin_y + 80))
        else:
            for i, skin in enumerate(self.skins):
                y = skin_y + 60 + i * 60

                is_selected = (i == self.skin_index and self.selected == 1)
                is_active = (skin == self.selected_skin)

                # card bg
                card_color = (45, 45, 60)
                if is_selected:
                    card_color = (70, 70, 95)

                pygame.draw.rect(
                    screen,
                    card_color,
                    (skin_x + 20, y - 15, skin_w - 40, 45),
                    border_radius=10
                )

                # indicator dot
                dot_color = (0, 255, 120) if is_active else (120, 120, 120)
                pygame.draw.circle(screen, dot_color, (skin_x + 35, y + 7), 6)

                text_color = (255, 255, 255)
                if is_selected:
                    text_color = (255, 220, 120)

                text = self.small_font.render(skin, True, text_color)
                screen.blit(text, (skin_x + 55, y))

        # =========================
        # STATUS BAR
        # =========================
        coins = self.small_font.render(
            f"Coins: {self.game.data.get('coins', 0)}",
            True,
            (255, 215, 0)
        )
        screen.blit(coins, (panel_x, panel_y - 50))

        sound = self.small_font.render(
            f"Sound: {'ON' if self.game.data.get('sound', True) else 'OFF'}",
            True,
            (180, 180, 180)
        )
        screen.blit(sound, (panel_x + 200, panel_y - 50))

        # =========================
        # HINT
        # =========================
        hint = self.small_font.render("↑ ↓ navigate | ← → skins | ENTER select", True, (120, 120, 120))
        hint_rect = hint.get_rect(center=(w // 2, h - 40))
        screen.blit(hint, hint_rect)