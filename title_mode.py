from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, get_canvas_height
from sdl2 import SDLK_ESCAPE, SDL_KEYDOWN, SDL_QUIT, SDLK_SPACE, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN

import game_framework
import play_mode

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_FAST = 12
FRAMES_PER_ACTION_SLOW = 0.5


def init():
    global BG_image, grass1, button_play, button_how, image_kirby, image_DDD
    global button_onoff

    global buttonX, buttonY
    global cur_mouse_x, cur_mouse_y, frame

    frame = 0

    image_kirby = load_image('./texture/sp_kirby.png')
    image_DDD = load_image('./texture/sp_dedede.png')

    buttonX = 400
    buttonY = (240, 140)
    cur_mouse_x, cur_mouse_y = 0, 0

    BG_image = load_image('./texture/Title_background.png')
    grass1 = load_image('./texture/grass.png')
    button_play = (load_image('./texture/Title_button_play_on.png'), load_image('./texture/Title_button_play_off.png'))
    button_how = (load_image('./texture/Title_button_how_on.png'), load_image('./texture/Title_button_how_off.png'))

    button_onoff = {'play': False, 'how': False}
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
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if button_onoff['play']:
                game_framework.change_mode(play_mode)
            elif button_onoff['how']:
                pass

    pass


def update():
    if buttonX + 130 > cur_mouse_x > buttonX - 130 and cur_mouse_y < buttonY[0] + 37 and cur_mouse_y > \
            buttonY[0] - 37:
        button_onoff['play'] = True
    else:
        button_onoff['play'] = False

    if buttonX + 130 > cur_mouse_x > buttonX - 130 and cur_mouse_y < buttonY[1] + 37 and cur_mouse_y > \
            buttonY[1] - 37:
        button_onoff['how'] = True
    else:
        button_onoff['how'] = False

    pass


def draw():
    global frame
    clear_canvas()
    BG_image.draw(400, 300)
    grass1.draw(400, 30)

    frame = (frame + FRAMES_PER_ACTION_SLOW * ACTION_PER_TIME * game_framework.frame_time) % 2

    if button_onoff['play']:
        button_play[0].draw(buttonX, buttonY[0])
    else:
        button_play[1].draw(buttonX, buttonY[0])

    if button_onoff['how']:
        button_how[0].draw(buttonX, buttonY[1])
    else:
        button_how[1].draw(buttonX, buttonY[1])

    image_kirby.clip_composite_draw(int(frame) * 100, 5 * 100, 100, 100, 0, '', 100,
                                    95,
                                    100 * 2, 100 * 2)
    image_DDD.clip_composite_draw(int(frame) * 100, 5 * 100, 100, 100, 0, 'h', 680,
                                  95 + 45,
                                  100 * 2, 100 * 2)

    update_canvas()
    pass


def pause(): pass


def resume(): pass
