# =========================
# FILE: core/game.py
# =========================
import pygame
import random
from core.game_state import GameState
from ui.menu import Menu
from ui.game_over import GameOver
from ui.hud import HUD
from ui.shop import Shop
from ui.settings import Settings
from ui.highscore import Highscore
from ui.controls import Controls
from systems.player_system import Player
from systems.zombie_system import ZombieManager
from systems.spawn_system import SpawnSystem
from data.settings import WIDTH, HEIGHT
from data.save_system import load_data, save_data


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Survivor")
        self.clock = pygame.time.Clock()

        self.data = load_data()

        self.state = GameState.MENU

        # gameplay
        self.bombs = []
        self.explosion_time = 3
        self.score = 0

        # effects
        self.explosions = []
        self.particles = []

        # screen shake
        self.shake_duration = 0
        self.shake_intensity = 0
        self.max_bombs = 5
        self.current_bombs = 5

        self.bomb_cooldown = 2.0  # sekunde za regeneraciju 1 bombe
        self.bomb_timer = 0

        # sound (safe load)
        try:
            pygame.mixer.init()
            self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
        except:
            self.explosion_sound = None

        # UI
        self.menu = Menu(self)
        self.shop = Shop(self)
        self.settings = Settings(self)
        self.highscore = Highscore(self)
        self.game_over = GameOver(self)
        self.controls = Controls(self)
        self.hud = HUD()

        self.reset()

    def reset(self):
        self.player = Player()
        self.zombies = ZombieManager()
        self.spawner = SpawnSystem(self.zombies)

        self.time_survived = 0
        self.score = 0
        self.bombs.clear()
        self.explosions.clear()
        self.particles.clear()

    # =========================
    # MAIN LOOP
    # =========================
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000

            # INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == GameState.MENU:
                    self.menu.handle_event(event)
                elif self.state == GameState.SHOP:
                    self.shop.handle_event(event)
                elif self.state == GameState.SETTINGS:
                    self.settings.handle_event(event)
                elif self.state == GameState.HIGHSCORE:
                    self.highscore.handle_event(event)
                elif self.state == GameState.CONTROLS:
                    self.controls.handle_event(event)
                elif self.state == GameState.GAME_OVER:
                    self.game_over.handle_event(event)

                # 🔥 SPACE bomb (single press)
                if event.type == pygame.KEYDOWN:
                    if self.state == GameState.PLAYING:
                        if event.key == pygame.K_SPACE:
                            self.throw_bomb()

            # UPDATE + DRAW
            if self.state == GameState.MENU:
                self.menu.update()
                self.menu.draw(self.screen)

            elif self.state == GameState.SHOP:
                self.shop.update()
                self.shop.draw(self.screen)

            elif self.state == GameState.SETTINGS:
                self.settings.update()
                self.settings.draw(self.screen)

            elif self.state == GameState.HIGHSCORE:
                self.highscore.update()
                self.highscore.draw(self.screen)

            elif self.state == GameState.PLAYING:
                self.update_game(dt)
                self.draw_game()

            elif self.state == GameState.CONTROLS:
                self.controls.update()
                self.controls.draw(self.screen)

            elif self.state == GameState.GAME_OVER:
                self.game_over.update()
                self.game_over.draw(self.screen)

            pygame.display.flip()

    # =========================
    # GAME UPDATE
    # =========================
    def update_game(self, dt):
        self.time_survived += dt

        # recharge bombi
        if self.current_bombs < self.max_bombs:
            self.bomb_timer += dt

            if self.bomb_timer >= self.bomb_cooldown:
                self.current_bombs += 1
                self.bomb_timer = 0

        self.player.update(dt)
        self.spawner.update(self.time_survived)
        self.zombies.update(self.player)

        self.update_bombs(dt)
        self.update_explosions(dt)
        self.update_particles(dt)
        self.update_shake(dt)

        if self.zombies.check_collision(self.player):
            self.handle_game_over()

    # =========================
    # BOMBS
    # =========================
    def throw_bomb(self):
        if self.current_bombs <= 0:
            return  # nema bombi

        pos = (self.player.rect.centerx, self.player.rect.centery)

        self.bombs.append({
            "pos": pos,
            "timer": self.explosion_time
        })

        self.current_bombs -= 1

    def update_bombs(self, dt):
        for bomb in self.bombs[:]:
            bomb["timer"] -= dt

            if bomb["timer"] <= 0:
                self.explode(bomb["pos"])
                self.bombs.remove(bomb)

    # =========================
    # EXPLOSION
    # =========================
    def explode(self, pos):
        explosion_radius = 100
        killed = []

        for z in self.zombies.zombies:
            dx = z.rect.centerx - pos[0]
            dy = z.rect.centery - pos[1]
            if (dx**2 + dy**2) ** 0.5 <= explosion_radius:
                killed.append(z)

        for z in killed:
            self.zombies.zombies.remove(z)

        self.score += len(killed)

        # visual
        self.explosions.append({
            "pos": pos,
            "radius": 10,
            "alpha": 255
        })

        # particles
        for _ in range(25):
            self.particles.append({
                "pos": list(pos),
                "vel": [random.uniform(-4, 4), random.uniform(-4, 4)],
                "life": random.uniform(0.3, 0.8)
            })

        # shake
        self.shake_duration = 0.3
        self.shake_intensity = 10

        # sound
        if self.explosion_sound:
            self.explosion_sound.play()

    def update_explosions(self, dt):
        for exp in self.explosions[:]:
            exp["radius"] += 300 * dt
            exp["alpha"] -= 400 * dt

            if exp["alpha"] <= 0:
                self.explosions.remove(exp)

    def update_particles(self, dt):
        for p in self.particles[:]:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["life"] -= dt

            if p["life"] <= 0:
                self.particles.remove(p)

    def update_shake(self, dt):
        if self.shake_duration > 0:
            self.shake_duration -= dt
        else:
            self.shake_intensity = 0

    # =========================
    # DRAW
    # =========================
    def draw_game(self):
        offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
        offset_y = random.randint(-self.shake_intensity, self.shake_intensity)

        self.screen.fill((30, 30, 30))

        # player
        self.player.draw(self.screen)

        # zombies
        self.zombies.draw(self.screen)

        # bombs
        for bomb in self.bombs:
            pygame.draw.circle(
                self.screen,
                (255, 100, 0),
                (int(bomb["pos"][0]), int(bomb["pos"][1])),
                15
            )

        # particles
        for p in self.particles:
            pygame.draw.circle(
                self.screen,
                (255, 180, 50),
                (int(p["pos"][0] + offset_x), int(p["pos"][1] + offset_y)),
                3
            )

        # =========================
        # BOMB UI
        # =========================
        for i in range(self.max_bombs):
            x = 20 + i * 40
            y = HEIGHT - 50

            # puna bomba
            if i < self.current_bombs:
                color = (255, 140, 0)
            else:
                color = (80, 80, 80)

            pygame.draw.circle(self.screen, color, (x, y), 12)

        # cooldown bar
        if self.current_bombs < self.max_bombs:
            progress = self.bomb_timer / self.bomb_cooldown

            bar_width = 100
            pygame.draw.rect(self.screen, (100, 100, 100), (20, HEIGHT - 25, bar_width, 8))
            pygame.draw.rect(self.screen, (255, 140, 0), (20, HEIGHT - 25, bar_width * progress, 8))

        # explosion
        for exp in self.explosions:
            surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

            pygame.draw.circle(
                surf,
                (255, 140, 0, int(exp["alpha"])),
                (int(exp["pos"][0]), int(exp["pos"][1])),
                int(exp["radius"])
            )

            pygame.draw.circle(
                surf,
                (255, 200, 50, int(exp["alpha"] * 0.5)),
                (int(exp["pos"][0]), int(exp["pos"][1])),
                int(exp["radius"] * 1.3),
                width=5
            )

            self.screen.blit(surf, (0, 0))

        # HUD
        self.hud.draw(self.screen, self.time_survived, self.score)

    # =========================
    # STATE
    # =========================
    def change_state(self, new_state):
        self.state = new_state

    # =========================
    # GAME OVER
    # =========================
    def handle_game_over(self):
        if "leaderboard" not in self.data:
            self.data["leaderboard"] = []

        self.data["leaderboard"].append({
            "name": "YOU",
            "score": self.score
        })

        self.data["leaderboard"] = sorted(
            self.data["leaderboard"],
            key=lambda x: x["score"],
            reverse=True
        )[:5]

        save_data(self.data)

        self.change_state(GameState.GAME_OVER)