import random
import numpy as np
from game.entities import *


def get_coord_fruits(state):
    fruit_xs, fruit_ys = np.where(state == FRUIT_ID)
    return list(zip(fruit_xs, fruit_ys))


def get_distance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def get_action_towards(coord1, coord2):
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
        self.agent_idx = agent_idx

    def get_coord_self(self, state):
        x, y = np.where(state == self.agent_idx)
        return list(zip(x, y))[0]

    def get_closest_fruit(self, state):
        coord_self = self.get_coord_self(state)
        coord_fruits = get_coord_fruits(state)
        if coord_fruits:
            return min(coord_fruits, key=lambda coord_fruit: get_distance(coord_self, coord_fruit))
        else:
            return None

    def get_action(self, state):
        return NotImplemented


class RandomAgent(BaseAgent):
    def get_action(self, state):
        return random.randint(0, 5)


class GreedyAgent(BaseAgent):
    def get_action(self, state):
        coord_self = self.get_coord_self(state)
        coord_closest_fruit = self.get_closest_fruit(state)
        if coord_closest_fruit is not None:
            return get_action_towards(coord_self, coord_closest_fruit)
        else:
            return random.randint(0, 5)


