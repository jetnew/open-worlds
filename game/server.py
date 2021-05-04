import time
import socket
import threading
from game.environment import *
from fastapi import FastAPI
import uvicorn

class GameServer:
    def __init__(self, host="", port=12345, dim_x=30, dim_y=30, n_fruits=30):
        self.host = host
        self.port = port
        self.actions = {}
        self.world = World(dim_x, dim_y, n_fruits)
        self.agent_ids = []
    def game_thread(self):
        while True:
            self.world.step(actions=self.actions)
            time.sleep(1)
    def start_game(self):
        threading.Thread(target=self.game_thread).start()
    def decode_action(self, response):
        return json.loads(response.decode('utf-8'))['action']
    def disconnect_player(self, address, agent_id):
        self.world.remove_agent(agent_id)
        self.agent_ids.remove(agent_id)
        print(f"Agent {agent_id} ({address[0]}:{address[1]}) has disconnected.")
    def connection_thread(self, connection, address, agent_id):
        self.world.add_agent(agent_id)
        with connection:
            while True:
                # Send world state and receive agent response
                encoded_state = self.world.get_encoded_world_state()
                try:
                    connection.send(encoded_state)
                    response = connection.recv(1024)
                except ConnectionResetError:
                    break
                if not response:
                    break

                # Execute action in game world
                action = self.decode_action(response)
                self.actions[agent_id] = action

                time.sleep(0.2)
        # Disconnect player
        self.disconnect_player(address, agent_id)
    def listen_for_clients(self):
        # Listener thread
        def client_listener():
            agent_id = 8
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                while True:
                    connection, address = s.accept()
                    print(f"Agent {agent_id} ({address[0]}:{address[1]}) has connected.")
                    self.agent_ids.append(agent_id)
                    threading.Thread(target=self.connection_thread, args=(connection, address, agent_id)).start()
                    agent_id += 1
        threading.Thread(target=client_listener).start()

game_server = GameServer(host="", port=12345, dim_x=30, dim_y=30, n_fruits=30)
game_server.start_game()
game_server.listen_for_clients()

app = FastAPI()

@app.get("/")
def read_root():
    return game_server.world.get_world_state()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)