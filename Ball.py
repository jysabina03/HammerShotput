import math

from pico2d import load_image, get_time, clamp, load_wav
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE

import game_framework
import game_world
import server
from Score_dee import Score_dee

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
        ball.y = 0
        ball.action = 0
        ball.frame = 0

        print('ball - Idle Enter')

    @staticmethod
    def exit(ball, e):

        if server.turn % 2 == 0:
            server.player_DDD.state_machine.handle_event(('START_TURN', 0))
        else:
            server.player_Kirby.state_machine.handle_event(('START_TURN', 0))

        ball.x = 0
        server.turn += 1
        print('ball - Idle Exit')

    @staticmethod
    def do(ball):
        if server.turn == 5:
            ball.state_machine.handle_event(('START_TURN', 0))

        ball.frame = (ball.frame + FRAMES_PER_ACTION_SLOW * ACTION_PER_TIME * game_framework.frame_time) % 2
        if ball.x > 0:
            ball.x -= ball.x / 10 * FRAMES_PER_ACTION_FAST * game_framework.frame_time + 0.5;

        else:
            ball.state_machine.handle_event(('START_TURN', 0))
        pass

    @staticmethod
    def draw(ball):
        ball.image.clip_composite_draw(int(ball.frame) * 26, (2 - ball.action) * 26, 26, 26, 0, '',
                                       ball.normal_x - ball.x, ball.normal_y, 26 * 2, 26 * 2)
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
        print(f'ball - fly_away Exit ㅡ 착지 위치: {ball.x} / 미터 환산: {ball.x / 25}')

        ball.sound_boing.set_volume(50)
        ball.sound_boing.play()
        score_dee = Score_dee(server.turn, ball.x, ball.dx)
        game_world.add_object(score_dee, 2)

    @staticmethod
    def do(ball):
        # 프레임타임으로 시간 단위, x, y 포물선 좌표 계산

        if int(ball.frame) ==0:
            ball.sound_fly.play()

        ball.x += ball.xspeed * FRAMES_PER_ACTION_FAST * game_framework.frame_time
        ball.yspeed += ball.gravity * FRAMES_PER_ACTION_FAST * game_framework.frame_time
        ball.y += ball.yspeed * FRAMES_PER_ACTION_FAST * game_framework.frame_time

        ball.sound_fly.set_volume(10 + abs(int(ball.yspeed)))

        if ball.y <= 0:
            ball.state_machine.handle_event(('TOUCH_THE_FLOOR', 0))

        ball.frame = (ball.frame + FRAMES_PER_ACTION_FAST * ACTION_PER_TIME * game_framework.frame_time) % 8


        pass

    @staticmethod
    def draw(ball):

        ball.image.clip_composite_draw(int(ball.frame) * 26, (2 - ball.action) * 26, 26, 26, 0, '',
                                       ball.dx, ball.dy, 26 * 2, 26 * 2)
        pass


class landing:  # 2. 착지
    @staticmethod
    def enter(ball, e):
        ball.action = 2
        ball.frame = 0
        ball.slide = 2
        ball.land_x = 0
        ball.land_y = 0
        ball.xspeed = clamp(0, ball.xspeed, 25)


        ball.landing_time = get_time()
        print('ball - landing Enter')

    @staticmethod
    def exit(ball, e):
        print('ball - landing Exit')

    @staticmethod
    def do(ball):

        if get_time() - ball.landing_time > 5:  # 시간
            ball.state_machine.handle_event(('END_TURN', 0))
            if server.turn % 2 == 0:
                server.player_Kirby.state_machine.handle_event(('END_TURN', 0))
            else:
                server.player_DDD.state_machine.handle_event(('END_TURN', 0))

        if ball.frame < 4:
            ball.land_x += ball.xspeed / 1.5 * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
        elif ball.frame < 10:
            ball.land_x += ball.xspeed / 1.5 * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
            ball.land_y -= (ball.frame - 7) * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
        elif ball.frame < 16:
            ball.land_x += ball.xspeed / 2 * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
        elif ball.slide < 7:
            ball.land_x += ball.xspeed / ball.slide * FRAMES_PER_ACTION_FAST * game_framework.frame_time;
            ball.slide += 1

        if ball.frame < 16:
            ball.frame = (
                    ball.frame + FRAMES_PER_ACTION_FAST * FRAMES_PER_ACTION_SLOW * ACTION_PER_TIME * game_framework.frame_time)

    @staticmethod
    def draw(ball):
        # ball.image.clip_draw(int(ball.frame)*40,0,40,24,200,90)
        ball.image.clip_composite_draw(int(ball.frame) * 40, 0, 40, 24, 0, '', ball.dx + ball.land_x,
                                       ball.dy + ball.land_y, 40 * 2, 24 * 2)

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

        self.image = load_image('./texture/st_wadlle.png')

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

        self.sound_fly = load_wav('./sound/fly.wav')
        self.sound_boing = load_wav('./sound/boing.wav')
        self.sound_boing.set_volume(50)

    def receive_speed(self, hammer_xspeed, hammer_yspeed, hammer_angle):
        print(f"스피드 수신 - x: {hammer_xspeed}, y: {hammer_yspeed}, angle: {hammer_angle}")
        self.xspeed = hammer_xspeed
        self.yspeed = hammer_yspeed
        self.angle = hammer_angle
        self.state_machine.handle_event(('SHOOT', 0))

    def update(self):
        self.state_machine.update()
        self.dx = clamp(0, self.x, 200) + 280
        self.dy = clamp(0, self.y, 400) + 75

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
