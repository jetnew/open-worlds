import threading
from fastapi import FastAPI, Request
from game.util import *
from game.database.database import AgentDatabase
import os
import psutil
import uvicorn
import logging

logging.basicConfig(filename='debug.log', level='logging.DEBUG')
get_ram = lambda: psutil.Process(os.getpid()).memory_info().rss // 1e6


class GameServer:
    """Manage the game thread, connections and action requests."""

    def __init__(self, agent_database):
        self.new_player_idx = 10
        self.world = World()
        self.agent_database = agent_database

    def start_game(self):
        """
        Start a game thread
        """
        logging.info("Starting game thread.")
        self.game = threading.Thread(target=self.run_game)
        self.game.start()

    def stop_game(self):
        """
        Stop the game thread
        """
        logging.info("Stopping game thread.")
        self.play_game = False
        self.game.join()

    def connect_agent(self, agent_api):
        """
        Connect an agent's API to the agent database
        Args:
            agent_api: str - agent's API, e.g. https://open-worlds-agents.herokuapp.com
        """
        # Check if agent exists in database
        if self.agent_database.is_agent_api_registered(agent_api):
            agent_idx = self.agent_database.get_agent_idx_from_api(agent_api)
            self.agent_database.activate_agent_api(agent_idx, agent_api)
            self.world.add_agent(agent_id=agent_idx)
            logging.info(f"Player {agent_idx} ({agent_api}) reconnected.")
        else:
            # Register new agent
            self.world.add_agent(agent_id=self.new_player_idx)
            self.agent_database.activate_agent_api(self.new_player_idx, agent_api)
            logging.info(f"Player {self.new_player_idx} ({agent_api}) registered.")
            self.new_player_idx += 1

    def disconnect_agent(self, agent_idx, agent_api):
        """
        Disconnect an agent by internal agent index
        Args:
            agent_idx: int - agent's internal index, e.g. 10
            agent_api: str - agent's API, e.g. https://open-worlds-agents.herokuapp.com
        """
        logging.info(f"Player {agent_idx} ({agent_api}) disconnected.")
        self.world.remove_agent(agent_id=agent_idx)
        if agent_idx in self.actions:
            self.actions.pop(agent_idx)
        self.agent_database.deactivate_agent_api(agent_idx)

    def request_action(self, agent_idx, agent_api):
        """
        Request an agent's action from its API
        Args:
            agent_idx: int - agent's internal index, e.g. 10
            agent_api: str - agent's API, e.g. https://open-worlds-agents.herokuapp.com

        Returns:
            action: int - agent's action given the current state, e.g. 3
        """
        logging.info(f"Requesting action from {agent_api}")
        world_model = convert_world_model(self.world)
        data = world_model.json()
        try:
            response = requests.post(f"{agent_api}/action/", data=data, timeout=(0.1, 0.8)).text
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            self.disconnect_agent(agent_idx, agent_api)
            return

        if "action" not in json.loads(response):
            return json.loads(response)['action']
        else:
            self.disconnect_agent(agent_idx, agent_api)

    def request_thread(self, agent_idx, agent_api):
        """
        Thread for requesting an agent's action from its API
        Args:
            agent_idx: int - agent's internal index, e.g. 10
            agent_api: str - agent's API, e.g. https://open-worlds-agents.herokuapp.com
        """
        action = self.request_action(agent_idx, agent_api)
        if action is not None:
            self.actions[agent_idx] = action
            self.agent_database.activate_agent_api(agent_idx, agent_api)

    def run_game(self):
        """
        Game thread that runs the game loop
        """
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

            logging.debug(f"Ram used: {get_ram()}")


# FastAPI endpoint
app = FastAPI()


# WARNING: For some reason Heroku runs this twice, so run heroku config:set WEB_CONCURRENCY=1
# Source: https://stackoverflow.com/questions/44292627/python-app-on-heroku-platform-seems-to-start-on-two-threads
@app.on_event("startup")  # For some reason Heroku runs this twice
def start_game_server():
    """
    Starts the game server upon app startup.
    """
    global game_server
    logging.info("Starting up FastAPI.")
    agent_database = AgentDatabase("game/database")
    agent_database.load_agent_apis()
    game_server = GameServer(agent_database)
    game_server.start_game()


@app.on_event("shutdown")
def stop_game_server():
    """
    Stops the game server upon app shutdown.
    """
    global game_server
    logging.info("Shutting down FastAPI.")
    game_server.stop_game()
    game_server.agent_database.save_agent_apis()


@app.get("/")
def state():
    """
    Handles requests for the current game state.
    Returns:
        Current state of the game
    """
    global game_server
    logging.info("Received state request.")
    return game_server.world.get_world_state()


@app.post("/connect/")
def connect(agent_api: str, request: Request):
    """
    Connects an agent to the game server by its API.
    Args:
        agent_api:
        request:

    Returns:

    """
    logging.info(f"Received connection request from {agent_api}")
    global game_server
    game_server.connect_agent(agent_api)
    return {"result": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
