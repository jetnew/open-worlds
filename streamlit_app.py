import time
import json
import requests
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import psutil
import pandas as pd
import cv2
import PIL

get_ram = lambda: psutil.Process(os.getpid()).memory_info().rss // 1e6


# Template
st.title("Open Worlds")
st.text("A MMO grid world game where players deploy agents to survive in an online world.")
st_time = st.empty()
st_scores = st.empty()
st.markdown("[Deploy an agent!](https://github.com/jetnew/open-worlds-agents)")
st_state = st.empty()
st.markdown("A game where players deploy [bots](https://en.wikipedia.org/wiki/Internet_bot) to play a game is not new (e.g. [screeps.com](https://screeps.com)), but because existing games host player-written scripts for the players, it is not scalable to the usage of [artificial intelligence](https://en.wikipedia.org/wiki/Deep_learning) techniques. By allowing players to host their own scripts, gameplay can scale to complex emergent agent behaviors.")
st.markdown("GitHub: [jetnew/open-worlds](https://github.com/jetnew/open-worlds)")

# Initialise
response = requests.get('https://open-worlds.herokuapp.com/')
state = json.loads(response.text)
game_state = state['state']

while True:
    # Query from server
    response = requests.get('https://open-worlds.herokuapp.com/')
    state = json.loads(response.text)
    game_time = state['time']
    game_state = np.array(state['state'], dtype=np.uint8)
    game_scores = state['scores']

    # Set agent scores in dataframe
    agent_idxs, agent_scores = [], []
    for idx, score in game_scores.items():
        agent_idxs.append(idx)
        agent_scores.append(score)
    df_game_scores = pd.DataFrame({
        "Agent": agent_idxs,
        "Score": agent_scores,
    })

    # Refresh Streamlit elements
    st_time.text(f"Time: {game_time}")
    st_scores.dataframe(df_game_scores)

    image = np.repeat(np.repeat(game_state, 15, axis=0), 15, axis=1)
    image *= 25
    image = cv2.applyColorMap(image, cv2.COLORMAP_HOT)
    st_state.image(image)

    time.sleep(0.1)
