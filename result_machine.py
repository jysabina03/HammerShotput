from pico2d import load_image, get_time, get_events
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE, SDLK_DOWN, SDLK_UP, SDL_Event
import game_framework
import math

import server

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_FAST = 12
FRAMES_PER_ACTION_SLOW = 0.5

def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:
    # 화면에 나오지 않는 상태
    @staticmethod
    def enter(player, e):

        print('result Idle Enter')

    @staticmethod
    def exit(player, e):
        print('result Idle Exit')

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass

class Score1:
    # 화면에 나오지 않는 상태
    @staticmethod
    def enter(player, e):

        print('result Idle Enter')

    @staticmethod
    def exit(player, e):
        print('result Idle Exit')

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass
class Score2:
    # 화면에 나오지 않는 상태
    @staticmethod
    def enter(player, e):

        print('result Idle Enter')

    @staticmethod
    def exit(player, e):
        print('result Idle Exit')

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass

class Score3:
    # 화면에 나오지 않는 상태
    @staticmethod
    def enter(player, e):

        print('result Idle Enter')

    @staticmethod
    def exit(player, e):
        print('result Idle Exit')

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass

class StateMachine:
    def __init__(self, result):
        self.player = result
        self.cur_state = Idle  # 초기 상태
        self.transitions = {
            Idle: {time_out: Score1},
            Score1: {time_out: Score2},
            Score2: {time_out: Score3},
            Score3: {},
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)

class Result_machine:
    def __init__(self, ):
        self.image_kirby = load_image('./texture/sp_kirby.png')
        self.image_DDD = load_image('./texture/sp_dedede.png')
        self.image_score_dee = load_image('./texture/score_dee.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
