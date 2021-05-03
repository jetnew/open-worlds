import time
import json
import random
import socket

# Socket config
host = '127.0.0.1'
port = 12345

def get_action(state):
    return random.randint(0,5)

def decode_game_state(encoded_state):
    return json.loads(encoded_state.decode('utf-8'))

CONNECTED = False

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((host,port))

    while True:
        # Get game state
        encoded_state = s.recv(2048)
        if not encoded_state:
            time.sleep(0.1)
            continue

        print(encoded_state)
        game_state = decode_game_state(encoded_state)

        # Send action
        action = get_action(game_state)
        response = json.dumps({"action": action})
        s.send(bytes(response, encoding='utf-8'))

