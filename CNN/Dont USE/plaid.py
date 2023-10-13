from random import randint

"""
field_mason = [[0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,1,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0]]

field_wall =  [[0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0]]

visited =     [[0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0]]
"""
n=10
total_turns = 30
current_location = [0,5]

field_mason = [[0 for j in range(n)]for i in range(n)]
field_wall = [[0 for j in range(n)]for i in range(n)]
visited = [[0 for j in range(n)]for i in range(n)]

id = 0
current_turns = 0
action_log = []
"""
for i in range(n):
    t = False
    for j in range(n):
        if field_mason[i][j] == 1:
            current_location = [i,j]
            t = True
            break
    if t:
        break
"""
field_mason[current_location[0]][current_location[1]] = 1
visited[current_location[0]][current_location[1]] = 1
#行動id
#0:移動(左上),1:移動(上),2:移動(右上),3:移動(右)
#4:移動(右下),5:移動(下),6:移動(左下),7:移動(左)
#8:建築(上),9:建築(右),10:建築(下),11:建築(左)
id_dict = {0:[-1,-1],1:[-1,0],2:[-1,1],3:[0,1],
           4:[1,1],5:[1,0],6:[1,-1],7:[0,-1],
           8:[-1,0],9:[0,1],10:[1,0],11:[0,-1]}
id_type = {0:"移動",1:"移動",2:"移動",3:"移動",
           4:"移動",5:"移動",6:"移動",7:"移動",
           8:"建築",9:"建築",10:"建築",11:"建築"}

def print_field():
    print("職人"+" "*((n-2)*2+1)+"壁")
    for i in range(n):
        print(" ".join(map(str,field_mason[i]))+' '," ".join(map(str,field_wall[i])))
    print("現在地",current_location,id_type[id],end=" ")
    if id_type[id]=="建築":
        print([current_location[0]+id_dict[id][0],current_location[1]+id_dict[id][1]])
    else:
        print()
    print("ターン",current_turns)
    print()

#print_field()

def move():
    action_log.append(id)
    current_location[0] += id_dict[id][0]
    current_location[1] += id_dict[id][1]
    #field_mason[current_location[0]-id_dict[id][0]][current_location[1]-id_dict[id][1]] = 0
    field_mason[current_location[0]][current_location[1]] += 1
    visited[current_location[0]][current_location[1]] = 1
def build():
    action_log.append(id)
    field_wall[current_location[0]+id_dict[id][0]][current_location[1]+id_dict[id][1]]=1
def infield():
    i = current_location[0]+id_dict[id][0]
    j = current_location[1]+id_dict[id][1]
    if i<0 or j<0 or i==n or j==n:
        return False
    return True
def unvisited():
    if visited[current_location[0]+id_dict[id][0]][current_location[1]+id_dict[id][1]]==0:
        return True
    return False
def can_move():
    li_1 = []
    li_2 = []
    global id
    for i in range(0,8,2):
        id = i
        if infield():
            li_2.append(i)
            if unvisited():
                li_1.append(i)
    #return li_1 + li_2 + li_1*10
    return li_1,li_2
def around_wall():
    li = []
    i = current_location[0]
    j = current_location[1]
    for id in range(8,12):
        if not infield():
            continue
        if field_wall[i+id_dict[id][0]][j+id_dict[id][1]]==0:
            li.append(id)
    return li
    
for i in range(total_turns):
    around_wall_li = around_wall()
    if around_wall_li != []:
        id = around_wall_li[0]
        build()
    else:
        #can_move_li = can_move()
        can_move_li_1,can_move_li_2 = can_move()
        #id = can_move_li[randint(0,len(can_move_li)-1)]
        if can_move_li_1 != []:
            id = can_move_li_1[randint(0,len(can_move_li_1)-1)]
        else:
            id = can_move_li_2[randint(0,len(can_move_li_2)-1)]
        move()
    current_turns+=1
    #print_field()
#print_field()
print("id_log",action_log)
