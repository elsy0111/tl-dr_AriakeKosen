
def convert():
    structures_ = open("./Field_Data/Field_Structures.txt","r")
    walls_ = open("./Field_Data/Field_Walls.txt","r")
    masons_ = open("./Field_Data/Field_Masons.txt","r")


    structures = eval(structures_.read())
    walls = eval(walls_.read())
    masons = eval(masons_.read())

    structures.close()
    walls.close()
    masons.close()

    f = open("./Plan/Break.txt", "r")
    to_break = eval(f.read())
    f.close()
    f = open("./Plan/Build.txt", "r")
    to_build = eval(f.read())
    f.close()
    f = open("./Plan/Move.txt", "r")
    to_move = eval(f.read())
    f.close()


    direction_dict = {0:[-1,-1],1:[-1,0],2:[-1,1],3:[0,1],
                      4:[1,1],5:[1,0],6:[1,-1],7:[0,-1],
                      8:[-1,0],9:[0,1],10:[1,0],11:[0,-1],
                      16:[0,0]}

    h = len(to_break)
    w = h

    move_set_A = set()
    #build_set_A = {(1,3)}
    build_set_A = set()
    #break_set_A = {(7,3)}
    break_set_A = set()

    n = 0
    for i in range(h):
        for j in range(w):
            if field_masons[i][j] > 0:
                n += 1
                masons_point_A[field_masons[i][j]-1] = (i,j)
    masons_point_A = masons_point_A[:n]
    masons_point_before = set(masons_point_A)

    for i in range(h):
        for j in range(w):
            if to_break[i][j] == 1:
                break_set_A.add ((i,j))
            if to_build[i][j] == 1:
                build_set_A.add((i,j))
            if to_move[i][j] == 1:
                move_set_A.add((i,j))


    def move_able(point,d):
        i = point[0] + direction_dict[d][0]
        j = point[1] + direction_dict[d][1]
        if not (0<=i and i<h):
            return False
        if not (0<=j and j<w):
            return False
        if masons[i][j] < 0:
            return False
        if walls[i][j] == 2 and d%2==0:
            return False
        if structures[i][j] == 1:
            return False
        if (i,j) in masons_point_before:
            return False
        return True

    # def move_able_random(point):
    #     move_able_li = []
    #     for d in range(8):
    #         if move_able(point,d):
    #             move_able_li.append(d)
    #     if len(move_able_li) == 0:
    #         return 16
    #     return move_able_li[randint(0,len(move_able_li)-1)]

    
    visit = [[-1 for j in range(w)]for i in range(h)]
    def bfs(start):
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
        if structures[point[0]][point[1]] == 2:
            cant_build.add(point)
        if masons[point[0]][point[1]] < 0:
            cant_build.add(point)
        if not (visit_able((point[0]-1,point[1])) or visit_able((point[0],point[1]+1)) or \
                visit_able((point[0]+1,point[1])) or visit_able((point[0],point[1]-1)) ):
            cant_build.add(point)
    build_set_A -= cant_build
    cant_break = set()
    for point in break_set_A:
        if walls[point[0]][point[1]] == 0:
            cant_break.add((point[0],point[1]))
        if  not (visit_able((point[0]-1,point[1])) or visit_able((point[0],point[1]+1)) or \
                visit_able((point[0]+1,point[1])) or visit_able((point[0],point[1]-1)) ):
            cant_break.add(point)
    break_set_A -= cant_break
    print(build_set_A)

    re_move_li  = [[0 for j in range(w)]for i in range(h)]
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


    f = open("./Plan/Break.txt", "w")
    f.write(str(re_break_li))
    f.close()
    f = open("./Plan/Build.txt", "w")
    f.write(str(re_build_li))
    f.close()
    f = open("./Plan/Move.txt", "w")
    f.write(str(re_move_li))
    f.close()
    
