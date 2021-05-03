# Open Worlds

Open Worlds is a MMO grid world game where players deploy agents to survive in an online world.

## TL;DR: How it works
1. The server runs constantly with an internal clock.
2. At each tick, it attempts to call players' provided cURL where they deployed their agents.
3. Each cURL provides the agent's observation, and expects an action response.
4. The server then executes the collected actions in the online world.

## Game Mechanics
* The world is 10x10, where outermost rows and columns are wall borders.
* 20 fruits are randomly dropped on the map, each giving +1 score to the agent that lands on it.
* Players' actions are: move left, right, up or down.

## Quickstart
```
git clone https://github.com/jetnew/open-worlds.git
pip install requirements.txt
uvicorn server.server:app
```

## Upcoming Plans
In order of priority:
1. Deploy the server.
2. Deploy a bot agent.
3. Deploy the game display.
4. Accept players' agents via cURL.
5. Add more game mechanics.