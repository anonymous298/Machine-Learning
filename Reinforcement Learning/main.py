# 1. It renders instances for 500 timesteps, performing random actions.
import gym
env = gym.make('Acrobot-v1')
env.reset()
for _ in range(500):
    env.render()
    env.step(env.action_space.sample())
# 2. To check all env available, uninstalled ones are also shown.
from gym import envs 
print(envs.registry.all())

import gym
env = gym.make('MountainCarContinuous-v0') # try for different environments
observation = env.reset()
for t in range(100):
        env.render()
        print( observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print( observation, reward, done, info)
        if done:
            print("Finished after {} timesteps".format(t+1))
            break

import gym
env = gym.make('CartPole-v0')
print(env.action_space) #[Output: ] Discrete(2)
print(env.observation_space) # [Output: ] Box(4,)
env = gym.make('MountainCarContinuous-v0')
print(env.action_space) #[Output: ] Box(1,)
print(env.observation_space) #[Output: ] Box(2,)