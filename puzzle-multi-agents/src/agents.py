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
import re








    
class Agent(Thread):
    isMoving = Semaphore(1)
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
        self.currentPosition = currentPosition
        self.target = target
        Agent.agentDict[currentPosition] = self
        Agent.initAgentMessages()
    
    
        
    def run(self) -> None:
        time.sleep(1)
        while self.running == True:
            self.communicate()
            self.resonate()
            self.decide()
            self.act()
            self.move()
            time.sleep(0.1)

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
        currentDistance = self.distManathan()
        if currentDistance == 0:
            self.running = False
            Agent.isMoving.release()
            return
        else:
            possibleDirection = self.neighborsOccupation(self.currentPosition)
            if len(possibleDirection) == 0:
                Agent.isMoving.release()
            else:
                
                goodDirection = [(direction, sum(abs(current - target) for current, target in zip(direction, self.target))) for direction in possibleDirection]
                if len(goodDirection) != 0:
                    Agent.agentDict.pop(self.currentPosition)
                    newPosition = sorted(goodDirection, key=lambda t: t[1])[0][0]
                    self.currentPosition = newPosition
                    Agent.agentDict[self.currentPosition] = self
                    Agent.showGrid()
                    Agent.isMoving.release()
                else:
                    Agent.isMoving.release()
    
    
    def initAgentMessages():
        agentMessages = dict()
        for agentPosition in Agent.agentDict.keys():
            agentThread = re.findall(r'Thread-\d+', str(Agent.agentDict[agentPosition]))[0]
            agentMessages[agentThread]  = dict()
            for subAgentPosition in Agent.agentDict.keys():  
                subAgentThread = re.findall(r'Thread-\d+', str(Agent.agentDict[subAgentPosition]))[0]
                if agentPosition == subAgentPosition:
                    agentMessages[agentThread][subAgentThread] = dict({'LOG':[]})             
                    continue
                agentMessages[agentThread][subAgentThread] = dict({'MESSAGE' : '', 'LOG':[]})             
        Agent.messages = agentMessages
        
    
    def neighborsOccupation(self, currentPosition):
        cPos_y, cPos_x = currentPosition
        availableDirection = []
        if (0 <= cPos_y - 1 <= self.nbRow) and (0 <= cPos_x <= self.nbCol) and ((cPos_y - 1, cPos_x) not in self.agentDict):  # Verify TOP
            availableDirection.append(((cPos_y - 1), cPos_x))
        if (0 <= cPos_y + 1 <= self.nbRow) and (0 <= cPos_x <= self.nbCol) and ((cPos_y + 1, cPos_x) not in self.agentDict): # Verify BOTTOM
            availableDirection.append(((cPos_y + 1), cPos_x))
        if (0 <= cPos_y <= self.nbRow) and (0 <= (cPos_x + 1) <= self.nbCol) and ((cPos_y, cPos_x + 1) not in self.agentDict): # Verify RIGHT
            availableDirection.append((cPos_y, (cPos_x + 1)))
        if (0 <= cPos_y <= self.nbRow) and (0 <= (cPos_x - 1) <= self.nbCol) and ((cPos_y, cPos_x - 1) not in self.agentDict): # Verify LEFT
            availableDirection.append(((cPos_y), (cPos_x - 1)))
        return availableDirection

    
    def distManathan(self):
        currentPosition, targetPosition = self.currentPosition, self.target
        return sum(abs(current - target) for current, target in zip(currentPosition, targetPosition))
        
    def getNeighbors(self):
        currentPosition, targetPosition = self.currentPosition, self.target
        directNeighboors = []
        neighboorPositions = dict({
            'TOP': {'POSITION': (currentPosition[0] - 1, currentPosition[1]), 'DIST_MANATHAN': self.distManathan((currentPosition[0] - 1, currentPosition[1]), targetPosition)},
            'RIGHT': {'POSITION': (currentPosition[0] + 1, currentPosition[1]), 'DIST_MANATHAN': self.distManathan((currentPosition[0] + 1, currentPosition[1]), targetPosition)},
            'BOTTOM':{'POSITION': (currentPosition[0], currentPosition[1] - 1), 'DIST_MANATHAN': self.distManathan((currentPosition[0], currentPosition[1] - 1), targetPosition)},
            'LEFT': {'POSITION': (currentPosition[0], currentPosition[1] + 1), 'DIST_MANATHAN': self.distManathan((currentPosition[0], currentPosition[1] + 1), targetPosition)}
        })
        
        for nPos in neighboorPositions:
            if neighboorPositions[nPos]['POSITION'] in self.agentDict:
                directNeighboors.append(neighboorPositions[nPos])
        return sorted(directNeighboors, key=lambda k: k['DIST_MANATHAN'], reverse=False)
