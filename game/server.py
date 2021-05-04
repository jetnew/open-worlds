import threading
from fastapi import FastAPI
import uvicorn
from game.util import *
import os
import psutil
get_ram = lambda: psutil.Process(os.getpid()).memory_info().rss // 1e6


class GameServer:
    def __init__(self):
        self.new_player_idx = 10
        print("Creating new world")
        self.world = World()
        self.agent_apis = {}
    # def start_game(self):
    #     print("Starting game")
    #     self.game = threading.Thread(target=self.run_game)
    #     self.game.start()
    def stop_game(self):
        self.play_game = False
        self.game.join()
    def request_thread(self, agent_idx, agent_api):
        try:
            action = request_action(self.world, api=agent_api)
            self.actions[agent_idx] = action
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            print(f"Player {agent_idx} ({agent_api}) disconnected.")
            self.world.remove_agent(agent_id=agent_idx)
            if agent_idx in self.actions:
                self.actions.pop(agent_idx)
    def run_game(self):
        """Game thread"""
        print("Starting game")
        # Initialise player list
        for agent_idx, agent_api in self.agent_apis.copy().items():
            self.world.add_agent(agent_id=agent_idx)

        self.play_game = True
        while self.play_game:
            self.actions = {}
            action_threads = []

            # Thread request actions
            for agent_idx, agent in self.world.agents.copy().items():
                agent_api = self.agent_apis[agent_idx]
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

@app.on_event("startup")  # For some reason Heroku runs this twice
def start_game_server():
    global game_server, heroku_thread
    game_server = GameServer()
    heroku_thread = threading.Thread(target=game_server.run_game)
    heroku_thread.start()

@app.on_event("shutdown")
def stop_game_server():
    global game_server
    game_server.stop_game()

@app.get("/")
def state():
    global game_server
    return game_server.world.get_world_state()

@app.post("/connect/")
def connect(agent_api: str):
    global game_server
    # Check if agent exists in database
    if agent_api in game_server.agent_apis.values():
        for agent_idx, existing_api in game_server.agent_apis.items():
            if agent_api == existing_api:
                game_server.world.add_agent(agent_id=agent_idx)
                print(f"Player {agent_idx} ({agent_api}) reconnected.")
                break
    else:
        # Register new agent
        game_server.world.add_agent(agent_id=game_server.new_player_idx)
        game_server.agent_apis[game_server.new_player_idx] = agent_api
        print(f"Player {game_server.new_player_idx} ({agent_api}) registered.")
        game_server.new_player_idx += 1
    return {"result": "success"}
