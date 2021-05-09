import json


class AgentDatabase:
    """Temporary database class using JSON, before a database server is set up."""
    def __init__(self, dir="/database/database_server"):
        """
        Initialise the agent database at specified directory.
        Args:
            dir: str - Folder where .json is found
        """
        self.dir = dir
        self.stored_agent_apis = {}
        self.active_agent_apis = {}

    def get_stored_agent_apis(self):
        """
        Get the full list of agent apis.
        Returns:
            dict - Dictionary mapping agent id to agent api
        """
        return self.stored_agent_apis.copy()

    def get_active_agent_apis(self):
        """
        Get the full list of currently online agent apis.
        Returns:
            dict - Dictionary mapping agent id to agent api
        """
        return self.active_agent_apis.copy()

    def save_agent_apis(self):
        """
        Save all agent apis to the .json file.
        """
        with open(f'{self.dir}/agent_apis.json', 'w') as f:
            json.dump(self.stored_agent_apis, f, sort_keys=True, indent=4)

    def load_agent_apis(self):
        """
        Load all agent apis from the .json file
        """
        with open(f'{self.dir}/agent_apis.json', 'r') as f:
            self.stored_agent_apis = json.load(f)
        self.active_agent_apis = self.stored_agent_apis

    def activate_agent_api(self, agent_idx, agent_api):
        """
        Copy the agent api from full list to currently online list of agent apis.
        Args:
            agent_idx: int - agent identifier
            agent_api: str - agent api, e.g. "https://open-worlds-agents.herokuapp.com"
        """
        self.active_agent_apis[agent_idx] = agent_api
        if agent_idx not in self.stored_agent_apis:
            self.stored_agent_apis[agent_idx] = agent_api

    def deactivate_agent_api(self, agent_idx):
        """
        Remove the agent api from the online list of agent apis.
        Args:
            agent_idx: int - agent identifier
        """
        self.active_agent_apis.pop(agent_idx)

    def is_agent_api_registered(self, agent_api):
        """
        Check if the agent api exists in the full list of agent apis
        Args:
            agent_api: str - agent api, e.g. "https://open-worlds-agents.herokuapp.com"

        Returns:
            True if agent api exists in full list else False
        """
        return agent_api in self.get_stored_agent_apis().values()

    def get_agent_idx_from_api(self, agent_api):
        """
        Return the agent identifier given the agent api
        Args:
            agent_api: str - agent api, e.g. "https://open-worlds-agents.herokuapp.com"

        Returns:
            agent_id: int - agent identifier
        """
        for agent_idx, existing_api in self.get_stored_agent_apis().items():
            if agent_api == existing_api:
                return agent_idx
        raise Exception("Failed to get unregistered agent ID.")
