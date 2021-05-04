import numpy as np
import pygame
import urllib.request
import json
import time

pygame.init()
display = pygame.display.set_mode((300, 300))

def get_game_array(url='http://127.0.0.1:8000/'):
    start = time.time()
    with urllib.request.urlopen(url) as r:
        response = r.read()
    end = time.time()
    print(f"Time: {end-start}")
    print(response)
    state = json.loads(response)
    game_state = state['state']
    game_array = np.array(game_state)
    game_array = 255 * game_array / game_array.max()
    return game_array

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Get game array
    game_array = get_game_array(url='http://127.0.0.1:8000/')

    # Display using PyGame
    surf = pygame.surfarray.make_surface(game_array)
    surf = pygame.transform.scale(surf, (300, 300))
    display.blit(surf, (0, 0))
    pygame.display.update()
    time.sleep(0.1)
pygame.quit()