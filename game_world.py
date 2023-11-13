# 게임월드 모듈

# 게임월드 표현
objects = [[] for _ in range(5)]
# 레이어 나누기
#   0. 배경
#   1. 땅
#   2. 공 캐릭터
#   3. 플레이어 캐릭터(커비, 디디디)
#   4. UI

# 충돌 그룹 정보 dictionary로 표현

collision_pairs = {}  # {'boy:ball',:[ [boy], [ball1, ball2, ...] ] }


# 지정된 깊이의 레이어에 객체 추가
def add_object(o, depth=0):
    objects[depth].append(o)

# 지정된깊이레이어에 객체 들 추가
def add_objects(ol, depth=0):
    objects[depth] += ol


# 게임월드 객체들을 몽땅 ㄱ업데이ㅡ트
def update():
    for layer in objects:
        for o in layer:
            o.update()


# 게임월드의 객체들을 몽땅 그리기
def render():
    for layer in objects:
        for o in layer:
            o.draw()


# fill here

def add_collision_pair(group, a, b):    # 나중에 add_cloo~_pair('boy:ball',None,ball) 나중에 추가되는 공도 잇어서 a,b없어도 넣어지게
    if group not in collision_pairs:  # 딕셔너리에 키 group이 존재하지 않으면
        print(f'new group {group} added ...')
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


        pass




def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()


# fill here

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True


def handle_coollisions():
    for group,pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a,b):
                    a.handle_collision(group,b)
                    b.handle_collision(group,a)
    return None