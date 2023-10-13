def inside_board(position,H,W):
    if 0 <= position[0] < W and 0 <= position[1] < H:
        return True
    else:
        return False

def legal_actions(Masons,Structures,Walls,H,W):
    Masons_positions = {}
    Masons_positions_set = set()
    Masons_My_positions_set = set()
    Masons_Your_positions_set = set()
    m = 0
    for i in range(H):
        for j in range(W):
            if Masons[i][j] != 0:
                m = max(m,Masons[i][j])
                Masons_positions[Masons[i][j]] = (j,i)
                Masons_positions_set.add((j,i))
                if Masons[i][j] > 0:
                    Masons_My_positions_set.add((j,i))
                else:
                    Masons_Your_positions_set.add((j,i))
                    
    Pond_positions_set = set()
    Castle_positions_set = set()
    for i in range(H):
        for j in range(W):
            if Structures[i][j] == 1:
                Pond_positions_set.add((j,i))
            if Structures[i][j] == 2:
                Castle_positions_set.add((j,i))
    Walls_My_positions_set = set()
    Walls_Your_positions_set = set()
    for i in range(H):
        for j in range(W):
            if Walls[i][j] == 1:
                Walls_My_positions_set.add((j,i))
            if Walls[i][j] == 2:
                Walls_Your_positions_set.add((j,i))
            if Walls[i][j] == 3:
                Walls_My_positions_set.add((j,i))
                Walls_Your_positions_set.add((j,i))
    Masons_My_id = [i for i in range(1,m + 1)]
    # print(Masons_positions)
    # print(Masons_My_id)
    # print(Masons_positions_set)
    actions = [[]for _ in range(m)]
    for Mason_id in Masons_My_id:
        Masons_Other_positions_set = Masons_positions_set - {Masons_positions[Mason_id]}
        # print(Masons_Other_positions_set)
        for i in range(8):
            id = i
            next_position = (Masons_positions[Mason_id][0] + direc[i][0],Masons_positions[Mason_id][1] + direc[i][1])
            # print(i,next_position)
            if inside_board(next_position,H,W):
                if not next_position in Pond_positions_set:
                    if not next_position in Masons_Other_positions_set:
                        if not next_position in Walls_Your_positions_set:
                            actions[Mason_id - 1].append(id)
        for i in range(4):
            next_position = (Masons_positions[Mason_id][0] + direc[i * 2 + 1][0],Masons_positions[Mason_id][1] + direc[i * 2 + 1][1])
            id = i + 8
            if inside_board(next_position,H,W):
                if not next_position in Castle_positions_set:
                    if not next_position in (Walls_My_positions_set | Walls_Your_positions_set):
                        if not next_position in Masons_Your_positions_set:
                            actions[Mason_id - 1].append(id)
        for i in range(4):
            next_position = (Masons_positions[Mason_id][0] + direc[i * 2 + 1][0],Masons_positions[Mason_id][1] + direc[i * 2 + 1][1])
            id = i + 12
            if inside_board(next_position,H,W):
                if next_position in (Walls_My_positions_set | Walls_Your_positions_set):
                    actions[Mason_id - 1].append(id)
            
    print(actions)
    actions_return = [[] for _ in range(m)]
    for i in range(m):
        for j in range(len(actions[i])):
            actions_return[i].append(convert_return[actions[i][j]])
    print(actions_return) 
    return actions_return

def greedy_actions(Masons,Structures,Walls,H,W):
    Masons_positions = {}
    Masons_positions_set = set()
    Masons_My_positions_set = set()
    Masons_Your_positions_set = set()
    m = 0
    for i in range(H):
        for j in range(W):
            if Masons[i][j] != 0:
                m = max(m,Masons[i][j])
                Masons_positions[Masons[i][j]] = (j,i)
                Masons_positions_set.add((j,i))
                if Masons[i][j] > 0:
                    Masons_My_positions_set.add((j,i))
                else:
                    Masons_Your_positions_set.add((j,i))
                    
    Pond_positions_set = set()
    Castle_positions_set = set()
    for i in range(H):
        for j in range(W):
            if Structures[i][j] == 1:
                Pond_positions_set.add((j,i))
            if Structures[i][j] == 2:
                Castle_positions_set.add((j,i))
    Walls_My_positions_set = set()
    Walls_Your_positions_set = set()
    for i in range(H):
        for j in range(W):
            if Walls[i][j] == 1:
                Walls_My_positions_set.add((j,i))
            if Walls[i][j] == 2:
                Walls_Your_positions_set.add((j,i))
            if Walls[i][j] == 3:
                Walls_My_positions_set.add((j,i))
                Walls_Your_positions_set.add((j,i))
    Masons_My_id = [i for i in range(1,m + 1)]
    # print(Masons_positions)
    # print(Masons_My_id)
    # print(Masons_positions_set)
    actions = [[]for _ in range(m)]
    for Mason_id in Masons_My_id:
        Masons_Other_positions_set = Masons_positions_set - {Masons_positions[Mason_id]}
        # print(Masons_Other_positions_set)
        for i in range(8):
            id = i
            next_position = (Masons_positions[Mason_id][0] + direc[i][0],Masons_positions[Mason_id][1] + direc[i][1])
            # print(i,next_position)
            if inside_board(next_position,H,W):
                if not next_position in Pond_positions_set:
                    if not next_position in Masons_Other_positions_set:
                        if not next_position in Walls_Your_positions_set:
                            actions[Mason_id - 1].append(id)
        for i in range(4):
            next_position = (Masons_positions[Mason_id][0] + direc[i * 2 + 1][0],Masons_positions[Mason_id][1] + direc[i * 2 + 1][1])
            id = i + 8
            if inside_board(next_position,H,W):
                if not next_position in Castle_positions_set:
                    if not next_position in (Walls_My_positions_set | Walls_Your_positions_set):
                        if not next_position in Masons_Your_positions_set:
                            actions[Mason_id - 1].append(id)
        for i in range(4):
            next_position = (Masons_positions[Mason_id][0] + direc[i * 2 + 1][0],Masons_positions[Mason_id][1] + direc[i * 2 + 1][1])
            id = i + 12
            if inside_board(next_position,H,W):
                if next_position in (Walls_Your_positions_set):
                    actions[Mason_id - 1].append(id)
            
    print(actions)
    actions_return = [[] for _ in range(m)]
    for i in range(m):
        for j in range(len(actions[i])):
            actions_return[i].append(convert_return[actions[i][j]])
    print(actions_return) 
    return actions_return
            

def greedy_check_actions(Masons,Structures,Walls,H,W):
    Masons_positions = {}
    Masons_positions_set = set()
    Masons_My_positions_set = set()
    Masons_Your_positions_set = set()
    m = 0
    for i in range(H):
        for j in range(W):
            if Masons[i][j] != 0:
                m = max(m,Masons[i][j])
                Masons_positions[Masons[i][j]] = (j,i)
                Masons_positions_set.add((j,i))
                if Masons[i][j] > 0:
                    Masons_My_positions_set.add((j,i))
                else:
                    Masons_Your_positions_set.add((j,i))
                    
    Pond_positions_set = set()
    Castle_positions_set = set()
    for i in range(H):
        for j in range(W):
            if Structures[i][j] == 1:
                Pond_positions_set.add((j,i))
            if Structures[i][j] == 2:
                Castle_positions_set.add((j,i))
    Walls_My_positions_set = set()
    Walls_Your_positions_set = set()
    for i in range(H):
        for j in range(W):
            if Walls[i][j] == 1:
                Walls_My_positions_set.add((j,i))
            if Walls[i][j] == 2:
                Walls_Your_positions_set.add((j,i))
            if Walls[i][j] == 3:
                Walls_My_positions_set.add((j,i))
                Walls_Your_positions_set.add((j,i))
    Masons_My_id = [i for i in range(1,m + 1)]
    # print(Masons_positions)
    # print(Masons_My_id)
    # print(Masons_positions_set)
    actions = [[]for _ in range(m)]
    for Mason_id in Masons_My_id:
        Masons_Other_positions_set = Masons_positions_set - {Masons_positions[Mason_id]}
        # print(Masons_Other_positions_set)
        for i in range(8):
            id = i
            next_position = (Masons_positions[Mason_id][0] + direc[i][0],Masons_positions[Mason_id][1] + direc[i][1])
            # print(i,next_position)
            if inside_board(next_position,H,W):
                if not next_position in Pond_positions_set:
                    if not next_position in Masons_Other_positions_set:
                        if not next_position in Walls_Your_positions_set:
                            if not ((next_position[0] + next_position[1]) % 2):
                                # print(next_position)
                                # print(next_position[0] + next_position[1])
                                actions[Mason_id - 1].append(id)
        for i in range(4):
            next_position = (Masons_positions[Mason_id][0] + direc[i * 2 + 1][0],Masons_positions[Mason_id][1] + direc[i * 2 + 1][1])
            id = i + 8
            if inside_board(next_position,H,W):
                if not next_position in Castle_positions_set:
                    if not next_position in (Walls_My_positions_set | Walls_Your_positions_set):
                        if not next_position in Masons_Your_positions_set:
                            actions[Mason_id - 1].append(id)
        for i in range(4):
            next_position = (Masons_positions[Mason_id][0] + direc[i * 2 + 1][0],Masons_positions[Mason_id][1] + direc[i * 2 + 1][1])
            id = i + 12
            if inside_board(next_position,H,W):
                if next_position in (Walls_Your_positions_set):
                    actions[Mason_id - 1].append(id)
            
    print(actions)
    actions_return = [[] for _ in range(m)]
    for i in range(m):
        for j in range(len(actions[i])):
            actions_return[i].append(convert_return[actions[i][j]])
    print(actions_return) 
    return actions_return
direc = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]

convert_return = [[1,1],
                  [1,2],
                  [1,3],
                  [1,4],
                  [1,5],
                  [1,6],
                  [1,7],
                  [1,8],

                  [2,2],
                  [2,4],
                  [2,6],
                  [2,8],

                  [3,2],
                  [3,4],
                  [3,6],
                  [3,8]]

def rev_Masons(Masons):
    H = W = len(Masons)
    Rev_Masons = [[]for _ in range(H)]
    for i in range(H):
        for j in range(W):
            if Masons[i][j] == 0:
                Rev_Masons[i].append(0)
            else:
                Rev_Masons[i].append(-Masons[i][j])
    return Rev_Masons

def rev_Walls(Walls):
    H = W = len(Walls)
    Rev_Walls = [[] for _ in range(H)]
    for i in range(H):
        for j in range(W):
            if Walls[i][j] == 0:
                Rev_Walls[i].append(0)
            if Walls[i][j] == 1:
                Rev_Walls[i].append(2)
            if Walls[i][j] == 2:
                Rev_Walls[i].append(1)
    return Rev_Walls

def rev_Territories(Territories):
    H = W = len(Territories)
    Rev_Territories = [[] for _ in range(H)]
    for i in range(H):
        for j in range(W):
            if Territories[i][j] == 0:
                Rev_Territories[i].append(0)
            if Territories[i][j] == 1:
                Rev_Territories[i].append(2)
            if Territories[i][j] == 2:
                Rev_Territories[i].append(1)
            if Territories[i][j] == 3:
                Rev_Territories[i].append(3)
    return Rev_Territories

def calc(Structures, Walls, Territories, H, W):
    scoreA = 0
    scoreB = 0
    for i in range(H):
        for j in range(W):
            if Territories[i][j] in (1, 3):
                if Structures[i][j] == 0:
                    scoreA += 30
                if Structures[i][j] == 2:
                    scoreA += 100
            if Territories[i][j] in (2, 3):
                if Structures[i][j] == 0:
                    scoreB += 30
                if Structures[i][j] == 2:
                    scoreB += 100
            if Walls[i][j] == 1:
                scoreA += 10
            if Walls[i][j] == 2:
                scoreB += 10
    return (scoreA, scoreB)

def calculate():
    try:
        s_ = open("./Field_Data/Field_Structures.txt","r")
        w_ = open("./Field_Data/Field_Walls.txt","r")
        t_ = open("./Field_Data/Field_Territories.txt","r")
        s = eval(s_.read())
        w = eval(w_.read())
        t = eval(t_.read())
        H = W = len(s)
        return calc(s, w, t, H, W)
    except:
        None


def convert(m,s,w,t,Bool):
    # try:
    if 1:
        s_ = open("./Field_Data/Field_Structures.txt","w")
        t_ = open("./Field_Data/Field_Territories.txt","w")

        m_ = open("./Field_Data/Field_Masons.txt","w")
        w_ = open("./Field_Data/Field_Walls.txt","w")

        # if Bool == False:
        #     print("REVERSE")
        #     m = rev_Masons(m)
        #     w = rev_Walls(w)
        #     t = rev_Territories(t)

        m_.write(str(m))
        m_.close()

        w_.write(str(w))
        w_.close()

        s_.write(str(s))
        s_.close()

        t_.write(str(t))
        t_.close()
        print("converted!")
        # return legal_actions(m,s,w,H,W)
        # return greedy_actions(m,s,w,H,W)
    # except:
    #     None

# main()

def convert_before_match(m,s):
    # try:
    if 1:
        s_ = open("./Field_Data/Field_Structures.txt","w")

        m_ = open("./Field_Data/Field_Masons.txt","w")

        # if Bool == False:
        #     print("REVERSE")
        #     m = rev_Masons(m)
        #     w = rev_Walls(w)
        #     t = rev_Territories(t)

        m_.write(str(m))
        m_.close()


        s_.write(str(s))
        s_.close()

        print("converted!")
        # return legal_actions(m,s,w,H,W)
        # return greedy_actions(m,s,w,H,W)
    # except:
    #     None

