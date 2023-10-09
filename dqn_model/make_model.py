import path
import network
import field

NONE=0 
FIRST=1
SECOND=2

def save_model(id,turn):
    width,height,ike,shiro,first_shokunin,second_shokunin=field.field_index(id)
    turn//=len(first_shokunin)
    policy=network.make_model(width,height,ike,shiro,first_shokunin,second_shokunin,turn)
    policy[FIRST].save(path.get_policydir(id,turn,False))
    policy[SECOND].save(path.get_policydir(id,turn,True))

save_model('A11',100)
