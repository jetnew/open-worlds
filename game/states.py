import random
import numpy as np
from game.procgen import generate_points, generate_clusters


class GameState:
    def __init__(self, shape=(30, 30)):
        self.x_dim, self.y_dim = shape
        self.state = np.zeros((self.y_dim, self.x_dim))

    def get(self):
        return self.state

    def query(self, x, y):
        return self.state[y, x]

    def __repr__(self):
        return str(self.state)


class BorderState(GameState):
    """
    Borders of the world.
    """
    def __init__(self, shape=(30, 30)):
        super().__init__(shape)

    def init_state(self):
        self.state[0, :] = 1  # top wall
        self.state[-1, :] = 1  # bottom wall
        self.state[:, 0] = 1  # left wall
        self.state[:, -1] = 1  # right wall


class LakeState(GameState):
    def __init__(self, shape=(30, 30)):
        super().__init__(shape)

    def init_state(self):
        self.state = generate_clusters(self.x_dim, self.y_dim)


class TreeState(GameState):
    def __init__(self, shape=(30, 30), initial=20):
        super().__init__(shape)
        self.initial = initial
        self.init_state()

    def init_state(self):
        generate_points(self.state, n=self.initial)


class FruitState(GameState):
    def __init__(self, shape=(30, 30), initial=30, droprate=0.05):
        super().__init__(shape)
        self.initial = initial
        self.droprate = droprate
        self.init_state()

    def init_state(self):
        generate_points(self.state, n=self.initial)

    def step(self):
        if random.random() < self.droprate:
            x, y = random.randint(0, self.x_dim), random.randint(0, self.y_dim)
            self.state[y, x] = 1


if __name__ == "__main__":
    x_dim, y_dim = 10, 10
    n_trees = 20
    n_fruits = 30

    lake_state = LakeState(shape=(x_dim, y_dim))
    print(lake_state)

    tree_state = TreeState(shape=(x_dim, y_dim), initial=n_trees)
    print(tree_state)

    fruit_state = FruitState(shape=(x_dim, y_dim), initial=n_fruits)
    print(fruit_state)






