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
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)

        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)

        elif event.key == pygame.K_RETURN:
            self.select_option()

    def select_option(self):
        if self.options[self.selected] == "Back":
            self.game.change_state(GameState.MENU)  # koristi fade

    def update(self):
       pass

    def draw(self, screen):
        screen.fill((30, 30, 30))

        # =========================
        # TITLE
        # =========================
        title = self.font.render("HIGHSCORE", True, (255, 255, 0))
        screen.blit(title, (100, 50))

        # =========================
        # OPTIONS
        # =========================
        for i, option in enumerate(self.options):
            color = (255, 255, 255)
            if i == self.selected:
                color = (255, 200, 0)

            text = option

            # dodatni info po opciji
            if option == "Toggle Sound":
                state = "ON" if self.game.data.get("sound", True) else "OFF"
                text = f"{option}: {state}"


                if self.skins:
                    current = self.skins[self.skin_index]
                    text = f"{option}: {current}"
                else:
                    text = f"{option}: None"

            rendered = self.font.render(text, True, color)
            screen.blit(rendered, (100, 150 + i * 60))

        # =========================
        # INFO
        # =========================
        coins = self.small_font.render(
            f"Coins: {self.game.data.get('coins', 0)}",
            True,
            (200, 200, 200)
        )
        screen.blit(coins, (100, 350))
