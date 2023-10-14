import streamlit as st
from copy import deepcopy as dc
from datetime import datetime
from PIL import Image
import vis
import lib
import threading
import time

import requests as rq
import json


# url = "https://www.procon.gr.jp/"
url = "http://127.0.0.1:3000/"
# api_token = "ariakee5d5af0c7ad9401b6449eda7ee0e8730f24f77d5b6da2ac615aca3c1f4"
api_token = "A"
# header = {"procon-token" : api_token}
is_accepted = [False for _ in range(201)]

header = {"Content-Type" : "application/json",
        "procon-token" : api_token}


def get_matches(First = True):
    """
    試合一覧取得API
    参加する試合の一覧を取得するAPIです

    Require : token
    Response { [
               int    id,                 試合ID                  (0 <= id)
               int    turns,              試合の総ターン数        (30 <= turns <= 200)
               int    turnSeconds,        １ターン当たりの秒数    (3 <= turnSeconds <= 15)

               bonus  {                   得点の係数
               int    wall: 10,           城壁係数        (const 10)
               int    territory : 30,     陣地係数        (const 30)
               int    castle : 100        城係数          (const 100)
                      }

               board  { 
               int    width,              横              (11 <= width <= 25)
               int    height,             縦              (11 <= height <= 25)
               int    mason,              職人の数        (2 <= mason <= 6)
               Arrint structures,         構造物          (0 : なし, 1 : 池, 2 : 城)
               Arrint masons              職人            (0 < masons: 自チーム, 0 > masons: 相手チーム)
                      }

               string opponent,           相手のチーム名
               bool   first               自チームが先手かどうか
               ] }
    """
    if First:
        header = {"Content-Type" : "application/json",
                "procon-token" : api_tokens[0]}
    else:
        header = {"Content-Type" : "application/json",
                "procon-token" : api_tokens[1]}
    r = rq.get(url + "matches", headers = header)
    response = r.json()
    status_code = r.status_code
    print("get_match status_code :", r.status_code)
    return response["matches"], status_code


def get_matching(id : int,First = True):
    """
     res = get_matches()
     ID = res['id']
     cout(res)
     print(ID)

     N = res['board']['mason']
     print(N)

     試合状態取得API
     試合の状態を取得するAPIです

     Require : token, id
     Response { 
                int    id,                 試合ID                  (0 <= id)
                int    turn,               どのターンのボードか    (0 <= turn <= turns)

                board  {
                Arrint walls,              城壁の情報      (0 : なし, 1 : 自チーム, 2 : 相手チーム の城壁)
                Arrint territories,        陣地の情報      (0 : 中立, 1 : 自チーム, 2 : 相手チーム, 3 : 両チーム の陣地)
                int    width,              横              (11 <= width <= 25)
                int    height,             縦              (11 <= height <= 25)
                int    mason,              職人の数        (2 <= mason <= 6)
                Arrint structures,         構造物          (0 : なし, 1 : 池, 2 : 城)
                Arrint masons              職人            (0 < masons: 自チーム, 0 > masons: 相手チーム)
                       }

                logs { [
                int    turn,               実施ターン          (1 <= turn <= turn)
                       actions { [
                       bool    succeeded,  行動が成功したか    (true : 成功, false : 失敗)
                       int     type,       行動タイプ          (0 : 滞在,  1 : 移動　, 2 : 建築, 3 : 解体)
                       int     dir         方向(左上を(1, 1))  (1 : 左上,  2 : 上　　, 3 : 右上, 
                               ] }                              8 : 左　,  0 : 無方向, 4 : 右　, 
                       ] }                                      7 : 左下,  6 : 下　　, 5 : 右下)

               }
    """
    if First:
        header = {"Content-Type" : "application/json",
                "procon-token" : api_tokens[0]}
    else:
        header = {"Content-Type" : "application/json",
                "procon-token" : api_tokens[1]}
    r = rq.get(url + "matches/" + str(id), headers = header)
    response = r.json()
    status_code = r.status_code
    # print("get_matching   status_code :", r.status_code)

    r_ = get_matches_id(id,First)
    response["first"] = r_["first"]
    response["opponent"] = r_["opponent"]
    response["turns"] = r_["turns"]
    response["turnSeconds"] = r_["turnSeconds"]

    return response, status_code

def post_actions(id : int, turn : int, actions_arr : list, First = True):

    """
    行動計画更新API
    現在のターンに対する行動計画を更新するAPIです

    Require : token, id
    Response  { 
               int    turn,        行動を計画するターン    (0 <= turn(次のターンのみ) <= 200)
               actions { [
               int     type,       行動タイプ          (0 : 滞在,  1 : 移動　, 2 : 建築, 3 : 解体)
               int     dir         方向(左上を(1, 1))  (1 : 左上,  2 : 上　　, 3 : 右上, 
                      ] }                               8 : 左　,  0 : 無方向, 4 : 右　, 
              }                                         7 : 左下,  6 : 下　　, 5 : 右下)
    """

    if First:
        header = {"Content-Type" : "application/json",
                "procon-token" : api_tokens[0]}
    else:
        header = {"Content-Type" : "application/json",
                "procon-token" : api_tokens[1]}
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

    # print(json.dumps(actions, indent=2))
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

def get_matches_id(id : int,First = True):
    if First:
        header = {"Content-Type" : "application/json",
                "procon-token" : api_tokens[0]}
    else:
        header = {"Content-Type" : "application/json",
                "procon-token" : api_tokens[1]}
    r = rq.get(url + "matches", headers = header)
    response = r.json()
    for match in response["matches"]:
        if match.get("id") == int(id):
            status_code = r.status_code
            # print("get_matches_id status_code :", status_code)
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

if "size" not in st.session_state:
    # int
    st.session_state.size = None

if "mason" not in st.session_state:
    #int
    st.session_state.mason = None

if "opponent" not in st.session_state:
    # string
    st.session_state.opponent = None

if "turns" not in st.session_state:
    # int
    st.session_state.turns = None

if "turnSeconds" not in st.session_state:
    # int
    st.session_state.turnSeconds = None

if "turn_now" not in st.session_state:
    #int
    st.session_state.turn_now = None

def page1():
    st.title("GET_Matches")

    # Init ==================================================================

    if "res1" not in st.session_state:
        st.session_state.res1 = None

    if "status_code1" not in st.session_state:
        st.session_state.status_code1 = None

    if "dt_now1" not in st.session_state:
        st.session_state.dt_now1 = None

    # Get_Matches ===========================================================

    Get_Matches = st.button("Get_Matches")
    if Get_Matches:
        print("\n// Get_Matches ==================")
        st.session_state.dt_now1 = datetime.now()
        st.session_state.res1, st.session_state.status_code1 = get_matches()
        print("\n   Get_Matches ==================//")

    # Input / Output ========================================================

    st.write("Status   :", st.session_state.status_code1, st.session_state.dt_now1)
    st.write("Raw      :", st.session_state.res1)

def page2():
    st.title("Get_Matching")

    # Init ==================================================================

    if "res2" not in st.session_state:
        st.session_state.res2 = None

    if "res_fmt2" not in st.session_state:
        st.session_state.res_fmt2 = None 

    if "status_code2" not in st.session_state:
        st.session_state.status_code2 = None

    if "dt_now2" not in st.session_state:
        st.session_state.dt_now2 = None

    # Get_Matching ==========================================================

    Get_Matching = st.button("Get_Matchng")
    if Get_Matching:
        print("\n// Get_Matching ==================")
        st.session_state.dt_now2 = datetime.now()
        try:
            st.session_state.res2, st.session_state.status_code2 = get_matching(st.session_state.ID)
            st.session_state.res_fmt2 = simple_get_matching(st.session_state.res2)
            st.session_state.is_first = st.session_state.res2["first"]
            st.session_state.size = st.session_state.res2["board"]["width"]
            st.session_state.mason = st.session_state.res2["board"]["mason"]
            st.session_state.turnSeconds = st.session_state.res2["turnSeconds"]
            st.session_state.opponent = st.session_state.res2["opponent"]
            st.session_state.turns = st.session_state.res2["turns"]
        except:
            st.session_state.status_code2 = 400
            st.session_state.res2 = {
                "operation Get_Matching" : {
                    "params" : 'id', 
                    "error" : "field required"
                }
            }
            st.session_state.res_fmt2 = None

        print("\n   Get_Matching ==================//")
    # Input / Output ========================================================

    st.text_input("ID", key="ID")

    st.write("Status :", st.session_state.status_code2, st.session_state.dt_now2)
    st.markdown(f"""
                ## First : {st.session_state.is_first}
                ## Size  : {st.session_state.size}
                ## Mason : {st.session_state.mason}
                ## turnSeconds : {st.session_state.turnSeconds}
                ## Opponent : {st.session_state.opponent}
                ## Turns : {st.session_state.turns}
                """)
    # st.write("Raw :  ", st.session_state.res2)
    st.write("Simple : ", st.session_state.res2["logs"])

def page4():
    st.title("Visualizer")

    # Init ==================================================================
    if 'worker' not in st.session_state:
        st.session_state.worker = None
    worker = st.session_state.worker

    if "Autoreload_4" not in st.session_state:
        st.session_state.Autoreload_4 = False

    class Worker(threading.Thread):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.res4 = None
            self.status_code4 = None
            self.turn4 = None
            self.dt_now4 = None
            self.ID = st.session_state.ID
            self.vis_struct_mason = Image.open("./img/None.png")
            self.vis_wall_territories = Image.open("./img/None.png")
            self.should_stop = threading.Event()
            self.scoreA = -1
            self.scoreB = -1
            
        def run(self):
            while not self.should_stop.wait(0):
                time.sleep(.5)
                # print("\n// Visualizer ==================")
                self.c = False
                try:
                    self.res4, self.status_code4 = get_matching(self.ID)
                    self.c = True
                except:
                    self.status_code4 = "400 get fault"
                    self.turn4 = None
                    # self.vis_struct_mason = Image.open("./img/None.png")
                    # self.vis_wall_territories = Image.open("./img/None.png")
                if self.c:
                    cc = 0
                    while cc < 10:
                        cc += 1
                        try:
                            self.turn4 = self.res4["turn"]
                            f = open("./Field_Data/Field_Structures.txt","w")
                            f.write(str(self.res4["board"]["structures"]))
                            f.close()
                            f = open("./Field_Data/Field_Masons.txt","w")
                            f.write(str(self.res4["board"]["masons"]))
                            f.close()
                            f = open("./Field_Data/Field_Walls.txt","w")
                            f.write(str(self.res4["board"]["walls"]))
                            f.close()
                            f = open("./Field_Data/Field_Territories.txt","w")
                            f.write(str(self.res4["board"]["territories"]))
                            f.close()
                            
                            lib.convert(self.res4["first"])
                            vis.main()
                            self.scoreA, self.scoreB = lib.calculate()

                            self.vis_struct_mason = Image.open("./Field_Data/visualized_struct_masons.png")
                            self.vis_wall_territories = Image.open("./Field_Data/visualized_wall_territories.png")

                            self.dt_now4 = datetime.now()
                            break
                        except:
                            time.sleep(.1)
                            # self.status_code4 = "400 read fault"
                            # self.turn4 = None
                            # self.vis_struct_mason = Image.open("./img/None.png")
                            # self.vis_wall_territories = Image.open("./img/None.png")
                # print("\n   Visualizer ==================//")
                
    st.text_input("ID", key="ID")
    Switch_Auto_Reload = st.button("Auto Reload")
    if Switch_Auto_Reload:
        print("Auto Reload", st.session_state.Autoreload_4,"->",not st.session_state.Autoreload_4)
        st.session_state.Autoreload_4 = not st.session_state.Autoreload_4
        if st.session_state.Autoreload_4:
            worker = st.session_state.worker = Worker(daemon=True)
            worker.start()
            st.experimental_rerun()
        else:
            try:
                worker.should_stop.set()
                # 終了まで待つ
                worker.join()
                worker = st.session_state.worker = None
                st.experimental_rerun()
            except:
                None

    # st.write("Auto Reload is ", st.session_state.Autoreload_4)


    # Input / Output ========================================================


    # worker の状態を表示する部分
    if worker is None:
        st.markdown('No worker running.')
    else:
        st.markdown(f'worker: {worker.getName()}')
        placeholder1 = st.empty()
        placeholder4 = st.empty()
        placeholder5 = st.empty()
        while worker.is_alive():
            st.session_state.turn_now = worker.turn4
            placeholder4.image(worker.vis_struct_mason, caption='Struct and Masons')
            placeholder5.image(worker.vis_wall_territories, caption='Walls and Territories')
            placeholder1.markdown(f"""
                        ## Status Code : {worker.status_code4}
                        ## Received Time : {worker.dt_now4}
                        ## Turn : {st.session_state.turn_now} / {st.session_state.turns}
                        ## Score : {worker.scoreA} vs {worker.scoreB}
            """)
            time.sleep(.2)

def page7():
    # global is_accepted
    st.title("Run_Queue")
    global is_accepted
    R = st.button("Reflesh accepted")
    if R:
        is_accepted = [0 for _ in range(201)]
        print(is_accepted)

    # Init ==================================================================
    if 'runner' not in st.session_state:
        st.session_state.runner = None
    runner = st.session_state.runner

    if "Autoreload_run" not in st.session_state:
        st.session_state.Autoreload_run = False

    class Runner(threading.Thread):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.ID = st.session_state.ID
            self.posted = None
            self.status_code7 = None
            self.mason = st.session_state.mason
            self.res7 = None
            self.status_code_get = None
            self.turn_now = None
            self.is_first = None
            self.res_get = None
            self.queue = None
            self.dt_now7 = None
            self.should_stop = threading.Event()

        def run(self):
            while not self.should_stop.wait(0):
                print(datetime.now())
                time.sleep(1)
                print("\n //Auto Posting ===========================")
                f = open("./Plan/run.txt", "r")
                Actions_Arr = eval(f.read())
                f.close()
                Send_Arr = [[] for _ in range(self.mason)]
                print(Actions_Arr)
                self.queue = Actions_Arr

                for i in range(self.mason):
                    if len(Actions_Arr[i]) > 0:
                        Send_Arr[i] = id2action[Actions_Arr[i][0]]
                    else:
                        Send_Arr[i] = id2action[16]

                print(Send_Arr)
                self.res_get, self.status_code_get = get_matching(self.ID)
                self.turn_now = self.res_get["turn"]
                self.is_first = self.res_get["first"]
                if (self.turn_now + self.is_first) % 2:
                    print("POST")

                    if not is_accepted[self.turn_now]:
                        f = open("./Plan/run.txt", "w")
                        Arr_ = [[]for _ in range(self.mason)]
                        for i in range(self.mason):
                            Arr_[i] = Actions_Arr[i][1:]
                        f.write(str(Arr_))
                        f.close()
                        print("SEND!!!!!!!!!!")
                        self.posted, self.res7, self.status_code7 = post_actions(self.ID, 
                                                                                self.turn_now + 1, 
                                                                                str(Send_Arr),self.is_first)
                        if self.status_code7 == 200:
                            print("200")
                            self.dt_now7 = datetime.now()
                            is_accepted[self.turn_now] = 1

    st.markdown(f"""
                ## ID : {st.session_state.ID}
                """)

    st.text_input("ID", key = "ID")

    Switch_Auto_Pop = st.button("Switch Auto Pop")
    if Switch_Auto_Pop:
        print("Auto Pop", st.session_state.Autoreload_run,"->",not st.session_state.Autoreload_run)
        st.session_state.Autoreload_run = not st.session_state.Autoreload_run
        if st.session_state.Autoreload_run:
            runner = st.session_state.runner = Runner(daemon=True)
            runner.start()
            st.experimental_rerun()
        else:
            try:
                runner.should_stop.set()
                # 終了まで待つ
                runner.join()
                runner = st.session_state.runner = None
                st.experimental_rerun()
            except:
                None

    # st.write("Auto Pop is ", st.session_state.Autoreload_run)

    # Input / Output ========================================================

    # runner の状態を表示する部分
    if runner is None:
        st.markdown('No runner running.')
    else:
        st.markdown(f'runner: {runner.getName()}')
        placeholder7_1 = st.empty()
        # placeholder7_2 = st.empty()
        while runner.is_alive():
            placeholder7_1.markdown(f"""
                        ## Mason : {runner.mason}
                        ## Status Code : {runner.status_code7}
                        ## Accepted Time : {runner.dt_now7}
                        ## Turn : {runner.turn_now} / {st.session_state.turns}
                        ## Posted : {runner.posted}
                        ## QUEUE  : {runner.queue}
            """)
            time.sleep(.3)

id2action =  [[1,1],
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
              [3,8], 
              [0,0]]

pages = dict(
    page1="Get_Matches",
    page2="Get_Matching",
    page4="Visualizer",
    page7="Run_Queue",
)

page_id = st.sidebar.selectbox( # st.sidebar.*でサイドバーに表示する
    "Change",
    [
     "page1",
     "page2", 
     "page4", 
     "page7", 
     ],
    format_func=lambda page_id: pages[page_id], # 描画する項目を日本語に変換
)

if page_id == "page1":
    page1()

if page_id == "page2":
    page2()

if page_id == "page4":
    page4()

if page_id == "page7":
    page7()
