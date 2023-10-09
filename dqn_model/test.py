import predict
import state
import field

import random

id='A11'
width,height,ike,shiro,first_shokunin,second_shokunin=field.field_index(id)
end_turn=100

board=state.State(width,height,ike,shiro,(first_shokunin[0],),(second_shokunin[0],),end_turn)
print(board)
while True:
    print(p:=predict.predict(id,end_turn,board))
    print(board.play((p,)))
    print(board)
    if board.is_end():
        print(board.winner())
        break