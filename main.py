from game.environment import *
from game.entities import *

# World parameters
dim_x, dim_y = 10, 10
n_fruits = 20

# Initialise world
world = World()
agent9 = Agent(idx=9, x=2, y=2)
agent8 = Agent(idx=8, x=7, y=7)
world.add_agent(agent9)
world.add_agent(agent8)
print(world)

# Take 5 random steps
for i in range(5):
    action9 = random.randint(0,4)  # to obtain actions from player API calls
    action8 = random.randint(0,4)
    world.step(actions=[action9, action8])
print(world)

# Show player scores
for agent in world.agents:
    print(f"Agent {agent.idx} scored: {agent.score}.")