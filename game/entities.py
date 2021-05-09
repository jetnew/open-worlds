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
    """Agent class that interacts in the environment."""
    def __init__(self, idx=9, x=1, y=1):
        """
        Initialise the agent with fixed parameters.
        """
        self.idx = idx
        self.x, self.y = x, y
        self.score = 0

    def nothing(self, state):
        """
        Do nothing as the action taken.
        Args:
            state:

        Returns:

        """
        return [Result.NOTHING]

    def left(self, state):
        """
        Move left as the action taken.
        Args:
            state: np.array - 2D array representing game state
        Returns:
            0 if failure, 1 if success
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
        """
        Move right as the action taken.
        Args:
            state: np.array - 2D array representing game state

        Returns:
            0 if failure, 1 if success
        """
        if self.check_wall(state, RIGHT):
            return [Result.FAIL]
        results = [Result.RIGHT]
        self.x += 1
        if self.check_fruit(state):
            results.append(Result.FRUIT)
            self.eat_fruit(state)
        return results

    def up(self, state):
        """
        Move up as the action taken.
        Args:
            state: np.array - 2D array representing game state

        Returns:
            0 if failure, 1 if success
        """
        if self.check_wall(state, UP):
            return [Result.FAIL]
        results = [Result.UP]
        self.y -= 1
        if self.check_fruit(state):
            results.append(Result.FRUIT)
            self.eat_fruit(state)
        return results

    def down(self, state):
        """
        Move down as the action taken.
        Args:
            state: np.array - 2D array representing game state

        Returns:
            0 if failure, 1 if success
        """
        if self.check_wall(state, DOWN):
            return [Result.FAIL]
        results = [Result.DOWN]
        self.y += 1
        if self.check_fruit(state):
            results.append(Result.FRUIT)
            self.eat_fruit(state)
        return results

    def act(self, action, state):
        """
        Take the action
        Args:
            action: int - action taken by the agent
            state: np.array - 2D array representing game state

        Returns:
            string - result having taken the action
        """
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
        """
        Eat fruit to obtain score of 1.
        Args:
            state: np.array - 2D array representing game state
        """
        self.score += FRUIT_SCORE

    def check_wall(self, state, action):
        """
        Check if taking an action in a given state would lead to a wall.
        Args:
            state: np.array - 2D array representing game state
            action: int - action taken by the agent

        Returns:
            True if agent would hit a wall else False
        """
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
        """
        Check if there exists a fruit at the agent's current position.
        Args:
            state: np.array - 2D array representing game state

        Returns:
            True if agent is on a fruit else False
        """
        return state[self.y, self.x] == FRUIT_ID

    def update_state(self, state):
        """
        Update the state with agent's identifier
        Args:
            state: np.array - 2D array representing game state
        """
        state[self.y, self.x] = self.idx
