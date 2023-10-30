from pico2d import *

import game_world
from grass import Grass
from sky import Sky


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        #else:
            #boy.handle_event(event)


def reset_world():
    global running
    global grass
    global team
    global grass_reset_y
    global sky
    running = True

    grass = Grass(30)
    game_world.add_object(grass, 3)

    sky = Sky(0)
    game_world.add_object(sky, 0)





def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas()
reset_world()

# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
