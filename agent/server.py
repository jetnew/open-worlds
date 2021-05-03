import random
from fastapi import FastAPI
from game.util import WorldModel

# FastAPI endpoint
app = FastAPI()

@app.get("/")
def read_root():
    return {"name": "random-agent"}

@app.post("/action/")
def get_action(state: WorldModel):
    return {"action": random.randint(0, 4)}
