#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wen Apr 07 11:46:22 2021

@author: bonfils
"""
import numpy as np

import random
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.backend import clear_session

from collections import deque

class DQN:
    def __init__(self, env):
        self.env           = env
        self.memory        = deque(maxlen=2000)
        
        self.gamma         = 0.85
        self.epsilon       = 1.0
        self.epsilon_min   = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau           = .125
        self.batch_size    = 16
        self.state_shape        = self.env.observ_shape[0]*self.env.observ_shape[1]

        self.model         = self.create_model()
        self.target_model  = self.create_model()


    def create_model(self):
        model              = Sequential()
        # print(state_shape)

        ## add layers
        model.add(Dense(units=24, input_dim=self.state_shape, activation="elu"))
        model.add(Dense(units=48, activation="elu"))
        model.add(Dense(units=24, activation="elu"))
        model.add(Dense(units=self.env.n_action_space, activation="linear"))

        ## compile the model
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        model.summary()
        return model


    def act(self, state):
        self.epsilon     *= self.epsilon_decay
        self.epsilon      = max(self.epsilon_min, self.epsilon)

        if np.random.random() < self.epsilon:
            # return self.env.action_space.sample()
            return np.random.randint(0, 7)
        prediction = np.argmax(self.model.predict(state)[0])
        return prediction


    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])


    def replay(self):
        if len(self.memory) < self.batch_size: 
            return

        samples = random.sample(self.memory, self.batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)


    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)


    def save_model(self, fn):
        self.model.save(fn)

def main():
    clear_session()
    n_rows    = 6
    n_columns = 7
    env       = Connect4(n_rows=n_rows, n_columns=n_columns)
    gamma     = 0.9
    epsilon   = .95

    trials    = 2000
    trial_len = 21

    # updateTargetNetwork = 1000
    dqn_agent = DQN(env=env)
    steps = []
    for trial in range(trials):
        print("---"*20)
        print("trial :", trial)
        dqn_agent.env.reset()
        if isinstance(dqn_agent.state_shape, int):
            cur_state = dqn_agent.env.board.reshape(1,-1)
        else:
            cur_state = dqn_agent.env.board

        for step in range(trial_len):
            # print("step : ", step)
            action = dqn_agent.act(cur_state)
            test = env.step(action)

            ## Test if the board is full
            if (test==-2):
                break
            ## compute another action while the action imply a full column
            elif (test==-1):
                continue
            else:
                new_state, reward, done = test

            # # reward = reward if not done else -20
            if isinstance(dqn_agent.state_shape, int):
                new_state = new_state.reshape(1,-1)
            dqn_agent.remember(cur_state, action, reward, new_state, done)
            
            dqn_agent.replay()       # internally iterates default (prediction) model
            dqn_agent.target_train() # iterates target model

            cur_state = new_state
            if done:
                break
        if step >= 199:
            print("Failed to complete in  {trial}".format(trial))

            if step % 10 == 0:
                # dqn_agent.save_model("trial-{}.model".format(trial))
                dqn_agent.save_model("trial-{}.h5".format(trial))
        else:
            print("Completed in {} trials".format(trial))
            dqn_agent.save_model("success.h5")
            # dqn_agent.save_model("success.model")
            #break


if __name__ == "__main__":
    main()