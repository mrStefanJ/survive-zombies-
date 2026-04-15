# =========================
# FILE: ui/shop.py
# =========================
import pygame
from core.game_state import GameState
from data.save_system import save_data

class Shop:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 25)

        self.options = ["Back"]

        # stavke u shop-u sa cenama
        self.items = [
            {"name": "Red Skin", "price": 20},
            {"name": "Blue Skin", "price": 20},
            {"name": "Green Skin", "price": 20},
        ]
        self.selected = 0
        self.key_pressed = False

        # pratimo koji skinovi su kupljeni
        self.owned = set()
        if "owned_skins" in self.game.data:
            self.owned = set(self.game.data["owned_skins"])

    def enter(self):
        self.key_pressed = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                self.game.change_state(GameState.MENU)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and not self.key_pressed:
            self.selected = (self.selected - 1) % len(self.items)
            self.key_pressed = True

        elif keys[pygame.K_DOWN] and not self.key_pressed:
            self.selected = (self.selected + 1) % len(self.items)
            self.key_pressed = True

        elif keys[pygame.K_RETURN] and not self.key_pressed:
            self.select_item()
            self.key_pressed = True

        if not any(keys):
            self.key_pressed = False

    def select_item(self):
        item = self.items[self.selected]

        if item["name"] == "Back":
            self.game.state = GameState.MENU
            return

        # kupovina ili već owned
        if item["name"] in self.owned:
            # već owned, samo select skin
            self.game.data["selected_skin"] = item["name"]
        else:
            if self.game.data.get("coins",0) >= item["price"]:
                self.game.data["coins"] -= item["price"]
                self.owned.add(item["name"])
                self.game.data["owned_skins"] = list(self.owned)
                self.game.data["selected_skin"] = item["name"]
            else:
                # nemas dovoljno coins
                print("Not enough coins!")

        save_data(self.game.data)

    def draw(self, screen):
        screen.fill((20,20,50))
        title = self.font.render("SHOP", True, (255,200,0))
        screen.blit(title, (100,50))

        # prikazi ukupno coins
        coins = self.game.data.get("coins",0)
        coins_text = self.small_font.render(f"Coins: {coins}", True, (255,255,0))
        screen.blit(coins_text, (600, 20))  # gornji desni ugao

        # lista skinova
        for i, item in enumerate(self.items):
            color = (255,255,255)
            price_color = (255,255,255)

            if i == self.selected:
                color = (255,200,0)

            # promena boje ako je skin owned
            if item["name"] in self.owned and item["name"] != "Back":
                price_color = (0,255,0)  # zeleno = owned
                price_text = "OWNED"
            elif item["name"] != "Back":
                price_text = f"{item['price']} coins"
            else:
                price_text = ""

            text = self.font.render(item["name"], True, color)
            screen.blit(text, (100,150 + i*60))

            if price_text:
                price_render = self.small_font.render(price_text, True, price_color)
                screen.blit(price_render, (350, 165 + i*60))  # pored naziva