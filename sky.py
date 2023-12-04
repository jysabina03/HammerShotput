from pico2d import load_image, get_canvas_width, get_canvas_height, clamp
import server


class Sky:
    grass_num = 0

    def __init__(self):
        self.window_left = None
        self.image = load_image('./texture/sky.PNG')  # 1000*600

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        self.image.clip_draw_to_origin(self.q1l, 0, self.q1w, 600, 0, 0)
        self.image.clip_draw_to_origin(self.q2l, 0, self.q2w, 600, self.q1w, 0)

    def update(self):
        self.window_left = clamp(0, int(server.wadlle_ball.x) - self.cw // 2, self.w - self.cw - 1)

        self.q1l = (int(server.wadlle_ball.x) - self.cw // 2) % self.w
        self.q1w = clamp(0, self.w - self.q1l, self.w)

        self.q2l = (self.q1l + self.q1w) % self.w  # 수정된 부분
        self.q2w = clamp(0, self.w - self.q2l, self.w)
