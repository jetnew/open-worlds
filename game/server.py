import threading
from fastapi import FastAPI
import uvicorn
from game.util import *
import os, psutil
get_ram = lambda: psutil.Process(os.getpid()).memory_info().rss // 1e6

# Request action thread
def request_thread(world, actions, agent_idx, agent_api):
    try:
        action = request_action(world, api=agent_api)
        actions[agent_idx] = action
    except Exception as e:
        print(f"Player {agent_idx} ({agent_api}) disconnected.")
        world.remove_agent(agent_id=agent_idx)
        if agent_idx in actions:
            actions.pop(agent_idx)

# Game thread
def run_game(world):
    global agent_apis, new_player_idx

    # Initialise player list
    for agent_idx, agent_api in agent_apis.copy().items():
        world.add_agent(agent_id=agent_idx)

    while True:
        actions = {}
        action_threads = []

        # Thread request actions
        for agent_idx, agent in world.agents.copy().items():
            agent_api = agent_apis[agent_idx]
            t = threading.Thread(target=request_thread, args=(world, actions, agent_idx, agent_api))
            t.start()
            action_threads.append(t)

        # Wait for all action threads to complete
        for t in action_threads:
            t.join()

        world.step(actions)
        time.sleep(0.5)

        print(f"Ram used: {get_ram()}")


# FastAPI endpoint
new_player_idx = 10
app = FastAPI()

@app.get("/")
def state():
    return world.get_world_state()

@app.post("/connect/")
def connect(agent_api: str):
    global new_player_idx
    if agent_api in agent_apis.values():
        for agent_idx, existing_api in agent_apis.items():
            if agent_api == existing_api:
                world.add_agent(agent_id=agent_idx)
                print(f"Player {agent_idx} ({agent_api}) reconnected.")
                break
    else:
        world.add_agent(agent_id=new_player_idx)
        agent_apis[new_player_idx] = agent_api
        print(f"Player {new_player_idx} ({agent_api}) registered.")
        new_player_idx += 1
    return {"result": "success"}

if __name__ == "__main__":
    # Agent APIs
    agent_apis = {}

    # Start game thread
    world = World()
    game = threading.Thread(target=run_game, args=(world,))
    game.start()

    # Start FastAPI
    uvicorn.run(app, host="127.0.0.1", port=8000)