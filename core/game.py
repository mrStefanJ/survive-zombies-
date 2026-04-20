# =========================
# FILE: core/game.py
# =========================
import pygame
import random
from core.game_state import GameState
from systems.bomb_system import BombSystem
from ui.menu import Menu
from ui.game_over import GameOver
from ui.hud import HUD
from ui.shop import Shop
from ui.settings import Settings
from ui.highscore import Highscore
from ui.controls import Controls
from ui.pause import Pause
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

        self.pause_selected = 0
        self.pause_options = ["Resume", "Exit"]

        self.state = GameState.MENU

        if "owned_skins" not in self.data:
            self.data["owned_skins"] = ["Green Skin"]

        if "selected_skin" not in self.data:
            self.data["selected_skin"] = "Green Skin"

        # gameplay
        self.score = 0

        # bomb system
        self.bomb_system = BombSystem(self)

        # effects
        self.explosions = []
        self.particles = []

        # screen shake
        self.shake_duration = 0
        self.shake_intensity = 0

        self.death_slow = False
        self.death_timer = 0
        self.death_duration = 0.6  # trajanje slow-motion

        self.bomb_font = pygame.font.SysFont("Arial", 30, bold=True)

        # sound (safe load)
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.set_num_channels(16)

            self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
            self.explosion_sound.set_volume(0.7)

            pygame.mixer.music.load("assets/background/zombie-hot-dogs-2-back-from-the-bread.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

        except Exception as e:
            print("Sound error:", e)
            self.explosion_sound = None

        # UI
        self.menu = Menu(self)
        self.shop = Shop(self)
        self.settings = Settings(self)
        self.highscore = Highscore(self)
        self.game_over = GameOver(self)
        self.controls = Controls(self)
        self.hud = HUD()
        self.pause = Pause(self)

        self.reset()

    def reset(self):
        self.player = Player(self)
        self.zombies = ZombieManager()
        self.spawner = SpawnSystem(self.zombies)

        self.time_survived = 0
        self.score = 0

        self.bomb_system.reset()

        self.explosions.clear()
        self.particles.clear()

        self.death_slow = False
        self.death_timer = 0

    def toggle_pause(self):
        if self.state == GameState.PLAYING:
            self.pause_selected = 0
            self.change_state(GameState.PAUSED)

        elif self.state == GameState.PAUSED:
            self.change_state(GameState.PLAYING)
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

                # ESC → pause
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.toggle_pause()
                        continue
                    elif self.state == GameState.PAUSED:
                        self.toggle_pause()
                        continue

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
                elif self.state == GameState.PAUSED:
                    self.handle_pause_event(event)

                # 🔥 SPACE bomb (single press)
                if event.type == pygame.KEYDOWN:
                    if self.state == GameState.PLAYING:
                        if event.key == pygame.K_SPACE:
                            self.bomb_system.throw(
                                (self.player.rect.centerx, self.player.rect.centery)
                            )

            # UPDATE + DRAW
            if self.state == GameState.MENU:
                self.menu.update()
                self.menu.draw(self.screen)

            elif self.state == GameState.SHOP:
                self.shop.update(dt)
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

            elif self.state == GameState.PAUSED:
                self.draw_game()  # background freeze
                self.pause.draw()


            elif self.state == GameState.GAME_OVER:
                self.game_over.update()
                self.game_over.draw(self.screen)

            pygame.display.flip()

    def finish_game_over(self):
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

        if self.score > self.data.get("highscore", 0):
            self.data["highscore"] = self.score

        if "coins" not in self.data:
            self.data["coins"] = 0

        self.data["coins"] += self.score

        save_data(self.data)

        self.change_state(GameState.GAME_OVER)
    # =========================
    # GAME UPDATE
    # =========================
    def update_game(self, dt):
        self.time_survived += dt

        # =========================
        # SLOW MOTION DEATH
        # =========================
        if self.death_slow:
            self.death_timer -= dt

            slow_factor = 0.15  # koliko usporava (0.1 = ultra slow)
            dt *= slow_factor

            if self.death_timer <= 0:
                self.death_slow = False

                # 🔥 tek sada ide game over
                self.finish_game_over()

        self.player.update(dt)
        self.spawner.update(self.time_survived)
        self.zombies.update(self.player)
        self.bomb_system.update(dt)
        self.update_explosions(dt)
        self.update_particles(dt)
        self.update_shake(dt)

        if not self.death_slow and self.zombies.check_collision(self.player):
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
            px, py = self.player.rect.center
            ex, ey = pos

            distance = ((px - ex) ** 2 + (py - ey) ** 2) ** 0.5
            max_distance = 500

            volume = max(0.0, min(1.0, 1 - distance / max_distance))

            self.explosion_sound.set_volume(volume)
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
        self.bomb_system.draw(self.screen)

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
        for i in range(self.bomb_system.max_bombs):

            x = 20 + i * 40
            y = HEIGHT - 50

            if i < self.bomb_system.current_bombs:
                color = (255, 140, 0)
            else:
                color = (80, 80, 80)

            pygame.draw.circle(self.screen, color, (x, y), 12)

        # cooldown bar
        if self.bomb_system.current_bombs < self.bomb_system.max_bombs:
            progress = self.bomb_system.bomb_timer / self.bomb_system.bomb_cooldown

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

        # =========================
        # DEATH OVERLAY
        # =========================
        if self.death_slow:
            alpha = int(150 * (1 - self.death_timer / self.death_duration))

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(alpha)
            overlay.fill((150, 0, 0))  # crveni tint

            self.screen.blit(overlay, (0, 0))

        # HUD
        self.hud.draw(self.screen, self.time_survived, self.score)

    # =========================
    # STATE
    # =========================
    def change_state(self, new_state):
        self.state = new_state

        # 🔥 TRIGGER ENTER
        if new_state == GameState.GAME_OVER:
            self.game_over.enter()
        elif new_state == GameState.HIGHSCORE:
            self.highscore.enter()

        elif new_state == GameState.SETTINGS:
            self.settings.enter()

        elif new_state == GameState.CONTROLS:
            self.controls.enter()

        elif new_state == GameState.MENU:
            self.menu.enter()

    def handle_pause_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP:
            self.pause_selected = (self.pause_selected - 1) % len(self.pause_options)

        elif event.key == pygame.K_DOWN:
            self.pause_selected = (self.pause_selected + 1) % len(self.pause_options)

        elif event.key == pygame.K_RETURN:
            option = self.pause_options[self.pause_selected]

            if option == "Resume":
                self.change_state(GameState.PLAYING)

            elif option == "Exit":
                self.change_state(GameState.MENU)
                self.reset()

    # =========================
    # GAME OVER
    # =========================
    def handle_game_over(self):
        if self.death_slow:
            return

        self.death_slow = True
        self.death_timer = self.death_duration

        if self.score > self.data.get("highscore", 0):
            self.data["highscore"] = self.score