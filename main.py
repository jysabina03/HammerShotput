from pico2d import open_canvas, close_canvas

import game_framework
import play_mode
import result_mode
import title_mode

open_canvas()
game_framework.run(title_mode)
close_canvas()

