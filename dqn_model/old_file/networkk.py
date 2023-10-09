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
import field

NONE=0 
FIRST=1
SECOND=2

REWARD_WIN=1
REWARD_LOSE=-1

width,height,ike,shiro,first_shokunin,second_shokunin=field.field_index('A11')
end_turn=100
#シミュレータークラス
class Board(py_environment.PyEnvironment):  
    def __init__(self):
        super(Board, self).__init__()  
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(height,width,1), dtype=np.float32, minimum=0, maximum=3
        )
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=15
        )
        self.reset()
    def observation_spec(self):
        return self._observation_spec
    def action_spec(self):
        return self._action_spec
    
    #ボードの初期化
    def _reset(self):
        self.board=state.State(width,height,ike,shiro,first_shokunin,second_shokunin,end_turn)
        time_step = ts.restart(self.board.state())
        return nest_utils.batch_nested_array(time_step)
    
    #行動による状態変化
    def _step(self,action):
        action=nest_utils.unbatch_nested_array(action)
        self.state.action((action),)
        if not all([0<=i<8 for i in action]):
            self.board.find_zinchi()
        time_step = ts.transition(self.board.state(),reward=0,discount=1)
        return nest_utils.batch_nested_array(time_step)
    
    #ターンチェンジ
    def change_turn(self, role=None):
        self.board.update_turn()
        
    #ランダムに石を置く場所を決める（ε-greedy用）
    def random_action(self):
        legal_acrtion=self.board.legal_action(number=0)
        return random.choice(legal_acrtion)
    
    @property
    def batched(self):
        return True

    @property
    def batch_size(self):
        return 1
    
#ネットワークの設定
class MyQNetwork(network.Network):
    def __init__(self, observation_spec, action_spec, n_hidden_channels=256, name='QNetwork'):
        super(MyQNetwork,self).__init__(
        input_tensor_spec=observation_spec, 
        state_spec=(), 
        name=name
        )
        n_action = action_spec.maximum - action_spec.minimum + 1
        self.model = keras.Sequential([
            keras.layers.Conv2D(4, 2, 1, activation='relu'),
            keras.layers.Conv2D(8, 2, 1, activation='relu'),
            keras.layers.Conv2D(16, 2, 1, activation='relu'),
            keras.layers.Dense(256, kernel_initializer='he_normal'),
            keras.layers.Flatten(),
            keras.layers.Dense(n_action, kernel_initializer='he_normal'),
        ])
        
    def call(self, observation, step_type=None, network_state=(), training=True):
        observation = tf.cast(observation, tf.float32)
        actions = self.model(observation, training=training)
        return actions, network_state
    
#ランダム行動を行うときのポリシー
def random_policy_step(random_action_function):
    random_act = random_action_function()
    if random_act is not False:
        return ps.PolicyStep(
            action=tf.constant([random_act]),
            state=(),
            info=()
            )
    else:
        raise Exception("No position avaliable.")

def main():
    #環境の設定
    env_py = Board()
    env = tf_py_environment.TFPyEnvironment(env_py)
    #黒と白の2つを宣言するために先に宣言
    primary_network = {}
    agent = {}
    replay_buffer = {}
    iterator = {}
    policy = {}
    tf_policy_saver = {}

    n_step_update = 1
    for role in (FIRST, SECOND):#黒と白のそれぞれの設定
        #ネットワークの設定
        primary_network[role] = MyQNetwork(env.observation_spec(), env.action_spec())
        #エージェントの設定
        agent[role] = dqn_agent.DqnAgent(
            env.time_step_spec(),
            env.action_spec(),
            q_network = primary_network[role],
            optimizer = keras.optimizers.Adam(learning_rate=1e-3),
            n_step_update = n_step_update,
            target_update_period=100,#0,
            gamma=0.99,
            train_step_counter = tf.Variable(0),
            epsilon_greedy = 0.0,
        )
        agent[role].initialize()
        agent[role].train = common.function(agent[role].train)
        #行動の設定
        policy[role] = agent[role].collect_policy
        #データの保存の設定
        replay_buffer[role] = tf_uniform_replay_buffer.TFUniformReplayBuffer(
            data_spec=agent[role].collect_data_spec,
            batch_size=env.batch_size,
            max_length=10**6,
        )
        dataset = replay_buffer[role].as_dataset(
            num_parallel_calls=tf.data.experimental.AUTOTUNE,
            sample_batch_size=16,
            num_steps=n_step_update+1,
        ).prefetch(tf.data.experimental.AUTOTUNE)
        iterator[role] = iter(dataset)
        #ポリシーの保存設定
        tf_policy_saver[role] = policy_saver.PolicySaver(agent[role].policy)

    num_episodes = 200#0
    decay_episodes = 70#0
    epsilon = np.concatenate( [np.linspace(start=1.0, stop=0.1, num=decay_episodes),0.1 * np.ones(shape=(num_episodes-decay_episodes,))])
    action_step_counter = 0
    replay_start_size = 100#0

    winner_counter = {FIRST:0, SECOND:0, NONE:0}#黒と白の勝った回数と引き分けの回数
    episode_average_loss = {FIRST:[], SECOND:[]}#黒と白の平均loss

    for episode in range(1, num_episodes + 1):
        policy[SECOND]._epsilon = epsilon[episode-1]#ε-greedy法用
        policy[FIRST]._epsilon = epsilon[episode-1]
        env.reset()

        rewards = {FIRST:0, SECOND:0}# 報酬リセット
        previous_time_step = {FIRST:None, SECOND:None}
        previous_policy_step = {FIRST:None, SECOND:None}

        while not env.board.is_end(): # ゲームが終わるまで繰り返す
            current_time_step = env.current_time_step()
            while True: # 置ける場所が見つかるまで繰り返す
                if previous_time_step[env.board.player()] is None:#1手目は学習データを作らない
                    pass
                else:
                    previous_step_reward = tf.constant([rewards[env.board.player()],],dtype=tf.float32)
                    current_time_step = current_time_step._replace(reward=previous_step_reward)

                    traj = trajectory.from_transition( previous_time_step[env.board.player()], previous_policy_step[env.board.player()], current_time_step )#データの生成
                    replay_buffer[env.board.player()].add_batch( traj )#データの保存

                    if action_step_counter >= 2*replay_start_size:#事前データ作成用
                        experience, _ = next(iterator[env.board.player()])
                        loss_info = agent[env.board.player()].train(experience=experience)#学習
                        episode_average_loss[env.board.player()].append(loss_info.loss.numpy())
                    else:
                        action_step_counter += 1
                if random.random() < epsilon[episode-1]:#ε-greedy法によるランダム動作
                    policy_step = random_policy_step(env.random_action)#設定したランダムポリシー
                else:
                    policy_step = policy[env.board.player()].action(current_time_step)#状態から行動の決定

                previous_time_step[env.board.player()] = current_time_step#1つ前の状態の保存
                previous_policy_step[env.board.player()] = policy_step#1つ前の行動の保存

                action = policy_step.action.numpy()[0]
                if action in env.board.legal_action(number=0):
                    rewards[env.board.player()]=0
                    break
                else:
                    rewards[env.board.player()]=REWARD_LOSE
                
                env.step(policy_step.action)# 石を配置
                
            if env.board.is_end():#ゲーム終了時の処理
                if env.winner == FIRST:#黒が勝った場合
                    rewards[FIRST] = REWARD_WIN  # 黒の勝ち報酬
                    rewards[SECOND] = REWARD_LOSE # 白の負け報酬
                    winner_counter[FIRST] += 1
                elif env.winner == SECOND:#白が勝った場合
                    rewards[FIRST] = REWARD_LOSE
                    rewards[SECOND] = REWARD_WIN
                    winner_counter[SECOND] += 1
                else:#引き分けの場合
                    winner_counter[NONE] += 1
                #エピソードを終了して学習
                final_time_step = env.current_time_step()#最後の状態の呼び出し
                for role in (SECOND, FIRST):
                    final_time_step = final_time_step._replace(step_type = tf.constant([2], dtype=tf.int32), reward = tf.constant([rewards[role]], dtype=tf.float32), )#最後の状態の報酬の変更
                    traj = trajectory.from_transition( previous_time_step[role], previous_policy_step[role], final_time_step )#データの生成
                    replay_buffer[role].add_batch( traj )#事前データ作成用
                    if action_step_counter >= 2*replay_start_size:
                        experience, _ = next(iterator[role])
                        loss_info = agent[role].train(experience=experience)
                        episode_average_loss[role].append(loss_info.loss.numpy())
            else:        
                env.change_turn()

        # カウンタ変数の初期化      
        winner_counter = {FIRST:0, SECOND:0, NONE:0}
        episode_average_loss = {SECOND:[], FIRST:[]}

    tf_policy_saver[FIRST].save(f"policy_first_{episode}")
    tf_policy_saver[SECOND].save(f"policy_second_{episode}")

if __name__ == '__main__':
  main()
