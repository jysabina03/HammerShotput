from pico2d import *

import game_framework
import game_world
import title_mode
from Ball import Ball
from Distance_sign import Distance_sign
from Player import Player
from grass import Grass, Grass_simple
from result_machine import Result_machine, Final_result
from sky import Sky, Sky_simple

import server

# Game object class here


def handle_events():
    global running
    global sound_button

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.key == SDLK_r and server.result_machine.state_machine.cur_state == Final_result:
            sound_button.play()
            game_framework.change_mode(title_mode)

        else:
            server.result_machine.handle_event(event)

def init():

    global sound_button

    server.result_machine = Result_machine()
    game_world.add_object(server.result_machine, 2)

    server.grass = Grass_simple()
    game_world.add_object(server.grass, 1)

    server.sky = Sky_simple()
    game_world.add_object(server.sky, 0)

    # 리스타트 사운드
    sound_button = load_wav('./sound/title_button.wav')
    sound_button.set_volume(60)


def finish():
    game_world.clear()
    server.score['p1'],server.score['p2']=[],[]
    server.turn=0
    pass

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
