def run():
    # READ FIELD
    field_Masons = open("./Field_Data/Field_Masons.txt","r")
    field_Walls = open("./Field_Data/Field_Walls.txt","r")
    # field_Structures = open("./Field_Data/Field_Structures.txt","r")

    field_Masons_Arr = eval(field_Masons.read())
    field_Walls_Arr = eval(field_Walls.read())
    # field_Structures_Arr = eval(field_Structures.read())

    field_Masons.close()
    field_Walls.close()
    # field_Structures.close()

    # READ PLAN
    # plan_move = open("./Plan/Move.txt", "r")
    plan_build = open("./Plan/Build.txt", "r")
    # plan_make_around = open("./Plan/make_around.txt", "r")

    # plan_move_Arr = eval(plan_move.read())
    plan_build_Arr = eval(plan_build.read())
    # plan_make_around_Arr = eval(plan_make_around.read())

    # plan_move.close()
    plan_build.close()
    # plan_make_around.close()

    # Inistialize H W
    h = len(field_Masons_Arr)
    w = h

    def build_able(i,j):
        if i < 0 or i == h:
            return False
        if j < 0 or j == w:
            return False
        if field_Masons_Arr[i][j] < 0:
            return False
        if field_Walls_Arr[i][j] != 0:
            return False
        # if field_Structures_Arr[i][j] == 2:
        #     return False
        return True


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

    # READ RUN
    f = open("./Plan/run.txt","r")
    run_ = eval(f.read())
    f.close()

    f = open("./Plan/run.txt","w")
        
    for mason_idx,mason in enumerate(masons_li):
        for di in range(4):
            d = 2 * di + 1
            if plan_build_Arr[mason[0] + id_dict[d][0]][mason[1] + id_dict[d][1]]:
                if build_able(mason[0] + id_dict[d][0],mason[1] + id_dict[d][1]):
                    if field_Walls_Arr[mason[0] + id_dict[d][0]][mason[1] + id_dict[d][1]] == 2:
                        run_[mason_idx].insert(0,8 + di)
                        run_[mason_idx].insert(0,12 + di)
                    else:
                        run_[mason_idx].insert(0,8 + di)
                        
    f.write(str(run_))
    f.close()
