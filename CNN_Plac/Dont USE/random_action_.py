from random import randint
from copy import deepcopy as dc

direction_dict = { 0:[-1,-1],
                   1:[-1, 0],
                   2:[-1, 1],
                   3:[ 0, 1],
                   4:[ 1, 1],
                   5:[ 1, 0],
                   6:[ 1,-1],
                   7:[ 0,-1],
                   8:[-1, 0],
                   9:[ 0, 1],
                  10:[ 1, 0],
                  11:[ 0,-1]
                  }
direc4_break_dict = {
                   1:12,
                   3:13,
                   5:14,
                   7:15
                   }


def move_able(point,d, masons_point_before, field_masons, field_structures, field_walls, h, w):
    i = point[0] + direction_dict[d][0]
    j = point[1] + direction_dict[d][1]
    if not (0<=i and i<h):
        return False
    if not (0<=j and j<w):
        return False
    if field_masons[i][j] < 0:
        return False
    if field_walls[i][j] == 2 and d%2==0:
        return False
    if field_structures[i][j] == 1:
        return False
    if (i,j) in masons_point_before:
        return False
    return True

def move_able_random(point, masons_point_before, field_masons, field_structures, field_walls, h, w):
    move_able_li = []
    for d in range(8):
        if move_able(point,d, masons_point_before, field_masons, field_structures, field_walls, h, w):
            move_able_li.append(d)
    try:
        return move_able_li[randint(0,len(move_able_li)-1)]
    except:
        # move_able_li == []
        return -1

def run():

    t = 0
    cnt = 0

    n = 0
    f = open("Field_Data/Field_Masons.txt", "r")
    field_masons = eval(f.read())
    w = h = len(field_masons)
    for i in field_masons:
        print(i)
    #! min_turn = h * w * 2
    min_turn = 30
    for i in range(h):
        for j in range(w):
            if field_masons[i][j] > 0:
                n += 1

    masons_point_cp = [[] for _ in range(n)]
    masons_que = [[] for _ in range(n)]
    for i in range(h):
        for j in range(w):
            if field_masons[i][j] > 0:
                masons_que[field_masons[i][j] - 1] = 0
                masons_point_cp[field_masons[i][j] - 1] = (i, j)
    f.close()

    log_li = [[] for _ in range(n)]
    min_log_li = []

    f = open("Field_Data/Field_Walls.txt", "r")
    field_walls = eval(f.read())
    f.close()

    f = open("Field_Data/Field_Structures.txt", "r")
    field_structures = eval(f.read())
    f.close()

    f = open("Plan/Move.txt", "r")
    Plan_move_list = eval(f.read())
    Plan_move_set = set()
    for i in range(h):
        for j in range(w):
            if Plan_move_list[i][j]:
                Plan_move_set.add((i, j))
    f.close()

    f = open("Plan/Build.txt", "r")
    Plan_build_list = eval(f.read())
    Plan_build_set = set()
    for i in range(h):
        for j in range(w):
            if Plan_build_list[i][j]:
                Plan_build_set.add((i, j))
    f.close()

    f = open("Plan/Break.txt", "r")
    Plan_break_list = eval(f.read())
    Plan_break_set = set()
    for i in range(h):
        for j in range(w):
            if Plan_break_list[i][j]:
                Plan_break_set.add((i, j))
    f.close()

    print("move")
    for i in Plan_move_list:
        print(i)
    print("build")
    for i in Plan_build_list:
        print(i)
    print("break")
    for i in Plan_break_list:
        print(i)

    while cnt < 50000:
        cnt += 1
        masons_point = dc(masons_point_cp)
        masons_point_before = set(masons_point_cp)
        move_set = dc(Plan_move_set)
        build_set = dc(Plan_build_set)
        break_set = dc(Plan_break_set)
        t = 0
        log_li = [[]for _ in range(n)]
        while len(move_set)+len(build_set)+len(break_set) > 0:
            if t > min_turn:
                break
            for mason in range(n):
                if masons_que[mason] > 0:
                    masons_que[mason] -= 1
                    continue
                
                move_d = move_able_random(masons_point[mason], masons_point_before, field_masons, field_structures, field_walls, h, w) #0~7
                if move_d == -1:
                    print("ERRRRRR")
                    continue
                masons_point_before.remove((masons_point[mason][0], masons_point[mason][1]))
                masons_point[mason] = (masons_point[mason][0] + direction_dict[move_d][0], 
                                       masons_point[mason][1] + direction_dict[move_d][1])
                masons_point_before.add((masons_point[mason][0],masons_point[mason][1]))

                if field_walls[masons_point[mason][0]][masons_point[mason][1]] == 2:
                    masons_que[mason] += 1
                    log_li[mason].append(direc4_break_dict[move_d])
                    if (masons_point[mason][0],masons_point[mason][1]) in break_set:
                        break_set.remove((masons_point[mason][0],masons_point[mason][1]))

                log_li[mason].append(move_d)

                if masons_point[mason] in move_set:
                    move_set.remove(masons_point[mason])

                for wall_d in range(8,11 + 1):
                    i = masons_point[mason][0] + direction_dict[wall_d][0]
                    j = masons_point[mason][1] + direction_dict[wall_d][1]
                    if (i,j) in build_set:
                        masons_que[mason] += 1
                        if field_walls[i][j] == 2:
                            masons_que[mason] += 1
                            log_li[mason].append(wall_d + 4)
                            if (i,j) in break_set:
                                break_set.remove((i,j))
                        log_li[mason].append(wall_d)
                        build_set.remove((i,j))
                    if (i,j) in break_set:
                        if field_walls[i][j] != 0:
                            masons_que[mason] += 1
                            log_li[mason].append(wall_d + 4)
                            break_set.remove((i,j))
            t += 1
        if t < min_turn:
            min_turn = t
            min_log_li = dc(log_li)
            print(min_turn)
    print(min_turn)
    print(min_log_li)
    # print(cnt)
    # for i in range(n):
    #     min_log_li[i].append(-1)
    f = open("./Plan/run.txt", "w")
    f.write(str(min_log_li))
    f.close()
