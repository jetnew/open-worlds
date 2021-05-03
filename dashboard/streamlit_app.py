import time
import json
import requests
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Open Worlds")
st_time = st.empty()
st_scores = st.empty()
st_state = st.empty()
fig, ax = plt.subplots()

headers = {
    'accept': 'application/json',
}

while True:
    # Query from server
    response = requests.get('http://localhost:8001/', headers=headers)
    state = json.loads(response.text)
    game_time = state['time']
    game_state = state['state']
    game_scores = [str(s) for s in state['scores']]

    # Display Streamlit elements
    st_time.text(f"Time: {game_time}")
    st_scores.text(f"Scores: {' '.join(game_scores)}")
    ax.imshow(np.array(game_state))
    st_state.pyplot(fig)

    time.sleep(0.1)
