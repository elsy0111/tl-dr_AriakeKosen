import numpy as np 
import random

class State:
    def __init__(self,width,height,end_turn,ike=[],shiro=[],first_shokunin=[],second_shokunin=[],coef=(10,30,100)) -> None:
        
        self.save=first_shokunin,second_shokunin
        
        #フィールドサイズ
        self.WIDTH=width    #11-25
        self.HEIGHT=height  #11-25
        
        #池、城の座標
        self.IKE=frozenset(ike)
        self.SHIRO=frozenset(shiro)
        
        #ターン
        self.turn=1
        self.END_TURN=end_turn

        #以下 False(0):1st True(1):2nd
        
        #職人の座標
        self.shokunin=[list(first_shokunin),list(second_shokunin)]
        
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
    
    def reset(self):
        self.__init__(self.WIDTH,self.HEIGHT,self.END_TURN,self.IKE,self.SHIRO,self.save[False],self.save[True],coef=(self.JOHEKI_COEF,self.ZINCHI_COEF,self.SHIRO_COEF))
     
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
            "    "+text_format('center',SCORE_WIDTH,"/"," ",f"joheki(x{self.JOHEKI_COEF})",f"zinchi(x{self.ZINCHI_COEF})",f"shiro(x{self.SHIRO_COEF})","total"),
            "1st:"+text_format('center',SCORE_WIDTH,"/"," ",f"{count[False][0]}({score[False][0]})",
                               f"{count[False][1]}({score[False][1]})",f"{count[False][2]}({score[False][2]})",f"{sum(score[False])}"),
            "2nd:"+text_format('center',SCORE_WIDTH,"/"," ",f"{count[True][0]}({score[True][0]})",
                               f"{count[True][1]}({score[True][1]})",f"{count[True][2]}({score[True][2]})",f"{sum(score[True])}"),
            text_format('left',1+2*self.WIDTH+int(self.HEIGHT>10)," "*3,"-","shokunin","joheki","zinchi"),
            text_format(None,None," "*3,None,head1,head1,head1) if self.WIDTH>10 else "",
            text_format(None,None," "*3,None,head2,head2,head2),
            "\n".join([text_format(None,None," "*3,None,
                                   "{} {}".format(str(i).zfill(side_head)," ".join(shokunin_board[i])),
                                   "{} {}".format(str(i).zfill(side_head)," ".join(joheki_board[i])),
                                   "{} {}".format(str(i).zfill(side_head)," ".join(zinchi_board[i]))) for i in range(self.HEIGHT)]),    
            "")
        return text
    
        #池,城,職人,城壁,陣地の初期化
    def initialize_field(self,ike=None,shiro=None,shokunin=None,joheki=None,closed_zinchi=None,opened_zinchi=None):
        if ike is not None:
            self.IKE=frozenset(ike)
        if shiro is not None:
            self.SHIRO=frozenset(shiro)
            
        if shokunin is not None:
            self.shokunin=[list(i) for i in shokunin]            
        if joheki is not None:
            self.joheki=[set(i) for i in joheki]
            
        if closed_zinchi is not None:
            self.closed_zinchi=[set(i) for i in closed_zinchi]
        if opened_zinchi is not None:
            self.opened_zinchi=[set(i) for i in opened_zinchi]
        if closed_zinchi or opened_zinchi:
            self.zinchi=[closed_zinchi[i] | opened_zinchi[i] for i in range(2)]

    #座標がフィールド上に存在するか判定
    def is_inside(self,cie):
        x,y=cie
        return 0<=x<=self.WIDTH-1 and 0<=y<=self.HEIGHT-1

    #入力座標の(上,左,右,下)の座標を返す
    def to_4cie(self,center):
        x,y=center
        cie=((x,y-1),(x-1,y),(x+1,y),(x,y+1))
        return cie
    
    #入力座標の(左上,上,右上,左,右,左下,下,右下)の座標を返す
    def to_8cie(self,center):
        x,y=center
        cie=((x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1))
        return cie
    
    #入力した職人の移動可能な範囲を返す(移動先の重複は判定されない)
    def legal_move(self,team,number,target=None):
        cie=self.to_8cie(self.shokunin[team][number])
        
        #! 行動条件:(1)周囲8方向　Not (2)池,(3)相手チームの城壁,(4)(5)両チームの職人へは移動不可(6)盤内
        cond=self.IKE | self.joheki[not team] | set(self.shokunin[False]) | set(self.shokunin[True])
        if target is None:
            able=[]
            for n,xy in enumerate(cie):
                if self.is_inside(xy) and not xy in cond:
                    able.append(n)
            return able
        else:
            return cie[target] if self.is_inside(cie[target]) and not cie[target] in cond else False
    
    #入力した職人の建築可能な範囲を返す    
    def legal_build(self,team,number,target=None):
        cie=self.to_4cie(self.shokunin[team][number])
        
        #! 行動条件:(1)周囲4方向　Not (2)城,(3)相手チームの城壁,(4)相手チームの職人へは建築不可 (5)盤内
        cond=self.SHIRO | self.joheki[not team] | set(self.shokunin[not team])
        if target is None:
            able=[]
            for n,xy in enumerate(cie):
                if self.is_inside(xy) and not xy in cond:
                    able.append(n)
            return able
        else:
            return cie[target] if self.is_inside(cie[target]) and not cie[target] in cond else False
    
    #入力した職人の解体可能な範囲を返す
    def legal_destory(self,team,number,target=None):
        cie=self.to_4cie(self.shokunin[team][number])
        
        #! 行動条件:(1)周囲4方向であること　かつ(2)どちらかのチームの城壁がある場合のみ破壊可 (3)盤内
        cond=self.joheki[False] | self.joheki[True]
        able=[]
        if target is None:
            able=[]
            for n,xy in enumerate(cie):
                if self.is_inside(xy) and xy in cond:
                    able.append(n)
            return able
        else:
            return cie if self.is_inside(cie[target]) and cie[target] in cond else False
    
    #行動をとる(行動失敗の場合は滞在) 行動成功/失敗の結果をリストで出力
    def action(self,actions,team):
        result=[False for _ in range(len(actions))]
        dupulications=set()
        move_point=set()
        move=[]
        
        for number,action in enumerate(actions):
            motion,target=action
            match motion:
                case 0: #滞在
                    result[number]=True
                case 1 if xy:=self.legal_move(team,number,target):   #移動  
                    move.append((number,xy))
                    if xy in move_point:
                        dupulications.add(xy)
                    else:
                        move_point.add(xy)      
                case 2 if xy:=self.legal_build(team,number,target):  #建築
                    result[number]=True
                    self.joheki[team].add(xy)
                case 3 if xy:=self.legal_destory(team,number,target):    #解体
                    result[number]=True
                    self.joheki[False].discard(xy)
                    self.joheki[True].discard(xy)
        
        #移動先の重複への対応     
        for number,xy in move:
            if not xy in dupulications:
                result[number]=True
                self.shokunin[team][number]=xy

        return result

    #四方に隣接,連結した城壁を探索(深さ優先探索)
    def dfs_4(self,team,x,y):
        if 0<=x<=self.WIDTH and 0<=y<=self.HEIGHT and not (x,y) in (self.visited | self.joheki[team]):
            self.visited.add((x,y))
            connect={(x,y)}
            #右下左上の順(4つ)
            connect.update(self.dfs_4(team,x+1,y))
            connect.update(self.dfs_4(team,x,y+1))
            connect.update(self.dfs_4(team,x-1,y))
            connect.update(self.dfs_4(team,x,y-1))
            return connect
        else:
            return set()
    
    def dfs_8(self,team,x,y):
        if 0<=x<=self.WIDTH and 0<=y<=self.HEIGHT and (x,y) in self.joheki[team] and not (x,y) in self.visited:
            self.visited.add((x,y))
            connect={(x,y)}
            #左上～右下の順(8つ)
            connect.update(self.dfs_8(team,x-1,y-1))
            connect.update(self.dfs_8(team,x,y-1))
            connect.update(self.dfs_8(team,x+1,y-1))
            connect.update(self.dfs_8(team,x-1,y))
            connect.update(self.dfs_8(team,x+1,y))
            connect.update(self.dfs_8(team,x-1,y+1))
            connect.update(self.dfs_8(team,x,y+1))
            connect.update(self.dfs_8(team,x+1,y+1))
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
                    dfs_tmp=self.dfs_4(team,i,j)
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
    
    def find_connected_joheki(self):
        connected_joheki=[list(),list()]
        for team in (False,True):
            for x in range(self.WIDTH):
                for y in range(self.HEIGHT):
                    connected_joheki[team].append(len(self.dfs_8(team,x,y)))
            self.visited.clear()
        return connected_joheki
    
    #############################################################################################################################
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
    
    #行動
    def next(self,actions,team=None):
        if team is None:
            team=self.turn%2==0
        reshaped_actions=[]
        flg=False
        for i in actions:
            if i<1:
                reshaped_actions.append((0,int(i)))
            elif i<9:
                reshaped_actions.append((1,int(i-1)))
            elif i<13:
                reshaped_actions.append((2,int(i-9)))
                flg=True
            elif i<17:
                reshaped_actions.append((3,int(i-13)))
                flg=True
        result=self.action(reshaped_actions,team=team)
        #移動のみの場合陣地の更新を行わない(高速化)
        if flg:
            self.find_zinchi()
                   
        self.turn+=1
        return result
        
    #現在のスコアに応じて1(win),0(drow),-1(lose)のどれかを返す
    def point(self,team=None):
        if team is None:
            team=self.turn%2==0
        score=self.score()
        own=sum(score[team])
        enemy=sum(score[not team])
        return 1 if own>enemy else 0 if own==enemy else -1
    
    #負けか判定
    def is_lose(self,team=None):
        if team is None:
            team=self.turn%2==0
        score=self.score()
        return sum(score[team])<sum(score[not team])
    
    #ゲーム終了か判定
    def is_done(self):
        return self.turn>=self.END_TURN
    
    #現在が先攻のターンか判定
    def is_first_player(self):
        return self.turn%2==1
    
    #合法手の取得
    def legal_actions(self,team=None,number=None):
        def list_add(li,n):
            return [i+n for i in li]
        if team is None:
            team=self.turn%2==0
        if number is None:
            result=[0 for _ in range(len(self.shokunin[team]))]
            for i in range(len(self.shokunin[team])):
                result[i]=[0]+list_add(self.legal_move(team,i),1)+list_add(self.legal_build(team,i),9)+list_add(self.legal_destory(team,i),13)
        else:
            result=[0]+list_add(self.legal_move(team,number),1)+list_add(self.legal_build(team,number),9)+list_add(self.legal_destory(team,number),13)
        return result

    #現在の盤の状態を返す
    def state(self):
        return self.shokunin,self.joheki,self.closed_zinchi,self.opened_zinchi
        
#本番で用いられる18種類の競技フィールドをから選んで生成  
def generate_board(id,turn=200,coef=(10,30,100)):
    """'A11','A13','A15','A17','A21','A25','B11','B13','B15','B17','B21','B25','C11','C13','C15','C17','C21','C25'"""
    if id == 'random':
        id=random.choice(('A11','A13','A15','A17','A21','A25','B11','B13','B15','B17','B21','B25','C11','C13','C15','C17','C21','C25'))
    if id == 'A11':
        width=11
        height=11
        ike=[(5, 0), (4, 1), (6, 1), (4, 2), (6, 2), (3, 3), (7, 3), (1, 4), (2, 4), (8, 4), (9, 4), (0, 5), (10, 5), (1, 6), (2, 6), (8, 6), (9, 6), (3, 7), (7, 7), (4, 8), (6, 8), (4, 9), (6, 9), (5, 10)]
        shiro=[(2, 2), (8, 2), (4, 4), (6, 4), (5, 5), (4, 6), (6, 6), (2, 8), (8, 8)]
        first_shokunin=[(1, 1), (9, 1), (1, 9), (9, 9)]
        second_shokunin=[(5, 2), (2, 5), (8, 5), (5, 8)]

    elif id == 'A13':
        width=13
        height=13
        ike=[(6, 0), (1, 1), (5, 1), (7, 1), (11, 1), (5, 2), (7, 2), (5, 3), (7, 3), (4, 4), (8, 4), (1, 5), (2, 5), (3, 5), (9, 5), (10, 5), (11, 5), (0, 6), (12, 6), (1, 7), (2, 7), (3, 7), (9, 7), (10, 7), (11, 7), (4, 8), (8, 8), (5, 9), (7, 9), (5, 10), (7, 10), (1, 11), (5, 11), (7, 11), (11, 11), (6, 12)]
        shiro=[(3, 3), (9, 3), (5, 5), (7, 5), (6, 6), (5, 7), (7, 7), (3, 9), (9, 9)]
        first_shokunin=[(2, 2), (10, 2), (2, 10), (10, 10)]
        second_shokunin=[(6, 3), (3, 6), (9, 6), (6, 9)]

    elif id == 'A15':
        width=15
        height=15
        ike=[(6, 0), (8, 0), (5, 1), (9, 1), (2, 2), (5, 2), (9, 2), (12, 2), (5, 3), (7, 3), (9, 3), (4, 4), (10, 4), (1, 5), (2, 5), (3, 5), (11, 5), (12, 5), (13, 5), (0, 6), (14, 6), (3, 7), (11, 7), (0, 8), (14, 8), (1, 9), (2, 9), (3, 9), (11, 9), (12, 9), (13, 9), (4, 10), (10, 10), (5, 11), (7, 11), (9, 11), (2, 12), (5, 12), (9, 12), (12, 12), (5, 13), (9, 13), (6, 14), (8, 14)]
        shiro=[(7, 1), (3, 2), (11, 2), (2, 3), (12, 3), (6, 6), (8, 6), (1, 7), (7, 7), (13, 7), (6, 8), (8, 8), (2, 11), (12, 11), (3, 12), (11, 12), (7, 13)]
        first_shokunin=[(1, 1), (13, 1), (1, 13), (13, 13)]
        second_shokunin=[(7, 5), (5, 7), (9, 7), (7, 9)]

    elif id == 'A17':
        width=17
        height=17
        ike=[(6, 0), (10, 0), (5, 1), (11, 1), (2, 2), (5, 2), (11, 2), (14, 2), (5, 3), (7, 3), (8, 3), (9, 3), (11, 3), (4, 4), (12, 4), (1, 5), (2, 5), (3, 5), (13, 5), (14, 5), (15, 5), (0, 6), (16, 6), (3, 7), (13, 7), (3, 8), (13, 8), (3, 9), (13, 9), (0, 10), (16, 10), (1, 11), (2, 11), (3, 11), (13, 11), (14, 11), (15, 11), (4, 12), (12, 12), (5, 13), (7, 13), (8, 13), (9, 13), (11, 13), (2, 14), (5, 14), (11, 14), (14, 14), (5, 15), (11, 15), (6, 16), (10, 16)]
        shiro=[(7, 1), (9, 1), (3, 2), (13, 2), (2, 3), (14, 3), (6, 6), (10, 6), (1, 7), (7, 7), (9, 7), (15, 7), (8, 8), (1, 9), (7, 9), (9, 9), (15, 9), (6, 10), (10, 10), (2, 13), (14, 13), (3, 14), (13, 14), (7, 15), (9, 15)]
        first_shokunin=[(1, 1), (15, 1), (1, 15), (15, 15)]
        second_shokunin=[(8, 5), (5, 8), (11, 8), (8, 11)]

    elif id == 'A21':
        width=21
        height=21
        ike=[(10, 0), (7, 1), (8, 1), (9, 1), (11, 1), (12, 1), (13, 1), (7, 2), (13, 2), (6, 3), (14, 3), (4, 4), (6, 4), (14, 4), (16, 4), (6, 5), (14, 5), (3, 6), (4, 6), (5, 6), (8, 6), (12, 6), (15, 6), (16, 6), (17, 6), (1, 7), (2, 7), (9, 7), (10, 7), (11, 7), (18, 7), (19, 7), (1, 8), (6, 8), (14, 8), (19, 8), (1, 9), (19, 9), (0, 10), (4, 10), (8, 10), (12, 10), (16, 10), (20, 10), (1, 11), (19, 11), (1, 12), (6, 12), (14, 12), (19, 12), (1, 13), (2, 13), (9, 13), (10, 13), (11, 13), (18, 13), (19, 13), (3, 14), (4, 14), (5, 14), (8, 14), (12, 14), (15, 14), (16, 14), (17, 14), (6, 15), (14, 15), (4, 16), (6, 16), (14, 16), (16, 16), (6, 17), (14, 17), (7, 18), (13, 18), (7, 19), (8, 19), (9, 19), (11, 19), (12, 19), (13, 19), (10, 20)]
        shiro=[(3, 2), (17, 2), (2, 3), (3, 3), (10, 3), (17, 3), (18, 3), (9, 4), (10, 4), (11, 4), (7, 7), (13, 7), (4, 8), (8, 8), (12, 8), (16, 8), (9, 9), (11, 9), (5, 10), (10, 10), (15, 10), (9, 11), (11, 11), (4, 12), (8, 12), (12, 12), (16, 12), (7, 13), (13, 13), (9, 16), (10, 16), (11, 16), (2, 17), (3, 17), (10, 17), (17, 17), (18, 17), (3, 18), (17, 18)]
        first_shokunin=[(1, 1), (19, 1), (2, 10), (18, 10), (1, 19), (19, 19)]
        second_shokunin=[(10, 6), (10, 8), (7, 10), (13, 10), (10, 12), (10, 14)]

    elif id == 'A25':
        width=25
        height=25
        ike=[(8, 2), (9, 2), (15, 2), (16, 2), (8, 3), (10, 3), (11, 3), (13, 3), (14, 3), (16, 3), (7, 4), (17, 4), (5, 5), (7, 5), (17, 5), (19, 5), (7, 6), (17, 6), (4, 7), (5, 7), (6, 7), (18, 7), (19, 7), (20, 7), (2, 8), (3, 8), (10, 8), (14, 8), (21, 8), (22, 8), (2, 9), (7, 9), (11, 9), (12, 9), (13, 9), (17, 9), (22, 9), (3, 10), (8, 10), (16, 10), (21, 10), (3, 11), (21, 11), (6, 12), (10, 12), (14, 12), (18, 12), (3, 13), (21, 13), (3, 14), (8, 14), (16, 14), (21, 14), (2, 15), (7, 15), (11, 15), (12, 15), (13, 15), (17, 15), (22, 15), (2, 16), (3, 16), (10, 16), (14, 16), (21, 16), (22, 16), (4, 17), (5, 17), (6, 17), (18, 17), (19, 17), (20, 17), (7, 18), (17, 18), (5, 19), (7, 19), (17, 19), (19, 19), (7, 20), (17, 20), (8, 21), (10, 21), (11, 21), (13, 21), (14, 21), (16, 21), (8, 22), (9, 22), (15, 22), (16, 22)]
        shiro=[(0, 0), (24, 0), (11, 1), (12, 1), (13, 1), (5, 2), (12, 2), (19, 2), (4, 3), (20, 3), (3, 4), (4, 4), (20, 4), (21, 4), (2, 5), (9, 5), (12, 5), (15, 5), (22, 5), (11, 6), (12, 6), (13, 6), (5, 9), (9, 9), (15, 9), (19, 9), (10, 10), (14, 10), (2, 11), (7, 11), (11, 11), (13, 11), (17, 11), (22, 11), (1, 12), (8, 12), (12, 12), (16, 12), (23, 12), (2, 13), (7, 13), (11, 13), (13, 13), (17, 13), (22, 13), (10, 14), (14, 14), (5, 15), (9, 15), (15, 15), (19, 15), (11, 18), (12, 18), (13, 18), (2, 19), (9, 19), (12, 19), (15, 19), (22, 19), (3, 20), (4, 20), (20, 20), (21, 20), (4, 21), (20, 21), (5, 22), (12, 22), (19, 22), (11, 23), (12, 23), (13, 23), (0, 24), (24, 24)]
        first_shokunin=[(2, 2), (22, 2), (4, 12), (20, 12), (2, 22), (22, 22)]
        second_shokunin=[(12, 8), (12, 10), (9, 12), (15, 12), (12, 14), (12, 16)]

    elif id == 'B11':
        width=11
        height=11
        ike=[(1, 1), (4, 1), (6, 1), (9, 1), (5, 2), (3, 3), (7, 3), (1, 4), (9, 4), (2, 5), (5, 5), (8, 5), (1, 6), (9, 6), (3, 7), (7, 7), (5, 8), (1, 9), (4, 9), (6, 9), (9, 9)]
        shiro=[(2, 2), (8, 2), (4, 4), (6, 4), (4, 6), (6, 6), (2, 8), (8, 8)]
        first_shokunin=[(5, 1), (5, 9)]
        second_shokunin=[(1, 5), (9, 5)]

    elif id == 'B13':
        width=13
        height=13
        ike=[(2, 1), (5, 1), (7, 1), (10, 1), (1, 2), (2, 2), (6, 2), (10, 2), (11, 2), (6, 3), (4, 4), (8, 4), (1, 5), (11, 5), (2, 6), (3, 6), (6, 6), (9, 6), (10, 6), (1, 7), (11, 7), (4, 8), (8, 8), (6, 9), (1, 10), (2, 10), (6, 10), (10, 10), (11, 10), (2, 11), (5, 11), (7, 11), (10, 11)]
        shiro=[(1, 1), (11, 1), (3, 3), (9, 3), (5, 5), (7, 5), (5, 7), (7, 7), (3, 9), (9, 9), (1, 11), (11, 11)]
        first_shokunin=[(6, 1), (4, 6), (8, 6), (6, 11)]
        second_shokunin=[(6, 4), (1, 6), (11, 6), (6, 8)]

    elif id == 'B15':
        width=15
        height=15
        ike=[(2, 1), (6, 1), (8, 1), (12, 1), (1, 2), (2, 2), (7, 2), (12, 2), (13, 2), (3, 3), (4, 3), (10, 3), (11, 3), (3, 4), (7, 4), (11, 4), (5, 5), (9, 5), (1, 6), (13, 6), (2, 7), (4, 7), (7, 7), (10, 7), (12, 7), (1, 8), (13, 8), (5, 9), (9, 9), (3, 10), (7, 10), (11, 10), (3, 11), (4, 11), (10, 11), (11, 11), (1, 12), (2, 12), (7, 12), (12, 12), (13, 12), (2, 13), (6, 13), (8, 13), (12, 13)]
        shiro=[(1, 1), (13, 1), (5, 2), (9, 2), (4, 4), (10, 4), (2, 5), (12, 5), (6, 6), (8, 6), (6, 8), (8, 8), (2, 9), (12, 9), (4, 10), (10, 10), (5, 12), (9, 12), (1, 13), (13, 13)]
        first_shokunin=[(7, 1), (5, 7), (9, 7), (7, 13)]
        second_shokunin=[(7, 5), (1, 7), (13, 7), (7, 9)]

    elif id == 'B17':
        width=17
        height=17
        ike=[(2, 1), (7, 1), (9, 1), (14, 1), (1, 2), (2, 2), (8, 2), (14, 2), (15, 2), (4, 3), (12, 3), (3, 4), (4, 4), (5, 4), (11, 4), (12, 4), (13, 4), (4, 5), (8, 5), (12, 5), (6, 6), (10, 6), (1, 7), (15, 7), (2, 8), (5, 8), (8, 8), (11, 8), (14, 8), (1, 9), (15, 9), (6, 10), (10, 10), (4, 11), (8, 11), (12, 11), (3, 12), (4, 12), (5, 12), (11, 12), (12, 12), (13, 12), (4, 13), (12, 13), (1, 14), (2, 14), (8, 14), (14, 14), (15, 14), (2, 15), (7, 15), (9, 15), (14, 15)]
        shiro=[(3, 3), (6, 3), (10, 3), (13, 3), (8, 4), (5, 5), (11, 5), (3, 6), (13, 6), (7, 7), (9, 7), (4, 8), (12, 8), (7, 9), (9, 9), (3, 10), (13, 10), (5, 11), (11, 11), (8, 12), (3, 13), (6, 13), (10, 13), (13, 13)]
        first_shokunin=[(8, 1), (6, 8), (10, 8), (8, 15)]
        second_shokunin=[(8, 6), (1, 8), (15, 8), (8, 10)]

    elif id == 'B21':
        width=21
        height=21
        ike=[(9, 1), (11, 1), (3, 2), (10, 2), (17, 2), (2, 3), (4, 3), (10, 3), (16, 3), (18, 3), (3, 4), (17, 4), (7, 5), (8, 5), (12, 5), (13, 5), (7, 6), (10, 6), (13, 6), (5, 7), (6, 7), (14, 7), (15, 7), (5, 8), (8, 8), (12, 8), (15, 8), (1, 9), (19, 9), (2, 10), (3, 10), (6, 10), (10, 10), (14, 10), (17, 10), (18, 10), (1, 11), (19, 11), (5, 12), (8, 12), (12, 12), (15, 12), (5, 13), (6, 13), (14, 13), (15, 13), (7, 14), (10, 14), (13, 14), (7, 15), (8, 15), (12, 15), (13, 15), (3, 16), (17, 16), (2, 17), (4, 17), (10, 17), (16, 17), (18, 17), (3, 18), (10, 18), (17, 18), (9, 19), (11, 19)]
        shiro=[(1, 1), (6, 1), (10, 1), (14, 1), (19, 1), (3, 3), (17, 3), (1, 6), (6, 6), (14, 6), (19, 6), (9, 9), (11, 9), (1, 10), (19, 10), (9, 11), (11, 11), (1, 14), (6, 14), (14, 14), (19, 14), (3, 17), (17, 17), (1, 19), (6, 19), (10, 19), (14, 19), (19, 19)]
        first_shokunin=[(6, 3), (14, 3), (7, 10), (13, 10), (6, 17), (14, 17)]
        second_shokunin=[(3, 6), (17, 6), (10, 7), (10, 13), (3, 14), (17, 14)]

    elif id == 'B25':
        width=25
        height=25
        ike=[(12, 0), (2, 1), (3, 1), (12, 1), (21, 1), (22, 1), (1, 2), (6, 2), (7, 2), (8, 2), (12, 2), (16, 2), (17, 2), (18, 2), (23, 2), (1, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3), (15, 3), (23, 3), (5, 4), (12, 4), (19, 4), (4, 5), (6, 5), (12, 5), (18, 5), (20, 5), (2, 6), (5, 6), (19, 6), (22, 6), (2, 7), (9, 7), (10, 7), (14, 7), (15, 7), (22, 7), (2, 8), (9, 8), (12, 8), (15, 8), (22, 8), (3, 9), (7, 9), (8, 9), (16, 9), (17, 9), (21, 9), (3, 10), (7, 10), (10, 10), (14, 10), (17, 10), (21, 10), (3, 11), (21, 11), (0, 12), (1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (8, 12), (12, 12), (16, 12), (19, 12), (20, 12), (21, 12), (22, 12), (23, 12), (24, 12), (3, 13), (21, 13), (3, 14), (7, 14), (10, 14), (14, 14), (17, 14), (21, 14), (3, 15), (7, 15), (8, 15), (16, 15), (17, 15), (21, 15), (2, 16), (9, 16), (12, 16), (15, 16), (22, 16), (2, 17), (9, 17), (10, 17), (14, 17), (15, 17), (22, 17), (2, 18), (5, 18), (19, 18), (22, 18), (4, 19), (6, 19), (12, 19), (18, 19), (20, 19), (5, 20), (12, 20), (19, 20), (1, 21), (9, 21), (10, 21), (11, 21), (12, 21), (13, 21), (14, 21), (15, 21), (23, 21), (1, 22), (6, 22), (7, 22), (8, 22), (12, 22), (16, 22), (17, 22), (18, 22), (23, 22), (2, 23), (3, 23), (12, 23), (21, 23), (22, 23), (12, 24)]
        shiro=[(0, 0), (24, 0), (9, 1), (15, 1), (3, 3), (21, 3), (5, 5), (19, 5), (11, 6), (13, 6), (7, 7), (17, 7), (1, 9), (9, 9), (15, 9), (23, 9), (6, 11), (11, 11), (13, 11), (18, 11), (6, 13), (11, 13), (13, 13), (18, 13), (1, 15), (9, 15), (15, 15), (23, 15), (7, 17), (17, 17), (11, 18), (13, 18), (5, 19), (19, 19), (3, 21), (21, 21), (9, 23), (15, 23), (0, 24), (24, 24)]
        first_shokunin=[(8, 5), (16, 5), (9, 12), (15, 12), (8, 19), (16, 19)]
        second_shokunin=[(5, 8), (19, 8), (12, 9), (12, 15), (5, 16), (19, 16)]

    elif id == 'C11':
        width=11
        height=11
        ike=[(10, 0), (9, 1), (10, 1), (8, 2), (4, 3), (5, 3), (6, 3), (8, 3), (3, 4), (4, 4), (6, 4), (8, 4), (2, 5), (3, 5), (7, 5), (8, 5), (2, 6), (4, 6), (6, 6), (7, 6), (2, 7), (4, 7), (5, 7), (6, 7), (2, 8), (0, 9), (1, 9), (0, 10)]
        shiro=[(8, 1), (9, 2), (7, 3), (9, 3), (5, 4), (4, 5), (5, 5), (6, 5), (5, 6), (1, 7), (3, 7), (1, 8), (2, 9)]
        first_shokunin=[(2, 1), (5, 1), (1, 4)]
        second_shokunin=[(9, 6), (5, 9), (8, 9)]

    elif id == 'C13':
        width=13
        height=13
        ike=[(11, 0), (12, 0), (3, 1), (11, 1), (2, 2), (9, 2), (10, 2), (9, 3), (5, 4), (6, 4), (7, 4), (9, 4), (4, 5), (5, 5), (7, 5), (9, 5), (3, 6), (4, 6), (8, 6), (9, 6), (3, 7), (5, 7), (7, 7), (8, 7), (3, 8), (5, 8), (6, 8), (7, 8), (3, 9), (2, 10), (3, 10), (10, 10), (1, 11), (9, 11), (0, 12), (1, 12)]
        shiro=[(4, 1), (5, 1), (1, 3), (8, 3), (10, 3), (1, 4), (8, 4), (10, 4), (6, 5), (5, 6), (6, 6), (7, 6), (6, 7), (2, 8), (4, 8), (11, 8), (2, 9), (4, 9), (11, 9), (7, 11), (8, 11)]
        first_shokunin=[(7, 1), (3, 3), (1, 6)]
        second_shokunin=[(11, 6), (9, 9), (5, 11)]

    elif id == 'C15':
        width=15
        height=15
        ike=[(14, 0), (5, 1), (7, 1), (9, 1), (13, 1), (14, 1), (4, 2), (6, 2), (8, 2), (10, 2), (13, 2), (3, 3), (7, 3), (11, 3), (12, 3), (2, 4), (10, 4), (11, 4), (1, 5), (6, 5), (7, 5), (8, 5), (10, 5), (2, 6), (5, 6), (6, 6), (8, 6), (10, 6), (12, 6), (1, 7), (3, 7), (4, 7), (5, 7), (9, 7), (10, 7), (11, 7), (13, 7), (2, 8), (4, 8), (6, 8), (8, 8), (9, 8), (12, 8), (4, 9), (6, 9), (7, 9), (8, 9), (13, 9), (3, 10), (4, 10), (12, 10), (2, 11), (3, 11), (7, 11), (11, 11), (1, 12), (4, 12), (6, 12), (8, 12), (10, 12), (0, 13), (1, 13), (5, 13), (7, 13), (9, 13), (0, 14)]
        shiro=[(6, 1), (8, 1), (12, 2), (6, 3), (8, 3), (13, 3), (9, 5), (11, 5), (1, 6), (3, 6), (7, 6), (11, 6), (13, 6), (6, 7), (7, 7), (8, 7), (1, 8), (3, 8), (7, 8), (11, 8), (13, 8), (3, 9), (5, 9), (1, 11), (6, 11), (8, 11), (2, 12), (6, 13), (8, 13)]
        first_shokunin=[(7, 2), (4, 4), (2, 7)]
        second_shokunin=[(12, 7), (10, 10), (7, 12)]

    elif id == 'C17':
        width=17
        height=17
        ike=[(15, 0), (16, 0), (5, 1), (6, 1), (7, 1), (9, 1), (15, 1), (5, 2), (8, 2), (10, 2), (15, 2), (3, 3), (4, 3), (9, 3), (11, 3), (13, 3), (14, 3), (3, 4), (12, 4), (13, 4), (1, 5), (2, 5), (11, 5), (12, 5), (1, 6), (7, 6), (8, 6), (9, 6), (11, 6), (2, 7), (6, 7), (7, 7), (9, 7), (11, 7), (12, 7), (14, 7), (1, 8), (3, 8), (5, 8), (6, 8), (10, 8), (11, 8), (13, 8), (15, 8), (2, 9), (4, 9), (5, 9), (7, 9), (9, 9), (10, 9), (14, 9), (5, 10), (7, 10), (8, 10), (9, 10), (15, 10), (4, 11), (5, 11), (14, 11), (15, 11), (3, 12), (4, 12), (13, 12), (2, 13), (3, 13), (5, 13), (7, 13), (12, 13), (13, 13), (1, 14), (6, 14), (8, 14), (11, 14), (1, 15), (7, 15), (9, 15), (10, 15), (11, 15), (0, 16), (1, 16)]
        shiro=[(8, 1), (10, 1), (14, 2), (8, 3), (10, 3), (15, 3), (10, 6), (12, 6), (1, 7), (3, 7), (8, 7), (13, 7), (15, 7), (7, 8), (8, 8), (9, 8), (1, 9), (3, 9), (8, 9), (13, 9), (15, 9), (4, 10), (6, 10), (1, 13), (6, 13), (8, 13), (2, 14), (6, 15), (8, 15)]
        first_shokunin=[(9, 2), (5, 4), (2, 8), (1, 11)]
        second_shokunin=[(15, 5), (14, 8), (11, 12), (7, 14)]

    elif id == 'C21':
        width=21
        height=21
        ike=[(19, 0), (20, 0), (8, 1), (18, 1), (19, 1), (7, 2), (9, 2), (16, 2), (17, 2), (6, 3), (10, 3), (14, 3), (15, 3), (17, 3), (18, 3), (5, 4), (7, 4), (9, 4), (11, 4), (14, 4), (18, 4), (4, 5), (8, 5), (12, 5), (14, 5), (15, 5), (17, 5), (18, 5), (3, 6), (13, 6), (15, 6), (16, 6), (2, 7), (4, 7), (13, 7), (14, 7), (1, 8), (5, 8), (9, 8), (10, 8), (11, 8), (13, 8), (15, 8), (2, 9), (4, 9), (8, 9), (9, 9), (11, 9), (13, 9), (16, 9), (3, 10), (7, 10), (8, 10), (12, 10), (13, 10), (17, 10), (4, 11), (7, 11), (9, 11), (11, 11), (12, 11), (16, 11), (18, 11), (5, 12), (7, 12), (9, 12), (10, 12), (11, 12), (15, 12), (19, 12), (6, 13), (7, 13), (16, 13), (18, 13), (4, 14), (5, 14), (7, 14), (17, 14), (2, 15), (3, 15), (5, 15), (6, 15), (8, 15), (12, 15), (16, 15), (2, 16), (6, 16), (9, 16), (11, 16), (13, 16), (15, 16), (2, 17), (3, 17), (5, 17), (6, 17), (10, 17), (14, 17), (3, 18), (4, 18), (11, 18), (13, 18), (1, 19), (2, 19), (12, 19), (0, 20), (1, 20)]
        shiro=[(17, 1), (8, 2), (18, 2), (7, 3), (8, 3), (9, 3), (16, 3), (8, 4), (12, 4), (15, 4), (16, 4), (17, 4), (11, 5), (13, 5), (16, 5), (12, 6), (14, 6), (3, 7), (15, 7), (2, 8), (3, 8), (4, 8), (12, 8), (14, 8), (16, 8), (3, 9), (10, 9), (15, 9), (9, 10), (10, 10), (11, 10), (5, 11), (10, 11), (17, 11), (4, 12), (6, 12), (8, 12), (16, 12), (17, 12), (18, 12), (5, 13), (17, 13), (6, 14), (8, 14), (4, 15), (7, 15), (9, 15), (3, 16), (4, 16), (5, 16), (8, 16), (12, 16), (4, 17), (11, 17), (12, 17), (13, 17), (2, 18), (12, 18), (3, 19)]
        first_shokunin=[(13, 1), (3, 2), (2, 3), (9, 6), (6, 9), (1, 13)]
        second_shokunin=[(19, 7), (14, 11), (11, 14), (18, 17), (17, 18), (7, 19)]

    elif id == 'C25':
        width=25
        height=25
        ike=[(10, 0), (24, 0), (3, 1), (10, 1), (23, 1), (24, 1), (2, 2), (4, 2), (10, 2), (21, 2), (22, 2), (1, 3), (5, 3), (6, 3), (7, 3), (8, 3), (10, 3), (20, 3), (21, 3), (2, 4), (4, 4), (9, 4), (11, 4), (18, 4), (19, 4), (3, 5), (8, 5), (12, 5), (16, 5), (17, 5), (19, 5), (20, 5), (3, 6), (7, 6), (9, 6), (11, 6), (13, 6), (16, 6), (20, 6), (3, 7), (6, 7), (10, 7), (14, 7), (16, 7), (17, 7), (19, 7), (20, 7), (3, 8), (5, 8), (10, 8), (15, 8), (17, 8), (18, 8), (4, 9), (6, 9), (10, 9), (15, 9), (16, 9), (0, 10), (1, 10), (2, 10), (3, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (15, 10), (17, 10), (4, 11), (6, 11), (10, 11), (11, 11), (13, 11), (15, 11), (18, 11), (5, 12), (9, 12), (10, 12), (14, 12), (15, 12), (19, 12), (6, 13), (9, 13), (11, 13), (13, 13), (14, 13), (18, 13), (20, 13), (7, 14), (9, 14), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), (16, 14), (17, 14), (21, 14), (22, 14), (23, 14), (24, 14), (8, 15), (9, 15), (14, 15), (18, 15), (20, 15), (6, 16), (7, 16), (9, 16), (14, 16), (19, 16), (21, 16), (4, 17), (5, 17), (7, 17), (8, 17), (10, 17), (14, 17), (18, 17), (21, 17), (4, 18), (8, 18), (11, 18), (13, 18), (15, 18), (17, 18), (21, 18), (4, 19), (5, 19), (7, 19), (8, 19), (12, 19), (16, 19), (21, 19), (5, 20), (6, 20), (13, 20), (15, 20), (20, 20), (22, 20), (3, 21), (4, 21), (14, 21), (16, 21), (17, 21), (18, 21), (19, 21), (23, 21), (2, 22), (3, 22), (14, 22), (20, 22), (22, 22), (0, 23), (1, 23), (14, 23), (21, 23), (0, 24), (14, 24)]
        shiro=[(0, 0), (23, 0), (3, 2), (2, 3), (3, 3), (4, 3), (19, 3), (3, 4), (10, 4), (20, 4), (9, 5), (10, 5), (11, 5), (18, 5), (10, 6), (14, 6), (17, 6), (18, 6), (19, 6), (13, 7), (15, 7), (18, 7), (14, 8), (16, 8), (5, 9), (17, 9), (4, 10), (5, 10), (6, 10), (14, 10), (16, 10), (18, 10), (5, 11), (12, 11), (17, 11), (11, 12), (12, 12), (13, 12), (7, 13), (12, 13), (19, 13), (6, 14), (8, 14), (10, 14), (18, 14), (19, 14), (20, 14), (7, 15), (19, 15), (8, 16), (10, 16), (6, 17), (9, 17), (11, 17), (5, 18), (6, 18), (7, 18), (10, 18), (14, 18), (6, 19), (13, 19), (14, 19), (15, 19), (4, 20), (14, 20), (21, 20), (5, 21), (20, 21), (21, 21), (22, 21), (21, 22), (1, 24), (24, 24)]
        first_shokunin=[(19, 1), (16, 2), (13, 3), (3, 13), (2, 16), (1, 19)]
        second_shokunin=[(23, 5), (22, 8), (21, 11), (11, 21), (8, 22), (5, 23)]
    
    return State(width,height,turn,ike,shiro,first_shokunin,second_shokunin,coef)

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
def generate_random_board(width=15,height=15,turn=50,ike=3,shiro=3,shokunin=3,joheki=60):
    shokunin=random_cie(width,height,[shokunin]*2+[ike])
    joheki=random_cie(width,height,[joheki]*2+[shiro])
    result=State(width,height,turn,ike=shokunin[2],shiro=joheki[2])
    result.initialize_field(shokunin=shokunin[:2],joheki=joheki[:2])
    result.find_zinchi()
    return result

#引数にStateオブジェクトを渡すことで合法手の中からランダムに行動を返す
def random_action(state,stay=False):
    legal_acrtions=state.legal_actions()
    result=[]
    if stay:
        for i in legal_acrtions:
            result.append(i[random.randint(0,len(i)-1)])
    else:
        for i in legal_acrtions:
            result.append(i[random.randint(1,len(i)-1)])         
    return result

#ランダム同士で対戦させる
def playout(id,turn=200,coef=(10,30,100)):
    state=generate_board(id,turn,coef)
    cnt=0
    legal_cnt=[]
    while True:
        if state.is_done():
            break
        for i in state.legal_actions():
            legal_cnt.append(len(i))
        print(action:=random_action(state))
        print(history:=state.next(action))
        cnt+=history.count(False)
        print(state)
    print(f"False_cnt:{cnt}")
    print(f"LegalAction_ave:{np.average(np.array(legal_cnt))}")

            
#ランダム対戦
def main1():
    from time import time
    start=time()
    playout('A15',turn=50)
    print(f"time:{time()-start}")

#state_for_modelメソッドの出力
def main2():
    print(x:=generate_random_board(width=5,height=5,joheki=5))
    print(x.state_for_model(False,1))

#legal_actionsメソッドの出力
def main3():
    print(x:=generate_board('A13',turn=200))
    print(x.legal_actions_for_model(False))
    print(x.legal_actions(False))

def main4():
    state=generate_board('A11')
    print(state)
    for _ in range(50):
        state.next(random_action(state))
    print(state)
    state.reset()
    print(state)
    
if __name__ == '__main__':
    main4()

'''
Stateクラスの説明
インスタンス生成:State(width,height,end_turn,ike=[],shiro=[],first_shokunin=[],second_shokunin=[],joheki_coef=10,zinchi_coef=30,shiro_coef=100)
    ike,shiro,firt_shokunin,second_shokuninは座標を示したタプル(x,y)をリストなどで渡す(例)ike=[(2,3),(4,5)]
    各ポイント係数についてはデフォルトが(10,30,100)である

以下,teamは先攻をFalse,後攻をTrueとする
team=Noneの引数があるメソッドはteamを入力しない場合、手番のチームとなる

各メソッド
initialize(self,ike=None,shiro=None,shokunin=None,joheki=None,closed_zinchi=None,opened_zinchi=None)
    池,城,各職人,各城壁,各開/閉の陣地を変えることができる
    城壁の設定後、陣地の探索は行われないため必要な場合はfind_zinchi()で個別に行う
count()
    両チームの城壁,陣地,城の数を返す
    出力は[[1st_joheki,1st_zinchi,1st_shiro],[2nd_joheki,2nd_zinchi,2nd_shiro]]
score()
    両チームの城壁,陣地,城の数に各ポイント係数をかけた得点を返す
    出力は[[1st_joheki,1st_zinchi,1st_shiro],[2nd_joheki,2nd_zinchi,2nd_shiro]]
next(actions,team=None)
    職人の行動を入力すると盤の状態を変化させる
    具体的な処理は
        行動が合法手かを判定し合法手であったもののみ行動をとる
        陣地の更新
        ターン数のインクリメント
        行動が成功したかをTrue/Falseの配列で返す
    teamはターン数に応じて自動的に決められるが、指定することも可能である
    actionの形式は行動idの配列で渡す(例):[1,1,2,5,16,0]
        行動id
         0:滞在
         1:左上へ移動
         2:上に移動
         3:右上に移動
         4:左に移動
        :
        :
         8:右下に移動
         9:上に建築
        10:左に建築
        11:右に建築
        12:下に建築
        13:上に解体
        :
        16:下に解体
             
*point(team=None)
    teamの勝敗(得点から判定)に応じて1(win),0(drow),-1(lose)を返す
*is_lose(team=None)
    teamが負けているかをTrue/Falseで返す
*is_done()
    ゲームが終了したか判定
*is_first_player()
    現在が先攻ターンか判定
    
legal_actions(team=None,number=None)
    合法手の取得
    出力は各職人の合法な行動idのリストのリスト(二次元リスト)
    (例)[[0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
    numberを指定することで指定した職人のみのリストを取得できる
legal_actions_for_model(team=None,number=None)
    合法手をnumpy配列を用いた形式で返す(学習モデル向け)
    滞在は含まれていないことに注意
evaluate(team=None)
    評価関数の値を返す
state()
    盤の状態を返す
    出力はshokunin,joheki,closed_zinchi,opened_zinchi
state_for_model(team,shokunin)
    盤の情報をnumpy配列を用いた形式で返す(学習モデル向け)

関数の説明
generate_board(id,turn=200,coef=(10,30,100))
    本番で用いられる18種類の競技フィールドから選んで生成
    idはA11,A13...A25,B11...C25まである
    ターン,ポイント係数についても指定可
random_cie(width,height,args)
    width,height内に収まるランダムな座標タプルを生成
    座標は重複しないようになっている
    argsで生成したい座標の数を指定することができる(例):(1,)->[(x,y)]    (1,2)->[[(x,y)],[(x,y),(x,y)]]
generate_random_board(width=15,height=15,turn=50,ike=3,shiro=3,shokunin=3,joheki=60)
    ランダムな盤の状態を生成できる
    各オブジェクト(池,職人...)の数を指定することである程度調整可
random_action(state,stay=False)
    引数にStateオブジェクトを渡すことで合法手の中からランダムに行動を返す
    出力した値はState.next()に直接渡せる
playout(id,turn=200,coef=10,30,100)
    ランダム同士で対戦させる
'''