import numpy as np
import pygame
import requests
import json

pygame.init()
display = pygame.display.set_mode((300, 300))

def get_game_array(url='http://localhost:50500/'):
    response = requests.get(url, headers={'accept': 'application/json'})
    state = json.loads(response.text)
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
    game_array = get_game_array(url='http://localhost:50500/')

    # Display using PyGame
    surf = pygame.surfarray.make_surface(game_array)
    surf = pygame.transform.scale(surf, (300, 300))
    display.blit(surf, (0, 0))
    pygame.display.update()
pygame.quit()