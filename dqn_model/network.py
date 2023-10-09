'''
決戦!n乗谷城:エージェント学習プログラム(CNN,DQNを利用)
実行環境:Python 3.10.11 / tensorflow 2.14.0 / tf-agents 0.18.0
'''

import random
from tqdm import tqdm
import numpy as np
import tensorflow as tf
from tensorflow import keras

from tf_agents.environments import py_environment,tf_py_environment
from tf_agents.agents.dqn import dqn_agent
from tf_agents.networks import network
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.policies import policy_saver
from tf_agents.trajectories import time_step as ts
from tf_agents.trajectories import trajectory,policy_step as ps
from tf_agents.specs import array_spec
from tf_agents.utils import common,nest_utils

import state

NONE=0 
FIRST=1
SECOND=2

REWARD_WIN=10000
REWARD_LOSE=-10000
        
def make_environment_class(width,height,ike,shiro,first_shokunin,second_shokunin,end_turn):
    class EnvironmentSimulator(py_environment.PyEnvironment):
        def __init__(self):
            super(EnvironmentSimulator, self).__init__()
            self._observations_spec=array_spec.BoundedArraySpec(
                shape=(height,width,1),dtype=np.float32,minimum=0,maximum=2
            )
            self._action_spec=array_spec.BoundedArraySpec(
                shape=(),dtype=np.int32,minimum=0,maximum=15
            )
            self.reset()
        
        def observation_spec(self):
            return self._observations_spec
        
        def action_spec(self):
            return self._action_spec
        
        def _reset(self):
            self.board=state.State(width,height,ike,shiro,first_shokunin,second_shokunin,end_turn)
            time_step=ts.restart(self.board.state())
            return nest_utils.batch_nested_array(time_step)

        def _step(self,action):
            action=nest_utils.unbatch_nested_array(action)
            self.board.action((action,))
            self.board.find_zinchi()
            self.board.update_turn()
            time_step=ts.transition(self.board.state(),reward=0,discount=1)
            return nest_utils.batch_nested_array(time_step)
        
        def update_turn(self):
            self.board.update_turn()
            
        def random_action(self):
            legal_acrtion=self.board.legal_action(number=0)
            return random.choice(legal_acrtion)

        @property
        def batched(self):
            return True

        @property
        def batch_size(self):
            return 1
        
    return EnvironmentSimulator
    

class MyQNetwork(network.Network):
    def __init__(self,observation_spec,action_spec,n_hidden_channels=256,name='QNetwork'):
        super(MyQNetwork,self).__init__(
            input_tensor_spec=observation_spec,
            state_spec=(),
            name=name
        )
        n_action=action_spec.maximum-action_spec.minimum+1
        self.model=keras.Sequential(
            [
            ###ネットワークは要変更
            keras.layers.Conv2D(4,2,1,activation='relu'),
            keras.layers.Conv2D(8,2,1,activation='relu'),
            keras.layers.Conv2D(16,2,1,activation='relu'),
            keras.layers.Dense(256,kernel_initializer='he_normal'),
            keras.layers.Flatten(),
            keras.layers.Dense(n_action,kernel_initializer='he_normal')
            ]
        )
    def call(self,observation,step_type=None,network_state=(),training=True):
        observation=tf.cast(observation,tf.float32)
        actions=self.model(observation,training=training)
        return actions,network_state

def random_policy_step(random_action_function):
    random_act=random_action_function()
    if random_act is not False:
        return ps.PolicyStep(
            action=tf.constant([random_act]),
            state=(),
            info=()
        )
    else:
        raise Exception("No action")
        
def make_model(width,height,ike,shiro,first_shokunin,second_shokunin,end_turn):
    first_shokunin=(random.choice(first_shokunin),)
    second_shokunin=(random.choice(second_shokunin),)
        
    env_py=make_environment_class(width,height,ike,shiro,first_shokunin,second_shokunin,end_turn)()
    env=tf_py_environment.TFPyEnvironment(env_py)
    
    primary_network={}
    agent={}
    replay_buffer={}
    iterator={}
    policy={}
    tf_policy_saver={}
    
    n_step_update=1
    for role in (FIRST,SECOND):
        primary_network[role]=MyQNetwork(env.observation_spec(),env.action_spec())
        
        agent[role]=dqn_agent.DdqnAgent(
            env.time_step_spec(),
            env.action_spec(),
            q_network=primary_network[role],
            optimizer=keras.optimizers.Adam(learning_rate=1e-3),
            n_step_update=n_step_update,
            target_update_period=100,
            gamma=0.99,
            train_step_counter=tf.Variable(0),
            epsilon_greedy=0.0
        )
        agent[role].initialize()
        agent[role].train=common.function(agent[role].train)

        policy[role]=agent[role].collect_policy
        
        replay_buffer[role]=tf_uniform_replay_buffer.TFUniformReplayBuffer(
            data_spec=agent[role].collect_data_spec,
            batch_size=env.batch_size,
            max_length=10**6
        )
        dataset=replay_buffer[role].as_dataset(
            num_parallel_calls=tf.data.experimental.AUTOTUNE,
            sample_batch_size=16,
            num_steps=n_step_update+1,
        ).prefetch(tf.data.experimental.AUTOTUNE)
        iterator[role]=iter(dataset)
        
        tf_policy_saver[role]=policy_saver.PolicySaver(agent[role].policy)
        
    num_episodes=200
    decay_episodes=70
    epsilon=np.concatenate([np.linspace(1.0,0.1,decay_episodes),0.1*np.ones((num_episodes-decay_episodes,))])    
    action_step_counter=0
    reply_start_size=100
    
    winner_counter={FIRST:0,SECOND:1,NONE:0}
    episode_average_loss={FIRST:[],SECOND:[]}
    
    for episode in tqdm(range(1,num_episodes+1)):
        policy[FIRST]._epsilon=epsilon[episode-1]
        policy[SECOND]._episodes=epsilon[episode-1]
        env.reset()
        
        rewards={FIRST:0,SECOND:0}
        previous_time_step={FIRST:None,SECOND:None}
        previous_policy_step={FIRST:None,SECOND:None}
        
        while not env.board.is_end():
            current_time_step=env.current_time_step()
            while True:
                if previous_time_step[env.board.now_team] is None:
                    pass
                else:
                    previous_step_reward=tf.constant([rewards[env.board.now_team],],dtype=tf.float32)
                    current_time_step=current_time_step._replace(reward=previous_step_reward)
                    
                    traj=trajectory.from_transition(previous_time_step[env.board.now_team],previous_policy_step[env.board.now_team],current_time_step)
                    replay_buffer[env.board.now_team].add_batch(traj)
                    
                    if action_step_counter >= 2*reply_start_size:
                        experience,_=next(iterator[env.board.now_team])
                        loss_info=agent[env.board.now_team].train(experience=experience)
                        episode_average_loss[env.board.now_team].append(loss_info.loss.numpy())
                    else:
                        action_step_counter+=1
                if random.random() < epsilon[episode-1]:
                    policy_step=random_policy_step(env.random_action)
                else:
                    policy_step=policy[env.board.now_team].action(current_time_step)
                
                previous_time_step[env.board.now_team]=current_time_step
                previous_policy_step[env.board.now_team]=policy_step
                
                action=policy_step.action.numpy()[0]
                if action in env.board.legal_action(number=0):
                    rewards[env.board.now_team]=0
                    break
                else:
                    rewards[env.board.now_team]=REWARD_LOSE
            
            env.step(policy_step.action)
        if env.board.is_end():
            if env.board.winner==FIRST:
                rewards[FIRST]=REWARD_WIN
                rewards[SECOND]=REWARD_LOSE
                winner_counter[FIRST]+=1
            elif env.board.winner==SECOND:
                rewards[FIRST]=REWARD_LOSE
                rewards[SECOND]=REWARD_WIN
                winner_counter[SECOND]+=1
            else:
                winner_counter[NONE]+=1
            
            final_time_step=env.current_time_step()
            for role in (FIRST,SECOND):
                final_time_step=final_time_step._replace(
                    step_type=tf.constant([2],dtype=tf.int32),
                    reward=tf.constant([rewards[role]],dtype=tf.float32),
                )
                traj=trajectory.from_transition(previous_time_step[role],previous_policy_step[role],final_time_step)
                replay_buffer[role].add_batch(traj)
                if action_step_counter >= 2*reply_start_size:
                    experience,_=next(iterator[role])
                    loss_info=agent[role].train(experience=experience)
                    episode_average_loss[role].append(loss_info.loss.numpy())
        else:
            env.board.update_turn()
         
    return tf_policy_saver