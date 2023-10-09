import sys

class ShokuninClass:
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y

    #座標を返す(タプル)
    def cie(self):
        return (self.x,self.y)

class BoardClass:
    def __init__(self,name,width,height,ike,shiro,first_shokunin,second_shokunin,coef_joheki=10,coef_zinchi=30,coef_shiro=100) -> None:
        
        self.name=name
        #フィールドサイズ
        self.WIDTH=width    #11-25
        self.HEIGHT=height  #11-25

        #各ポイント係数
        self.JOHEKI_COEF=coef_joheki
        self.ZINCHI_COEF=coef_zinchi
        self.SHIRO_COEF=coef_shiro
        
        #池、城の座標
        self.IKE=frozenset(ike)
        self.SHIRO=frozenset(shiro)

        #以下 False(0):1st True(1):2nd
        
        #職人の座標
        self.shokunins=[[ShokuninClass(i[0],i[1]) for i in first_shokunin],[ShokuninClass(i[0],i[1]) for i in second_shokunin]]
    
    #すべての職人の座標を返す(listで返す.set=Trueでsetとして返す)
    def shokunins_cie(self,set=False):
        if set:
            return ({i.cie() for i in self.shokunins[False]},{i.cie() for i in self.shokunins[True]})
        else:
            return ([i.cie() for i in self.shokunins[False]],[i.cie() for i in self.shokunins[True]])
        
    #現在の盤の状態を返す(shokunin,pond,castle)
    def state(self):
        shokunin=[]
        pond=[]
        castle=[]
        first=self.shokunins_cie(set=True)[False]
        second=self.shokunins_cie(set=True)[True]
        #行/列の転置はfor のi/jを入れ替える
        for i in range(self.HEIGHT):
            tmp1=[]
            tmp2=[]
            tmp3=[]
            for j in range(self.WIDTH):
                if (i,j) in first:
                    tmp1.append("o")
                elif (i,j) in second:
                    tmp1.append("x")
                else:
                    tmp1.append("-")
                
                if (i,j) in self.IKE:
                    tmp2.append("p")
                else:
                    tmp2.append("-")
                    
                if (i,j) in self.SHIRO:
                    tmp3.append("c")
                else:
                    tmp3.append("-")
                        
            shokunin.append(tmp1)
            pond.append(tmp2)
            castle.append(tmp3)
        return [shokunin,pond,castle]
    
    #CUIで現在の状態を出力         
    def print_state(self):
        board_state=self.state()
        print("{}".format(self.name).ljust(162,"-"))
        print("1st:{}".format("".join("({},{})".format(i[0],i[1]) for i in self.shokunins_cie()[False])))
        print("2nd:{}".format("".join("({},{})".format(i[0],i[1]) for i in self.shokunins_cie()[True])))
        print("shokunin({})".format(len(self.shokunins[False])).ljust(1+2*self.WIDTH+int(self.HEIGHT>10),"-"),"ike({})".format(len(self.IKE)).ljust(1+2*self.WIDTH+int(self.HEIGHT>10),"-"),"shiro({})".format(len(self.SHIRO)).ljust(1+2*self.WIDTH+int(self.HEIGHT>10),"-"),sep=" "*3)
        head1=" "*(3 if self.HEIGHT>10 else 2) + " ".join([str(i//10) for i in range(self.WIDTH)])
        head2=" "*(3 if self.HEIGHT>10 else 2) + " ".join([str(i%10) for i in range(self.WIDTH)])
        if self.WIDTH>10:
            print(head1,head1,head1,sep=" "*3)
        print(head2,head2,head2,sep=" "*3)
        for i in range(self.HEIGHT):
            print(str(i).zfill(2 if self.HEIGHT>10 else 1)+" "+" ".join(board_state[0][i]),str(i).zfill(2 if self.HEIGHT>10 else 1)+" "+" ".join(board_state[1][i]),str(i).zfill(2 if self.HEIGHT>10 else 1)+" "+" ".join(board_state[2][i]),sep=" "*3)
        

def generate_template_board(id):
    #['A11','A13','A15','A17','A21','A25','B11','B13','B15','B17','B21','B25','C11','C13','C15','C17','C21','C25']
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

    return BoardClass(id,width,height,ike,shiro,first_shokunin,second_shokunin)

sys.stdout=open("output_csv_table.log", "w")
ids=['A11','A13','A15','A17','A21','A25','B11','B13','B15','B17','B21','B25','C11','C13','C15','C17','C21','C25']
for i in ids:
    generate_template_board(i).print_state()
sys.stdout.close()
sys.stdout=sys.__stdout__
'''
boardクラスの説明

●クラスを生成
    BoardClass(width,height,[ike],[shiro],[1st-shokunin],[2nd-shokunin],coef_joheki=10,coef_zinchi=30,coef_shiro=100)
    whidth,heightは横,縦の分割数。生成される座標は0から始まることに注意
    coef_joheki,coef_zinchi,coef_shiroは各係数
    [ike],[shiro],[1st-shokunin],[2nd-shokunin]の中には設置したい座標をタプルで入力。複数入力可
    例:board1を生成するとき
    board1=BoardClass(6,5,1,3,5,[(1,2),(2,3)],[(4,0)],[(0,1)],[(4,5),(5,3)])

    生成後、最初にprint_stateメゾットで盤の状況を表示するとよい 例:board1.print_state()
    そのあとはintegration_turnメゾットでゲームを進めるとよい

●各メゾットの説明
    operation(team,operations):各職人の操作を行う。各行動が成功したかどうかなどをタプルで返す。引数については後述。
    turn_end():operationが完了した後に行うもの。陣地の判定,得点の処理,内部ターン数を増やすことなどを行っている。
    print_state():現在の盤の状況、各職人の座標を表示する。
    integration_turn(team,operations):operation,turn_end,print_stateを一括で行えるメゾット。
    state():現在の盤の状況をリストで返す。
    history():現在までの職人の行動記録等をリストで返す。ヒストリ機能。
    game_end():ゲームが終了した際に行うもの。勝ったチームの表示、記録が行われる

●operation,integration_turnの引数について
    引数は(team,operations)となっている。
    teamは操作したい職人のチームをTrue or Falseで入力 (先攻:True  後攻:False)
    operationsは職人の数だけリスト(またはタプル)で以下のように入力していき、リストで囲む
    滞在:[0]
    移動:[1,x,y]
    建築:[2,x,y]
    解体:[3,x,y]
    なお、x,yは行動対象の座標
    各操作が適切(ルール参照)であれば行動成功となり操作が行われる。そうでなければ行動失敗となり滞在となる。
    boardクラス生成時に入力した職人の順にこちらも入力する。例えば職人を(0,1),(5,2)の順に生成した後[1,5,3],[1,0,2]の順に入力すると行動失敗となる
    返す値は[(ターン,職人番号,行動名,行動対象座標x,行動対象座標y,成功/失敗)...]で出力される
    例えば[(1, 1, 2, 0, 1, True),(1, 2, 2, 0, 2, True)...]

●state,print_stateの出力について
    print_stateはstateの出力結果を見やすく整えて標準出力している。次にprint_stateの出力結果例を示す。

    turn4----------------------------------------------------------------
    shokunin_coordinate-----------------------------------------
    1st:(1,1)(1,2)(1,3)(1,4)(1,5)(1,6)(1,7)(1,8)
    2nd:(5,3)(7,3)(7,6)(5,5)(3,1)
    score-------------------------------------------------------
          joheki(x1) /  zinchi(x3) /  shiro(x5)  /    total    
    1st:    35(35)   /   59(177)   /     1(5)    /     217     
    2nd:     4(4)    /     1(3)    /     0(0)    /      7      

    shokunin-------------   joheki---------------   zinchi---------------
      0 1 2 3 4 5 6 7 8 9     0 1 2 3 4 5 6 7 8 9     0 1 2 3 4 5 6 7 8 9
    0 p - - - - - - - - -   0 p o o - o o o o o o   0 - - - - - - - - - -
    1 - o - x - - - - - -   1 o - - - - - - - - o   1 - o o o o o o o o -
    2 - o - - c - - - - -   2 o - - - c - - - - o   2 - o o o o o o o o -
    3 - o - - - x - x - -   3 o - - - - - x - - o   3 - o o o o o - o o -
    4 - o - - - - - - - -   4 o - - - - x - x - o   4 - o o o o - x - o -
    5 - o - - - x - - - -   5 o - - - - - x - - o   5 - o o o o o - o o -
    6 - o - - - - - x - -   6 o - - - - - - - - o   6 - o o o o o o o o -
    7 - o - - - - - - - -   7 o - - - - - - - - o   7 - o o o o o o o o -
    8 - o - - - - - - - -   8 o - - - - - - - - o   8 - o o o o o o o o -
    9 - - - - - - - - - -   9 o o o o o o o o o o   9 - - - - - - - - - -

    上から
    現在のターン(turn3)
    職人の座標(shokunin_cooedinate)
    得点:城壁,陣地,が個数(個数×係数)で表示,合計も表示
    shokunin:職人(先攻:o 後攻:x)と池(p),城(c)の位置(職人と城の座標が重なった場合、職人の表示が優先される。城の見落としを防ぐならjohekiの盤を見るとよい)
    joheki:城壁、城の位置
    zinchi:(先攻:o 後攻:x 両チーム:b)陣地の位置

●入力例:

    stay=0
    move=1
    build=2
    destroy=3
    first=False
    second=True

    board1=BoardClass(6,6,[(1,5),(3,5)],[(0,3)],[(1,1),(3,3)],[(4,5),(2,4)])
    board1.print_state()
    board1.integration_turn(first,[(stay),(move,3,4)])
    board1.integration_turn(second,[(build,5,5),(build,2,3)])
    :
    :
    [print(i) for i in board1,history()]
    :
    BoardClass.game_end()
'''

def main():
    pass
'''
    from time import time
    start=time()

    stay=0
    move=1
    build=2
    destroy=3
    first=False
    second=True
    board1=generate_template_board('C25')
    board1.print_state()
    
    board1=BoardClass(10,10,[(0,0)],[(4,2)],[(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8)],[(5,3),(7,3),(7,5),(5,5),(3,2)])
    board1.print_state()
    [print(i) for i in board1.operation(first,[(build,0,1),(build,0,2),(build,0,3),(build,0,4),(build,0,5),(build,0,6),(build,0,7),(build,0,8)])]
    #board1.joheki[True].update(set(board1.OUTSIDE))
    board1.turn_end()
    board1.print_state()
    [print(i) for i in board1.operation(second,[(build,6,3),(build,7,4),(build,6,5),(build,5,4),(move,3,1)])]
    board1.turn_end()
    board1.print_state()
    [print(i) for i in board1.operation(second,[(move,6,3),(move,6,3),(move,7,6),[stay],(destroy,3,0)])]
    board1.turn_end()
    board1.print_state()
    board1.game_end()
    [print(i) for i in board1.history()]

    print(board1.__sizeof__()) 
    print(time()-start)
'''
if __name__=="__main__":
    main()