from random import randint
from multiprocessing import Pool

h = w = 8
n = 2
g = 0
direction_dict = {0:[-1,-1],1:[-1,0],2:[-1,1],3:[0,1],
                  4:[1,1],5:[1,0],6:[1,-1],7:[0,-1],
                  8:[-1,0],9:[0,1],10:[1,0],11:[0,-1]}
field_masons = [[ 0, 0, 0, 0, 0, 1, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 1, 0, 0, g],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, g, 0, 0],
                [ 0, g, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],]
field_walls = [[ 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0],]
field_structures = [[ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],]

def move_able(point,d, masons_point_before):
    i = point[0] + direction_dict[d][0]
    j = point[1] + direction_dict[d][1]
    if not (0<=i and i<h):
        return False
    if not (0<=j and j<w):
        return False
    if field_masons[i][j] == 1 or field_masons[i][j] == 2:
        return False
    if field_walls[i][j] == 2 and d%2==0:
        return False
    if field_structures[i][j] == 1:
        return False
    if (i,j) in masons_point_before:
        return False
    return True

def move_able_random(point, masons_point_before):
    move_able_li = []
    for d in range(8):
        if move_able(point,d, masons_point_before):
            move_able_li.append(d)
    return move_able_li[randint(0,len(move_able_li)-1)]

def main():
    min_turn = 2*h*w
    t = 0
    cnt = 0

    masons_point = [(0,5),(3,4)]
    masons_point_before = set(masons_point)
    masons_que = [0 for _ in range(n)]

    log_li = [[]for _ in range(n)]
    min_log_li = []

    while cnt < 10000:
        cnt += 1
        masons_point = [(0,5),(3,4)]
        masons_point_before = set(masons_point)
        move_set = {(5,5),(3,7),(6,1)}
        build_set = set()
        break_set = set()
        t = 0
        log_li = [[]for _ in range(n)]
        while len(move_set)+len(build_set)+len(break_set) > 0:
            #print(t,log_li)
            if t > min_turn:
                # print(t)
                break
            for mason in range(n):
                if masons_que[mason] > 0:
                    masons_que[mason] -= 1
                    continue
                
                move_d = move_able_random(masons_point[mason], masons_point_before)
                #print(masons_point_before)
                masons_point_before.remove((masons_point[mason][0],masons_point[mason][1]))
                #masons_point[mason][0] += direction_dict[move_d][0]
                #masons_point[mason][1] += direction_dict[move_d][1]
                masons_point[mason] = (masons_point[mason][0] + direction_dict[move_d][0],masons_point[mason][1] + direction_dict[move_d][1])
                #masons_que[mason] += 1
                masons_point_before.add((masons_point[mason][0],masons_point[mason][1]))
                if field_walls[masons_point[mason][0]][masons_point[mason][1]] == 2:
                    masons_que[mason] += 1
                    log_li[mason].append()
                log_li[mason].append(move_d)
                if masons_point[mason] in move_set:
                    move_set.remove(masons_point[mason])
                #print(masons_point,log_li)
                for wall_d in range(8,12):
                    i = masons_point[mason][0]+direction_dict[wall_d][0]
                    j = masons_point[mason][1]+direction_dict[wall_d][1]
                    if (i,j) in build_set:
                        #masons_que[mason] += 1
                        if field_walls[i][j] == 2:
                            masons_que[mason] += 1
                        build_set.remove([i,j])
                    if (i,j) in break_set:
                        if field_walls[i][j] == 2:
                            #masons_que[mason] += 1
                            break_set.remove([i,j])
            t += 1
        if t-1 < min_turn:
            # print(t)
            min_turn = t-1
            min_log_li = list(log_li)
        min_turn = min(min_turn,t)

    print("", t)
    print(min_log_li)
    print(cnt)

main()
