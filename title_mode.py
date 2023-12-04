from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, get_canvas_height
from sdl2 import SDLK_ESCAPE, SDL_KEYDOWN, SDL_QUIT, SDLK_SPACE, SDL_MOUSEMOTION

import game_framework
import play_mode


def init():
    global BG_image, grass1,button_play,button_how
    global mouse_on_button

    global buttonX,buttonY
    buttonX=400
    buttonY=(200,140)
    BG_image = load_image('./texture/Title_background.png')
    grass1 = load_image('./texture/grass.png')
    button_play = (load_image('./texture/Title_button_play_off.png'), load_image('./texture/Title_button_play_on.png'))
    button_how = (load_image('./texture/Title_button_how_off.png'), load_image('./texture/Title_button_how_on.png'))

    pass


def finish():
    pass


def handle_events():

    global cur_mouse_x, cur_mouse_y


    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:  # 마우스 움직임 감지
            cur_mouse_x, cur_mouse_y = event.x, get_canvas_height() - 1 - event.y  # y 좌표 뒤집음

    pass


def update():
    if
    pass


def draw():
    clear_canvas()
    BG_image.draw(400, 300)
    grass1.draw(400, 300)
    if cur_mouse_x<buttonX+130 and cur_mouse_x>buttonX-130 and cur_mouse_y<buttonY[0]+37and cur_mouse_y > buttonY[0]-37:
        button_play[0].draw(buttonX,buttonY)
    else:
        button_play[1].draw(buttonX,buttonY)

    update_canvas()
    pass


def pause(): pass


def resume(): pass
