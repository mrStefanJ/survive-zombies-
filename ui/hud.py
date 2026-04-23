import pygame

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 30)

    def format_time(self, time_seconds):
        minutes = int(time_seconds) // 60
        seconds = int(time_seconds) % 60
        return f"{minutes}:{seconds:02d}"

    def draw(self, screen, time_survived, highscore):
        time_text = self.format_time(time_survived)

        screen.blit(
            self.font.render(f"Time: {time_text}", True, (255, 255, 255)),
            (10, 10)
        )

        screen.blit(
            self.font.render(f"Highscore: {highscore}", True, (255, 255, 0)),
            (10, 40)
        )