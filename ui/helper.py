import pygame
import math


class UIHelper:
    @staticmethod
    def draw_title(screen, text, font, time, y=80, color=(0, 255, 200)):
        """
        Draw animated title with pulse, shadow and glow.

        :param screen: pygame surface
        :param text: string (title text)
        :param font: pygame font
        :param time: animation time (float)
        :param y: vertical position
        :param color: main color
        """

        scale = 1 + math.sin(time) * 0.05

        # MAIN
        title_surface = font.render(text, True, color)
        title_surface = pygame.transform.rotozoom(title_surface, 0, scale)

        w = screen.get_width()
        title_rect = title_surface.get_rect(center=(w // 2, y))

        # SHADOW
        shadow = font.render(text, True, (0, 80, 60))
        shadow = pygame.transform.rotozoom(shadow, 0, scale)
        screen.blit(shadow, (title_rect.x + 5, title_rect.y + 5))

        # GLOW
        glow = font.render(text, True, (0, 180, 120))
        glow = pygame.transform.rotozoom(glow, 0, scale)
        screen.blit(glow, (title_rect.x - 2, title_rect.y - 2))

        # MAIN TEXT
        screen.blit(title_surface, title_rect)