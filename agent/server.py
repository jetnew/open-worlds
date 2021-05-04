import random
from fastapi import FastAPI
from game.util import WorldModel
import requests
import json
import os, psutil
get_ram = lambda: psutil.Process(os.getpid()).memory_info().rss // 1e6

app = FastAPI()

@app.get("/")
def read_root():
    return {"name": "random-agent"}

@app.post("/action/")
def get_action(state: WorldModel):
    print("Ram used:", get_ram())
    return {"action": random.randint(1, 4)}

@app.on_event("startup")  # For some reason Heroku runs this twice
def start_agent_server():
    port = int(os.environ.get('PORT', 5000))
    response = requests.post("https://open-worlds.herokuapp.com/connect/", params=(('agent_api', str(port)),))
    print(f"Connection {json.loads(response.text)['result']}.")
