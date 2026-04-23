# =========================
# FILE: systems/zombie_system.py
# =========================
import pygame
import random

class Zombie:
    def __init__(self, pos, zombie_type="normal"):
        self.type = zombie_type

        self.rect = pygame.Rect(pos[0], pos[1], 30, 30)

        if self.type == "normal":
            self.speed = 1.5
            self.color = (255, 0, 0)

        elif self.type == "fast":
            self.speed = 2
            self.color = (255, 165, 0)

        elif self.type == "tank":
            self.speed = 0.8
            self.color = (139, 0, 0)
            self.rect.inflate_ip(20, 20)

        else:
            # safety fallback (OBAVEZNO)
            self.speed = 1.5
            self.color = (255, 0, 0)

    def update(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        dist = (dx**2 + dy**2) ** 0.5

        if dist != 0:
            dx /= dist
            dy /= dist

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class ZombieManager:
    def __init__(self):
        self.zombies = []

    def add_zombie(self, pos, time_survived):
        if time_survived < 60:
            z_type = "normal"
        elif time_survived < 120:
            z_type = random.choice(["normal", "fast"])
        else:
            z_type = random.choice(["normal", "fast", "tank"])

        zombie = Zombie(pos, z_type)
        self.zombies.append(zombie)

    def update(self, player):
        for z in self.zombies:
            z.update(player)

    def draw(self, screen):
        for z in self.zombies:
            z.draw(screen)

    def check_collision(self, player):
        return any(z.rect.colliderect(player.rect) for z in self.zombies)