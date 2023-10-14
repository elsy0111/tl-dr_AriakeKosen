from random import randint
from queue import Queue

"""
f = open("./Field_Data/Masons.txt", "r")
field_masons = eval(f.read())
f.close()
f = open("./Field_Data/Walls.txt", "r")
field_walls = eval(f.read())
f.close()
f = open("./Field_Data/Structures.txt", "r")
field_structures = eval(f.read())
f.close()
"""

g = 0
field_masons = [[ 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 2, 0, 0, g, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, g, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
b = 2
x = 2
field_walls = [[ 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, b, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, x, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]
field_structures = [[ 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]
"""("""
#move_set_A = {(3,7),(6,1)}
move_set_A = set()
#build_set_A = {(1,3)}
build_set_A = set()
#break_set_A = {(7,3)}
break_set_A = set()
#bfs(break_set_A,True)

f = open("./Plan/Break.txt", "r")
to_break = eval(f.read())
f.close()
f = open("./Plan/Build.txt", "r")
to_build = eval(f.read())
f.close()
f = open("./Plan/Move.txt", "r")
to_move = eval(f.read())
f.close()
h = w = len(to_move)

for i in range(h):
    for j in range(w):
        if to_break[i][j] == 1:
            break_set_A.add ((i,j))
        if to_build[i][j] == 1:
            build_set_A.add((i,j))
        if to_move[i][j] == 1:
            move_set_A.add((i,j))
""")"""
print(move_set_A)
print(build_set_A)
print(break_set_A)

#h = w = 11
min_turn = 2*h*w
t = 0
cnt = 0

masons_point_A = [(-1,-1) for _ in range(6)]

n = 0
for i in range(h):
    for j in range(w):
        if field_masons[i][j] > 0:
            n += 1
            masons_point_A[field_masons[i][j]-1] = (i,j)
masons_point_A = masons_point_A[:n]
masons_point_before = set(masons_point_A)
print(masons_point_A)
masons_que = [0 for _ in range(n)]
direction_dict = {0:[-1,-1],1:[-1,0],2:[-1,1],3:[0,1],
                  4:[1,1],5:[1,0],6:[1,-1],7:[0,-1],
                  8:[-1,0],9:[0,1],10:[1,0],11:[0,-1],
                  16:[0,0]}
move_break_dict = {1:12,3:13,5:14,7:15}
build_break_dict = {8:12,9:13,10:14,11:15}
log_li = [[]for _ in range(n)]
min_log_li = []

def move_able(point,d):
    i = point[0] + direction_dict[d][0]
    j = point[1] + direction_dict[d][1]
    if not (0<=i and i<h):
        return False
    if not (0<=j and j<w):
        return False
    if field_masons[i][j] != 0:
        return False
    if field_walls[i][j] == 2 and d%2==0:
        return False
    if field_structures[i][j] == 1:
        return False
    if (i,j) in masons_point_before:
        return False
    return True

def move_able_random(point):
    move_able_li = []
    for d in range(8):
        if move_able(point,d):
            move_able_li.append(d)
    if len(move_able_li) == 0:
        return 16
    return move_able_li[randint(0,len(move_able_li)-1)]

"""("""
visit = [[-1 for j in range(w)]for i in range(h)]
def bfs(start):
    global k
    que = Queue()
    que.put(start)
    while not que.empty():
        point = que.get()
        for d in range(8):
            if move_able(point,d):
                if visit[point[0]+direction_dict[d][0]][point[1]+direction_dict[d][1]] == -1:
                    visit[point[0]+direction_dict[d][0]][point[1]+direction_dict[d][1]] = 1
                    que.put((point[0]+direction_dict[d][0],point[1]+direction_dict[d][1]))

for mason in range(n):
    bfs(masons_point_A[mason])
def visit_able(point):
    if visit[point[0]][point[1]] == 1:
        return True
    return False
cant_move = set()
for point in move_set_A:
    if not visit_able(point):
        cant_move.add(point)
move_set_A -= cant_move
cant_build = set()
for point in build_set_A: #城ダメ相手の職人の場所ダメ =>  最初にlen(build_set_A)回見て、build_set_A-=ダメだったの
    if field_structures[point[0]][point[1]] == 2:
        cant_build.add(point)
    if field_masons[point[0]][point[1]] < 0:
        cant_build.add(point)
    if not (visit_able((point[0]-1,point[1])) or visit_able((point[0],point[1]+1)) or \
             visit_able((point[0]+1,point[1])) or visit_able((point[0],point[1]-1)) ):
        cant_build.add(point)
build_set_A -= cant_build
cant_break = set()
for point in break_set_A:
    if field_walls[point[0]][point[1]] == 0:
        cant_break.add((point[0],point[1]))
    if  not (visit_able((point[0]-1,point[1])) or visit_able((point[0],point[1]+1)) or \
             visit_able((point[0]+1,point[1])) or visit_able((point[0],point[1]-1)) ):
        cant_break.add(point)
break_set_A -= cant_break
print(build_set_A)

re_move_li = [[0 for j in range(w)]for i in range(h)]
re_build_li = [[0 for j in range(w)]for i in range(h)]
re_break_li = [[0 for j in range(w)]for i in range(h)]
for i in range(h):
    for j in range(w):
        if (i,j) in move_set_A:
            re_move_li[i][j] = 1
        if (i,j) in build_set_A:
            re_build_li[i][j] = 1
        if (i,j) in break_set_A:
            re_break_li[i][j] = 1

def pl(li):
    for i in range(len(li)):
        print(li[i])
    print()
pl(visit)
pl(to_build)
""")"""

while cnt < 0:
#while min_turn > 10:
    cnt += 1
    break_set = set(break_set_A)
    build_set = set(build_set_A)
    move_set = set(move_set_A)
    masons_point = list(masons_point_A)
    masons_point_before = set(masons_point_A)
    t = 0
    log_li = [[]for _ in range(n)]
    while len(move_set)+len(build_set)+len(break_set) > 0:
        if t > min_turn:
            break
        for mason in range(n):
            if masons_que[mason] > 0:
                masons_que[mason] -= 1
                continue
            
            move_d = move_able_random(masons_point[mason])
            masons_point_before.remove((masons_point[mason][0],masons_point[mason][1]))
            masons_point[mason] = (masons_point[mason][0] + direction_dict[move_d][0],masons_point[mason][1] + direction_dict[move_d][1])
            #masons_que[mason] += 1
            masons_point_before.add((masons_point[mason][0],masons_point[mason][1]))
            if field_walls[masons_point[mason][0]][masons_point[mason][1]] == 2:
                masons_que[mason] += 1
                log_li[mason].append(move_break_dict[move_d])
                if (masons_point[mason][0],masons_point[mason][1]) in break_set:
                    break_set.remove((masons_point[mason][0],masons_point[mason][1]))
            """("""
            if move_d != 16:
                log_li[mason].append(move_d)
            """)"""
            if masons_point[mason] in move_set:
                move_set.remove(masons_point[mason])
            for wall_d in range(8,12):
                i = masons_point[mason][0]+direction_dict[wall_d][0]
                j = masons_point[mason][1]+direction_dict[wall_d][1]
                if (i,j) in build_set:
                    masons_que[mason] += 1
                    if field_walls[i][j] == 2:
                        masons_que[mason] += 1
                        log_li[mason].append(build_break_dict[wall_d])
                        if (i,j) in break_set:
                            break_set.remove((i,j))
                    log_li[mason].append(wall_d)
                    build_set.remove((i,j))
                if (i,j) in break_set:
                    if field_walls[i][j] == 2:
                        masons_que[mason] += 1
                        log_li[mason].append(build_break_dict[wall_d])
                        break_set.remove((i,j))
        t += 1
    if t < min_turn:
        min_turn = t
        min_log_li = list(log_li)
        print(min_turn)
print(min_turn)
print(min_log_li)
print(cnt)
