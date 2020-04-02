from random import randint
from QLearning import QLearning
from time import time
from time import sleep
from matplotlib import pyplot as plt
import numpy as np
import pyglet

# in pyglet, the coordinate system starts from the bottom left, as is the mathematical convention

window = pyglet.window.Window(caption='AI', width=440, height=440, resizable=False)
window.set_location(500, 200)
maze_bg = pyglet.resource.image('assets/Maze.png')          # background image showing the maze
agent_img = pyglet.resource.image('assets/agent.png')       # the orange dot representing the agent
target_img = pyglet.resource.image('assets/target.png')     # the green dot representing the goal
maze = pyglet.sprite.Sprite(img=maze_bg, x=0, y=0)          # converted to sprite, so it can be drawn, later
agent = pyglet.sprite.Sprite(img=agent_img, x=0, y=360)     # (0, 360) are the initial coordinates of the agent
target = pyglet.sprite.Sprite(img=target_img, x=400, y=40)  # (400, 40) are the initial coordinates of the goal

sleep_time = 0.08        # alter this to change the speed of the program
start_state = [0, 360]  # initial coordinates of the agent
one_step = 40           # 40 pixels in each step
n_actions = 4           # maximum no of possible actions
n_states = 121          # total possible states
states = np.zeros((n_states, 2))    # array containing the coordinates of each state
rewards = np.zeros(n_states)        # contains rewards of each state, at the corresponding indexes
learning_rate = 1.0                 # alpha, ranging from 0 to 1
discount_factor = 0.95              # gamma, ranging from 0 to 1
# epsilon ranges between 1 and 0. 0 means no exploration, and only following the path with max Q value.
# higher epsilon means more random exploration
epsilon = 0.0
episodes = 0            # counts number of episodes/generations gone by
restart = True          # flag to reset the agent after each episode
start_time = 0          # stores the time stamp when episode starts
end_time = 0            # stores the time stamp when episode ends
delta_t = 0             # time for one episode stored here. start_time - end_time
time_elapsed = []       # time elapsed in each episode will be added to this list

# Object of the class Q learning
Q_obj = QLearning(learning_rate, discount_factor, states, rewards, n_states, n_actions)


# initializing the array states with all the possible coordinates on the board
def init_states(st, n_st):
    # initializing the states array
    m = 0
    p = 0
    for n in range(n_st):
        st[n][0] = m
        st[n][1] = p
        if p == 400:
            m += one_step
            p = 0
        else:
            p += 40


# initializing the rewards array
def init_rewards(rw):
    # the goal has a reward of 50. all the blue squares are out of bounds for the agent, having reward -1
    rw[0:9] = -1
    rw[10:131:11] = -1
    rw[112:120] = -1
    rw[11:121:11] = -1
    rw[19] = -1
    rw[30] = -1
    rw[22:27] = -1
    rw[28] = -1
    rw[39] = -1
    rw[50:54] = -1
    rw[72:76] = -1
    rw[46:49] = -1
    rw[57:101:11] = -1
    rw[67] = -1
    rw[4 + 66:4 + 66 + 33:11] = -1
    rw[5 + 88] = -1
    rw[6 + 88:6 + 88 + 22:11] = -1
    rw[8 + 88:8 + 88 + 22:11] = -1

    rw[1 + 99 + 11] = 50


# function which draws and paints in the window, rendering the images
@window.event
def on_draw():
    # clearing window, and redrawing everything
    window.clear()
    maze.draw()
    target.draw()
    agent.draw()


# handles key-presses to control speed of the agent
@window.event
def on_key_press(symbol, modifiers):
    global sleep_time
    # if + pressed, speed of agent increased. if - pressed, the agent slowed down. if Q pressed, print QTable
    if symbol == pyglet.window.key.NUM_ADD:
        if sleep_time > 0.2:
            sleep_time -= 0.1
        elif 0.02 < sleep_time <= 0.2:
            sleep_time -= 0.02
        print("----------------")
        print("Sleep Time: ", sleep_time)
        print("----------------")
    elif symbol == pyglet.window.key.NUM_SUBTRACT:
        if sleep_time < 0.1:
            sleep_time += 0.02
        elif 0.1 <= sleep_time < 1.5:
            sleep_time += 0.1
        print("----------------")
        print("Sleep Time: ", sleep_time)
        print("----------------")
    elif symbol == pyglet.window.key.Q:
        Q_obj.print_q_table()


# performing the action chosen by the agent
def new_possible_state(a, x, y):
    if a == 0:
        y += one_step
    elif a == 1:
        x += one_step
    elif a == 2:
        y -= one_step
    elif a == 3:
        x -= one_step
    return x, y


# giving the new coordinates to the agent
def update_agent(x, y):
    global agent
    agent.x = x
    agent.y = y


# finds the index of the element passed as the parameter, in the array
def extract_index(element, array):
    for i in range(len(array)):
        if array[i][0] == element[0] and array[i][1] == element[1]:
            return i


init_rewards(rewards)
init_states(states, n_states)


def event_loop(dt):
    global episodes, restart, start_time, end_time, delta_t
    # checking if episode has ended, and resetting the agent
    if restart:
        start_time = time()
        agent.x = start_state[0]
        agent.y = start_state[1]
        restart = False
        return
    
    # getting the index of the current state of the agent
    old_state = extract_index([agent.x, agent.y], states)

    # explore vs exploit
    prob = np.random.uniform(0, 1)
    if prob < epsilon:
        # explore
        act = randint(0, 3)
    else:
        # exploit, and follow the action with max Q value
        act = Q_obj.max_q_action(old_state)
    
    # next proposed state. Could be valid or invalid.
    possible_state = new_possible_state(act, agent.x, agent.y)

    # if agent goes out of the board, those are not possible states, and hence that action is discarded
    if possible_state[0] < 0 or possible_state[0] > 400 or possible_state[1] < 0 or possible_state[1] > 400:
        return

    # if the possible state is a valid state, then update the agent
    update_agent(possible_state[0], possible_state[1])
    
    # gets the index of the new state of the agent in the states array
    new_state = extract_index([agent.x, agent.y], states)

    Q_obj.update_q_table(old_state, act, new_state)

    # if the agent reaches the goal or steps on the blue squares, end the episode
    if rewards[new_state] == -1 or rewards[new_state] == 50:
        if rewards[new_state] == 50:
            print("In this episode, it reached the goal!")
        episodes += 1
        print('Episode', episodes)

        end_time = time()
        delta_t = end_time - start_time
        time_elapsed.append(delta_t)
        restart = True

    # to control the speed of the agent
    sleep(sleep_time)


pyglet.clock.schedule(event_loop)           # schedule the eventloop for continuous running
pyglet.app.run()                            # runs the application

# once the window is closed, this is run.
print("Episodes elapsed: ", episodes)       # prints the number of episodes elapsed
Q_obj.print_q_table()                       # prints the final Q Table

episode_array = [item for item in range(1, episodes+1)]     # creates the array of episodes, ranging starting from 1

# plots time vs episodes graph
plt.plot(episode_array, time_elapsed)
plt.xlabel('Episodes')
plt.ylabel('Time per Episode')
plt.show()


