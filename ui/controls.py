import pygame
from core.game_state import GameState


class Controls:
    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.font = pygame.font.SysFont("Arial", 30)

        self.options = ["Back"]
        self.selected = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                self.game.change_state(GameState.MENU)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((30,30,30))

        # TITLE
        title = self.title_font.render("CONTROLS", True, (255, 255, 0))
        screen.blit(title, (100, 50))

        # CONTROLS LIST
        controls = [
            "W / A / S / D  - Move",
            "SPACE          - Throw Bomb",
            "ESC            - Back/Menu",
            "ENTER          - Select"
        ]

        for i, text in enumerate(controls):
            render = self.font.render(text, True, (255, 255, 255))
            screen.blit(render, (100, 150 + i * 50))

        # BACK BUTTON
        for i, option in enumerate(self.options):
            color = (255, 255, 255)
            if i == self.selected:
                color = (255, 200, 0)

            render = self.font.render(option, True, color)
            screen.blit(render, (100, 400))