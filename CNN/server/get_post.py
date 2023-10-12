import requests as rq
import json

# url = "https://www.procon.gr.jp/"
url = "http://127.0.0.1:3000/"
# api_token = "ariakee5d5af0c7ad9401b6449eda7ee0e8730f24f77d5b6da2ac615aca3c1f4"
api_token = "abc12345"
# header = {"procon-token" : api_token}
header = {"Content-Type" : "application/json",
           "procon-token" : api_token}

# ただの表示用
def cout(json_):
    print("\n", "- " * 20, "\n")
    STK = set(["structures", "masons", "walls", "territories"])
    ind = 0
    c = 0
    txt = str(json_).replace(" ", "")
    p = False
    o = 0
    stk = ""
    for i in txt:
        if c:
            print("  " * ind, end = "")
            c = 0

        if (i == "'"):
            p = not p
            if not p:
                if (stk in STK):
                    o = 1
                stk = ""

        if p:
            if (i != "'"):
                stk += i

        if (i == "{" or i == "["):
            if o > 0:
                o += 1
            if o > 2:
                print(i, end = " ")
            else:
                ind += 1
                print(i)
                c = 1
        elif (i == "}" or i == "]"):
            if o > 0:
                o -= 1
                if o == 1:
                    o = 0
            if o > 1:
                print(i, end = " ")
            else:
                ind -= 1
                print()
                print("  " * ind, end = i)
                c = 0
        elif (i == ","):
            if o > 2:
                print(i, end = " ")
            else:
                print(i)
                c = 1
        else:
            print(i, end = "")
    print()
    print("\n", "- " * 20, "\n")



# 試合一覧取得API
# 参加する試合の一覧を取得するAPIです

# Require : token
# Response { [
#            int    id,                 試合ID                  (0 <= id)
#            int    turns,              試合の総ターン数        (30 <= turns <= 200)
#            int    turnSeconds,        １ターン当たりの秒数    (3 <= turnSeconds <= 15)

#            bonus  {                   得点の係数
#            int    wall: 10,           城壁係数        (const 10)
#            int    territory : 30,     陣地係数        (const 30)
#            int    castle : 100        城係数          (const 100)
#                   }

#            board  { 
#            int    width,              横              (11 <= width <= 25)
#            int    height,             縦              (11 <= height <= 25)
#            int    mason,              職人の数        (2 <= mason <= 6)
#            Arrint structures,         構造物          (0 : なし, 1 : 池, 2 : 城)
#            Arrint masons              職人            (0 < masons: 自チーム, 0 > masons: 相手チーム)
#                   }

#            string opponent,           相手のチーム名
#            bool   first               自チームが先手かどうか
#            ] }

def get_match():
    r = rq.get(url + "matches", headers = header)
    print("get_match status_code :", r.status_code)
    response = r.json()
    return response["matches"][0]
    # result = ast.literal_eval(r.text)

res = get_match()
ID = res['id']
# cout(res)
print(ID)

N = res['board']['mason']
print(N)

# 試合状態取得API
# 試合の状態を取得するAPIです

# Require : token, id
# Response { 
#            int    id,                 試合ID                  (0 <= id)
#            int    turn,               どのターンのボードか    (0 <= turn <= turns)

#            board  {
#            Arrint walls,              城壁の情報      (0 : なし, 1 : 自チーム, 2 : 相手チーム の城壁)
#            Arrint territories,        陣地の情報      (0 : 中立, 1 : 自チーム, 2 : 相手チーム, 3 : 両チーム の陣地)
#            int    width,              横              (11 <= width <= 25)
#            int    height,             縦              (11 <= height <= 25)
#            int    mason,              職人の数        (2 <= mason <= 6)
#            Arrint structures,         構造物          (0 : なし, 1 : 池, 2 : 城)
#            Arrint masons              職人            (0 < masons: 自チーム, 0 > masons: 相手チーム)
#                   }

#            logs { [
#            int    turn,               実施ターン          (1 <= turn <= turn)
#                   actions { [
#                   bool    succeeded,  行動が成功したか    (true : 成功, false : 失敗)
#                   int     type,       行動タイプ          (0 : 滞在,  1 : 移動　, 2 : 建築, 3 : 解体)
#                   int     dir         方向(左上を(1, 1))  (1 : 左上,  2 : 上　　, 3 : 右上, 
#                           ] }                              8 : 左　,  0 : 無方向, 4 : 右　, 
#                   ] }                                      7 : 左下,  6 : 下　　, 5 : 右下)
#
#           }
def get_matching(id : int):
    r = rq.get(url + "matches/" + str(id), headers = header)
    print("get_matching status_code :", r.status_code)
    response = r.json()
    return response

res = get_matching(ID)
# cout(res)
t = res['turn']

# 行動計画更新API
# 現在のターンに対する行動計画を更新するAPIです

# Require : token, id
# Response  { 
#            int    turn,        行動を計画するターン    (0 <= turn(次のターンのみ) <= 200)
#            actions { [
#            int     type,       行動タイプ          (0 : 滞在,  1 : 移動　, 2 : 建築, 3 : 解体)
#            int     dir         方向(左上を(1, 1))  (1 : 左上,  2 : 上　　, 3 : 右上, 
#                   ] }                               8 : 左　,  0 : 無方向, 4 : 右　, 
#           }                                         7 : 左下,  6 : 下　　, 5 : 右下)

def post_actions(id : int, masons : int, turn : int, type : int, direction : int):
    actions = {
            'turn' : turn, 
            'actions' : [
                {
                    'type' : type, 
                    'dir' : direction
                }, 
                {
                    'type' : type, 
                    'dir' : direction
                }
            ]
        }
    print(json.dumps(actions, indent = 2))
    # cout(actions)
    r = rq.post(url + "matches/" + str(id), headers = header, data = json.dumps(actions))
    print("post_actions status_code :", r.status_code)
    print(r.text)

post_actions(ID, N, t + 1, 0, 0)

#POST だけできない (status_code : 400)
