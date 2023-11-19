import math

from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE

import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_FAST = 12
FRAMES_PER_ACTION_SLOW = 0.5


def start_turn(e):
    return e[0] == 'START_TURN'


def touch_the_floor(e):
    return e[0] == 'TOUCH_THE_FLOOR'


def shoot(e):
    return e[0] == 'SHOOT'


def end_turn(e):
    return e[0] == 'END_TURN'


class Idle:
    # 화면에 나오지 않는 상태
    @staticmethod
    def enter(ball, e):
        ball.xspeed = 0
        ball.yspeed = 0

        print('ball - Idle Enter')

    @staticmethod
    def exit(ball, e):
        print('ball - Idle Exit')

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass


class Stand_by_Shoot:  # 0. 앉아서 슛 대기
    @staticmethod
    def enter(ball, e):
        ball.action = 0
        ball.frame = 0
        print('ball - Stand_by_Shoot Enter')

    @staticmethod
    def exit(ball, e):
        print('ball - Stand_by_Shoot Exit')

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + FRAMES_PER_ACTION_SLOW * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    @staticmethod
    def draw(ball):
        # ball.image.clip_draw(int(ball.frame)*26,(2-ball.action)*26,26,26,200,90)

        ball.image.clip_composite_draw(int(ball.frame) * 26, (2 - ball.action) * 26, 26, 26, 0, '',
                                       ball.x + ball.normal_x, ball.y + ball.normal_y, 26 * 2, 26 * 2)
        pass


class fly_away:  # 1. 날라감

    GRAVITY = 9.8  # 중력 가속도

    @staticmethod
    def enter(ball, e):
        ball.action = 1
        ball.frame = 0
        ball.launch_time = 0
        ball.gravity = -1

        print('ball - fly_away Enter')

    @staticmethod
    def exit(ball, e):
        ball.Landing_position = ball.x
        print(f'ball - fly_away Exit ㅡ 착지 위치: {ball.x}')

    @staticmethod
    def do(ball):
        # 프레임타임으로 시간 단위, x, y 포물선 좌표 계산

        ball.x += ball.xspeed * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
        ball.yspeed += ball.gravity * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
        ball.y += ball.yspeed * FRAMES_PER_ACTION_FAST * game_framework.frame_time;

        if ball.y <=  0:
            ball.state_machine.handle_event(('TOUCH_THE_FLOOR', 0))

        ball.frame = (ball.frame + FRAMES_PER_ACTION_FAST * ACTION_PER_TIME * game_framework.frame_time) % 8
        pass

    @staticmethod
    def draw(ball):
        ball.image.clip_composite_draw(int(ball.frame) * 26, (2 - ball.action) * 26, 26, 26, 0, '',
                                       ball.x + ball.normal_x, ball.y + ball.normal_y, 26 * 2, 26 * 2)
        pass


class landing:  # 2. 착지
    @staticmethod
    def enter(ball, e):
        ball.action = 2
        ball.frame = 0
        ball.slide = 2
        print('ball - landing Enter')

    @staticmethod
    def exit(ball, e):
        print('ball - landing Exit')

    @staticmethod
    def do(ball):

        if ball.frame < 4:
            ball.x += ball.xspeed / 1.5 * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
        elif ball.frame < 10:
            ball.x += ball.xspeed / 1.5 * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
            ball.y -= (ball.frame-7) * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
        elif ball.frame < 16:
            ball.x += ball.xspeed / 2 * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
        elif ball.slide < 7:
            ball.x += ball.xspeed / ball.slide * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
            ball.slide+=1



        if ball.frame < 16:
            ball.frame = (
                        ball.frame + FRAMES_PER_ACTION_FAST * FRAMES_PER_ACTION_SLOW * ACTION_PER_TIME * game_framework.frame_time)

    @staticmethod
    def draw(ball):
        # ball.image.clip_draw(int(ball.frame)*40,0,40,24,200,90)
        ball.image.clip_composite_draw(int(ball.frame) * 40, 0, 40, 24, 0, '', ball.x + ball.normal_x,
                                       ball.y + ball.normal_y, 40 * 2, 24 * 2)

        pass


#   Idle(액션 없음)
#   0. 날라갈 준비   Stand_by_Shoot
#   1. 날라감(공중)  fly_away
#   2. 착지         landing


class StateMachine:
    def __init__(self, ball):
        self.ball = ball
        # self.cur_state = Idle   # 초기 상태
        self.cur_state = Stand_by_Shoot  # 초기 상태 (테스트용)
        self.transitions = {
            Idle: {start_turn: Stand_by_Shoot},
            Stand_by_Shoot: {shoot: fly_away},
            fly_away: {touch_the_floor: landing},
            landing: {end_turn: Idle},
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ball, e)
                self.cur_state = next_state
                self.cur_state.enter(self.ball, e)
                return True

        return False

    def start(self):
        self.cur_state.enter(self.ball, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.ball)

    def draw(self):
        self.cur_state.draw(self.ball)


#   Idle(액션 없음)
#   0. 날라갈 준비
#   1. 날라감(공중)
#   2. 착지

class Ball:
    def __init__(self):
        self.frame = 0
        self.action = 0

        self.image = load_image('st_wadlle.png')

        # X축/Y축 스피드
        self.xspeed = 0
        self.yspeed = 0
        self.angle = 0

        self.normal_x = 280
        self.normal_y = 75
        self.x = 0
        self.y = 0

        self.Landing_position = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()

        self.shoot = False

    def receive_speed(self, hammer_xspeed, hammer_yspeed, hammer_angle):
        print(f"스피드 수신 - x: {hammer_xspeed}, y: {hammer_yspeed}, angle: {hammer_angle}")
        self.xspeed = hammer_xspeed
        self.yspeed = hammer_yspeed
        self.angle = hammer_angle
        self.state_machine.handle_event(('SHOOT', 0))

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
