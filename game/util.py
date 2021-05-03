from typing import List
from pydantic import BaseModel

class WorldModel(BaseModel):
    """Pydantic model for FastAPI usage"""
    time: int
    state: List[list] = []
    scores: List[int] = []


def convert_world_model(world):
    """Convert the World object into a Pydantic object for FastAPI"""
    world_model = WorldModel(time=world.time,
                             state=world.state.tolist(),
                             scores={agent_id: agent.score for agent_id, agent in world.agents.items()})
    return world_model