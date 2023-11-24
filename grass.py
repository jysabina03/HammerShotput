from pico2d import load_image, get_canvas_width, get_canvas_height, clamp
import server

class Grass:
    grass_num = 0

    def __init__(self,y):
        self.image = load_image('grass.png')
        self.grass_y = y
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        self.image.clip_draw_to_origin(self.q1l, 0, self.q1w, 62, 0, 0)
        self.image.clip_draw_to_origin(self.q2l, 0, self.q2w, 62, self.q1w, 0)

    def update(self):
        self.q1l = (int(server.wadlle_ball.x) - self.cw // 2) % self.w
        self.q1w = clamp(0, self.w - self.q1l, self.w)

        self.q2l = (self.q1l + self.q1w) % self.w  # 수정된 부분
        self.q2w = clamp(0, self.w - self.q2l, self.w)



