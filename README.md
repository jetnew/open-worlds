# Open Worlds [WIP]

Open Worlds is a MMO grid world game where players deploy agents to survive in an online world.

#### Play Now: [Open Worlds](https://share.streamlit.io/jetnew/open-worlds)

![image](assets/demo.gif)

## Why?
A game where players deploy [bots](https://en.wikipedia.org/wiki/Internet_bot) to play a game is not new (e.g. [screeps.com](https://screeps.com)), but because existing games host player-written scripts for the players, it is not scalable to the usage of [artificial intelligence](https://en.wikipedia.org/wiki/Deep_learning) techniques.
By allowing players to host their own scripts, gameplay can scale to complex emergent agent behaviors.

## Quickstart
```
git clone --recurse-submodules https://github.com/jetnew/open-worlds.git
pip install requirements.txt
uvicorn game.server:app --port 8000
streamlit run display/streamlit_app.py
python agent/server.py 8002
python agent/server.py 8003
```
By default, all services are hosted on localhost (127.0.0.1), the game server runs on port 8000, display server on port 8001, so agent servers should deploy on port 8002+.

## Server Deployment
Set web concurrency to 1 ([source](https://stackoverflow.com/questions/44292627/python-app-on-heroku-platform-seems-to-start-on-two-threads)):
```
heroku config:set -a <game server> WEB_CONCURRENCY=1
```
Use 2 procfiles for game and agent servers ([source](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-multi-procfile)):
```
heroku buildpacks:add -a <game server> heroku-community/multi-procfile
heroku buildpacks:add -a <agent server> heroku-community/multi-procfile
heroku config:set -a <game server> PROCFILE=Procfile
heroku config:set -a <agent server> PROCFILE=agent/Procfile
```