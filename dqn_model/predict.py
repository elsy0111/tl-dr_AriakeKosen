import path
import network

import tensorflow as tf
from tf_agents.trajectories import time_step as ts
from tf_agents.utils import nest_utils

import copy

def make_environment_class(state):
    
    class EnvironmentSimulator(network.make_environment_class(0,0,[],[],[],[],0)):
        def _reset(self):
            self.board=copy.deepcopy(state)
            time_step=ts.restart(self.board.state())
            return nest_utils.batch_nested_array(time_step)

        def _step(self,action):
            action=nest_utils.unbatch_nested_array(action)
            self.board.action((action,))
            self.board.find_zinchi()
            self.board.update_turn()
            time_step=ts.transition(self.board.state(),reward=0,discount=1)
            return nest_utils.batch_nested_array(time_step) 
              
    return EnvironmentSimulator

def predict(id,end_turn,state):
    game=make_environment_class(state)()
    policy=tf.compat.v2.saved_model.load(path.get_policydir(id,end_turn,team=False))
    
    current_time_step = game.current_time_step()
    action_step = policy.action( current_time_step )
    action = int(action_step.action.numpy())
    return action