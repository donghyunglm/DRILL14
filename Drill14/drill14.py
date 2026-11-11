from pathlib import Path

from pico2d import *

CANVAS_WIDTH, CANVAS_HEIGHT = 1600, 600


class Bird:
    image = None

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image(str(Path(__file__).with_name('bird_animation.png')))
        self.x, self.y = CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2

    def update(self, frame_time):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)


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
