from pathlib import Path

from pico2d import *

CANVAS_WIDTH, CANVAS_HEIGHT = 1600, 600
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
        self.x, self.y = CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2
        self.frame = 0.0
        self.dir = 1
        self.speed = FLY_SPEED_PPS

    def update(self, frame_time):
        self.frame = (self.frame + FRAMES_PER_SECOND * frame_time) % FRAME_COUNT

        self.x += self.dir * self.speed * frame_time
        left, right = BIRD_WIDTH / 2, CANVAS_WIDTH - BIRD_WIDTH / 2
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


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        bird = Bird()
        running = True
        current_time = get_time()
        while running:
            new_time = get_time()
            frame_time = new_time - current_time
            current_time = new_time
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                    running = False
            if not running:
                break
            bird.update(frame_time)
            clear_canvas()
            bird.draw()
            update_canvas()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
