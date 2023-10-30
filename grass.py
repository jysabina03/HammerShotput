from pico2d import load_image

class Grass:

    grass_num = 0

    def __init__(self,y):
        self.image = load_image('grass.png')
        self.grass_y = y

    def draw(self):
        self.image.draw(400,self.grass_y)

    def update(self):
        pass
