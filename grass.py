from pico2d import load_image, get_canvas_width, get_canvas_height, clamp

import game_framework
import server


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_SLOW = 0.5

class Grass:
    grass_num = 0

    def __init__(self, y):
        self.image = load_image('./texture/grass.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        self.image.clip_draw_to_origin(self.q1l, 0, self.q1w, 62, 0, self.dy)
        self.image.clip_draw_to_origin(self.q2l, 0, self.q2w, 62, self.q1w, self.dy)

    def update(self):
        self.dy = 0 - server.wadlle_ball.y-1


        self.window_left = clamp(0, int(server.wadlle_ball.x+280) - self.cw // 2, self.w - self.cw - 1)

        self.q1l = (int(server.wadlle_ball.x) - self.cw // 2) % self.w
        self.q1w = clamp(0, self.w - self.q1l, self.w)

        self.q2l = (self.q1l + self.q1w) % self.w  # 수정된 부분
        self.q2w = clamp(0, self.w - self.q2l, self.w)


class Grass_simple:
    def __init__(self):
        self.image = load_image('./texture/grass.png')

    def draw(self):
        self.image.draw(400, 30)

    def update(self):
        pass
