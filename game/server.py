import time
import json
import socket
import threading
from game.entities import *
from game.environment import *
from game.util import *
from fastapi import FastAPI

# World config
dim_x, dim_y = 20, 20
n_fruits = 20
actions = {}

def test_game(world):
    """Test game of 2 agents (8 and 9) to be run within a thread."""
    global actions
    while True:
        world.step(actions=actions)
        time.sleep(1)

# Start game thread
world = World(dim_x=dim_x, dim_y=dim_y, n_fruits=n_fruits)
game = threading.Thread(target=test_game, args=(world,))
game.start()


def get_world_state(world):
    world_state = {
        "time": world.time,
        "state": world.state.tolist(),
        "scores": {agent_id: agent.score for agent_id, agent in world.agents.items()}
    }
    return world_state

def encode_world_state(world_state):
    return bytes(json.dumps(world_state), encoding='utf-8')

def decode_action(response):
    return json.loads(response.decode('utf-8'))['action']

def disconnect_player(address, world, actions, player_id):
    actions.pop(player_id)
    world.agents.pop(player_id)
    print(f'Disconnected from: {address[0]}:{address[1]}')


# Connection Thread
def player_connection(connection, address, player_id):
    agent = Agent(idx=player_id, x=5, y=5)
    world.add_agent(agent)
    actions[player_id] = 0
    with connection:
        while True:
            # Send world state
            world_state = get_world_state(world)
            encoded_state = encode_world_state(world_state)

            # Delay before sending
            time.sleep(1)
            try:
                connection.send(encoded_state)
            except ConnectionResetError:
                break

            # Receive agent response
            response = connection.recv(1024)
            if not response:
                break

            # Execute action in game world
            action = decode_action(response)
            actions[player_id] = action

    # Disconnect player
    disconnect_player(address, world, actions, player_id)

# Connection config
host = ""
port = 12345

# Client listener
def client_listener():
    player_id = 8
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        while True:
            connection, address = s.accept()
            print(f"Connected to: {address[0]}:{address[1]}")
            threading.Thread(target=player_connection, args=(connection, address, player_id)).start()
            player_id += 1

threading.Thread(target=client_listener).start()

app = FastAPI()

@app.get("/")
def read_root():
    return get_world_state(world)
    # world_model = convert_world_model(world)
    # return world_model