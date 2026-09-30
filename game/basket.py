"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


BOOST_DURATION_FRAMES = 180  # 3 seconds at 60 FPS
BOOST_SPEED_MULTIPLIER = 1.8


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.normal_speed = speed
        self.boost_speed = speed * BOOST_SPEED_MULTIPLIER
        self.speed = speed
        self.boosted_frames = 0

    @property
    def is_boosted(self):
        return self.boosted_frames > 0

    def activate_boost(self):
        """Activates temporary speed boost if not already active."""
        if not self.is_boosted:
            self.boosted_frames = BOOST_DURATION_FRAMES

    def update(self):
        """Updates basket state each frame, managing active speed boost duration."""
        if self.boosted_frames > 0:
            self.boosted_frames -= 1
            self.speed = self.boost_speed
        else:
            self.speed = self.normal_speed

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )

