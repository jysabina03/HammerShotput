from pico2d import load_image, get_time, get_events, load_font, load_wav, load_music
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE, SDLK_DOWN, SDLK_UP, SDL_Event
import game_framework
import math

import server

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_FAST = 12
FRAMES_PER_ACTION_SLOW = 0.75

# 공으로 전진하는 스피드
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10  # Km / Hour      #아주 조금 전진(공이 가까움...)
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

font_move = 26

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
            result_machine.text_x += 1.2 * RUN_SPEED_PPS * game_framework.frame_time

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

        result_machine.sound_play = True
    @staticmethod
    def exit(result_machine, e):
        result_machine.total_p1 = round(result_machine.total_p1 + server.score['p1'][0], 1)
        result_machine.total_p2 = round(result_machine.total_p2 + server.score['p2'][0], 1)

        print('result Score1 Exit')

    @staticmethod
    def do(result_machine):

        if int(result_machine.dee_x)==80 and result_machine.sound_play:
            result_machine.sound_play=False
            result_machine.sound_result_dis.play()
        if result_machine.dee_x < 200:
            result_machine.dee_x += 3 * RUN_SPEED_PPS * game_framework.frame_time
        else:
            result_machine.state_machine.handle_event(('TIME_OUT', 0))

        result_machine.frame = (
                                       result_machine.frame + FRAMES_PER_ACTION_SLOW * 2 * ACTION_PER_TIME * game_framework.frame_time) % 4

        pass

    @staticmethod
    def draw(result_machine):

        # 결과발표
        result_machine.result_text.draw(400, result_machine.text_y)

        # 캐릭터들
        result_machine.image_kirby.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 100,
                                                       95, 100 * 2, 100 * 2)
        result_machine.image_DDD.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 680,
                                                     95 + 45, 100 * 2, 100 * 2)

        # 라운드별 점수들
        # 커비 1라운드
        result_machine.image_score_dee.clip_composite_draw(0, 4 * 70, 70, 70, 0, 'h', result_machine.dee_x, 350, 70 * 2,
                                                           70 * 2)
        result_machine.font_s.draw(result_machine.dee_x - font_move, 370, f'{server.score["p1"][0]}m', (14, 14, 14))

        # 디디디 1라운드
        result_machine.image_score_dee.clip_composite_draw(70, 4 * 70, 70, 70, 0, '', 800 - result_machine.dee_x, 350,
                                                           70 * 2,
                                                           70 * 2)
        result_machine.font_s.draw(800 - result_machine.dee_x - font_move, 370, f'{server.score["p2"][0]}m', (14, 14, 14))

        # 전체합산점수들

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
        print('result Score1 Enter')

        result_machine.dee_x = -20

        result_machine.sound_play = True

    @staticmethod
    def exit(result_machine, e):

        result_machine.total_p1 = round(result_machine.total_p1 + server.score['p1'][1], 1)
        result_machine.total_p2 = round(result_machine.total_p2 + server.score['p2'][1], 1)

        print('result Score1 Exit')

    @staticmethod
    def do(result_machine):

        if int(result_machine.dee_x)==40 and result_machine.sound_play:
            result_machine.sound_play=False
            result_machine.sound_result_dis.play()
        if result_machine.dee_x < 120:
            result_machine.dee_x += 2 * RUN_SPEED_PPS * game_framework.frame_time
        else:
            result_machine.state_machine.handle_event(('TIME_OUT', 0))

        result_machine.frame = (
                                       result_machine.frame + FRAMES_PER_ACTION_SLOW * 2 * ACTION_PER_TIME * game_framework.frame_time) % 4

        pass

    @staticmethod
    def draw(result_machine):

        # 결과발표
        result_machine.result_text.draw(400, result_machine.text_y)

        # 캐릭터들
        result_machine.image_kirby.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 100,
                                                       95, 100 * 2, 100 * 2)
        result_machine.image_DDD.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 680,
                                                     95 + 45, 100 * 2, 100 * 2)

        # 라운드별 점수들
        # 커비 1라운드
        result_machine.image_score_dee.clip_composite_draw(0, 4 * 70, 70, 70, 0, 'h', 200, 350, 70 * 2,
                                                           70 * 2)
        result_machine.font_s.draw(200 - font_move, 370, f'{server.score["p1"][0]}m', (14, 14, 14))

        # 디디디 1라운드
        result_machine.image_score_dee.clip_composite_draw(70, 4 * 70, 70, 70, 0, '', 600, 350, 70 * 2,
                                                           70 * 2)
        result_machine.font_s.draw(600 - font_move, 370, f'{server.score["p2"][0]}m', (14, 14, 14))

        # 커비 2라운드
        result_machine.image_score_dee.clip_composite_draw(0, 4 * 70, 70, 70, 0, 'h', result_machine.dee_x, 350, 70 * 2,
                                                           70 * 2)
        result_machine.font_s.draw(result_machine.dee_x - font_move, 370, f'{server.score["p1"][1]}m', (14, 14, 14))

        # 디디디 2라운드
        result_machine.image_score_dee.clip_composite_draw(70, 4 * 70, 70, 70, 0, '', 800 - result_machine.dee_x, 350,
                                                           70 * 2,70 * 2)
        result_machine.font_s.draw(800 - result_machine.dee_x - font_move, 370, f'{server.score["p2"][1]}m', (14, 14, 14))

        # 전체합산점수들

        result_machine.dis_kirby.clip_composite_draw(0, 0, 150, 30, 0, '', 50 + result_machine.text_x, 250, 150 * 2,
                                                     30 * 2)
        result_machine.font.draw(-80 + result_machine.text_x, 250, f'{result_machine.total_p1}m', (14, 14, 14))

        result_machine.dis_DDD.clip_composite_draw(0, 0, 150, 30, 0, 'h', 750 - result_machine.text_x, 250, 150 * 2,
                                                   30 * 2)
        result_machine.font.draw(680 - result_machine.text_x, 250, f'{result_machine.total_p2}m', (14, 14, 14))

        pass


class Score3:
    @staticmethod
    def enter(result_machine, e):
        result_machine.next_time = get_time()
        result_machine.frame = 0
        print('result Score1 Enter')

        result_machine.dee_x = -20

        result_machine.sound_play = True
    @staticmethod
    def exit(result_machine, e):

        result_machine.total_p1 = round(result_machine.total_p1 + server.score['p1'][2], 1)
        result_machine.total_p2 = round(result_machine.total_p2 + server.score['p2'][2], 1)

        print('result Score1 Exit')

    @staticmethod
    def do(result_machine):
        if int(result_machine.dee_x)==8 and result_machine.sound_play:
            result_machine.sound_play=False
            result_machine.sound_result_dis.play()
        if result_machine.dee_x < 40:
            result_machine.dee_x += RUN_SPEED_PPS * game_framework.frame_time
        else:
            result_machine.state_machine.handle_event(('TIME_OUT', 0))

        result_machine.frame = (
                                       result_machine.frame + FRAMES_PER_ACTION_SLOW * 2 * ACTION_PER_TIME * game_framework.frame_time) % 4

        pass

    @staticmethod
    def draw(result_machine):

        # 결과발표
        result_machine.result_text.draw(400, result_machine.text_y)

        # 캐릭터들
        result_machine.image_kirby.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 100,
                                                       95, 100 * 2, 100 * 2)
        result_machine.image_DDD.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '', 680,
                                                     95 + 45, 100 * 2, 100 * 2)

        # 라운드별 점수들
        for _ in range(2):
            result_machine.image_score_dee.clip_composite_draw(0, 4 * 70, 70, 70, 0, 'h', 200 - (_ * 80), 350, 70 * 2,
                                                               70 * 2)
            result_machine.font_s.draw(200 - (_ * 80) - font_move, 370, f'{server.score["p1"][_]}m', (14, 14, 14))

        for _ in range(2):
            result_machine.image_score_dee.clip_composite_draw(70, 4 * 70, 70, 70, 0, '', 600 + (_ * 80), 350, 70 * 2,
                                                               70 * 2)
            result_machine.font_s.draw(600 + (_ * 80) - font_move, 370, f'{server.score["p2"][_]}m', (14, 14, 14))

        # 커비 3라운드
        result_machine.image_score_dee.clip_composite_draw(0, 4 * 70, 70, 70, 0, 'h', result_machine.dee_x, 350, 70 * 2,
                                                           70 * 2)
        result_machine.font_s.draw(result_machine.dee_x - font_move, 370, f'{server.score["p1"][2]}m', (14, 14, 14))

        # 디디디 3라운드
        result_machine.image_score_dee.clip_composite_draw(70, 4 * 70, 70, 70, 0, '', 800 - result_machine.dee_x, 350,
                                                           70 * 2,70 * 2)
        result_machine.font_s.draw(800 - result_machine.dee_x - font_move, 370, f'{server.score["p2"][2]}m', (14, 14, 14))

        # 전체합산점수들

        result_machine.dis_kirby.clip_composite_draw(0, 0, 150, 30, 0, '', 50 + result_machine.text_x, 250, 150 * 2,
                                                     30 * 2)
        result_machine.font.draw(-80 + result_machine.text_x, 250, f'{result_machine.total_p1}m', (14, 14, 14))

        result_machine.dis_DDD.clip_composite_draw(0, 0, 150, 30, 0, 'h', 750 - result_machine.text_x, 250, 150 * 2,
                                                   30 * 2)
        result_machine.font.draw(680 - result_machine.text_x, 250, f'{result_machine.total_p2}m', (14, 14, 14))

        pass


class Final_result:
    @staticmethod
    def enter(result_machine, e):
        result_machine.next_time = get_time()
        result_machine.frame = 0
        print('result Score1 Enter')

        result_machine.text_y2 = 620

        if result_machine.total_p1 > result_machine.total_p2:
            result_machine.result_final = 1
        elif result_machine.total_p1 < result_machine.total_p2:
            result_machine.result_final = 2
        else:
            result_machine.result_final = 0

        result_machine.kirby_lose_trigger = True

        result_machine.sound_result.play()
    @staticmethod
    def exit(result_machine, e):
        print('result Score1 Exit')

    @staticmethod
    def do(result_machine):

        if result_machine.text_y2 > 450:
            result_machine.text_y2 -= RUN_SPEED_PPS * game_framework.frame_time

        result_machine.frame = (
                                       result_machine.frame + FRAMES_PER_ACTION_SLOW * 2 * ACTION_PER_TIME * game_framework.frame_time) % 4
        if int(result_machine.frame) == 3:
            result_machine.kirby_lose_trigger = False

        pass

    @staticmethod
    def draw(result_machine):

        # 결과발표
        result_machine.result_text.draw(400, result_machine.text_y)

        # 캐릭터들

        if result_machine.result_final == 0:

            result_machine.image_kirby.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '',
                                                           100, 95, 100 * 2, 100 * 2)
            result_machine.image_DDD.clip_composite_draw(int(result_machine.frame) * 100, (1) * 100, 100, 100, 0, '',
                                                         680, 95 + 45, 100 * 2, 100 * 2)
        elif result_machine.result_final == 1:

            result_machine.image_kirby.clip_composite_draw(int(result_machine.frame) * 100, 0 * 100, 100, 100, 0, '',
                                                           100, 95, 100 * 2, 100 * 2)
            result_machine.image_DDD.clip_composite_draw(int(result_machine.frame + 4) * 100, 0 * 100, 100, 100, 0, '',
                                                         680, 95 + 45, 100 * 2, 100 * 2)
        else:
            if result_machine.kirby_lose_trigger:
                result_machine.image_kirby.clip_composite_draw(int(result_machine.frame + 4) * 100, 0 * 100, 100, 100,
                                                               0, '',100, 95, 100 * 2, 100 * 2)
            else:
                result_machine.image_kirby.clip_composite_draw(int(3 + 4) * 100, 0 * 100, 100, 100,
                                                               0, '',100, 95, 100 * 2, 100 * 2)

            result_machine.image_DDD.clip_composite_draw(int(result_machine.frame) * 100, 0 * 100, 100, 100, 0, '',
                                                         680, 95 + 45, 100 * 2, 100 * 2)


        for _ in range(3):
            result_machine.image_score_dee.clip_composite_draw(0, 4 * 70, 70, 70, 0, 'h', 200 - (_ * 80), 350, 70 * 2,
                                                               70 * 2)
            result_machine.font_s.draw(200 - (_ * 80) - font_move, 370, f'{server.score["p1"][_]}m', (14, 14, 14))

        for _ in range(3):
            result_machine.image_score_dee.clip_composite_draw(70, 4 * 70, 70, 70, 0, '', 600 + (_ * 80), 350, 70 * 2,
                                                               70 * 2)
            result_machine.font_s.draw(600 + (_ * 80) - font_move, 370, f'{server.score["p2"][_]}m', (14, 14, 14))

        # 전체합산점수들

        result_machine.dis_kirby.clip_composite_draw(0, 0, 150, 30, 0, '', 50 + result_machine.text_x, 250, 150 * 2,
                                                     30 * 2)
        result_machine.font.draw(-80 + result_machine.text_x, 250, f'{round(result_machine.total_p1, 1)}m', (14, 14, 14))

        result_machine.dis_DDD.clip_composite_draw(0, 0, 150, 30, 0, 'h', 750 - result_machine.text_x, 250, 150 * 2,
                                                   30 * 2)
        result_machine.font.draw(680 - result_machine.text_x, 250, f'{round(result_machine.total_p2, 1)}m', (14, 14, 14)) \

        if result_machine.result_final == 0:
            result_machine.result_draw.draw(120, result_machine.text_y2)
            result_machine.result_draw.draw(680, result_machine.text_y2)
        elif result_machine.result_final == 1:
            result_machine.result_win.draw(120, result_machine.text_y2)
            result_machine.result_lose.draw(680, result_machine.text_y2)
        else:
            result_machine.result_lose.draw(120, result_machine.text_y2)
            result_machine.result_win.draw(680, result_machine.text_y2)

        result_machine.font_s.draw(335,530-result_machine.text_y2,'restart? >>> R', (14, 14, 14))

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
        self.result_draw = load_image('./texture/result_draw.png')

        self.dis_kirby = load_image('./texture/Distance_UI_kirby.png')
        self.dis_DDD = load_image('./texture/Distance_UI_DDD.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start()

        self.total_p1 = 0
        self.total_p2 = 0

        self.font = load_font('ENCR10B.TTF', 22)
        self.font_s = load_font('ENCR10B.TTF', 16)



        #결과 발표 배경음악
        self.bgm = load_music('./sound/bgm.mp3')
        self.bgm.set_volume(40)
        self.bgm.repeat_play()

        #결과 발표 사운드
        self.sound_result = load_wav('./sound/result.wav')
        self.sound_result.set_volume(50)

        # 결과 합산 사운드
        self.sound_result_dis = load_wav('./sound/result_dis.wav')
        self.sound_result_dis.set_volume(30)


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
