import numpy as np


class QLearning:

    def __init__(self, learning_rate, discount_factor, states, rewards, n_states, n_actions):
        """learning rate = alpha, discount factor = gamma, states and rewards refer to the arrays,
        n_states and n_actions are the number of states and actions"""

        self.alpha = learning_rate
        self.gamma = discount_factor
        self.states = states
        self.rewards = rewards
        self.n_states = n_states
        self.n_actions = n_actions
        self.QTable = np.zeros((self.n_states, self.n_actions))           # initialize the Q Table with zeros

    def update_q_table(self, old_state, action, new_state):

        # Bellman Equation
        # Q(s, a) = Q(s, a) + alpha * (reward(s') + gamma * max(Q(s', a')) - Q(s, a))

        current_q = self.QTable[old_state][action]
        value = self.rewards[new_state] + self.gamma * self.QTable[new_state].max() - current_q
        alpha_value = self.alpha * value
        self.QTable[old_state][action] = current_q + alpha_value

    def print_q_table(self):
        print("--------------------------------------")
        print("QTable:")
        print("States    Up Right Down Left")

        for i in range(self.n_states):
            print(self.states[i], end="")
            print("\t", self.QTable[i], end="")
            print("")
        print("--------------------------------------")

    def max_q_action(self, current_state):
        y = self.QTable[current_state].max()
        qlist = np.where(self.QTable[current_state] == y)
        # if, for a state, 2 or more Q values are same, then choose randomly between them.
        # Else, return the index of that value, to be used as the current action
        if len(qlist[0]) > 1:
            x = np.random.choice(qlist[0])
            return x
        else:
            for x in range(self.n_actions):
                if self.QTable[current_state][x] == y:
                    return x
