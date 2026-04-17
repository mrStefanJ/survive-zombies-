import pygame
from core.game_state import GameState
from data.save_system import save_data
import math


class Shop:
    def __init__(self, game):
        self.game = game

        # fonts
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 25)

        # items
        self.items = [
            {"name": "Green Skin", "price": 0, "default": True},
            {"name": "Blue Skin", "price": 20},
            {"name": "Red Skin", "price": 20},
        ]

        self.selected = 0

        # animation
        self.anim_time = 0

        # debounce
        self.last_input_time = 0
        self.input_delay = 120

        # sounds
        # self.move_sound = pygame.mixer.Sound("assets/sounds/move.wav")
        # self.select_sound = pygame.mixer.Sound("assets/sounds/select.wav")

        # owned skins
        self.owned = set(self.game.data.get("owned_skins", []))

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
            # self.move_sound.play()

        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % (len(self.items) + 1)
            # self.move_sound.play()

        elif event.key == pygame.K_RETURN:
            # self.select_sound.play()

            if self.selected == len(self.items):
                self.game.change_state(GameState.MENU)
            else:
                self.select_item()

    # =========================
    # LOGIC
    # =========================
    def select_item(self):
        item = self.items[self.selected]
        # DEFAULT SKIN
        if item.get("default"):
            self.game.data["selected_skin"] = item["name"]

        elif item["name"] in self.owned:
            self.game.data["selected_skin"] = item["name"]
        else:
            if self.game.data.get("coins", 0) >= item["price"]:
                self.game.data["coins"] -= item["price"]
                self.owned.add(item["name"])

                self.game.data["owned_skins"] = list(self.owned)
                self.game.data["selected_skin"] = item["name"]

        save_data(self.game.data)

    def update(self, dt):
        self.anim_time += dt * 0.04

    # =========================
    # DRAW
    # =========================
    def draw(self, screen):
        screen.fill((20, 20, 20))

        # title glow
        glow = 200 + int(math.sin(self.anim_time) * 4)
        title = self.font.render("SHOP", True, (0, 220, 220))
        screen.blit(title, (100, 50))

        # coins
        coins = self.game.data.get("coins", 0)
        coins_text = self.small_font.render(f"Coins: {coins}", True, (255, 255, 0))
        screen.blit(coins_text, (600, 20))

        # items
        for i, item in enumerate(self.items):
            y = 150 + i * 70

            selected = (i == self.selected)

            # scale animacija
            scale = 1.0
            if selected:
                scale = 1.0 + 0.05 * math.sin(self.anim_time * 1.5)

            # boje
            color = (255, 255, 255)
            if selected:
                color = (255, 200, 0)

            # tekst
            text_surface = self.font.render(item["name"], True, color)

            # scale apply
            text_rect = text_surface.get_rect(topleft=(100, y))
            scaled_surface = pygame.transform.scale(
                text_surface,
                (int(text_rect.width * scale), int(text_rect.height * scale))
            )

            screen.blit(scaled_surface, (100, y))

            # glow effect (outline)
            if selected:
                glow_color = (255, 180, 0)
                pygame.draw.rect(
                    screen,
                    glow_color,
                    (95, y - 5, text_rect.width + 10, text_rect.height + 10),
                    2
                )

            # price / owned
            if item.get("default"):
                price_text = "DEFAULT"
                price_color = (0, 200, 255)

            elif item["name"] in self.owned:
                price_text = "OWNED"
                price_color = (0, 255, 0)
            else:
                price_text = f"{item['price']} coins"
                price_color = (255, 255, 255)

            price_render = self.small_font.render(price_text, True, price_color)
            screen.blit(price_render, (400, y + 10))

        # BACK
        back_index = len(self.items)
        y = 150 + back_index * 70

        selected = (self.selected == back_index)

        color = (255, 255, 255)
        if selected:
            color = (255, 200, 0)

        text_surface = self.font.render("Back", True, color)

        scale = 1.0
        if selected:
            scale = 1.0 + 0.1 * math.sin(self.anim_time * 4)

        scaled_surface = pygame.transform.scale(
            text_surface,
            (int(text_surface.get_width() * scale),
             int(text_surface.get_height() * scale))
        )

        screen.blit(scaled_surface, (100, y))

        if selected:
            pygame.draw.rect(
                screen,
                (255, 180, 0),
                (95, y - 5, text_surface.get_width() + 10, text_surface.get_height() + 10),
                2
            )