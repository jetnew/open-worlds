from enum import Enum

# Entity IDs
WALL_ID = 1
FRUIT_ID = 2

# Entity Scores
FRUIT_SCORE = 1

# Action IDs
NOTHING = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4


class Result(Enum):
    FAIL = "failed to act"
    NOTHING = "did nothing"
    LEFT = "moved left"
    RIGHT = "moved right"
    UP = "moved up"
    DOWN = "moved down"
    FRUIT = "ate fruit"


class Agent:
    def __init__(self, idx=9, x=1, y=1):
        self.idx = idx
        self.x, self.y = x, y
        self.score = 0

    def nothing(self, state):
        return [Result.NOTHING]

    def left(self, state):
        """
        Results:
        0 - failure
        1 - success
        """
        if self.check_wall(state, LEFT):
            return [Result.FAIL]
        results = [Result.LEFT]
        self.x -= 1
        if self.check_fruit(state):
            results.append(Result.FRUIT)
            self.eat_fruit(state)
        return results

    def right(self, state):
        if self.check_wall(state, RIGHT):
            return [Result.FAIL]
        results = [Result.RIGHT]
        self.x += 1
        if self.check_fruit(state):
            results.append(Result.FRUIT)
            self.eat_fruit(state)
        return results

    def up(self, state):
        if self.check_wall(state, UP):
            return [Result.FAIL]
        results = [Result.UP]
        self.y -= 1
        if self.check_fruit(state):
            results.append(Result.FRUIT)
            self.eat_fruit(state)
        return results

    def down(self, state):
        if self.check_wall(state, DOWN):
            return [Result.FAIL]
        results = [Result.DOWN]
        self.y += 1
        if self.check_fruit(state):
            results.append(Result.FRUIT)
            self.eat_fruit(state)
        return results

    def act(self, action, state):
        results = [Result.FAIL]
        state[self.y][self.x] = 0  # clear past position
        if action == NOTHING:
            results = self.nothing(state)
        elif action == LEFT:
            results = self.left(state)
        elif action == RIGHT:
            results = self.right(state)
        elif action == UP:
            results = self.up(state)
        elif action == DOWN:
            results = self.down(state)
        self.update_state(state)
        return ", ".join([r.value for r in results])

    def eat_fruit(self, state):
        self.score += FRUIT_SCORE

    def check_wall(self, state, action):
        if action == LEFT:
            return state[self.y, self.x - 1] == WALL_ID
        elif action == RIGHT:
            return state[self.y, self.x + 1] == WALL_ID
        elif action == UP:
            return state[self.y - 1, self.x] == WALL_ID
        elif action == DOWN:
            return state[self.y + 1, self.x] == WALL_ID
        raise Exception(f"Action movement invalid. Expected: [1, 2, 3, 4], Given: {action}")

    def check_fruit(self, state):
        return state[self.y, self.x] == FRUIT_ID

    def update_state(self, state):
        state[self.y, self.x] = self.idx
