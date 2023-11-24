from pico2d import *

import game_framework
import game_world
from Ball import Ball
from Player import Player
from grass import Grass
from sky import Sky

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
            player_Kirby.handle_event(event)

def init():
    global running
    global grass
    global team
    global grass_reset_y
    global sky
    global player_Kirby, player_DDD
    global wadlle_ball
    running = True

    grass = Grass(30)
    game_world.add_object(grass, 1)

    sky = Sky(0)
    game_world.add_object(sky, 0)

    sky = Sky(0)
    game_world.add_object(sky, 0)


    wadlle_ball = Ball()
    game_world.add_object(wadlle_ball, 3)

    player_Kirby = Player('DDD',wadlle_ball)
    game_world.add_object(player_Kirby, 2)

def finish():
    pass

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
