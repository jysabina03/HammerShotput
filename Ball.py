from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE



def start_turn(e):
    return e[0] == 'START_TURN'


def touch_the_floor(e):
    return e[0]=='TOUCH_THE_FLOOR'

def shoot(e):
    return e[0] =='SHOOT'

def end_turn(e):
    return e[0] == 'END_TURN'


class Idle:
    # 화면에 나오지 않는 상태
    @staticmethod
    def enter(ball,e):

        ball.xspeed=0
        ball.yspeed=0

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


class Stand_by_Shoot:    # 0. 앉아서 슛 대기
    @staticmethod
    def enter(ball,e):
        ball.action=0
        ball.frame = 0
        print('ball - Stand_by_Shoot Enter')

    @staticmethod
    def exit(ball,e):
        print('ball - Stand_by_Shoot Exit')

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame+1)%2
        pass

    @staticmethod
    def draw(ball):
        ball.image.clip_draw(ball.frame*26,(2-ball.action)*26,26,26,200,90)
        pass

class fly_away:    # 1. 날라감
    @staticmethod
    def enter(ball,e):
        ball.action=1
        ball.frame = 0
        print('ball - fly_away Enter')

    @staticmethod
    def exit(ball,e):
        print('ball - fly_away Exit')

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame+1)%8
        pass

    @staticmethod
    def draw(ball):
        ball.image.clip_draw(ball.frame*26,(2-ball.action)*26,26,26,200,90)
        pass


class landing:    # 2. 착지
    @staticmethod
    def enter(ball,e):
        ball.action=2
        ball.frame = 0
        print('ball - landing Enter')

    @staticmethod
    def exit(ball,e):
        print('ball - landing Exit')

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame+1)%8
        pass

    @staticmethod
    def draw(ball):
        ball.image.clip_draw(ball.frame*40,0,40,24,200,90)
        pass


#   Idle(액션 없음)
#   0. 날라갈 준비   Stand_by_Shoot
#   1. 날라감(공중)  fly_away
#   2. 착지         landing


class StateMachine:
    def __init__(self,ball):
        self.ball = ball
        # self.cur_state = Idle   # 초기 상태
        self.cur_state = Stand_by_Shoot   # 초기 상태 (테스트용)
        self.transitions = {
            Idle: {start_turn: Stand_by_Shoot},
            Stand_by_Shoot: {shoot: fly_away},
            fly_away: {touch_the_floor: landing},
            landing: {end_turn: Idle},
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ball,e)
                self.cur_state=next_state
                self.cur_state.enter(self.ball,e)
                return True

        return False
    def start(self):
        self.cur_state.enter(self.ball,('NONE',0))

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
        self.xspeed=0
        self.yspeed=0

        self.x=0
        self.y=0

        self.state_machine = StateMachine(self)
        self.state_machine.start()

        self.shoot = False

    def receive_speed(self,hammer_xspeed,hammer_yspeed):
        print(f"스피드 수신 - x: {hammer_xspeed}, y: {hammer_yspeed}")
        self.xspeed=hammer_xspeed
        self.yspeed=hammer_yspeed
        self.state_machine.handle_event(('SHOOT', 0))


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()