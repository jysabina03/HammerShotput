from pico2d import open_canvas, close_canvas

import game_framework
import play_mode


open_canvas()
game_framework.run(play_mode)
close_canvas()

