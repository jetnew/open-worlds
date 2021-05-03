import time

from typing import List
from pydantic import BaseModel

from server.environment import *
from server.entities import *


# Random game (used as game thread)
def random_game(world):
    """Random game of 2 agents (8 and 9) to be run within a thread."""
    agent9 = Agent(idx=9, x=2, y=2)
    agent8 = Agent(idx=8, x=7, y=7)
    world.add_agent(agent9)
    world.add_agent(agent8)
    while True:
        # take random actions
        world.step(actions=[random.randint(0, 4), random.randint(0, 4)])
        time.sleep(1)


class WorldModel(BaseModel):
    """Pydantic model for FastAPI usage"""
    time: int
    state: List[list] = []
    scores: List[int] = []


def convert_world_model(world):
    """Convert the World object into a Pydantic object for FastAPI"""
    world_model = WorldModel(time=world.time,
                             state=world.state.tolist(),
                             scores=[agent.score for agent in world.agents])
    return world_model
