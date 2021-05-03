import random
import numpy as np


dim_x, dim_y = 30, 30
n_fruits = 30

class World:
    def __init__(self, dim_x=dim_x, dim_y=dim_y, n_fruits=n_fruits):
        self.time = 0
        self.dim_x, self.dim_y = dim_x, dim_y
        self.agents = {}
        self.n_fruits = n_fruits
        self.state = self.init_state(self.dim_x, self.dim_y)
    def init_state(self, dim_x, dim_y):
        board = np.zeros((dim_x, dim_y), dtype=int)
        board = self.create_borders(board)
        board = self.drop_fruits(board, n=self.n_fruits)
        return board
    def create_borders(self, board):
        board[0, :] = 1  # top wall
        board[-1, :] = 1  # bottom wall
        board[:, 0] = 1  # left wall
        board[:, -1] = 1  # right wall
        return board
    def drop_fruits(self, board, n):
        fruit_idx = []
        for i in range(n):
            fruit_x = random.randint(1, self.dim_x-1)
            fruit_y = random.randint(1, self.dim_y-1)
            if board[fruit_y, fruit_x] == 0:
                fruit_idx.append(np.array([fruit_y, fruit_x]))
        fruit_idx = np.array(fruit_idx)
        board[fruit_idx[:,0], fruit_idx[:,1]] = 2
        return board
    def add_agent(self, agent):
        self.agents[agent.idx] = agent
        self.state[agent.y, agent.x] = agent.idx
    def step(self, actions):
        for agent_id, action in actions.items():
            agent = self.agents[agent_id]
            result = agent.act(action, self.state)
            print(f"{self.time}: Agent {agent.idx} {result}.")
        self.time += 1
    def __repr__(self):
        assert self.state is not None
        return str(self.state)
