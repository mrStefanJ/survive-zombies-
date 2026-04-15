# =========================
# FILE: ui/settings.py
# =========================
import pygame
from core.game_state import GameState

class Settings:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 25)

        self.options = ["Toggle Sound", "Back"]
        self.selected = 0
        self.key_pressed = False

    def enter(self):
        self.key_pressed = True

    def handle_event(self, event):
        pass

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

    def select_option(self):
        option = self.options[self.selected]

        if option == "Toggle Sound":
            self.game.data["sound"] = not self.game.data.get("sound", True)
            from data.save_system import save_data
            save_data(self.game.data)
        elif option == "Back":
            self.game.state = GameState.MENU

    def draw(self, screen):
        screen.fill((30,30,30))
        title = self.font.render("SETTINGS", True, (0,200,200))
        screen.blit(title, (100,50))

        for i, option in enumerate(self.options):
            color = (255,255,255)
            if i == self.selected:
                color = (0,255,200)
            text = self.font.render(option, True, color)
            screen.blit(text, (100,150 + i*60))

        status = self.small_font.render(
            f"Sound: {'ON' if self.game.data.get('sound', True) else 'OFF'}",
            True, (200,200,200)
        )
        screen.blit(status, (400, 150))
        hint = self.small_font.render("Use ↑ ↓ and ENTER", True, (180,180,180))
        screen.blit(hint, (100,450))