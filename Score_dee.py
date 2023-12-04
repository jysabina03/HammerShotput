from pico2d import *

import server


class Score_dee:
    def __init__(self, turn, dis, ball_dx):
        self.image = load_image('./texture/score_dee.png')
        self.distance = round(dis / 25, 1)
        self.x = dis
        self.y = 107
        self.plusdx = ball_dx
        self.turn = turn
        self.type = turn % 2
        if self.type == 0:
            server.score["p1"][int(server.turn / 2)] = self.distance
        else:
            server.score["p2"][int((server.turn-1) / 2)] = self.distance

        self.font = load_font('ENCR10B.TTF', 12)
        self.font_s = load_font('ENCR10B.TTF', 9)

    def update(self):
        pass

    def draw(self):

        self.dx = self.x - server.wadlle_ball.x + self.plusdx
        self.dy = self.y - server.wadlle_ball.y

        if self.type == 0:
            self.image.clip_composite_draw(self.type * 70, 4 * 70, 70, 70, 0, '', 50 * (self.turn+1) / 2+10, 450+57, 70*1.2,
                                           70*1.2)
            self.font_s.draw(50 * (self.turn+1) / 2 - 15+10, 450+55 + 13, f'{self.distance}m', (14, 14, 14))
        else:
            self.image.clip_composite_draw(self.type * 70, 4 * 70, 70, 70, 0, '', 50 * self.turn / 2+10, 350+57,
                                           70*1.2, 70*1.2)
            self.font_s.draw(50 * self.turn / 2 - 15+10, 350+55 + 13, f'{self.distance}m', (14, 14, 14))

        self.image.clip_composite_draw(self.type * 70, 4 * 70, 70, 70, 0, '',
                                       self.dx, self.dy, 70 * 1.5,70 * 1.5)
        self.font.draw(self.dx - 19, self.dy + 15,
                       f'{self.distance}m', (14, 14, 14))
