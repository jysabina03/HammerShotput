import random

from pico2d import load_image, get_time, get_events, load_wav
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE, SDLK_DOWN, SDLK_UP, SDL_Event
import game_framework
import math

import server

# 공으로 전진하는 스피드
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 3  # Km / Hour      #아주 조금 전진(공이 가까움...)
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_FAST = 12
FRAMES_PER_ACTION_SLOW = 0.5


#   Idle(액션 없음)

#   0. Set_angle
#   1. Charging
#   2-1. Timing
#   2-2. Shoot
#   3. Finish_action


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def time_out(e):
    return e[0] == 'TIME_OUT'


def start_turn(e):
    return e[0] == 'START_TURN'


def finish_shoot(e):
    return e[0] == 'FINISH_SHOOT'


def end_turn(e):
    return e[0] == 'END_TURN'


class Idle:
    # 화면에 나오지 않는 상태
    @staticmethod
    def enter(player, e):
        player.hammer_angle = 0
        player.hammer_charge = 0
        player.hammer_accuracy = 0
        player.hammer_xspeed = 0
        player.hammer_yspeed = 0
        player.is_up_key_pressed = False
        player.is_down_key_pressed = False

        print(f'{player.type} - player Idle Enter')

    @staticmethod
    def exit(player, e):
        print(f'{player.type} - Idle Exit')

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass


class Set_angle:  # 0. 각도조절
    @staticmethod
    def enter(player, e):
        if e[0] == 'START_TURN':
            player.action = 0
            player.frame = 0
            player.anglespeed = round(random.uniform(1.5, 3.0), 1)

        print(f'{player.type} - Set_angle Enter')


    @staticmethod
    def exit(player, e):
        if e[1].key == SDLK_SPACE:
            player.sound_angle.play()

            print(f'Set_angle Exit ㅡ 각도: {player.hammer_angle}')
        elif e[1].type == SDL_KEYDOWN:
            player.anglespeed = round(random.uniform(2.0, 4.0), 1)
            if e[1].key == SDLK_DOWN:
                player.is_down_key_pressed = True
                player.is_up_key_pressed = False
                print('Down 키 눌림')
            elif e[1].key == SDLK_UP:
                player.is_up_key_pressed = True
                player.is_down_key_pressed = False
                print('Up 키 눌림')

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION_SLOW * ACTION_PER_TIME * game_framework.frame_time) % 2

        if player.is_up_key_pressed:
            if player.hammer_angle < 90:
                player.hammer_angle = (
                        player.hammer_angle + player.anglespeed * FRAMES_PER_ACTION_FAST * ACTION_PER_TIME * game_framework.frame_time)
                if player.hammer_angle > 90:
                    player.hammer_angle = 90

        if player.is_down_key_pressed:
            if player.hammer_angle > 0:
                player.hammer_angle = (
                        player.hammer_angle + player.anglespeed * FRAMES_PER_ACTION_FAST * -1 * ACTION_PER_TIME * game_framework.frame_time)
                if player.hammer_angle < 0:
                    player.hammer_angle = 0

    def handle_event(player, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_UP:
                player.is_up_key_pressed = True
                player.is_down_key_pressed = False
                print('Up 키 눌림')
            elif event.key == SDLK_DOWN:
                player.is_down_key_pressed = True
                player.is_up_key_pressed = False
                print('Down 키 눌림')
        return

    @staticmethod
    def draw(player):
        # player.image.clip_draw(int(player.frame)*100,(5-player.action)*100,100,100,50,70)
        player.image.clip_composite_draw(int(player.frame) * 100, (5 - player.action) * 100, 100, 100, 0, '', 50,
                                         95 + (45 * player.type),
                                         100 * 2, 100 * 2)
        player.arrow_image.clip_composite_draw(0, 0, 100, 100, math.radians(player.hammer_angle), '',
                                               95 + (30 * player.type), 100 + (30 * player.type), 100 * 2,
                                               100 * 2)


class Charging:  # 1. 좌우연타차징
    @staticmethod
    def enter(player, e):
        if e[1].key == SDLK_SPACE:
            player.action = 1
            player.frame = 0
            player.forward = 0
            player.charge_time = get_time()
            print('Charging Enter')
            player.key_R = False
            player.key_L = False

    @staticmethod
    def exit(player, e):

        if e[0] == 'TIME_OUT':
            print(f'Charging Exit - 차지:{player.hammer_charge}')
        elif e[1].type == SDL_KEYDOWN:
            player.sound_charge2.play()

            player.sound_charge1.set_volume(player.sound_charge1.get_volume()+2)
            if e[1].key == SDLK_RIGHT:
                if player.key_R is False:
                    player.key_R = True
                    player.key_L = False
                    player.hammer_charge += 1
                    player.frame += 0.7
                    #player.sound_charge1.play()
                print('오른쪽 키 눌림')
            elif e[1].key == SDLK_LEFT:
                if player.key_L is False:
                    player.key_R = False
                    player.key_L = True
                    player.hammer_charge += 1
                    player.frame += 0.7
                    #player.sound_charge2.play()

    @staticmethod
    def do(player):

        # 앞으로 조금씩 이동
        player.forward += RUN_SPEED_PPS * game_framework.frame_time

        player.frame = (player.frame + FRAMES_PER_ACTION_SLOW * 2 * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - player.charge_time > 5:  # 시간
            player.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(player):
        # player.image.clip_draw(int(player.frame)*120,(5-player.action)*100,100,100,50+player.forward,70)
        player.image.clip_composite_draw(int(player.frame) * 120, (5 - player.action) * 100, 120, 100, 0, '',
                                         50 + player.forward, 95 + (45 * player.type), 120 * 2, 100 * 2)

        if player.key_R is False:
            player.key_on.clip_composite_draw(0, 0, 100, 100, 0, '', 200, 210, 80, 80)
        else:
            player.key_off.clip_composite_draw(0, 0, 100, 100, 0, '', 200, 200, 80, 80)

        if player.key_L is False:
            player.key_on.clip_composite_draw(0, 0, 100, 100, 0, 'h', 100, 210, 80, 80)
        else:
            player.key_off.clip_composite_draw(0, 0, 100, 100, 0, 'h', 100, 200, 80, 80)


class Timing:  # 2-1 타이밍 맞춰서
    @staticmethod
    def enter(player, e):
        player.action = 2
        player.frame = 0
        print('Timing Enter')
        player.acc = 0

    @staticmethod
    def exit(player, e):
        if player.acc > 100:
            player.acc -= (player.acc - 100)
        player.hammer_accuracy = player.acc

        if player.acc > 90:
            player.sound_shot1.play()
        else:
            player.sound_shot2.play()
        print(f'Timing Exit - 정확도: {player.hammer_accuracy}')

    @staticmethod
    def do(player):
        if player.acc >= 125:
            player.acc = 20
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.acc = (player.acc + FRAMES_PER_ACTION_FAST * 1.9 * ACTION_PER_TIME * game_framework.frame_time)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(int(player.frame) * 100, (5 - player.action) * 100, 100, 100, 0, '',
                                         80 + player.forward, 95 + (45 * player.type), 100 * 2, 100 * 2)

        player.timing_hammer.clip_composite_draw(0, 0, 100, 100, 0, 'h', 250, 220, player.acc * 1.5, player.acc * 1.5)
        player.timing_target.clip_composite_draw(0, 0, 100, 100, 0, 'h', 250, 220, 150, 150)
        pass


class Shoot:  # 2-2 날리기
    @staticmethod
    def enter(player, e):
        player.action = 2
        player.frame = 0
        print('Shoot Enter')

        energy = player.hammer_charge * player.hammer_accuracy / 5
        player.hammer_xspeed = energy * (90 - player.hammer_angle) / 1000 + 3
        player.hammer_yspeed = energy * (player.hammer_angle) / 1000 + 3

    @staticmethod
    def exit(player, e):
        print(f'Shoot Exit - X속도: {player.hammer_xspeed} | Y속도: {player.hammer_yspeed}')

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION_FAST * ACTION_PER_TIME * game_framework.frame_time)
        if player.frame > 8:
            player.send_speed_to_ball(player.hammer_xspeed, player.hammer_yspeed, player.hammer_angle)
            player.state_machine.handle_event(('FINISH_SHOOT', 0))

    @staticmethod
    def draw(player):
        # player.image.clip_draw(int(player.frame)*100,(5-player.action)*100,100,100,50+player.forward,70)
        player.image.clip_composite_draw(int(player.frame) * 100, (5 - player.action) * 100, 100, 100, 0, '',
                                         80 + player.forward, 95 + (45 * player.type), 100 * 2, 100 * 2)


class Finish_action:  # 피니시 동작
    @staticmethod
    def enter(player, e):
        player.action = 3
        player.frame = 0
        print('Finish_action Enter')

    @staticmethod
    def exit(player, e):
        print('Finish_action Exit')

    @staticmethod
    def do(player):
        if player.frame < 3:
            player.frame = player.frame + 1
        pass

    @staticmethod
    def draw(player):
        player.dx = 80 + player.forward - server.wadlle_ball.x
        player.dy = 95 + (45 * player.type) - server.wadlle_ball.y
        # player.image.clip_draw(player.frame*100,(5-player.action)*100,100,100,50+player.forward,70)
        player.image.clip_composite_draw(int(player.frame) * 100, (5 - player.action) * 100, 100, 100, 0, '',
                                         player.dx, player.dy, 100 * 2, 100 * 2)
        pass


#   Idle(액션 없음)
#   0. Set_angle
#   1. Charging
#   2-1. Timing
#   2-2. Shoot
#   3. Finish_action


class StateMachine:
    def __init__(self, player):
        self.player = player
        # self.cur_state = Idle   # 초기 상태
        self.cur_state = Idle  # 초기 상태 (테스트용)
        self.transitions = {
            Idle: {start_turn: Set_angle},
            Set_angle: {space_down: Charging, up_down: Set_angle, down_down: Set_angle},
            Charging: {time_out: Timing, right_down: Charging, left_down: Charging},
            Timing: {space_down: Shoot, time_out: Shoot},
            Shoot: {finish_shoot: Finish_action},
            Finish_action: {end_turn: Idle},
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


class Player:
    def __init__(self, type, target_ball):
        self.frame = 0
        self.action = 0  # 0:각도조절 2:좌우연타 3:타이밍치기 4:치고대기 5:결과발표대기 6: 승/패모션

        self.forward = 0
        # X축/Y축 스피드

        self.hammer_angle = 0
        self.hammer_charge = 0
        self.hammer_accuracy = 0
        self.hammer_xspeed = 0
        self.hammer_yspeed = 0
        self.ball = target_ball

        # 이벤트 안에서 쓰는 것
        self.is_up_key_pressed = False  # 꾹누르고있는지
        self.is_down_key_pressed = False

        self.charge_time = 0
        self.key_R = False
        self.key_L = False

        self.arrow_image = load_image('./texture/arrow.png')
        self.key_on = load_image('./texture/key_on.png')
        self.key_off = load_image('./texture/key_off.png')
        self.timing_target = load_image('./texture/timing_target.png')
        self.timing_hammer = load_image('./texture/timing_hammer.png')

        if type == 'Kirby':
            self.image = load_image('./texture/sp_kirby.png')
            self.type = 0
        else:
            self.image = load_image('./texture/sp_dedede.png')
            self.type = 1

        #각도 결정 사운드
        self.sound_angle = load_wav('./sound/angle.wav')
        self.sound_angle.set_volume(70)

        #차지 사운드
        self.sound_charge1 = load_wav('./sound/charge1.wav')
        self.sound_charge1.set_volume(20)
        self.sound_charge2 = load_wav('./sound/charge2.wav')
        self.sound_charge2.set_volume(20)

        #슈팅 사운드
        self.sound_shot1 = load_wav('./sound/shot1.wav')
        self.sound_shot1.set_volume(70)
        self.sound_shot2 = load_wav('./sound/shot2.wav')
        self.sound_shot2.set_volume(70)


        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def send_speed_to_ball(self, hammer_xspeed, hammer_yspeed, hammer_angle):
        print("공에게 속도값 전달")
        self.ball.receive_speed(hammer_xspeed, hammer_yspeed, hammer_angle)

    def draw(self):
        self.state_machine.draw()
