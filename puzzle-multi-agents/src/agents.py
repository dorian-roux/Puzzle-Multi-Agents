import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import random
from threading import Thread
from threading import Semaphore
import time
import sys

from color_print import ColorPrint as CP

class Agent(Thread):
    isMoving = Semaphore(1)

    # Position of an agent
    agentDict = {}

    nbRow = None
    nbCol = None

    def showGrid():        
        print("---------------------------------")
        for row in range(Agent.nbRow + 1):
            for col in range(Agent.nbCol + 1):
                if (row, col) in Agent.agentDict:
                    if (row, col) == Agent.agentDict[(row, col)].target:
                        CP.print_pass('X', end=" ")
                        continue
                    CP.print_fail('X', end=" ")
                    continue
                
                CP.print_bold(".", end=" ")
            print()
        print("---------------------------------")
        
        
    def __init__(self, currentPosition, target) -> None:
        super().__init__()
        self.running = True
        # initial position
        self.currentPosition = currentPosition
        self.target = target
        Agent.agentDict[currentPosition] = self

    def run(self) -> None:
        time.sleep(1)
        while self.running == True:
            self.communicate()
            self.resonate()
            self.decide()
            self.act()
            self.move()
            time.sleep(0.1)

            # if keyboard.is_pressed("q"):
            #     print("Exit")
            #     sys.exit()

    def communicate(self):
        pass
    
    def resonate(self):
        pass
    
    def decide(self):
        pass

    def act(self):
        pass

    def move(self):
        Agent.isMoving.acquire()       
        currentDistance = np.linalg.norm(np.array(self.currentPosition) - np.array(self.target))
        if currentDistance == 0:
            self.running = False
            Agent.isMoving.release()
            return
        else:
            possibleDirection = self.neighborsOccupation(self.currentPosition)
            if len(possibleDirection) == 0:
                Agent.isMoving.release()
            else:
                
                goodDirection = [(direction, np.linalg.norm(np.array(direction) - np.array(self.target))) for direction in possibleDirection]
                if len(goodDirection) != 0:
                    Agent.agentDict.pop(self.currentPosition)
                    newPosition = sorted(goodDirection, key=lambda t: t[1])[0][0]
                    # print("Agent", self.currentPosition,"moved to", newPosition)
                    self.currentPosition = newPosition
                    Agent.agentDict[self.currentPosition] = self
                    Agent.showGrid()
                    Agent.isMoving.release()
                else:
                    Agent.isMoving.release()
    
    def neighborsOccupation(self, currentPosition):
        possibleDirection = []
        if (currentPosition[0] + 1 <= Agent.nbRow) and (currentPosition[1] <= Agent.nbCol) and ((currentPosition[0] + 1, currentPosition[1]) not in Agent.agentDict):
            possibleDirection.append((currentPosition[0] + 1, currentPosition[1]))
        if (currentPosition[0] - 1 <= Agent.nbRow) and (currentPosition[1] <= Agent.nbCol) and ((currentPosition[0] - 1, currentPosition[1]) not in Agent.agentDict):
            possibleDirection.append((currentPosition[0] - 1,  currentPosition[1]))
        if (currentPosition[0] <= Agent.nbRow) and (currentPosition[1] + 1 <= Agent.nbCol) and ((currentPosition[0], currentPosition[1] + 1) not in Agent.agentDict):
            possibleDirection.append((currentPosition[0], currentPosition[1] + 1))
        if (currentPosition[0] <= Agent.nbRow) and (currentPosition[1] - 1 <= Agent.nbCol) and ((currentPosition[0], currentPosition[1] - 1) not in Agent.agentDict):
            possibleDirection.append((currentPosition[0], currentPosition[1] - 1))
        return possibleDirection



if __name__ == '__main__':
    Agent.nbRow = 5
    Agent.nbCol = 5
    Agent.agendDict = {}

    allPosition = [(r,c) for r in range(Agent.nbRow+1) for c in range(Agent.nbCol+1)]
    allTarget = allPosition.copy()

    NUMBER_AGENT = 15
    MAX_AGENT = Agent.nbRow * Agent.nbCol
    if NUMBER_AGENT > MAX_AGENT:
        NUMBER_AGENT = MAX_AGENT
        
    for _ in range(NUMBER_AGENT):
        init = random.choice(allPosition)
        allPosition.remove(init)

        target = random.choice(allTarget)
        allTarget.remove(target)

        agent = Agent(init, target)

    AgentList = list(Agent.agentDict.values())
    InitList = list(Agent.agentDict.keys())
    for init in InitList:
        print("Initial State:",init, "Target State:",Agent.agentDict[init].target)

    for agent in AgentList:
        agent.start()

    Agent.showGrid()