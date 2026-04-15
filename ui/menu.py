import pygame
import math
from core.game_state import GameState

class Menu:
    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 25)
        self.font = pygame.font.SysFont("Arial", 40)

        self.options = ["Play", "Shop", "Highscore", "Settings","Controls","Exit"]
        self.selected = 0

        self.time = 0  # za animaciju

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                self.select_option()

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
            self.game.change_state((GameState.CONTROLS))

        elif option == "Settings":
            self.game.change_state(GameState.SETTINGS)

        elif option == "Exit":
            pygame.quit()
            exit()

    def update(self):
        self.time += 0.05  # brzina animacije

    def draw(self, screen):
        screen.fill((10, 10, 10))

        width = screen.get_width()

        # =========================
        # 🧠 TITLE ANIMACIJA (PULSE)
        # =========================
        scale = 1 + math.sin(self.time) * 0.05

        title_surface = self.title_font.render("ZOMBIE SURVIVE", True, (0, 255, 100))
        title_surface = pygame.transform.rotozoom(title_surface, 0, scale)

        title_rect = title_surface.get_rect(center=(width // 2, 120))

        # shadow (dubina)
        shadow = self.title_font.render("ZOMBIE SURVIVE", True, (0, 80, 40))
        shadow = pygame.transform.rotozoom(shadow, 0, scale)
        screen.blit(shadow, (title_rect.x + 5, title_rect.y + 5))

        # glow (soft)
        glow = self.title_font.render("ZOMBIE SURVIVE", True, (0, 180, 80))
        glow = pygame.transform.rotozoom(glow, 0, scale)
        screen.blit(glow, (title_rect.x - 2, title_rect.y - 2))

        # main title
        screen.blit(title_surface, title_rect)

        # =========================
        # 🎮 SUBTITLE
        # =========================
        subtitle = self.subtitle_font.render("Survive as long as you can...", True, (180, 180, 180))
        subtitle_rect = subtitle.get_rect(center=(width // 2, 200))
        screen.blit(subtitle, subtitle_rect)

        # =========================
        # 🎮 MENU OPCIJE (CENTER)
        # =========================
        for i, option in enumerate(self.options):
            color = (200, 200, 200)

            if i == self.selected:
                # highlight animacija
                color = (255, 220, 100)

                # mali scale efekat
                text = self.font.render(option, True, color)
                text = pygame.transform.scale(text, (int(text.get_width()*1.1), int(text.get_height()*1.1)))
            else:
                text = self.font.render(option, True, color)

            rect = text.get_rect(center=(width // 2, 300 + i * 60))
            screen.blit(text, rect)