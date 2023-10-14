# import numpy as np

def run():
    from collections import deque
    # READ FIELD
    field_Masons = open("./Field_Data/Field_Masons.txt","r")
    field_Walls = open("./Field_Data/Field_Walls.txt","r")
    field_Structures = open("./Field_Data/Field_Structures.txt","r")

    field_Masons_Arr = eval(field_Masons.read())
    field_Walls_Arr = eval(field_Walls.read())
    field_Structures_Arr = eval(field_Structures.read())

    field_Masons.close()
    field_Walls.close()
    field_Structures.close()

    # Inistialize H W
    h = len(field_Masons_Arr)
    w = h

    # READ PLAN
    plan_move = open("./Plan/Move.txt", "r")
    # plan_build = open("./Plan/Build.txt", "r")
    # plan_make_around = open("./Plan/make_around.txt", "r")

    plan_move_Arr = eval(plan_move.read())
    # plan_build_Arr = eval(plan_build.read())
    # plan_make_around_Arr = eval(plan_make_around.read())

    plan_move.close()
    # plan_build.close()
    # plan_make_around.close()

    id_dict = {
            0:[-1,-1],
            1:[-1,0],
            2:[-1,1],
            3:[0,1],
            4:[1,1],
            5:[1,0],
            6:[1,-1],
            7:[0,-1]
            }

    masons_li = [[] for _ in range(6)]

    masons=0
    for i in range(h):
        for j in range(w):
            if field_Masons_Arr[i][j] > 0:
                masons +=1
                masons_li[field_Masons_Arr[i][j]-1] = (i,j)
    masons_li = masons_li[:masons]
    print(masons_li)


    def move_able(ii,jj,visited):
        #bangai
        if ii<0 or ii==h or jj<0 or jj==w:
            return False
        #ike
        if field_Structures_Arr[ii][jj]==1:
            return False
        #相手の壁
        if field_Walls_Arr[ii][jj]==2:
            return False
        #相手の職人
        if field_Masons_Arr[ii][jj]<0:
            return False
        if visited[ii][jj]!=-1:
            return False
        return True

    # Inisialize goal point
    goal_point_set = set()
    for i in range(h):
        for j in range(w):
            if plan_move_Arr[i][j]:
                goal_point_set.add((i,j))
    goal_point_list = list(goal_point_set)
                

    #i,jに関する方向(行動id)ログ
    # point_log_li = [[[] for _ in range(w)] for _ in range(h)]
    print(goal_point_list)

    log = [[] for _ in range(masons)]

    remain_masons_set = set(masons_li)
    for goal_point in goal_point_list:
        # Initialize visited
        visited = [[-1 for _ in range(w)] for _ in range(h)]
        visited[goal_point[0]][goal_point[1]] = 0
        print(goal_point)

        q = deque([goal_point])

        while len(q) != 0:
            li = q.popleft()
            i = li[0]
            j = li[1]
            for d in range(8):
                #移動先
                ii = i+id_dict[d][0]
                jj = j+id_dict[d][1]
                #移動できる?
                if move_able(ii,jj,visited=visited):
                    #移動出来たら
                    q.append([ii,jj])
                    #ii,jjに今のターン数 + 1手でいける!
                    visited[ii][jj] = visited[i][j]+1
                    # point_log_li[i][j] = d
        # pprint(visited)
        # print(np.array(visited))
        shortest_mason_id = -1
        shortest_distance = 200
        for mason in remain_masons_set:
            if visited[mason[0]][mason[1]] < shortest_distance:
                shortest_mason_id =  masons_li.index(mason)
                shortest_distance = visited[mason[0]][mason[1]]
        if shortest_mason_id == -1:
            print("UNREACH to",goal_point)
        else:
            remain_masons_set.remove(masons_li[shortest_mason_id])
            print("shortest_mason :","id =",shortest_mason_id + 1,"posision =",masons_li[shortest_mason_id])
            print("turn :",visited[masons_li[shortest_mason_id][0]][masons_li[shortest_mason_id][1]])

            cy,cx = masons_li[shortest_mason_id]
            
            min_d = visited[masons_li[shortest_mason_id][0]][masons_li[shortest_mason_id][1]] + 1
            while 1:
                # print(cy,cx)
                shortest_act = -1
                for d in range(8):
                    # print(visited[cy + id_dict[d][0]][cx + id_dict[d][1]])
                    # print("mind",min_d)
                    if 0 <= cy + id_dict[d][0] < h  and 0 <= cx + id_dict[d][1] < w:
                        if visited[cy + id_dict[d][0]][cx + id_dict[d][1]] != -1:
                            if visited[cy + id_dict[d][0]][cx + id_dict[d][1]] < min_d:
                                min_d = visited[cy + id_dict[d][0]][cx + id_dict[d][1]]
                                shortest_act = d
                # print("")
                if shortest_act == -1:
                    raise
                cy += id_dict[shortest_act][0]
                cx += id_dict[shortest_act][1]
                log[shortest_mason_id].append(shortest_act)
                if min_d == 0:
                    break
    # print(log)
    # return log

    f = open("./Plan/run.txt", "w")
    f.write(str(log))
    f.close()
    print("SIMPLE MOVE COMPLETED")