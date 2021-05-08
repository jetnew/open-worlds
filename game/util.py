import time
from typing import List, Dict
from pydantic import BaseModel
from game.environment import *


def random_game(world):
    """Random game of 2 agents (8 and 9) to be run within a thread."""
    world.add_agent(agent_id=8)
    world.add_agent(agent_id=9)
    while True:
        # take random actions
        world.step(actions=[random.randint(0, 4), random.randint(0, 4)])
        time.sleep(1)


class WorldModel(BaseModel):
    """Pydantic model for FastAPI usage"""
    time: int
    state: List[list]
    scores: Dict[str, int]


def convert_world_model(world):
    """Convert the World object into a Pydantic object for FastAPI"""
    world_model = WorldModel(time=world.time,
                             state=world.state.tolist(),
                             scores={agent_id: agent.score for agent_id, agent in world.agents.items()})
    return world_model
