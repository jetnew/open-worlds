import threading
from fastapi import FastAPI, Request
from game.util import *
from game.database.database import AgentDatabase
import os
import psutil
import uvicorn
get_ram = lambda: psutil.Process(os.getpid()).memory_info().rss // 1e6


class GameServer:
    def __init__(self, agent_database):
        self.new_player_idx = 10
        print("Creating new world")
        self.world = World()
        self.agent_database = agent_database
    def start_game(self):
        print("Starting game")
        self.game = threading.Thread(target=self.run_game)
        self.game.start()
    def stop_game(self):
        self.play_game = False
        self.game.join()
    def request_action(self, api="http://127.0.0.1:8002"):
        world_model = convert_world_model(self.world)
        data = world_model.json()
        response = requests.post(f"{api}/action/", data=data, timeout=(0.1, 0.8)).text
        # response = requests.post("https://open-worlds-agents.herokuapp.com/action/", data=data, timeout=(0.1, 0.8)).text
        return json.loads(response)['action']
    def request_thread(self, agent_idx, agent_api):
        try:
            action = self.request_action(api=agent_api)
            self.actions[agent_idx] = action
            self.agent_database.activate_agent_api(agent_idx, agent_api)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            print(f"Player {agent_idx} ({agent_api}) disconnected.")
            self.world.remove_agent(agent_id=agent_idx)
            if agent_idx in self.actions:
                self.actions.pop(agent_idx)
            self.agent_database.deactivate_agent_api(agent_idx)
    def run_game(self):
        """Game thread"""
        # Initialise player list
        for agent_idx, agent_api in self.agent_database.get_active_agent_apis().items():
            self.world.add_agent(agent_id=agent_idx)

        self.play_game = True
        while self.play_game:
            self.actions = {}
            action_threads = []

            # Thread request actions
            for agent_idx, agent in self.world.agents.copy().items():
                agent_api = self.agent_database.get_active_agent_apis()[agent_idx]
                t = threading.Thread(target=self.request_thread, args=(agent_idx, agent_api))
                t.start()
                action_threads.append(t)

            # Wait for all action threads to complete
            for t in action_threads:
                t.join()

            self.world.step(self.actions)
            time.sleep(0.5)

            # print(f"Ram used: {get_ram()}")

# FastAPI endpoint
app = FastAPI()

# WARNING: For some reason Heroku runs this twice, so run heroku config:set WEB_CONCURRENCY=1
# Source: https://stackoverflow.com/questions/44292627/python-app-on-heroku-platform-seems-to-start-on-two-threads
@app.on_event("startup")  # For some reason Heroku runs this twice
def start_game_server():
    global game_server
    agent_database = AgentDatabase("game/database")
    agent_database.load_agent_apis()
    game_server = GameServer(agent_database)
    game_server.start_game()

@app.on_event("shutdown")
def stop_game_server():
    global game_server
    game_server.stop_game()
    print("Saving")
    game_server.agent_database.save_agent_apis()

@app.get("/")
def state():
    global game_server
    return game_server.world.get_world_state()

@app.post("/connect/")
def connect(agent_api: str, request: Request):
    global game_server
    # Check if agent exists in database
    if game_server.agent_database.is_agent_api_registered(agent_api):
        agent_idx = game_server.agent_database.get_agent_idx_from_api(agent_api)
        game_server.agent_database.activate_agent_api(agent_idx, agent_api)
        game_server.world.add_agent(agent_id=agent_idx)
        print(f"Player {agent_idx} ({agent_api}) reconnected.")
    else:
        # Register new agent
        game_server.world.add_agent(agent_id=game_server.new_player_idx)
        game_server.agent_database.activate_agent_api(game_server.new_player_idx, agent_api)
        print(f"Player {game_server.new_player_idx} ({agent_api}) registered.")
        game_server.new_player_idx += 1
    return {"result": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)