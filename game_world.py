# 게임월드 모듈

# 게임월드 표현

worlds = [[],[],[],[],[]]
# 레이어 나누기
#   0. 배경
#   1. 공 캐릭터
#   2. 플레이어 캐릭터(커비, 디디디)
#   3. 땅
#   4. UI

# 게임 월드에 개체 담기

def add_object(o,depth=0):
    worlds[depth].append(o) # 지정된 깊이의 레이어에 객체 추가

# 게임월드 객체들을 몽땅 ㄱ업데이ㅡ트

def update():
    for layer in worlds:
        for o in layer:
            o.update()

# 게임월드의 객체들을 몽땅 그리기

def render():
    for layer in worlds:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in worlds:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError("remove fail(없는걸지우려함..)")