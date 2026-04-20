import pygame
from core.game_state import GameState
from data.save_system import save_data
from ui.helper import UIHelper


class Shop:
    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 24)

        self.time = 0

        # =========================
        # COLORS (SHARED STYLE)
        # =========================
        self.colors = {
            "bg": (18, 18, 22),
            "card": (28, 28, 35),
            "card_hover": (40, 40, 50),
            "border": (60, 60, 80),
            "text": (220, 220, 220),
            "text_active": (0, 255, 200),
        }

        # =========================
        # ITEMS
        # =========================
        self.items = [
            {"name": "Green Skin", "price": 0, "default": True},
            {"name": "Blue Skin", "price": 20},
            {"name": "Red Skin", "price": 20},
        ]

        self.selected = 0
        self.anim_time = 0

        # smooth scaling
        self.scales = [1.0 for _ in range(len(self.items) + 1)]

        # debounce
        self.last_input_time = 0
        self.input_delay = 120

        # owned
        self.owned = set(self.game.data.get("owned_skins", []))

        # feedback
        self.message = ""
        self.message_timer = 0

    # =========================
    # INPUT
    # =========================
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        now = pygame.time.get_ticks()
        if now - self.last_input_time < self.input_delay:
            return

        self.last_input_time = now

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % (len(self.items) + 1)

        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % (len(self.items) + 1)

        elif event.key == pygame.K_RETURN:
            if self.selected == len(self.items):
                self.game.change_state(GameState.MENU)
            else:
                self.select_item()

    # =========================
    # LOGIC
    # =========================
    def select_item(self):
        item = self.items[self.selected]

        if item.get("default"):
            self.game.data["selected_skin"] = item["name"]
            self.set_message("Equipped")

        elif item["name"] in self.owned:
            self.game.data["selected_skin"] = item["name"]
            self.set_message("Equipped")

        else:
            if self.game.data.get("coins", 0) >= item["price"]:
                self.game.data["coins"] -= item["price"]
                self.owned.add(item["name"])

                self.game.data["owned_skins"] = list(self.owned)
                self.game.data["selected_skin"] = item["name"]

                self.set_message("Purchased!")
            else:
                self.set_message("Not enough coins!")

        save_data(self.game.data)

    def set_message(self, text):
        self.message = text
        self.message_timer = 1200

    def update(self, dt):
        self.anim_time += dt * 0.04

        self.time += 0.05

        # smooth scale (lerp)
        for i in range(len(self.scales)):
            target = 1.08 if i == self.selected else 1.0
            self.scales[i] += (target - self.scales[i]) * 0.15

        if self.message_timer > 0:
            self.message_timer -= dt

    # =========================
    # DRAW
    # =========================
    def draw(self, screen):
        screen.fill(self.colors["bg"])

        # TITLE
        UIHelper.draw_title(
            screen,
            "SHOP",
            self.title_font,
            self.time,
            y=90
        )

        # COINS
        coins = self.game.data.get("coins", 0)
        coins_text = self.small_font.render(f"Coins: {coins}", True, (255, 215, 0))
        screen.blit(coins_text, (600, 20))

        # =========================
        # ITEMS
        # =========================
        for i, item in enumerate(self.items):
            y = 150 + i * 70
            selected = (i == self.selected)

            # CARD BACKGROUND
            pygame.draw.rect(
                screen,
                self.colors["card_hover"] if selected else self.colors["card"],
                (80, y - 10, 600, 60),
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                self.colors["border"],
                (80, y - 10, 600, 60),
                2,
                border_radius=10
            )

            # TEXT
            color = self.colors["text_active"] if selected else self.colors["text"]

            text_surface = self.font.render(item["name"], True, color)

            scale = self.scales[i]
            scaled_surface = pygame.transform.scale(
                text_surface,
                (int(text_surface.get_width() * scale),
                 int(text_surface.get_height() * scale))
            )

            screen.blit(scaled_surface, (100, y))

            # STATE LABEL
            if item.get("default"):
                label = "DEFAULT"
                label_color = (0, 200, 255)

            elif item["name"] == self.game.data.get("selected_skin"):
                label = "EQUIPPED"
                label_color = (0, 255, 150)

            elif item["name"] in self.owned:
                label = "OWNED"
                label_color = (0, 255, 0)
            else:
                label = f"{item['price']} coins"
                label_color = (200, 200, 200)

            label_render = self.small_font.render(label, True, label_color)
            screen.blit(label_render, (450, y + 10))

        # =========================
        # BACK BUTTON
        # =========================
        i = len(self.items)
        y = 150 + i * 70
        selected = (self.selected == i)

        pygame.draw.rect(
            screen,
            self.colors["card_hover"] if selected else self.colors["card"],
            (80, y - 10, 600, 60),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            self.colors["border"],
            (80, y - 10, 600, 60),
            2,
            border_radius=10
        )

        color = self.colors["text_active"] if selected else self.colors["text"]

        text_surface = self.font.render("Back", True, color)

        scale = self.scales[i]
        scaled_surface = pygame.transform.scale(
            text_surface,
            (int(text_surface.get_width() * scale),
             int(text_surface.get_height() * scale))
        )

        screen.blit(scaled_surface, (100, y))

        # =========================
        # MESSAGE FEEDBACK
        # =========================
        if self.message_timer > 0:
            alpha = min(255, int(self.message_timer / 1200 * 255))
            msg_surface = self.small_font.render(self.message, True, (255, 255, 255))
            msg_surface.set_alpha(alpha)

            rect = msg_surface.get_rect(center=(400, 520))
            screen.blit(msg_surface, rect)