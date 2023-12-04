from pico2d import load_image, get_time, get_events, load_font
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE, SDLK_DOWN, SDLK_UP, SDL_Event
import game_framework
import math

import server

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_FAST = 12
FRAMES_PER_ACTION_SLOW = 0.5

# 공으로 전진하는 스피드
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10  # Km / Hour      #아주 조금 전진(공이 가까움...)
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:
    # 화면에 나오지 않는 상태
    @staticmethod
    def enter(result_machine, e):
        result_machine.next_time = get_time()
        result_machine.frame = 0
        print('result Idle Enter')
        result_machine.text_y = 620
        result_machine.text_x = -50

    @staticmethod
    def exit(result_machine, e):
        print('result Idle Exit')

    @staticmethod
    def do(result_machine):
        if result_machine.text_y > 500:
            result_machine.text_y -= RUN_SPEED_PPS * game_framework.frame_time
        if result_machine.text_x < 100:
            result_machine.text_x += 1.2* RUN_SPEED_PPS * game_framework.frame_time

        result_machine.frame = (
                                       result_machine.frame + FRAMES_PER_ACTION_SLOW * 2 * ACTION_PER_TIME * game_framework.frame_time) % 4

        if get_time() - result_machine.next_time > 2:  # 시간
            result_machine.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(result_machine):
        result_machine.image_kirby.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 100,
                                                       95, 100 * 2, 100 * 2)
        result_machine.image_DDD.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 680,
                                                     95 + 45, 100 * 2, 100 * 2)

        result_machine.result_text.draw(400, result_machine.text_y)

        result_machine.dis_kirby.clip_composite_draw(0, 0, 150, 30, 0, '', 50 + result_machine.text_x, 250, 150 * 2,
                                                     30 * 2)
        result_machine.font.draw(-80 + result_machine.text_x, 250, f'{result_machine.total_p1}m', (14, 14, 14))

        result_machine.dis_DDD.clip_composite_draw(0, 0, 150, 30, 0, 'h', 750 - result_machine.text_x, 250, 150 * 2,
                                                   30 * 2)
        result_machine.font.draw(680 - result_machine.text_x, 250, f'{result_machine.total_p2}m', (14, 14, 14))

        pass


class Score1:
    @staticmethod
    def enter(result_machine, e):
        result_machine.next_time = get_time()
        result_machine.frame = 0
        print('result Score1 Enter')

        result_machine.dee_x = -20

    @staticmethod
    def exit(result_machine, e):
        print('result Score1 Exit')

    @staticmethod
    def do(result_machine):


        if result_machine.dee_x < 200:
            result_machine.dee_x += 3*RUN_SPEED_PPS * game_framework.frame_time
            #첫 번째 점수 합산
    
            result_machine.total_p1 += server.score['p1'][0]
            result_machine.total_p2 += server.score['p2'][0]

        result_machine.frame = (
                                       result_machine.frame + FRAMES_PER_ACTION_SLOW * 2 * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - result_machine.next_time > 5:  # 시간
            result_machine.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(result_machine):

        #결과발표
        result_machine.result_text.draw(400, result_machine.text_y)

        #캐릭터들
        result_machine.image_kirby.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 100,
                                                       95, 100 * 2, 100 * 2)
        result_machine.image_DDD.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 680,
                                                     95 + 45, 100 * 2, 100 * 2)

        #라운드별 점수들
        #커비 1라운드
        result_machine.image_score_dee.clip_composite_draw(0, 4 * 70, 70, 70, 0, '', result_machine.dee_x, 350, 70*2,
                                           70*2)
        result_machine.font_s.draw(result_machine.dee_x-19, 370, f'{server.score["p1"][0]}m', (14, 14, 14))

        #커비 2라운드
        result_machine.image_score_dee.clip_composite_draw(70, 4 * 70, 70, 70, 0, '', 800-result_machine.dee_x, 350, 70*2,
                                           70*2)
        result_machine.font_s.draw(800-result_machine.dee_x-19, 370, f'{server.score["p2"][0]}m', (14, 14, 14))


        #전체합산점수들

        result_machine.dis_kirby.clip_composite_draw(0, 0, 150, 30, 0, '', 50 + result_machine.text_x, 250, 150 * 2,
                                                     30 * 2)
        result_machine.font.draw(-80 + result_machine.text_x, 250, f'{result_machine.total_p1}m', (14, 14, 14))


        result_machine.dis_DDD.clip_composite_draw(0, 0, 150, 30, 0, 'h', 750 - result_machine.text_x, 250, 150 * 2,
                                                   30 * 2)
        result_machine.font.draw(680 - result_machine.text_x, 250, f'{result_machine.total_p2}m', (14, 14, 14))

        pass


class Score2:
    @staticmethod
    def enter(result_machine, e):
        result_machine.next_time = get_time()
        result_machine.frame = 0
        print('result Idle Enter')

    @staticmethod
    def exit(result_machine, e):
        print('result Idle Exit')

    @staticmethod
    def do(result_machine):
        result_machine.frame = (
                                       result_machine.frame + FRAMES_PER_ACTION_SLOW * 2 * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - result_machine.next_time > 5:  # 시간
            result_machine.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(result_machine):
        result_machine.image_kirby.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 100,
                                                       95, 100 * 2, 100 * 2)
        result_machine.image_DDD.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 680,
                                                     95 + 45, 100 * 2, 100 * 2)
        pass


class Score3:
    @staticmethod
    def enter(result_machine, e):
        result_machine.next_time = get_time()
        result_machine.frame = 0
        print('result Idle Enter')

    @staticmethod
    def exit(result_machine, e):
        print('result Idle Exit')

    @staticmethod
    def do(result_machine):
        result_machine.frame = (
                                       result_machine.frame + FRAMES_PER_ACTION_SLOW * 2 * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - result_machine.next_time > 5:  # 시간
            result_machine.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(result_machine):
        result_machine.image_kirby.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 100,
                                                       95, 100 * 2, 100 * 2)
        result_machine.image_DDD.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 680,
                                                     95 + 45, 100 * 2, 100 * 2)
        pass


class Final_result:
    @staticmethod
    def enter(result_machine, e):
        result_machine.next_time = get_time()
        result_machine.frame = 0
        print('result Idle Enter')

    @staticmethod
    def exit(result_machine, e):
        print('result Idle Exit')

    @staticmethod
    def do(result_machine):
        result_machine.frame = (
                                       result_machine.frame + FRAMES_PER_ACTION_SLOW * 2 * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - result_machine.next_time > 5:  # 시간
            result_machine.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(result_machine):
        result_machine.image_kirby.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 100,
                                                       95, 100 * 2, 100 * 2)
        result_machine.image_DDD.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 680,
                                                     95 + 45, 100 * 2, 100 * 2)
        pass


class StateMachine:
    def __init__(self, result):
        self.player = result
        self.cur_state = Idle  # 초기 상태
        self.transitions = {
            Idle: {time_out: Score1},
            Score1: {time_out: Score2},
            Score2: {time_out: Score3},
            Score3: {time_out: Final_result},
            Final_result: {}
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

        self.result_text = load_image('./texture/result_text.png')
        self.result_win = load_image('./texture/result_win.png')
        self.result_lose = load_image('./texture/result_lose.png')

        self.dis_kirby = load_image('./texture/Distance_UI_kirby.png')
        self.dis_DDD = load_image('./texture/Distance_UI_DDD.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start()

        self.total_p1 = 0
        self.total_p2 = 0

        self.font = load_font('ENCR10B.TTF', 24)
        self.font_s = load_font('ENCR10B.TTF', 18)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
