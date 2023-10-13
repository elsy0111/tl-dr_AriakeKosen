#任意の地点に最小で行くことができる職人について、その地点に行くまでの行動idログを出力する
#誰もいけない場合は-1
#任意の地点からbfsをして、各職人のその地点までの最小手数を出すように逆算する形で計算
#城壁を破壊するのはむずすぎるんで考えない
from collections import deque
def print_li(li_2d):
    for i in range(len(li_2d)):
        print(li_2d[i])

field_mesons = [[ 1, 0, 0, 0, 0, 0,-2],
                [ 0, 0, 0, 2,-4, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0],
                [ 0,-1, 0, 0, 0, 0, 0],
                [ 0, 0, 3, 0, 0, 4, 0],
                [ 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0,-3, 0, 0, 0]]
field_walls = [[ 0, 0, 0, 0, 0, 0, 0],
               [ 2, 2, 2, 2, 2, 0, 0],
               [ 2, 0, 0, 0, 2, 0, 0],
               [ 2, 0, 0, 0, 2, 0, 0],
               [ 2, 2, 0, 0, 2, 0, 0],
               [ 2, 2, 2, 2, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0]]
field_structures = [[ 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0]]
n = 7
goal_point = [0,5]
visited = [[-1 for j in range(n)] for i in range(n)]
visited[goal_point[0]][goal_point[1]] = 0
id_dict = {0:[-1,-1],1:[-1,0],2:[-1,1],3:[0,1],
           4:[1,1],5:[1,0],6:[1,-1],7:[0,-1],}
id_dict_reverse = {0:4, 1:5, 2:6, 3:7, 4:0, 5:1, 6:2, 7:3}
point_log_li = [[[] for j in range(n)] for i in range(n)]
mesons_li = [[] for _ in range(6)]
total_mesons=0
for i in range(n):
    for j in range(n):
        if field_mesons[i][j]>0:
            total_mesons+=1
            mesons_li[field_mesons[i][j]-1] = [i,j]
mesons_li = mesons_li[:total_mesons]

def move_able(ii,jj):
    if ii<0 or ii==n or jj<0 or jj==n:
        return False
    if field_structures[ii][jj]==1:
        return False
    if field_walls[ii][jj]==2:
        return False
    if field_mesons[ii][jj]<0:
        return False
    if visited[ii][jj]!=-1:
        return False
    return True

q = deque([goal_point])
while len(q) != 0:
    li = q.popleft()
    i = li[0]
    j = li[1]
    for id in range(8):
        ii = i+id_dict[id][0]
        jj = j+id_dict[id][1]
        if move_able(ii,jj):
            q.append([ii,jj])
            visited[ii][jj] = visited[i][j]+1
            point_log_li[ii][jj] = point_log_li[i][j]+[id]
#print_li(point_log_li)
#print(point_log_li[4][2])
#print_li(visited)
#print(mesons_li)
min_turn = 500
min_meson = -1
for meson in range(total_mesons):
    arrive_turn = visited[mesons_li[meson][0]][mesons_li[meson][1]]
    if arrive_turn<min_turn and arrive_turn>=0:
        min_turn = arrive_turn
        min_meson = meson

def id_log_reverse(id_log):
    li = []
    for id in id_log[::-1]:
        li.append(id_dict_reverse[id])
    return li

def print_log(meson):
    print("手数",visited[mesons_li[meson][0]][mesons_li[meson][1]])
    print("職人番号",meson+1)
    print(id_log_reverse(point_log_li[mesons_li[meson][0]][mesons_li[meson][1]]))

if min_meson==-1:
    print(-1)
else:
    print_log(min_meson)
    """
    print("手数",min_turn)
    print("職人番号",min_meson+1)
    print(id_log_reverse(point_log_li[mesons_li[min_meson][0]][mesons_li[min_meson][1]]))"""

"""
print()
for meson in range(total_mesons):
    print_log(meson)
    print()
"""
