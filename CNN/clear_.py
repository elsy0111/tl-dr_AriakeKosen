
def run():
    import numpy as np
    
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
    plan_build = open("./Plan/Build.txt", "r")
    # plan_make_around = open("./Plan/make_around.txt", "r")

    plan_move_Arr = eval(plan_move.read())
    plan_build_Arr = eval(plan_build.read())
    # plan_make_around_Arr = eval(plan_make_around.read())

    plan_move.close()
    plan_build.close()
    # plan_make_around.close()


    # WRITE
    plan_move = open("./Plan/Move.txt", "w")
    plan_build = open("./Plan/Build.txt", "w")
    
    # print(np.array(field_Masons_Arr))
    for i in range(h):
        for j in range(w):
            #達成した
            if plan_move_Arr[i][j] and (field_Masons_Arr[i][j] > 0):
                plan_move_Arr[i][j] = 0
            if plan_build_Arr[i][j] and (field_Walls_Arr[i][j] == 1):
                plan_build_Arr[i][j] = 0
            #そもそも無理
            if plan_move_Arr[i][j] and (field_Structures_Arr[i][j] == 1):
                plan_move_Arr[i][j] = 0
            if plan_build_Arr[i][j] and (field_Structures_Arr[i][j] == 2):
                plan_build_Arr[i][j] = 0
                
    # print(np.array(plan_move_Arr))
            
    plan_move.write(str(plan_move_Arr))
    plan_build.write(str(plan_build_Arr))

    plan_move.close()
    plan_build.close()