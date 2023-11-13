from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE


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


def time_out(e):
    return e[0] == 'TIME_OUT'

def start_turn(e):
    return e[0] == 'START_TURN'

def finish_shoot(e):
    return e[0]=='FINISH_SHOOT'
def end_turn(e):
    return e[0] == 'END_TURN'

class Idle:
    # 화면에 나오지 않는 상태
    @staticmethod
    def enter(player):

        player.hammer_angle=0
        player.hammer_charge=0
        player.hammer_accuracy=0
        player.hammer_xspeed=0
        player.hammer_yspeed=0

        print('Set_angle Idle')

    @staticmethod
    def exit(player):
        print('Set_angle Idle')

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass


class Set_angle:    # 0. 각도조절
    @staticmethod
    def enter(player):
        player.action=0
        player.frame = 0
        print('Set_angle Enter')

    @staticmethod
    def exit(player):
        print('Set_angle Exit')

    @staticmethod
    def do(player):
        player.frame = (player.frame+1)%2
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame*100,player.action*100,100,100,50,50)
        pass



class Charging:    # 1. 좌우연타차징
    @staticmethod
    def enter(player):
        player.action=1
        player.frame = 0
        player.forward = 0
        print('Charging Enter')

    @staticmethod
    def exit(player):

        print('Charging Exit')

    @staticmethod
    def do(player):
        player.frame = (player.frame+1)%8
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame*100,player.action*100,100,100,50+player.forward,50)
        pass


class Timing:    # 2-1 타이밍 맞춰서
    @staticmethod
    def enter(player):
        player.action=2
        player.frame = 0
        print('Timing Enter')

    @staticmethod
    def exit(player):
        print('Timing Exit')

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame*100,player.action*100,100,100,50+player.forward,50)
        pass

class Shoot:    # 2-2 날리기
    @staticmethod
    def enter(player):
        player.action=2
        player.frame = 0
        print('Shoot Enter')

    @staticmethod
    def exit(player):

        print('Shoot Exit')

    @staticmethod
    def do(player):
        player.frame = player.frame+1
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame*100,player.action*100,100,100,50+player.forward,50)
        pass


class Finish_action:    # 피니시 동작
    @staticmethod
    def enter(player):
        player.action=2
        player.frame = 0
        print('Finish_action Enter')

    @staticmethod
    def exit(player):

        print('Finish_action Exit')

    @staticmethod
    def do(player):
        player.frame = player.frame+1
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame*100,player.action*100,100,100,50+player.forward,50)
        pass


#   Idle(액션 없음)
#   0. Set_angle
#   1. Charging
#   2-1. Timing
#   2-2. Shoot
#   3. Finish_action


class StateMachine:
    def __init__(self,player):
        self.player = player
        self.cur_state = Idle   # 초기 상태
        self.transitions = {
            Idle:{start_turn: Set_angle},
            Set_angle:{space_down: Charging},
            Charging: {time_out: Timing},
            Timing: {space_down: Shoot},
            Shoot: {finish_shoot: Finish_action},
            Finish_action: {end_turn: Idle},
        }

    def start(self):
        self.cur_state.enter(self.player)

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)




class Player:
    def __init__(self,type):
        self.frame = 0
        self.action = 0 # 0:각도조절 2:좌우연타 3:타이밍치기 4:치고대기 5:결과발표대기 6: 승/패모션
        self.type = type

        self.forward = 0
        # X축/Y축 스피드

        self.hammer_angle=0
        self.hammer_charge=0
        self.hammer_accuracy=0
        self.hammer_xspeed=0
        self.hammer_yspeed=0


        if type is 'Kirby':
            self.image = load_image('sp.kirby.png')
        else:
            self.image = load_image('sp.dedede.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()