# Open Worlds [WIP]

Open Worlds is a MMO grid world game where players deploy agents to survive in an online world.

![image](assets/demo.gif)

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
python game/server.py
streamlit run display/streamlit_app.py
python agent/server.py 8002
python agent/server.py 8003
```
By default, all services are hosted on localhost (127.0.0.1), the game server runs on port 8000, display server on port 8001, so agent servers should deploy on port 8002+.

## Upcoming Plans
In order of priority:
1. Improve game display latency.
2. Log running time for each component.
3. Add more game mechanics.
