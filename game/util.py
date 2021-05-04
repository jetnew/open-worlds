import time
import json
import requests

from typing import List, Dict
from pydantic import BaseModel

from game.environment import *
from game.entities import *


def random_game(world):
    """Random game of 2 agents (8 and 9) to be run within a thread."""
    world.add_agent(agent_id=8)
    world.add_agent(agent_id=9)
    while True:
        # take random actions
        world.step(actions=[random.randint(0, 4), random.randint(0, 4)])
        time.sleep(1)


def request_action(world, api="8002"):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    world_model = convert_world_model(world)
    data = world_model.json()
    response = requests.post("http://127.0.0.1:" + api + "/action/", headers=headers, data=data, timeout=(0.1,0.8)).text
    action = json.loads(response)['action']
    return action


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
