import random
from pathlib import Path

from pico2d import *

import game_framework

FRAME_COUNT = 14
FRAMES_PER_SECOND = FRAME_COUNT / 0.7
BIRD_WIDTH, BIRD_HEIGHT = 100, 92
PIXEL_PER_METER = 10.0 / 0.3
FLY_SPEED_KMPH = 30.0
FLY_SPEED_PPS = FLY_SPEED_KMPH * 1000.0 / 3600.0 * PIXEL_PER_METER


class Bird:
    image = None

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image(str(Path(__file__).with_name('bird_animation.png')))
        self.x = random.uniform(BIRD_WIDTH / 2, get_canvas_width() - BIRD_WIDTH / 2)
        self.y = random.uniform(250, get_canvas_height() - BIRD_HEIGHT / 2)
        self.frame = random.uniform(0, FRAME_COUNT)
        self.dir = random.choice((-1, 1))
        self.speed = FLY_SPEED_PPS * random.uniform(0.8, 1.2)

    def update(self):
        frame_time = game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_SECOND * frame_time) % FRAME_COUNT

        self.x += self.dir * self.speed * frame_time
        left, right = BIRD_WIDTH / 2, get_canvas_width() - BIRD_WIDTH / 2
        # Reflect overshoot as well, including frames spanning multiple turns.
        while self.x < left or self.x > right:
            if self.x > right:
                self.x = 2 * right - self.x
                self.dir = -1
            elif self.x < left:
                self.x = 2 * left - self.x
                self.dir = 1
        if self.x == left:
            self.dir = 1
        elif self.x == right:
            self.dir = -1

    def draw(self):
        # Source: 918 x 506, 5 columns x 3 rows, last cell empty.
        # Read left to right, top to bottom; pico2d clips from the bottom.
        row, column = divmod(int(self.frame), 5)
        left = round(column * self.image.w / 5)
        right = round((column + 1) * self.image.w / 5)
        top = round(row * self.image.h / 3)
        bottom = round((row + 1) * self.image.h / 3)
        if self.dir == 1:
            self.image.clip_draw(left, self.image.h - bottom,
                                 right - left, bottom - top,
                                 self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)
        else:
            self.image.clip_composite_draw(
                left, self.image.h - bottom, right - left, bottom - top,
                0, 'h', self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

