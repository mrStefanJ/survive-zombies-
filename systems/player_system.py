import pygame

class Player:
    def __init__(self, skin="default"):
        self.skin = skin
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

    def draw(self, screen):
        color = (0, 255, 0)

        if self.skin == "blue":
            color = (0, 0, 255)
        elif self.skin == "gold":
            color = (255, 215, 0)

        pygame.draw.rect(screen, color, self.rect)

        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))