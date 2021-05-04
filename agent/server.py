import random
from fastapi import FastAPI
from game.util import WorldModel
import uvicorn
import sys
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


if __name__ == "__main__":
    port = int(sys.argv[1])
    response = requests.post("http://127.0.0.1:8000/connect/", params=(('agent_api', str(port)),))
    print(f"Connection {json.loads(response.text)['result']}.")
    uvicorn.run(app, host="127.0.0.1", port=port)