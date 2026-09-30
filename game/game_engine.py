"""
GameEngine: owns the basket and all falling objects.

Starter version: basket movement and spawning both work at a basic
level (Tasks 2 and 3 ask you to improve them), there's no speed boost
yet (Task 4 builds it from scratch), and catch detection has two
known bugs (see game/collision.py and the catch-checking loop below)
that Task 1 asks you to fix.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_MIN = 35
SPAWN_INTERVAL_MAX = 65
MAX_OBJECTS = 5
MAX_MISSES = 5
MIN_SPAWN_DISTANCE = 50


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.score = 0
        self.misses = 0
        self.game_over = False
        self.last_spawn_x = None

    def _spawn_object(self):
        if len(self.objects) >= MAX_OBJECTS:
            return

        default_radius = 14
        min_x = default_radius
        max_x = WIDTH - default_radius

        # Pick random x within screen bounds, avoiding positions too close to last spawn x
        x = random.randint(min_x, max_x)
        if self.last_spawn_x is not None:
            for _ in range(5):
                if abs(x - self.last_spawn_x) >= MIN_SPAWN_DISTANCE:
                    break
                x = random.randint(min_x, max_x)

        self.last_spawn_x = x
        self.objects.append(FallingObject(x=x, y=-default_radius, radius=default_radius, speed=3))

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed

        # Boundary handling: account for basket's half width so it stays fully on screen
        half_width = self.basket.width / 2
        self.basket.x = max(half_width, min(WIDTH - half_width, self.basket.x))

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()
        elif not self.game_over and key == pygame.K_SPACE:
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return

        self.basket.update()

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            if len(self.objects) < MAX_OBJECTS:
                self._spawn_object()
                self.frames_until_spawn = random.randint(SPAWN_INTERVAL_MIN, SPAWN_INTERVAL_MAX)
            else:
                # Delay spawn check briefly if maximum active object count reached
                self.frames_until_spawn = 10

        for obj in self.objects:
            obj.update()

        # Safe collision handling without mutating self.objects during iteration
        basket_rect = self.basket.get_rect()
        remaining_objects = []
        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
            else:
                remaining_objects.append(obj)
        self.objects = remaining_objects

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))

        if self.basket.is_boosted:
            renderer.draw_text(surface, font, "BOOST ACTIVE", (WIDTH - 160, 10), color=(255, 200, 50))

        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")

