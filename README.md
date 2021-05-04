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
uvicorn game.server:app --port 8000
streamlit run display/streamlit_app.py
python agent/server.py 8002
python agent/server.py 8003
```
By default, all services are hosted on localhost (127.0.0.1), the game server runs on port 8000, display server on port 8001, so agent servers should deploy on port 8002+.

## Server Deployment [WIP]
Set web concurrency to 1:
```
heroku config:set -a <game server> WEB_CONCURRENCY=1
```
Use 2 procfiles for game and agent servers:
```
heroku buildpacks:add -a <game server> heroku-community/multi-procfile
heroku buildpacks:add -a <agent server> heroku-community/multi-procfile
heroku config:set -a <game server> PROCFILE=Procfile
heroku config:set -a <agent server> PROCFILE=agent/Procfile
```