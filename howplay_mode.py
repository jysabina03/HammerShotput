from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, pico2d
from sdl2 import SDLK_ESCAPE, SDL_KEYDOWN, SDL_QUIT, SDLK_SPACE, SDLK_1

import game_framework
import play_mode
import title_mode

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_FAST = 6
FRAMES_PER_ACTION_SLOW = 0.5


def init():

    global image_kirby,image_how_to_play
    global button_onoff

    global buttonX, buttonY
    global cur_mouse_x, cur_mouse_y, frame1,frame2

    frame1, frame2 = 0,0

    image_how_to_play= load_image('./texture/how_to_play.png')
    image_kirby = load_image('./texture/sp_kirby.png')


    pass

def finish():
    pass

def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)


    pass

def update():
    pass

def draw():
    global frame1, frame2


    image_how_to_play.draw(400, 300)


    frame1 = (frame1 + FRAMES_PER_ACTION_SLOW * ACTION_PER_TIME * game_framework.frame_time) % 2
    frame2 = (frame2 + FRAMES_PER_ACTION_FAST * ACTION_PER_TIME * game_framework.frame_time) % 8

    image_kirby.clip_composite_draw(int(frame1) * 100, 5 * 100, 100, 100, 0, '', 150, 380,
                                    100 * 2, 100 * 2)

    image_kirby.clip_composite_draw(int(frame2) * 120, 4 * 100, 120, 100, 0, '',
                                 600 , 300 , 120 * 2, 100 * 2)


    update_canvas()

def finish():
    pass

def pause(): pass
def resume(): pass
