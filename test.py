#!/usr/bin/env python
# coding=utf-8
import numpy as np
import pandas as pd
import time

np.random.seed(2) # reproduciable

N_STATES = 6
ACTIONS = ['left', 'right']
EPSILON = 0.9
ALPHA = 0.1
GAMMA = 0.9
MAX_EPISODES = 13
FRESH_TIME = 0.01


def build_q_table(n_states, actions):
    table = pd.DataFrame(np.zeros((n_states, len(actions))), columns=actions,) #print(table), show table
    return table

def choose_action(state, q_table):
    # This is how to choose an action 
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):     # acct non-greedy or state-action have no value
        action_name = np.random.choice(ACTIONS)
    else: # act greedy
        action_name = state_actions.idxmax() # replace argmax to idxmax as argmax means a different function in new version of pandas 
    return action_name


def get_env_feedback(S, A):
    # This is how agent will interact with the environment
    if A == 'right':        #move right 
        if S == N_STATES -2 :
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else:
        R = 0
        if S == 0:
            S_ = S # reach the wall
        else:
            S_ = S -1
    return S_, R

    
def update_env(S, episode, step_counter):
    # This is how envirment be updated
    env_list = ['-']*(N_STATES-1) + ['T']
    if S == 'terminal':
        interaction = 'Episode %s: total_steps = %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                               ', end='')
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)


def rl():
    # main part of RL loop
    q_table = build_q_table(N_STATES , ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_terminated = False
        update_env(S, episode, step_counter)
        while not is_terminated:


            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)
            q_predict = q_table.loc[S, A]
            if S_ != 'terminal':
                q_target = R + GAMMA * q_table.iloc[S_, :].max()
            else:
                q_target = R
                is_terminated = True



            q_table.loc[S, A] += ALPHA * (q_target - q_predict) # update
            S = S_ # move to next state 
            update_env(S, episode, step_counter + 1)
            step_counter +=  1
        return q_table


if __name__ == "__main__":
    q_table = rl()
    print('\r\nQ-table:\n')
    print(q_table)
            

