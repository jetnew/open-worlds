import random
from fastapi import FastAPI
from game.util import WorldModel
import requests
import json
import uvicorn
import os
import psutil

get_ram = lambda: psutil.Process(os.getpid()).memory_info().rss // 1e6

app = FastAPI()

@app.get("/")
def read_root():
    return {"name": "random-agent"}

@app.post("/action/")
def get_action(state: WorldModel):
    print("Ram used:", get_ram())
    return {"action": random.randint(1, 4)}

@app.on_event("startup")
def start_agent_server():
    # agent_api = "http://127.0.0.1:8002"  # for dev
    agent_api = "https://open-worlds-agents.herokuapp.com"
    # game = "http://127.0.0.1:8000"  # for dev
    game = "https://open-worlds.herokuapp.com"
    params = (
        ('agent_api', agent_api),
    )
    response = requests.post(f"{game}/connect/", params=params)
    print(f"Connection {json.loads(response.text)['result']}.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)