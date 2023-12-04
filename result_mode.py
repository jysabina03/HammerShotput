from pico2d import *

import game_framework
import game_world
from Ball import Ball
from Distance_sign import Distance_sign
from Player import Player
from grass import Grass
from result_machine import Result_machine
from sky import Sky

import server

# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.result_machine.handle_event(event)

def init():

    running = True

    server.result_machine = Result_machine()
    game_world.add_object(server.result_machine, 2)

    server.grass = Grass(30)
    game_world.add_object(server.grass, 1)

    server.sky = Sky()
    game_world.add_object(server.sky, 0)


def finish():
    pass

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
