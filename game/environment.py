import random
import json
import numpy as np
from game.entities import *


class World:
    def __init__(self, dim_x=30, dim_y=30, n_fruits=30):
        self.time = 0
        self.dim_x, self.dim_y = dim_x, dim_y
        self.agents = {}
        self.n_fruits = n_fruits
        self.state = self.init_state(self.dim_x, self.dim_y)
    def init_state(self, dim_x, dim_y):
        board = np.zeros((dim_x, dim_y), dtype=int)
        board = self.create_borders(board)
        print("Dropping fruits")
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
    def add_agent(self, agent_id):
        agent = Agent(idx=agent_id, x=self.dim_x//2, y=self.dim_y//2)
        self.agents[agent.idx] = agent
        self.state[agent.y, agent.x] = agent.idx
    def remove_agent(self, agent_id):
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            self.state[agent.y, agent.x] = 0
    def spawn_fruit(self):
        fruit_x = random.randint(1, self.dim_x - 1)
        fruit_y = random.randint(1, self.dim_y - 1)
        if random.randint(1, 20) == 1 and self.state[fruit_y, fruit_x] == 0:
            self.state[fruit_y, fruit_x] = 2
    def step(self, actions):
        for agent_id, action in actions.items():
            agent = self.agents[agent_id]
            result = agent.act(action, self.state)
            print(f"{self.time}: Agent {agent.idx} {result}.")
        self.spawn_fruit()
        self.time += 1
    def get_world_state(self):
        world_state = {
            "time": self.time,
            "state": self.state.tolist(),
            "scores": {agent_id: agent.score for agent_id, agent in self.agents.items()}
        }
        return world_state
    def get_encoded_world_state(self):
        return bytes(json.dumps(self.get_world_state()), encoding='utf-8')
    def __repr__(self):
        assert self.state is not None
        return str(self.state)