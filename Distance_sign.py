from pico2d import *
import game_world
import game_framework
import random

import server


class Distance_sign:
    def __init__(self):
        self.image = load_image('wadlle_m.png')
        self.x = 280
        self.y = 107

        self.font = load_font('ENCR10B.TTF', 12)

    def update(self):
        pass

    def draw(self):
        dx = self.x - server.wadlle_ball.x
        dy = self.y - server.wadlle_ball.y

        for i in range(500,int(server.wadlle_ball.x+1000),500):
            self.image.clip_composite_draw(0, 0, 70, 70, 0, '',
                                         dx+i, dy, 70 * 1.5, 70 * 1.5)
            self.font.draw(dx+i-15, dy+15, f'{i/50}m', (14, 14, 14))
