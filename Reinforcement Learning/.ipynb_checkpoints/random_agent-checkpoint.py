import gym
import numpy as np

cliffEnv = gym.make('CliffWalking-v0')

done = False
state = cliffEnv.reset()

while not done:
    print(cliffEnv.render(mode='ansi'))
    action = np.random.randint(low=0, high=4, size=1)
    print(state, '->', action)
    state, reward, done, _ = cliffEnv.step(action)

cliffEnv.close()