import random
import numpy as np
from game.entities import *


def get_coord_fruits(state):
    """
    Get coordinates of fruits given current game state.
    Args:
        state: np.array - 2D array representing game state

    Returns:
        List of x,y-coordinates of fruits
    """
    fruit_xs, fruit_ys = np.where(state == FRUIT_ID)
    return list(zip(fruit_xs, fruit_ys))


def get_distance(coord1, coord2):
    """
    Get the Manhattan distance between 2 coordinates.
    Args:
        coord1: tuple - (y, x) representing coordinates
        coord2: tuple - (y, x) representing coordinates

    Returns:
        int - Manhattan distance between 2 coordinates.
    """
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def get_action_towards(coord1, coord2):
    """
    Get the immediate action to go from coordinate 1 to coordinate 2.
    Args:
        coord1: tuple - (y, x) representing coordinates
        coord2: tuple - (y, x) representing coordinates

    Returns:
        int - Action taken to go from coordinate 1 to coordinate 2
    """
    if coord1[0] < coord2[0]:
        return DOWN
    elif coord1[0] > coord2[0]:
        return UP
    if coord1[1] < coord2[1]:
        return RIGHT
    elif coord1[1] > coord2[1]:
        return LEFT
    return NOTHING


class BaseAgent:
    def __init__(self, agent_idx):
        """
        Initialise base agent.
        Args:
            agent_idx: int - Agent identifier
        """
        self.agent_idx = agent_idx

    def get_coord_self(self, state):
        """
        Get coordinates for the agent itself.
        Args:
            state: np.array - 2D array representing game state

        Returns:
            Tuple - (y, x) representing coordinates of agent itself.
        """
        y, x = np.where(state == self.agent_idx)
        return list(zip(y, x))[0]

    def get_closest_fruit(self, state):
        """
        Get coordinates for the closest fruit to the agent.
        Args:
            state: np.array - 2D array representing game state

        Returns:
            Tuple - (y, x) representing coordinates of the closest fruit
        """
        coord_self = self.get_coord_self(state)
        coord_fruits = get_coord_fruits(state)
        if coord_fruits:
            return min(coord_fruits, key=lambda coord_fruit: get_distance(coord_self, coord_fruit))
        else:
            return None

    def get_action(self, state):
        """
        Get action given current game state.
        Args:
            state: np.array - 2D array representing game state

        Returns:
            int - action taken
        """
        return NotImplemented


class RandomAgent(BaseAgent):
    def get_action(self, state):
        """
        Return a random action no matter the game state.
        Args:
            state: np.array - 2D array representing game state

        Returns:
            int - action taken
        """
        return random.randint(0, 5)


class GreedyAgent(BaseAgent):
    def get_action(self, state):
        """
        Return a greedy action towards immediate nearest fruit.
        Args:
            state: np.array - 2D array representing game state

        Returns:
            int - action taken
        """
        coord_self = self.get_coord_self(state)
        coord_closest_fruit = self.get_closest_fruit(state)
        if coord_closest_fruit is not None:
            return get_action_towards(coord_self, coord_closest_fruit)
        else:
            return random.randint(0, 5)


