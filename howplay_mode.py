from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, pico2d
from sdl2 import SDLK_ESCAPE, SDL_KEYDOWN, SDL_QUIT, SDLK_SPACE, SDLK_1

import game_framework
import game_world
import play_mode
from pannel import Pannel


def init():
    global pannel
    pannel = Pannel()
    game_world.add_object(pannel,3)

    pass

def finish():
    pass

def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_0:
                    play_mode.boy.item = None
                    game_framework.pop_mode()
                case pico2d.SDLK_1:
                    play_mode.boy.item = 'Ball'
                    game_framework.pop_mode()
                case pico2d.SDLK_2:
                    play_mode.boy.item = 'BigBall'
                    game_framework.pop_mode()


    pass

def update():
    game_world.update()
    pass

def draw():

    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.remove_object(pannel)
    pass

def pause(): pass
def resume(): pass
