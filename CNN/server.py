import requests as rq
import json

# url = "https://www.procon.gr.jp/"
url = "http://127.0.0.1:3000/"
# api_token = "ariakee5d5af0c7ad9401b6449eda7ee0e8730f24f77d5b6da2ac615aca3c1f4"
api_token = "A"
# header = {"procon-token" : api_token}
header = {"Content-Type" : "application/json",
           "procon-token" : api_token}

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

def get_matches():
    r = rq.get(url + "matches", headers = header)
    response = r.json()
    status_code = r.status_code
    print("get_match status_code :", r.status_code)
    return response["matches"], status_code

# res = get_matches()
# ID = res['id']
# cout(res)
# print(ID)

# N = res['board']['mason']
# print(N)

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
    response = r.json()
    status_code = r.status_code
    print("get_matching status_code :", r.status_code)

    r_ = get_matches_id(id) #id の試合を取得
    response["first"] = r_["first"]
    response["opponent"] = r_["opponent"]
    response["turns"] = r_["turns"]
    response["turnSeconds"] = r_["turnSeconds"]

    return response, status_code

def get_matches_id(id : int):
    r = rq.get(url + "matches", headers = header)
    response = r.json()
    for match in response["matches"]:
        if match.get("id") == int(id):
            status_code = r.status_code
            print("get_matches_id status_code :", r.status_code)
            return match
    return -1


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

def post_actions(id : int, turn : int, actions_arr : list):
    try:
        # actions_arr = eval(actions_arr)

        actions = {
                'turn' : turn, 
                'actions' : 
                    list2json(actions_arr)
                # [
                #     {
                #         'type' : 0, 
                #         'dir' :  0
                #         }, 
                #     {
                #         'type' : 0, 
                #         'dir' : 0
                #     }
                # ]
            }

    except:
        actions = "feild"
        response = {
                "operation Post_Actions" : {
                    "params" : "Actions", 
                    "error" : "wrong format"
                }
                }
        status_code = 400
        print("Actions wrong format")
        return actions, response, status_code

    print(json.dumps(actions, indent=2))
    r = rq.post(url + "matches/" + str(id), headers = header, data = json.dumps(actions))
    try:
        response = r.json()
        print(response)
    except:
        print("Error")
        response = -1
    status_code = r.status_code
    # print("post_actions status_code :", r.status_code)
    return actions, response, status_code

def list2json(actions : list):
    # print(actions)
    j = []
    for action in actions:
        j.append({
                'type' : action[0], 
                'dir'  : action[1]
                })
    # print(j)
    return j
