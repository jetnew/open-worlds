import json

class AgentDatabase:
    def __init__(self, dir="/game/database"):
        self.dir = dir
        self.stored_agent_apis = {}
        self.active_agent_apis = {}
    def get_stored_agent_apis(self):
        return self.stored_agent_apis.copy()
    def get_active_agent_apis(self):
        return self.active_agent_apis.copy()
    def save_agent_apis(self):
        with open(f'{self.dir}/agent_apis.json', 'w') as f:
            json.dump(self.stored_agent_apis, f, sort_keys=True, indent=4)
    def load_agent_apis(self):
        with open(f'{self.dir}/agent_apis.json', 'r') as f:
            self.stored_agent_apis = json.load(f)
        self.active_agent_apis = self.stored_agent_apis
    def activate_agent_api(self, agent_idx, agent_api):
        self.active_agent_apis[agent_idx] = agent_api
        if agent_idx not in self.stored_agent_apis:
            self.stored_agent_apis[agent_idx] = agent_api
    def deactivate_agent_api(self, agent_idx):
        self.active_agent_apis.pop(agent_idx)
    def is_agent_api_registered(self, agent_api):
        return agent_api in self.get_stored_agent_apis().values()
    def get_agent_idx_from_api(self, agent_api):
        for agent_idx, existing_api in self.get_stored_agent_apis().items():
            if agent_api == existing_api:
                return agent_idx
        raise Exception("Failed to get unregistered agent ID.")