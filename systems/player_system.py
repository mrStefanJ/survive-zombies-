import pygame

class Player:
    def __init__(self, game):
        self.game = game
        self.rect = pygame.Rect(400, 300, 40, 40)
        self.speed = 200

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.rect.y += self.speed * dt
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt

        # ✅ koristi game dimenzije
        self.rect.x = max(0, min(self.rect.x, self.game.world_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.game.world_height - self.rect.height))

    def draw(self, screen):
        skin = self.game.data.get("selected_skin", "Green Skin")

        color = (0, 255, 0)

        if skin == "Red Skin":
            color = (255, 0, 0)
        elif skin == "Blue Skin":
            color = (0, 0, 255)

        pygame.draw.rect(screen, color, self.rect)