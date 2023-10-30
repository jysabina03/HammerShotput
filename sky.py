from pico2d import load_image

class Sky:

    grass_num = 0

    def __init__(self,x):
        self.image = load_image('sky.PNG')  # 1000*600
        self.sky_x = x+500

    def draw(self):
        self.image.draw(self.sky_x,300)

    def update(self):
        pass
