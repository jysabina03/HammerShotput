from pico2d import *

import game_framework
import game_world
from Ball import Ball
from Distance_sign import Distance_sign
from Player import Player
from grass import Grass
from sky import Sky

import server

# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
            #running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
            #running = False
        else:
            server.player_Kirby.handle_event(event)

def init():
    global running
    global grass
    global team
    global grass_reset_y
    global sky
    global player_Kirby, player_DDD
    global wadlle_ball
    running = True

    server.grass = Grass(30)
    game_world.add_object(server.grass, 1)

    server.sky = Sky()
    game_world.add_object(server.sky, 0)

    server.wadlle_ball = Ball()
    game_world.add_object(server.wadlle_ball, 3)

    server.player_Kirby = Player('DDD',server.wadlle_ball)
    game_world.add_object(server.player_Kirby, 2)

    server.distance_sign = Distance_sign()
    game_world.add_object(server.distance_sign, 2)

def finish():
    pass

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
