import time
import json
import random
import socket

def random_policy(state):
    return random.randint(0,5)

def do_nothing_policy(state):
    return 0

class AgentClient:
    def __init__(self, host='127.0.0.1', port=12345, policy=random_policy):
        self.host = host
        self.port = port
        self.policy = policy  # given state, return action
    def decode_game_state(self, encoded_state):
        return json.loads(encoded_state.decode('utf-8'))
    def connect_to_server(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            while True:
                # Get full game state
                encoded_state = s.recv(4096)
                if not encoded_state:  # Ensure all bytes received
                    continue
                game_state = self.decode_game_state(encoded_state)

                # Send action
                action = self.policy(game_state)
                response = json.dumps({"action": action})
                s.send(bytes(response, encoding='utf-8'))


agent_client = AgentClient(host='127.0.0.1', port=12345, policy=random_policy)
agent_client.connect_to_server()
