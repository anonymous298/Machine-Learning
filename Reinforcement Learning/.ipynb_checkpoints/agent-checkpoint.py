import pygame
import numpy as np
import random

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SNAKE_SIZE = 20
FOOD_SIZE = 20
MOVE_STEP = 20

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RL Snake Agent")
clock = pygame.time.Clock()

class Environment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [np.array([WIDTH // 2, HEIGHT // 2])]
        self.food_pos = np.array([random.randint(0, (WIDTH - FOOD_SIZE) // MOVE_STEP) * MOVE_STEP,
                                  random.randint(0, (HEIGHT - FOOD_SIZE) // MOVE_STEP) * MOVE_STEP])
        self.direction = random.choice([0, 1, 2, 3])  # Initial direction: Up, Down, Left, Right
        self.state_space = (WIDTH // MOVE_STEP) * (HEIGHT // MOVE_STEP)
        self.action_space = 4  # Up, Down, Left, Right
        return self.get_state()

    def get_state(self):
        head_x = self.snake[0][0] // MOVE_STEP
        head_y = self.snake[0][1] // MOVE_STEP
        return head_x * (HEIGHT // MOVE_STEP) + head_y

    def step(self, action):
        if action == 0:  # Up
            self.direction = 0
        elif action == 1:  # Down
            self.direction = 1
        elif action == 2:  # Left
            self.direction = 2
        elif action == 3:  # Right
            self.direction = 3

        # Move the snake
        head = np.array(self.snake[0])
        if self.direction == 0:  # Up
            head[1] = max(0, head[1] - MOVE_STEP)
        elif self.direction == 1:  # Down
            head[1] = min(HEIGHT - SNAKE_SIZE, head[1] + MOVE_STEP)
        elif self.direction == 2:  # Left
            head[0] = max(0, head[0] - MOVE_STEP)
        elif self.direction == 3:  # Right
            head[0] = min(WIDTH - SNAKE_SIZE, head[0] + MOVE_STEP)

        reward = -1
        print(reward)
        done = False

        # Check if the snake eats the food
        if np.array_equal(head, self.food_pos):
            self.snake.insert(0, head)
            reward = 100
            self.food_pos = np.array([random.randint(0, (WIDTH - FOOD_SIZE) // MOVE_STEP) * MOVE_STEP,
                                      random.randint(0, (HEIGHT - FOOD_SIZE) // MOVE_STEP) * MOVE_STEP])
        else:
            self.snake.insert(0, head)
            self.snake.pop()

        # Check for collisions with walls
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            done = True
            reward = -100

        # Check for collisions with itself
        if len(self.snake) != len(set(tuple(x) for x in self.snake)):
            done = True
            reward = -100

        return self.get_state(), reward, done

    def render(self):
        screen.fill(BLACK)
        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, (*segment, SNAKE_SIZE, SNAKE_SIZE))
        pygame.draw.rect(screen, RED, (*self.food_pos, FOOD_SIZE, FOOD_SIZE))
        pygame.display.flip()

class QLearningAgent:
    def __init__(self, state_space, action_space, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995):
        self.state_space = state_space
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = np.zeros((state_space, action_space))

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_space - 1)
        else:
            return np.argmax(self.q_table[state])

    def learn(self, state, action, reward, next_state):
        predict = self.q_table[state, action]
        target = reward + self.discount_factor * np.max(self.q_table[next_state])
        self.q_table[state, action] += self.learning_rate * (target - predict)
        self.exploration_rate *= self.exploration_decay

# Main loop
def main():
    env = Environment()
    agent = QLearningAgent(env.state_space, env.action_space)

    num_episodes = 1000
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state
            env.render()
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

if __name__ == "__main__":
    main()
