from pico2d import *

import server


class Distance_sign:
    def __init__(self):
        # self.image = load_image('wadlle_m.png')
        self.dis_kirby = load_image('./texture/Distance_UI_kirby.png')
        self.dis_DDD = load_image('./texture/Distance_UI_DDD.png')
        self.dis_now = load_image('./texture/Distance_UI.png')

        self.font = load_font('ENCR10B.TTF', 18)

    def update(self):
        pass

    def draw(self):
        self.dis_now.clip_composite_draw(0, 0, 150, 30, 0, '', 75, 550, 150, 30)
        self.font.draw(10, 550, f'now {round(server.wadlle_ball.x / 25, 1)}m', (14, 14, 14))

        if server.turn <6:
            self.dis_kirby.clip_composite_draw(0, 0, 150, 30, 0, '', 75, 450, 150, 30)
            self.font.draw(10, 450, f'P1: {round(server.score["p1"][int(server.turn / 2)], 1)}m', (14, 14, 14))

            self.dis_DDD.clip_composite_draw(0, 0, 150, 30, 0, '', 75, 350, 150, 30)
            self.font.draw(10, 350, f'P2: {round(server.score["p2"][int((server.turn - 1) / 2)], 1)}m', (14, 14, 14))

    # for i in range(0, int(server.wadlle_ball.x + 1000), 250):

    #     dx = i - server.wadlle_ball.x + 0 + server.wadlle_ball.normal_x
    #     dy = self.y - server.wadlle_ball.y

    # self.image.clip_composite_draw(0, 0, 70, 70, 0, '',
    #                               dx, dy, 70 * 1.5, 70 * 1.5)
    # self.font.draw(dx - 15 , dy + 15, f'{i / 25}m', (14, 14, 14))

    # for i in range(0, 100):
    #    self.font.draw(dx +normal+280, dy + 55, f'{i*100}pixel', (14, 14, 14))
    #   self.font.draw(dx +normal+280, dy + 40, f'{i*100/25}m', (14, 14, 14))
