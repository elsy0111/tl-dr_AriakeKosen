import os
from pathlib import Path

BASE_DIR=Path(__file__).parent
FIELDDATA_DIR=BASE_DIR / "fielddata"
POLICY_DIR=BASE_DIR / "policy"

def get_policydir(id,turn,team=None):
    if team is None:
        return POLICY_DIR / f'policy_{id}_{turn}'
    return POLICY_DIR / f'policy_{id}_{turn}_{"2nd" if team else "1st"}'

def get_fielddata(id):
    return FIELDDATA_DIR / f'{id}.csv'

def get_policy_kind():
    files=POLICY_DIR.iterdir()
    result=[]
    for i in files:
        _,id,turn,team=str(i.name).split('_')
        result.append((id,int(turn),team=='2nd'))
    return result

def get_turn(id,team):
    files=get_policy_kind()
    result=[]
    for i in files:
        if i[0]==id and i[2]==team:
            result.append(i[1])
    result.sort()
    return result
