import pygame
import math
from core.game_state import GameState

class GameOver:
    def __init__(self, game):
        self.game = game

        self.font_big = pygame.font.SysFont("Arial", 80, bold=True)
        self.font = pygame.font.SysFont("Arial", 40)
        self.small = pygame.font.SysFont("Arial", 25)

        self.options = ["Restart", "Exit"]
        self.selected = 0

        self.key_pressed = False

        # animation
        self.alpha = 0
        self.anim_time = 0

    def enter(self):
        self.alpha = 0
        self.selected = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)

        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)

        elif event.key == pygame.K_RETURN:
            self.select()

    def select(self):
        option = self.options[self.selected]

        if option == "Restart":
            self.game.reset()
            self.game.change_state(GameState.PLAYING)

        elif option == "Exit":
            self.game.change_state(GameState.MENU)

    def update(self):
        # fade in
        if self.alpha < 180:
            self.alpha += 5

        self.anim_time += 0.05

    def draw(self, screen):
        w, h = screen.get_size()

        # =========================
        # DARK OVERLAY
        # =========================
        overlay = pygame.Surface((w, h))
        overlay.set_alpha(self.alpha)
        overlay.fill((10, 10, 15))
        screen.blit(overlay, (0, 0))

        # =========================
        # TITLE (pulse effect)
        # =========================
        scale = 1 + 0.05 * math.sin(self.anim_time)
        title = self.font_big.render("GAME OVER", True, (255, 60, 60))

        title = pygame.transform.scale(
            title,
            (int(title.get_width() * scale),
             int(title.get_height() * scale))
        )

        title_rect = title.get_rect(center=(w // 2, 150))
        screen.blit(title, title_rect)

        # =========================
        # SCORE PANEL
        # =========================
        score = self.game.score
        coins = score  # koliko si zaradio

        panel = pygame.Rect(w//2 - 200, 230, 400, 120)

        pygame.draw.rect(screen, (30, 30, 40), panel, border_radius=12)
        pygame.draw.rect(screen, (80, 80, 100), panel, 2, border_radius=12)

        score_text = self.font.render(f"Score: {score}", True, (255,255,255))
        coins_text = self.font.render(f"Coins earned: {coins}", True, (255, 200, 0))

        screen.blit(score_text, (panel.x + 30, panel.y + 20))
        screen.blit(coins_text, (panel.x + 30, panel.y + 60))

        # =========================
        # OPTIONS
        # =========================
        for i, option in enumerate(self.options):
            y = 400 + i * 70

            is_selected = (i == self.selected)

            scale = 1.0
            if is_selected:
                scale = 1.1 + 0.05 * math.sin(self.anim_time * 2)

            color = (200, 200, 200)
            if is_selected:
                color = (255, 220, 120)

            text = self.font.render(option, True, color)

            text = pygame.transform.scale(
                text,
                (int(text.get_width() * scale),
                 int(text.get_height() * scale))
            )

            rect = text.get_rect(center=(w // 2, y))
            screen.blit(text, rect)

            # glow border
            if is_selected:
                pygame.draw.rect(
                    screen,
                    (255, 180, 80),
                    rect.inflate(20, 10),
                    2,
                    border_radius=8
                )

        # =========================
        # HINT
        # =========================
        hint = self.small.render("↑ ↓ select | ENTER confirm", True, (120,120,120))
        hint_rect = hint.get_rect(center=(w // 2, h - 50))
        screen.blit(hint, hint_rect)