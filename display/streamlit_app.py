import time
import json
import requests
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os, psutil
get_ram = lambda: psutil.Process(os.getpid()).memory_info().rss // 1e6

st.title("Open Worlds")
st_time = st.empty()
st_scores = st.empty()
st_state = st.empty()
st_ram = st.empty()
fig, ax = plt.subplots()

response = requests.get('http://127.0.0.1:8000/')
state = json.loads(response.text)
game_state = state['state']
ax_obj = ax.imshow(np.array(game_state))

while True:
    # Query from server
    response = requests.get('http://127.0.0.1:8000/')
    state = json.loads(response.text)
    game_time = state['time']
    game_state = state['state']
    game_scores = [str(i) + ':' + str(s) for i, s in state['scores'].items()]

    # Display Streamlit elements
    st_time.text(f"Time: {game_time}")
    st_scores.text(f"Scores: {' '.join(game_scores)}")
    ax_obj.set_data(np.array(game_state))
    st_state.pyplot(fig)

    time.sleep(0.1)
    st_ram.text("Ram used: " + str(get_ram()))
