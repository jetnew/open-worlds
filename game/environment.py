import random
import json
import numpy as np
from game.entities import *


class World:
    """Contain all internal world variables and dynamics."""
    def __init__(self, dim_x=30, dim_y=30, n_fruits=30):
        """
        Initialise the world with some parameters
        Args:
            dim_x: int - X dimension of grid world
            dim_y: int - Y dimension of grid world
            n_fruits: int - Number of fruits to initialise in worldgen
        """
        self.time = 0
        self.dim_x, self.dim_y = dim_x, dim_y
        self.agents = {}
        self.n_fruits = n_fruits
        self.state = self.init_state()

    def init_state(self):
        """
        Initialises the 2D grid representing game state
        """
        board = np.zeros((self.dim_x, self.dim_y), dtype=int)
        board = self.create_borders(board)
        board = self.drop_fruits(board, n=self.n_fruits)
        return board

    def create_borders(self, board):
        """
        Create the borders of the grid world, where walls are represented with 1.
        Args:
            board: np.array - 2D array representing game state

        Returns:
            Game state board updated with game border walls
        """
        board[0, :] = 1  # top wall
        board[-1, :] = 1  # bottom wall
        board[:, 0] = 1  # left wall
        board[:, -1] = 1  # right wall
        return board

    def drop_fruits(self, board, n):
        """
        Add fruits onto the board at world initialisation, where fruits are represented with 2.
        Args:
            board: np.array - 2D array representing game state
            n: int - number of fruits to drop

        Returns:
            Game state board updated with dropped fruits
        """
        fruit_idx = []
        for i in range(n):
            fruit_x = random.randint(1, self.dim_x - 1)
            fruit_y = random.randint(1, self.dim_y - 1)
            if board[fruit_y, fruit_x] == 0:
                fruit_idx.append(np.array([fruit_y, fruit_x]))
        fruit_idx = np.array(fruit_idx)
        board[fruit_idx[:, 0], fruit_idx[:, 1]] = 2
        return board

    def add_agent(self, agent_id):
        """
        Add an agent with its identifier.
        Args:
            agent_id: int - agent identifier
        """
        agent = Agent(idx=agent_id, x=self.dim_x // 2, y=self.dim_y // 2)
        self.agents[agent.idx] = agent
        self.state[agent.y, agent.x] = agent.idx

    def remove_agent(self, agent_id):
        """
        Remove an agent by its identifier.
        Args:
            agent_id: int - agent identifier
        """
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            self.state[agent.y, agent.x] = 0

    def spawn_fruit(self, prob=0.05):
        """
        Drop a fruit randomly on the board.
        """
        fruit_x = random.randint(1, self.dim_x - 1)
        fruit_y = random.randint(1, self.dim_y - 1)
        if random.random() < prob and self.state[fruit_y, fruit_x] == 0:
            self.state[fruit_y, fruit_x] = 2

    def step(self, actions):
        """
        Iterate over 1 game clock tick, updating the game state.
        Args:
            actions: dict - Dictionary mapping agent id (str) to respective actions (int)
        """
        for agent_id, action in actions.items():
            agent = self.agents[agent_id]
            result = agent.act(action, self.state)
            print(f"{self.time}: Agent {agent.idx} {result}.")
        self.spawn_fruit()
        self.time += 1

    def get_world_state(self):
        """
        Return the current state of the world.
        Returns:
            Dictionary mapping attribute (str) to various attributes
        """
        world_state = {
            "time": self.time,
            "state": self.state.tolist(),
            "scores": {agent_id: agent.score for agent_id, agent in self.agents.items()}
        }
        return world_state

    def __repr__(self):
        """
        Returns:
            String representation of current world state for debugging.
        """
        assert self.state is not None
        return str(self.state)


if __name__ == "__main__":
    world = World()
