from pico2d import *

import server


class Distance_sign:
    def __init__(self):
        self.image = load_image('wadlle_m.png')
        self.y = 107

        self.font = load_font('ENCR10B.TTF', 12)

    def update(self):
        pass

    def draw(self):
        dx = -server.wadlle_ball.x
        dy = self.y - server.wadlle_ball.y
        normal = round(-server.wadlle_ball.x,1)

        for i in range(0, int(server.wadlle_ball.x + 1000), 250):


            self.image.clip_composite_draw(0, 0, 70, 70, 0, '',
                                           dx + i+280, dy, 70 * 1.5, 70 * 1.5)
            self.font.draw(dx + i - 15+280 , dy + 15, f'{i / 25}m', (14, 14, 14))

        for i in range(0, 100):
            normal=i*100
            self.font.draw(dx +normal+280, dy + 55, f'{i*100}pixel', (14, 14, 14))
            self.font.draw(dx +normal+280, dy + 40, f'{i*100/25}m', (14, 14, 14))
