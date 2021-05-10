import random
import numpy as np
import matplotlib.pyplot as plt
from opensimplex import OpenSimplex


def generate_points(state, n):
    """
    Randomly set coordinates in state to 1.
    Args:
        state: np.array - 2D array representing game state
        n: int - Number of points to set to 1

    Returns:
        state: np.array - 2D array representing updated game state
    """
    item_idx = []
    for i in range(n):
        item_x = random.randint(1, state.shape[0] - 1)
        item_y = random.randint(1, state.shape[1] - 1)
        item_idx.append(np.array([item_x, item_y]))
    item_idx = np.array(item_idx)
    state[item_idx[:, 1], item_idx[:, 0]] = 1


def generate_clusters(x_dim, y_dim):
    gen = OpenSimplex(seed=random.randint(0,1000))
    factor = (x_dim+y_dim) / 3
    grid = []
    for y in range(y_dim):
        row = []
        for x in range(x_dim):
            if gen.noise2d(x / factor, y / factor) < 0.5:
                row.append(1)
            else:
                row.append(0)
        grid.append(row)
    return np.array(grid)


if __name__ == "__main__":
    grid = generate_clusters(50, 50)
    plt.title("Lake Generation")
    plt.imshow(grid)
    print(grid)
    plt.show()
