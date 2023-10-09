import numpy as np 
import random
import copy

DIR4=((0,-1),(1,0),(0,1),(-1,0))
DIR8=((-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0))

''''
<行動id>
0:移動(左上)
1:移動(上)
2:移動(右上)
3:移動(右)
4:移動(右下)
5:移動(下)
6:移動(左下)
7:移動(左)
8:建築(上)
9:建築(右)
10:建築(下)
11:建築(左)
12:解体(上)
13:解体(右)
14:解体(下)
15:解体(左)
16:滞在
'''

class State:
    def __init__(self,width,height,ike=[],shiro=[],first_shokunin=[],second_shokunin=[],end_turn=200,coef=(10,30,100),reverse=False) -> None:
        #フィールドサイズ
        self.WIDTH=width    #11-25
        self.HEIGHT=height  #11-25
        
        #池、城の座標
        self.IKE=frozenset(ike)
        self.SHIRO=frozenset(shiro)
        
        #ターン
        self.turn=1
        self.END_TURN=end_turn
        self.now_team=1

        #以下 False(0):1st True(1):2nd
        
        #職人の座標
        self.REVERSE=reverse
        self.shokunin=[list(first_shokunin),list(second_shokunin)]
        if reverse:
            self.shokunin.reverse()
            
        #城壁の座標
        self.joheki=[set(),set()]
        self.zinchi=[set(),set()]

        #陣地の座標
        self.closed_zinchi=[set(),set()]
        self.opened_zinchi=[set(),set()]
        
        self.visited=set()

        #各ポイント係数
        self.JOHEKI_COEF=coef[0]
        self.ZINCHI_COEF=coef[1]
        self.SHIRO_COEF=coef[2]
        
        #フィールドの外周の座標 find_zinchi()に使用
        self.OUTSIDE=set()
        for i in range(width):
            for j in range(height):
                if i==0 or i==width-1 or j==0 or j==height-1:
                    self.OUTSIDE.add((i,j))
        self.OUTSIDE=frozenset(self.OUTSIDE)
     
    def __str__(self):
        count=self.count()
        score=self.score()
        
        shokunin_board=[]
        joheki_board=[]
        zinchi_board=[]
        
        for y in range(self.HEIGHT):
            tmp1=[]
            tmp2=[]
            tmp3=[]
            for x in range(self.WIDTH):
                if (x,y) in self.IKE:
                    tmp1.append("p")
                elif (x,y) in self.shokunin[False]:
                    tmp1.append("o")
                elif (x,y) in self.shokunin[True]:
                    tmp1.append("x")
                elif (x,y) in self.SHIRO:
                    tmp1.append("c")
                else:
                    tmp1.append("-")
                    
                if (x,y) in self.SHIRO:
                    tmp2.append("c")
                elif (x,y) in self.joheki[False]:
                    tmp2.append("o")
                elif (x,y) in self.joheki[True]:
                    tmp2.append("x")
                elif (x,y) in self.IKE:
                    tmp2.append("p")
                else:
                    tmp2.append("-")
                
                if (x,y) in self.zinchi[False] and (x,y) in self.zinchi[True]:
                    tmp3.append("b")
                elif (x,y) in self.zinchi[False]:
                    tmp3.append("o")
                elif (x,y) in self.zinchi[True]:
                    tmp3.append("x")
                else:
                    tmp3.append("-")
                    
            shokunin_board.append(tmp1)
            joheki_board.append(tmp2)
            zinchi_board.append(tmp3)
                
        SCORE_WIDTH = 13
        def text_format(just,width,sep,fill,*args):
            #just...c or l or r
            if just=='left':
                text=[i.ljust(width,fill) for i in args]
            elif just=='right':
                text=[i.rjust(width,fill) for i in args]
            elif just=='center':
                text=[i.center(width,fill) for i in args]
            else:
                text=args
            return sep.join(text)
        
        head1=" "*(3 if self.HEIGHT>10 else 2) + " ".join([str(i//10) for i in range(self.WIDTH)])
        head2=" "*(3 if self.HEIGHT>10 else 2) + " ".join([str(i%10) for i in range(self.WIDTH)])
        side_head=2 if self.HEIGHT>10 else 1
        
        text=text_format(None,None,"\n",None,
            "turn{}".format(self.turn).ljust(9+6*self.WIDTH,"-"),
            "shokunin_CIE".ljust(60,"-"),
            "1st:{}".format(",".join(f"({i[0]},{i[1]})" for i in self.shokunin[False])),
            "2nd:{}".format(",".join(f"({i[0]},{i[1]})" for i in self.shokunin[True])),
            "score".ljust(60,"-"),
            "    "+text_format('center',SCORE_WIDTH,"/"," ",f"joheki(x{self.JOHEKI_COEF})",f"zinchi(x{self.ZINCHI_COEF})",f"shiro(x{self.SHIRO_COEF})","total","evaluate"),
            "1st:"+text_format('center',SCORE_WIDTH,"/"," ",f"{count[False][0]}({score[False][0]})",
                               f"{count[False][1]}({score[False][1]})",f"{count[False][2]}({score[False][2]})",f"{sum(score[False])}",f"{self.evaluate(False):+}"),
            "2nd:"+text_format('center',SCORE_WIDTH,"/"," ",f"{count[True][0]}({score[True][0]})",
                               f"{count[True][1]}({score[True][1]})",f"{count[True][2]}({score[True][2]})",f"{sum(score[True])}",f"{self.evaluate(True):+}"),
            text_format('left',1+2*self.WIDTH+int(self.HEIGHT>10)," "*3,"-","shokunin","joheki","zinchi"),
            text_format(None,None," "*3,None,head1,head1,head1) if self.WIDTH>10 else "",
            text_format(None,None," "*3,None,head2,head2,head2),
            "\n".join([text_format(None,None," "*3,None,
                                   "{} {}".format(str(i).zfill(side_head)," ".join(shokunin_board[i])),
                                   "{} {}".format(str(i).zfill(side_head)," ".join(joheki_board[i])),
                                   "{} {}".format(str(i).zfill(side_head)," ".join(zinchi_board[i]))) for i in range(self.HEIGHT)]),    
            "")
        return text

    def load_field(self,shokunin=None,joheki=None,zinchi=None):
        if shokunin is not None:
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if p:=shokunin[y][x]>0:
                        self.shokunin[False][p-1]=(x,y)
                    elif p:=shokunin[y][x]<0:
                        self.shokunin[True][p-1]=(x,y)
        if joheki is not None:
            for team in (False,True):
                self.joheki[team].clear()
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if shokunin[y][x]==1:
                        self.joheki[False].add((x,y))
                    elif shokunin[y][x]==-1:
                        self.joheki[True].add((x,y))
        if zinchi is not None:
            for team in (False,True):
                self.zinchi[team].clear()
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if shokunin[y][x]==1:
                        self.zinchi[False].add((x,y))
                    elif shokunin[y][x]==-1:
                        self.zinchi[True].add((x,y))
    
    def copy_field(self,state):
        self.shokunin=copy.deepcopy(state.shokunin)
        self.joheki=copy.deepcopy(state.joheki)
        self.zinchi=copy.deepcopy(state.zinchi)
        self.opened_zinchi=copy.deepcopy(state.opened_zinchi)
        self.closed_zinchi=copy.deepcopy(state.closed_zinchi)
            
    #座標がフィールド上に存在するか判定
    def is_inside(self,cie):
        x,y=cie
        return 0<=x<=self.WIDTH-1 and 0<=y<=self.HEIGHT-1

    #入力座標の(上,左,右,下)の座標を返す
    def to_4cie(self,center):
        x,y=center
        result=[(x+dx,y+dy) for dx,dy in DIR4]
        return result
    
    #入力座標の(左上,上,右上,左,右,左下,下,右下)の座標を返す
    def to_8cie(self,center):
        x,y=center
        result=[(x+dx,y+dy) for dx,dy in DIR8]
        return result
    
    #入力した職人の移動可能な範囲を返す(移動先の重複は判定されない)
    def legal_move(self,team,number,target=None):
        cie=self.to_8cie(self.shokunin[team][number])
        
        #行動条件:(1)周囲8方向であること　かつ(2)池,(3)相手チームの城壁,(4)(5)両チームの職人へは移動不可
        cond=self.IKE | self.joheki[not team] | set(self.shokunin[False]) | set(self.shokunin[True])
        if target is None:
            result=[]
            for n,xy in enumerate(cie):
                if self.is_inside(xy) and not xy in cond:
                    result.append(n)
            return result
        else:
            return cie[target] if self.is_inside(cie[target]) and not cie[target] in cond else False
    
    #入力した職人の建築可能な範囲を返す    
    def legal_build(self,team,number,target=None):
        cie=self.to_4cie(self.shokunin[team][number])
        
        #行動条件:(1)周囲4方向であること　かつ(2)城,(3)相手チームの城壁,(4)相手チームの職人へは建築不可
        cond=self.SHIRO | self.joheki[not team] | set(self.shokunin[not team])
        if target is None:
            result=[]
            for n,xy in enumerate(cie):
                if self.is_inside(xy) and not xy in cond:
                    result.append(n)
            return result
        else:
            return cie[target] if self.is_inside(cie[target]) and not cie[target] in cond else False
    
    #入力した職人の解体可能な範囲を返す
    def legal_destory(self,team,number,target=None):
        cie=self.to_4cie(self.shokunin[team][number])
        
        #行動条件:(1)周囲4方向であること　かつ(2)どちらかのチームの城壁がある場合のみ破壊可
        cond=self.joheki[False] | self.joheki[True]
        if target is None:
            result=[]
            for n,xy in enumerate(cie):
                if self.is_inside(xy) and xy in cond:
                    result.append(n)
            return result
        else:
            return cie[target] if self.is_inside(cie[target]) and cie[target] in cond else False
        
    #行動をとる(行動失敗の場合は滞在) 行動成功/失敗の結果をリストで出力
    def action(self,actions,team=None):
        if team is None:
            team=self.now_team==2
        result=[False for _ in range(len(actions))]
        dupulications=set()
        move_point=set()
        move=[]
        
        for number,action in enumerate(actions):
            if 0<=action<8:
                if xy:=self.legal_move(team,number,action):
                    move.append((number,xy))
                    if xy in move_point:
                        dupulications.add(xy)
                    else:
                        move_point.add(xy) 
            elif 8<=action<12:
                if xy:=self.legal_build(team,number,action-8):
                    result[number]=True
                    self.joheki[team].add(xy)
            elif 12<=action<16:
                if xy:=self.legal_destory(team,number,action-12):
                    result[number]=True
                    self.joheki[False].discard(xy)
                    self.joheki[True].discard(xy) 
            else:
                result[number]=True
        
        #移動先の重複への対応     
        for number,xy in move:
            if not xy in dupulications:
                result[number]=True
                self.shokunin[team][number]=xy

        return result

    #四方に隣接,連結した城壁を探索(深さ優先探索)
    def dfs4(self,team,x,y):
        if 0<=x<=self.WIDTH and 0<=y<=self.HEIGHT and not (x,y) in (self.visited | self.joheki[team]):
            self.visited.add((x,y))
            connect={(x,y)}
            for dx,dy in DIR4:
                connect.update(self.dfs4(team,x+dx,y+dy))
            return connect
        else:
            return set()
    
    #八方に隣接した城壁を探索
    def dfs8(self,team,x,y):
        if 0<=x<=self.WIDTH and 0<=y<=self.HEIGHT and (x,y) in self.joheki[team] and not (x,y) in self.visited:
            self.visited.add((x,y))
            connect={(x,y)}
            for dx,dy in DIR8:
                connect.update(self.dfs8(team,x+dx,y+dy))
            return connect
        else:
            return set()
    
    #陣地の探索
    def find_zinchi(self):
        closed_zinchi_tmp=[set(),set()]
        #dfsによる囲み探索→closed_zinchi_tmpに格納
        for team in (False,True):
            for i in range(self.WIDTH):
                for j in range(self.HEIGHT):
                    dfs_tmp=self.dfs4(team,i,j)
                    if dfs_tmp.isdisjoint(self.OUTSIDE):
                        closed_zinchi_tmp[team].update(dfs_tmp)
            self.visited.clear()
        #前ターンのclosed_zinchiとclosed_zinchi_tmpさらにjoheki[自チーム]を比較しopened_zinchiに格納
        #closed_zinchiにclosed_zinchi_tmpを代入
        #opened_zinchiからjoheki[相手チーム],closed_zinchi_tmp[相手チーム]を引く
        for team in (False,True):
            self.opened_zinchi[team].update(self.closed_zinchi[team] - closed_zinchi_tmp[team])
            self.opened_zinchi[team].difference_update(self.joheki[team] | self.joheki[not team] | closed_zinchi_tmp[not team])
            self.closed_zinchi[team]=closed_zinchi_tmp[team]
            self.zinchi[team]=self.opened_zinchi[team] | self.closed_zinchi[team]
    
    #城郭の連結成分
    def find_connected_joheki(self):
        connected_joheki=[list(),list()]
        for team in (False,True):
            for x in range(self.WIDTH):
                for y in range(self.HEIGHT):
                    connected_joheki[team].append(len(self.dfs8(team,x,y)))
            self.visited.clear()
        return connected_joheki

    #両チームの城壁,陣地,城の数を返す
    def count(self):
        first_cnt=[len(self.joheki[False]),len(self.zinchi[False]),0]
        second_cnt=[len(self.joheki[True]),len(self.zinchi[True]),0]
        for i in self.SHIRO:
            if i in self.zinchi[False]:
                first_cnt[2]+=1
            if i in self.zinchi[True]:
                second_cnt[2]+=1    
        return [first_cnt,second_cnt]
    
    #両チームの各ポイント
    def score(self):
        count=self.count()
        coef=[self.JOHEKI_COEF,self.ZINCHI_COEF,self.SHIRO_COEF]
        for i in (False,True):
            for j in range(3):
                count[i][j]*=coef[j]
        return count
    
    def update_turn(self):
        self.turn+=1
        self.now_team=1 if self.now_team==2 else 2

    #現在ターンの手番(1 or 2)を取得
    def player(self):
        return 2 if self.turn%2==0 else 1
    
    #現在ポイントの多い方を返す(1 or 2 or 0(drow))
    def winner(self):
        score=self.score()
        first,second=[sum(i) for i in score]
        if first>second:
            return 1
        elif first<second:
            return 2
        else:
            return 0
        
    #ゲーム終了か判定
    def is_end(self):
        return self.turn>=self.END_TURN
    
    #合法手の取得
    def legal_action(self,team=None,number=None):
        def list_add(li,n):
            return [i+n for i in li]
        
        if team is None:
            team=self.now_team==2
            
        if number is None:
            result=[0 for _ in range(len(self.shokunin[team]))]
            for i in range(len(self.shokunin[team])):
                result[i]=self.legal_move(team,i)+list_add(self.legal_build(team,i),8)+list_add(self.legal_destory(team,i),12)
        else:
            result=self.legal_move(team,number)+list_add(self.legal_build(team,number),8)+list_add(self.legal_destory(team,number),12)
        return result
    
    #評価関数
    def evaluate(self,team=None):
        if team is None:
            team=self.now_team==2
        result=0
        score=self.score()
        result+=sum(score[team])-sum(score[not team])
        connested_joheki=self.find_connected_joheki()
        result+=sum([i**2 for i in connested_joheki[team]])-sum([i**2 for i in connested_joheki[not team]])
        return result
    
    #状態の出力(本人,両城壁のみの出力)
    def state(self,team=None):
        if team is None:
            team=self.now_team==2
        result=np.zeros((self.HEIGHT,self.WIDTH,1),dtype=np.float32)
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if (x,y) in self.shokunin[team]:
                    result[y][x][0]=1
                elif (x,y) in self.joheki[team]:
                    result[y][x][0]=2
                elif (x,y) in self.joheki[not team]:
                    result[y][x][0]=3
        return result
    
    def play(self,actions,team=None):
        if team is None:
            team=self.now_team==2
        result=self.action(actions,team)
        if all([0<=i<8 for i in actions]):
            self.find_zinchi()
        self.update_turn()
        return result

#width,height内に収まるランダムな座標タプルを生成
def random_cie(width,height,args): 
    cie=set()
    cnt=0
    while True:
        cie.add((random.randint(0,width-1),random.randint(0,height-1)))
        cnt+-1
        if len(cie)==sum(args):
            break
        if cnt>10**4:
            raise ValueError("値が大きすぎます")
    cie=list(cie)
    result=[]
    cnt=0
    for i in args:
        result.append(cie[cnt:cnt+i])
        cnt+=i
    return result

#ランダムな盤の状態を生成できる
def generate_random_board(width=25,height=25,turn=50,ike=15,shiro=15,shokunin=6,joheki=60):
    shokunin=random_cie(width,height,[shokunin]*2+[ike])
    joheki=random_cie(width,height,[joheki]*2+[shiro])
    result=State(width,height,ike=shokunin[2],first_shokunin=shokunin[0],second_shokunin=shokunin[1],shiro=joheki[2])
    # result.initialize_field(shokunin=shokunin[:2],joheki=joheki[:2])
    result.find_zinchi()
    return result


def main():
    state=State(10,10,first_shokunin=((0,0),(2,3),(3,4)))
    print(state)
    print(state.legal_action())
    print(state.action((7,8,9)))
    print(state)
if __name__ == "__main__":
    main()
    
    
# #ランダム同士で対戦させる
# def playout(id,turn=200,coef=(10,30,100)):
#     state=generate_board(id,turn,coef)
#     cnt=0
#     legal_cnt=[]
#     while True:
#         if state.is_done():
#             break
#         for i in state.legal_action():
#             legal_cnt.append(len(i))
#         print(action:=random_action(state))
#         print(history:=state.next(action))
#         cnt+=history.count(False)
#         print(state)
#     print(f"False_cnt:{cnt}")
#     print(f"LegalAction_ave:{np.average(np.array(legal_cnt))}")

            
# #ランダム対戦
# def main1():
#     from time import time
#     start=time()
#     playout('A15',turn=50)
#     print(f"time:{time()-start}")

# #state_for_modelメソッドの出力
# def main2():
#     print(x:=generate_random_board(width=5,height=5,joheki=5))
#     print(x.state_for_model(False,1))

# #legal_actionメソッドの出力
# def main3():
#     print(x:=generate_board('A13',turn=200))
#     print(x.legal_action_for_model(False))
#     print(x.legal_action(False))

# def main4():
#     state=generate_board('A11')
#     print(state)
#     for _ in range(50):
#         state.next(random_action(state))
#     print(state)
#     state.reset()
#     print(state)
    
# if __name__ == '__main__':
#     main4()


# Stateクラスの説明
# インスタンス生成:State(width,height,end_turn,ike=[],shiro=[],first_shokunin=[],second_shokunin=[],joheki_coef=10,zinchi_coef=30,shiro_coef=100)
#     ike,shiro,firt_shokunin,second_shokuninは座標を示したタプル(x,y)をリストなどで渡す(例)ike=[(2,3),(4,5)]
#     各ポイント係数についてはデフォルトが(10,30,100)である

# 以下,teamは先攻をFalse,後攻をTrueとする
# team=Noneの引数があるメソッドはteamを入力しない場合、手番のチームとなる

# 各メソッド
# initialize(self,ike=None,shiro=None,shokunin=None,joheki=None,closed_zinchi=None,opened_zinchi=None)
#     池,城,各職人,各城壁,各開/閉の陣地を変えることができる
#     城壁の設定後、陣地の探索は行われないため必要な場合はfind_zinchi()で個別に行う
# count()
#     両チームの城壁,陣地,城の数を返す
#     出力は[[1st_joheki,1st_zinchi,1st_shiro],[2nd_joheki,2nd_zinchi,2nd_shiro]]
# score()
#     両チームの城壁,陣地,城の数に各ポイント係数をかけた得点を返す
#     出力は[[1st_joheki,1st_zinchi,1st_shiro],[2nd_joheki,2nd_zinchi,2nd_shiro]]
# next(actions,team=None)
#     職人の行動を入力すると盤の状態を変化させる
#     具体的な処理は
#         行動が合法手かを判定し合法手であったもののみ行動をとる
#         陣地の更新
#         ターン数のインクリメント
#         行動が成功したかをTrue/Falseの配列で返す
#     teamはターン数に応じて自動的に決められるが、指定することも可能である
#     actionの形式は行動idの配列で渡す(例):[1,1,2,5,16,0]
#         行動id
#          1:滞在
#          2:左上へ移動
#          3:上に移動
#          4:右上に移動
#          5:左に移動
#         :
#         :
#          7:右下に移動
#          8:上に建築
#         9:左に建築
#         10:右に建築
#         11:下に建築
#         12:上に解体
#         :
#         15:下に解体
#         16:滞在
             
# *is_done()
#     ゲームが終了したか判定
    
# legal_action(team=None,number=None)
#     合法手の取得
#     出力は各職人の合法な行動idのリストのリスト(二次元リスト)
#     (例)[[0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
#     numberを指定することで指定した職人のみのリストを取得できる
# legal_action_for_model(team=None,number=None)
#     合法手をnumpy配列を用いた形式で返す(学習モデル向け)
#     滞在は含まれていないことに注意
# evaluate(team=None)
#     評価関数の値を返す
# state()
#     盤の状態を返す
#     出力はshokunin,joheki,closed_zinchi,opened_zinchi
# state_for_model(team,shokunin)
#     盤の情報をnumpy配列を用いた形式で返す(学習モデル向け)

# 関数の説明
# generate_board(id,turn=200,coef=(10,30,100))
#     本番で用いられる18種類の競技フィールドから選んで生成
#     idはA11,A13...A25,B11...C25まである
#     ターン,ポイント係数についても指定可
# random_cie(width,height,args)
#     width,height内に収まるランダムな座標タプルを生成
#     座標は重複しないようになっている
#     argsで生成したい座標の数を指定することができる(例):(1,)->[(x,y)]    (1,2)->[[(x,y)],[(x,y),(x,y)]]
# generate_random_board(width=15,height=15,turn=50,ike=3,shiro=3,shokunin=3,joheki=60)
#     ランダムな盤の状態を生成できる
#     各オブジェクト(池,職人...)の数を指定することである程度調整可
# random_action(state,stay=False)
#     引数にStateオブジェクトを渡すことで合法手の中からランダムに行動を返す
#     出力した値はState.next()に直接渡せる