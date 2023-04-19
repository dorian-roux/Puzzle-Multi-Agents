#################################
# OPENING - PUZZLE MULTI-AGENTS #
#################################


# - IMPORTS -

# -- Add "src" folder to the system Paths --
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# -- General Libraries --
import random

# -- Custom Variables and Functions --
from agents import Agent



# - MAIN - 

if __name__ == '__main__':
    
    # Initialize the GRID information
    Agent.nbRow = Agent.nbCol = 5
    Agent.agendDict = {}

    allPosition = [(r,c) for r in range(Agent.nbRow+1) for c in range(Agent.nbCol+1)]
    allTarget = allPosition.copy()

    NUMBER_AGENT = 10
    MAX_AGENT = (Agent.nbRow + 1) * (Agent.nbCol + 1)
    NUMBER_AGENT = int(MAX_AGENT*0.8)
        
    for _ in range(NUMBER_AGENT):
        init = random.choice(allPosition)
        target = random.choice(allTarget)
        allPosition.remove(init)
        allTarget.remove(target)
        agent = Agent(init, target)

    AgentList = list(Agent.agentDict.values())
    InitList = list(Agent.agentDict.keys())

    for agent in AgentList:
        agent.start()

    Agent.showGrid()