import threading
from fastapi import FastAPI

from util import *

# Start game thread
world = World()
game = threading.Thread(target=random_game, args=(world,))
game.start()

# FastAPI endpoint
app = FastAPI()

@app.get("/")
def read_root():
    world_model = convert_world_model(world)
    return world_model
