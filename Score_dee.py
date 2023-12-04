from pico2d import *

import server


class Score_dee:
    def __init__(self, turn, dis, ball_dx):
        self.image = load_image('score_dee.png')
        self.distance = round(dis / 25, 1)
        self.x = dis
        self.y = 107
        self.plusdx = ball_dx
        self.type = turn % 2
        if self.type == 0:
            server.score['p1'].append(self.distance)
        else:
            server.score['p2'].append(self.distance)


        self.font = load_font('ENCR10B.TTF', 12)

    def update(self):
        pass

    def draw(self):

        self.dx = self.x - server.wadlle_ball.x + self.plusdx
        self.dy = self.y - server.wadlle_ball.y

        self.image.clip_composite_draw(self.type * 70, 4 * 70, 70, 70, 0, '',
                                       self.dx, self.dy, 70 * 1.5,
                                       70 * 1.5)
        self.font.draw(self.dx - 15, self.dy + 15,
                       f'{self.distance}m', (14, 14, 14))
