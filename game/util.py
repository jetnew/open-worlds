import time
import json
import requests

from typing import List
from pydantic import BaseModel

from game.environment import *
from game.entities import *


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


def test_game(world):
    """Test game that calls actions from test agent server."""
    agent_apis = ["http://localhost:8000/action/"]
    agent9 = Agent(idx=9, x=5, y=5)
    world.add_agent(agent9)
    while True:
        world.step(actions=[request_action(world, url=url) for url in agent_apis])
        time.sleep(1)

def request_action(world, url="http://localhost:8000/action/"):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    world_model = convert_world_model(world)
    data = world_model.json()
    response = requests.post('http://localhost:8000/action/', headers=headers, data=data).text
    action = json.loads(response)['action']
    return action


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
