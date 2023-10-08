import streamlit as st
from copy import deepcopy as dc
from datetime import datetime
from time import sleep
from PIL import Image



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

    r_ = get_matches_id(id)
    response["first"] = r_["first"]
    response["opponent"] = r_["opponent"]
    response["turns"] = r_["turns"]
    response["turnSeconds"] = r_["turnSeconds"]

    return response, status_code


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
        actions_arr = eval(actions_arr)

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

def get_matches_id(id : int):
    r = rq.get(url + "matches", headers = header)
    response = r.json()
    for match in response["matches"]:
        if match.get("id") == int(id):
            status_code = r.status_code
            print("get_matches_id status_code :", r.status_code)
            return match
    return -1

def simple_get_matches(res : json):
    Res = dc(res)

    structures_arr = Res["board"]["structures"]
    masons_arr = Res["board"]["masons"]

    Res["board"]["structures"] = []
    Res["board"]["masons"] = []
    for i in structures_arr:
        Res["board"]["structures"].append(str(i))
    for i in masons_arr:
        Res["board"]["masons"].append(str(i))

    return Res

def simple_get_matching(res : json):
    Res = dc(res)
    del Res["logs"]

    structures_arr = Res["board"]["structures"]
    masons_arr = Res["board"]["masons"]
    walls_arr = Res["board"]["walls"]
    territories_arr = Res["board"]["territories"]

    Res["board"]["structures"] = []
    Res["board"]["masons"] = []
    Res["board"]["walls"] = []
    Res["board"]["territories"] = []
    for i in structures_arr:
        Res["board"]["structures"].append(str(i))
    for i in masons_arr:
        Res["board"]["masons"].append(str(i))
    for i in walls_arr:
        Res["board"]["walls"].append(str(i))
    for i in territories_arr:
        Res["board"]["territories"].append(str(i))

    return Res

# Init (Global) =============================================================

if "ID" not in st.session_state:
    # int
    st.session_state.ID = None

if "is_first" not in st.session_state:
    # bool
    st.session_state.is_first = None

if "opponent" not in st.session_state:
    # string
    st.session_state.opponent = "None"

if "turns" not in st.session_state:
    # int
    st.session_state.turns = None

if "turnSeconds" not in st.session_state:
    # int
    st.session_state.turnSeconds = None

def page1():
    st.title("GET_Matches")

    # Init ==================================================================

    if "res1" not in st.session_state:
        st.session_state.res1 = None

    if "res_fmt1" not in st.session_state:
        st.session_state.res_fmt1 = None

    if "status_code1" not in st.session_state:
        st.session_state.status_code1 = None

    if "dt_now1" not in st.session_state:
        st.session_state.dt_now1 = None

    # Get_Matches ===========================================================

    Get_Matches = st.button("Get_Matches")
    if Get_Matches:
        print("\nGet_Matches ============================")
        st.session_state.dt_now1 = datetime.now()
        st.session_state.res1, st.session_state.status_code1 = get_matches()
        st.session_state.res_fmt1 = None

    # Input / Output ========================================================

    st.write("Status Code :", st.session_state.status_code1, st.session_state.dt_now1)
    st.write("Raw :  ", st.session_state.res1)

def page2():
    st.title("Get_Matching")

    # Init ==================================================================

    if "res2" not in st.session_state:
        st.session_state.res2 = None

    if "res_fmt2" not in st.session_state:
        st.session_state.res_fmt2 = None 

    if "status_code2" not in st.session_state:
        st.session_state.status_code2 = None

    if "logs2" not in st.session_state:
        st.session_state.logs2 = None

    if "dt_now2" not in st.session_state:
        st.session_state.dt_now2 = None

    # Get_Matching ==========================================================

    Get_Matching = st.button("Get_Matchng")
    if Get_Matching:
        print("\nGet_Matching ===========================")
        st.session_state.dt_now2 = datetime.now()
        c = False
        try:
            st.session_state.res2, st.session_state.status_code2 = get_matching(st.session_state.ID)
            c = True
        except:
            st.session_state.status_code2 = 400
            st.session_state.res2 = {
                "operation Get_Matching" : {
                    "params" : 'id', 
                    "error" : "field required"
                }
            }
            st.session_state.res_fmt2 = None
            st.session_state.logs2 = None
        if c:
            try:
                st.session_state.res_fmt2 = simple_get_matching(st.session_state.res2)
                st.session_state.logs2 = st.session_state.res2["logs"]
            except:
                st.session_state.status_code2 = 400
                st.session_state.logs2 = None

    # Input / Output ========================================================

    st.text_input("ID", key="ID")

    st.write("Status Code :", st.session_state.status_code2, st.session_state.dt_now2)
    # st.write("Raw :  ", st.session_state.res2)
    st.write("Simple : ", st.session_state.res_fmt2)
    st.write("Logs : ", st.session_state.logs2)

def page3():
    st.title("Post_Actions")

    # Init ==================================================================

    if "res3_1" not in st.session_state:
        st.session_state.res3_1 = None

    if "res_fmt3_1" not in st.session_state:
        st.session_state.res_fmt3_1 = None

    if "res3_2" not in st.session_state:
        st.session_state.res3_2 = None

    if "turn" not in st.session_state:
        st.session_state.turn = -1

    if "status_code3_1" not in st.session_state:
        st.session_state.status_code3_1 = None

    if "status_code3_2" not in st.session_state:
        st.session_state.status_code3_2 = None

    if "dt_now3_1" not in st.session_state:
        st.session_state.dt_now3_1 = None

    if "dt_now3_2" not in st.session_state:
        st.session_state.dt_now3_2 = None
    
    if "post" not in st.session_state:
        st.session_state.post = None

    # Get_Matching (Get & Post) =============================================

    Post_Auto = st.button("Get_Matchng & Post")
    if Post_Auto:
        print("\nPost_Auto ==============================")

        c = False
        st.session_state.dt_now3_1 = datetime.now()
        try:
            st.session_state.res3_1, st.session_state.status_code3_1 = get_matching(st.session_state.ID)
            c = True
        except:
            st.session_state.status_code3_1 = 400
            st.session_state.res_fmt3_1 = {
                "operation Get_Matching" : {
                    "params" : 'id', 
                    "error" : "field required"
                    }
            }
            st.session_state.turn = -1
        if c:
            try:
                st.session_state.res_fmt3_1 = simple_get_matching(st.session_state.res3_1)
                st.session_state.turn = st.session_state.res3_1["turn"]
            except:
                st.session_state.status_code3_1 = 400
                st.session_state.turn = -1

        st.session_state.dt_now3_2 = datetime.now()
        if (st.session_state.turn == -1):
            st.session_state.res3_2 = {
                    "operation Post_Actions" : {
                            "params" : 'turn', 
                            "error" : "its opponent turn. not your turn"
                        }
                    }
            st.session_state.post = None
            st.session_state.status_code3_2 = 400
        elif ((st.session_state.turn + st.session_state.res3_1["first"]) % 2 == 0):
            st.session_state.res3_2 = {
                    "operation Post_Actions" : {
                            "params" : 'turn', 
                            "error" : "its opponent turn. not your turn"
                        }
                    }
            st.session_state.post = None
            st.session_state.status_code3_2 = 400
        else:
            st.session_state.post, st.session_state.res3_2, st.session_state.status_code3_2 = post_actions(st.session_state.ID, 
                                                                                    st.session_state.turn + 1, 
                                                                                    st.session_state.Actions)
        print("post_actions status code :", st.session_state.status_code3_2)

    # Get_Matching (Auto_Fill) ==============================================

    Get_Matching = st.button("Get_Matchng (Auto_Fill)")
    if Get_Matching:
        print("\nGet_Matching ===========================")
        c = False
        st.session_state.dt_now3_1 = datetime.now()
        try:
            st.session_state.res3_1, st.session_state.status_code3_1 = get_matching(st.session_state.ID)
            c = True
        except:
            st.session_state.status_code3_1 = 400
            st.session_state.res_fmt3_1 = {
                "operation Get_Matching" : {
                    "params" : 'id', 
                    "error" : "field required"
                    }
            }
            st.session_state.turn = None
        if c:
            try:
                st.session_state.res_fmt3_1 = simple_get_matching(st.session_state.res3_1)
                st.session_state.turn = st.session_state.res3_1["turn"]
            except:
                st.session_state.status_code3_1 = 400
                st.session_state.turn = None

    # Input / Output ========================================================

    st.text_input("ID", key="ID")

    st.write("Status Code :", st.session_state.status_code3_1, st.session_state.dt_now3_1)
    st.write("Simple :", st.session_state.res_fmt3_1)

    # Post_Actions ========================================================

    Post_Actions = st.button("Post_Actions")
    if Post_Actions:
        print("\nPost_Actions ===========================")
        st.session_state.dt_now3_2 = datetime.now()
        if ((st.session_state.turn + 1) % 2 == 0):
            st.session_state.res3_2 = {
                    "operation Post_Actions" : {
                            "params" : 'turn', 
                            "error" : "its opponent turn. not your turn"
                        }
                    }
            st.session_state.post = None
            print("post_actions status_code : 400")
        else:
            st.session_state.post, st.session_state.res3_2, st.session_state.status_code3_2 = post_actions(st.session_state.ID, 
                                                                                    st.session_state.turn + 1, 
                                                                                    st.session_state.Actions)

    # Input / Output ========================================================

    st.write("Turn + 1")
    st.code(st.session_state.turn + 1, language='text')
    st.text_input("Actions [[type, direction], ...]", key="Actions")

    st.write("Status Code :", st.session_state.status_code3_2, st.session_state.dt_now3_2)
    st.write("Post :", st.session_state.post)
    st.write("Response :", st.session_state.res3_2)

def page4():
    st.title("Visualizer")

    # Init ==================================================================

    if "res4" not in st.session_state:
        st.session_state.res4 = None

    if "turn4" not in st.session_state:
        st.session_state.turn4 = -1

    if "status_code4" not in st.session_state:
        st.session_state.status_code4 = None

    if "dt_now4" not in st.session_state:
        st.session_state.dt_now4 = None
    
    if "vis_struct_mason" not in st.session_state:
        st.session_state.vis_struct_mason = Image.open("./img/None.png")

    if "vis_wall_territories" not in st.session_state:
        st.session_state.vis_wall_territories = Image.open("./img/None.png")

    
    # Get_Matching (Auto_Reload) ==============================================

    Get_Matching = st.button("Auto Reload")
    if Get_Matching:
        print("\nGet_Matching ===========================")
        c = False
        st.session_state.dt_now4 = datetime.now()
        try:
            st.session_state.res4, st.session_state.status_code4 = get_matching(st.session_state.ID)
            c = True
        except:
            st.session_state.status_code4 = 400
            st.session_state.turn4 = None
            st.session_state.vis_struct_mason = Image.open("./img/None.png")
            st.session_state.vis_wall_territories = Image.open("./img/None.png")
        if c:
            try:
                st.session_state.turn4 = st.session_state.res4["turn"]
                f = open("./Field_Data/Field_Structures.txt","w")
                f.write(str(st.session_state.res4["board"]["structures"]))
                f.close()
                f = open("./Field_Data/Field_Masons.txt","w")
                f.write(str(st.session_state.res4["board"]["masons"]))
                f.close()
                f = open("./Field_Data/Field_Walls.txt","w")
                f.write(str(st.session_state.res4["board"]["walls"]))
                f.close()
                f = open("./Field_Data/Field_Territories.txt","w")
                f.write(str(st.session_state.res4["board"]["territories"]))
                f.close()
                import vis
                st.session_state.vis_struct_mason = Image.open("./Field_Data/visualized_struct_masons.png")
                st.session_state.vis_wall_territories = Image.open("./Field_Data/visualized_wall_territories.png")
            except:
                st.session_state.status_code4 = 400
                st.session_state.turn4 = None
                st.session_state.vis_struct_mason = Image.open("./img/None.png")
                st.session_state.vis_wall_territories = Image.open("./img/None.png")

    # Input / Output ========================================================

    st.text_input("ID", key="ID")

    st.write("Status Code :", st.session_state.status_code4, st.session_state.dt_now4)
    st.write("Raw :", st.session_state.res4)
    st.write("Turn :", st.session_state.turn4)
    st.image(st.session_state.vis_struct_mason, caption='Struct and Masons')


    st.image(st.session_state.vis_wall_territories, caption='Walls and Territories')

    # while True:
    #     sleep(1)

pages = dict(
    page1="Get_Matches",
    page2="Get_Matching",
    page3="Post_Actions",
    page4="Visualizer"
)

page_id = st.sidebar.selectbox( # st.sidebar.*でサイドバーに表示する
    "Change",
    ["page1", "page2", "page3", "page4"],
    format_func=lambda page_id: pages[page_id], # 描画する項目を日本語に変換
)

if page_id == "page1":
    page1()

if page_id == "page2":
    page2()

if page_id == "page3":
    page3()

if page_id == "page4":
    page4()
