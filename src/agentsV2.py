import random
from threading import Thread
from threading import Semaphore
import time
from draw_grid import drawGrid
from message import Message

class Agent(Thread):
    
    isMoving = Semaphore(1)
    imitTime = (30*60) # 30 minutes
    nbRow = None
    nbCol = None

    # Position of an agent
    agentDict = {}
    prevDict = {}
    messageStack = []

    # Stack of GRID
    pathFolder = 'tmp'
    pathFont = ''
    saveGrid = True
    gridStack = []  
    count = 1
    start_time = time.time()
    update_time = time.time()
    displayTime = 2     
    Terminated = False

    def defaultConfig():
        Agent.isMoving = Semaphore(1)
        Agent.limitTime = (30*60) # 30 minutes
        Agent.nbRow = None
        Agent.nbCol = None

        # Position of an agent
        Agent.agentDict = {}
        Agent.prevDict = {}
        Agent.messageStack = []

        # Stack of GRID
        Agent.pathFolder = 'tmp'
        Agent.pathFont = ''
        Agent.saveGrid = True
        Agent.gridStack = []  
        Agent.count = 1
        Agent.start_time = time.time()
        Agent.update_time = time.time()
        Agent.displayTime = 2     
        Agent.Terminated = False

    def generateInit(allTarget, numIteration=1000):
        # Generate a random possible initial position grid based on the target coordinates list
        i = 0
        dictInit = {target : target for target in allTarget}
        while i < numIteration:
            i = i + 1
            voids = Agent.getVoid(dictInit)
            for void in random.sample(voids, k=len(voids)):
                lsVoidNeighbors = []
                for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    neighborPos = (void[0] + newPos[0], void[1] + newPos[1])
                    if neighborPos in dictInit.values():
                        lsVoidNeighbors.append(neighborPos)
                if len(lsVoidNeighbors) != 0:
                    neighbor = random.choice(lsVoidNeighbors)
                    neighborTarget = [k for k, v in dictInit.items() if v == neighbor][0]
                    dictInit[neighborTarget] = void          
                    break
                continue
        return dictInit         

    def getVoid(dictInit):
        lsVoid = []
        for col in range(0, Agent.nbRow):
            for row in range(0, Agent.nbCol):
                if (col,row) not in dictInit.values():
                    lsVoid.append((col,row))
        return lsVoid
        
    def __init__(self, currentPosition, target) -> None:
        super().__init__()
        self.running = True
        # initial position
        self.currentPosition = currentPosition
        self.target = target
        Agent.agentDict[currentPosition] = self
        
    def run(self) -> None:
        while (time.time() - Agent.start_time < Agent.limitTime) and (not Agent.verifyRunning()):
            Agent.isMoving.acquire()
            self.move()
            Agent.isMoving.release()
            time.sleep(0.01)

            if Agent.saveGrid:
                if time.time() - Agent.update_time >= Agent.displayTime:
                    if Agent.prevDict != Agent.agentDict:
                        Agent.prevDict = Agent.agentDict.copy()
                        Agent.gridStack.insert(0, drawGrid(Agent))
                        Agent.count = Agent.count + 1
                    Agent.update_time = time.time()
                    
        
        if not Agent.Terminated:
            Agent.Terminated = True
            Agent.gridStack.insert(0, drawGrid(Agent))
            print('Time to Complete: ', time.time() - Agent.start_time)


    def verifyRunning():
        for agent in Agent.agentDict.values():
            if agent.currentPosition != agent.target:
                return False
        return True

    def move(self):
        if len(Agent.messageStack) == 0:
            # The stack is empty, the thread is the new master
            Agent.messageStack.append(Message(self, self, self.target))
            return 

        # The stack is not empty we need to check if the thread is the master
        # print(Agent.messageStack[0].sender, self)
        if Agent.messageStack[0].sender == self:
            # The thread is the master
            
            if self.currentPosition == self.target:
                # The agent has reached its target we can clear the stack
                Agent.messageStack = []
                return
            
            # The agent has not reached its target but it is not able to move
            if len(Agent.messageStack) == 1:
                closestPos = self.Astar(self.target)[1]
                if closestPos not in Agent.agentDict:
                    Agent.agentDict.pop(self.currentPosition)
                    self.currentPosition = closestPos
                    Agent.agentDict[self.currentPosition] = self
                
                    # print(closestPos in Agent.agentDict)
                    # print(self.currentPosition, self.target, closestPos)
                    # print( Agent.agentDict)

                    return
                else:          
                    # The master send a message to the closest agent on the best path to move
                    closestPos_path = Agent.agentDict[closestPos].getClosestVoid()
                    # print((self.currentPosition, self.target), closestPos, closestPos_path)
                    Agent.messageStack.append(Message(self, Agent.agentDict[closestPos_path[0]], closestPos_path[1]))
                    for i in range(len(closestPos_path[:-2])):
                        Agent.messageStack.append(Message(Agent.agentDict[closestPos_path[i]], Agent.agentDict[closestPos_path[i+1]], closestPos_path[i+2]))
                    return
                
        else:
            # The thread is not the master 
            if Agent.messageStack[-1].receiver == self:
                # print(Agent.messageStack[-1].receiver, self, Agent.messageStack[-1].position)
                # print(Agent.messageStack[-1].position, self.currentPosition)
                # print('----------------------')
                # # The thread is the receiver, we change the position of the agent to the new position
                Agent.agentDict.pop(self.currentPosition)
                self.currentPosition = Agent.messageStack[-1].position
                Agent.agentDict[self.currentPosition] = self
                
                # We delete the message from the stack
                Agent.messageStack.pop()
                return

    def getClosestVoid(self):
        lsVoid = []
        for col in range(0, Agent.nbRow):
            for row in range(0, Agent.nbCol):
                if (col,row) not in Agent.agentDict:
                    lsVoid.append((col,row))
        
        lsDistance = []
        for void in lsVoid:
            path_to_void = self.Astar(void)
            lsDistance.append((len(path_to_void), path_to_void))
        return random.choice(list(filter(lambda distInf : distInf == min(lsDistance, key=lambda x: x[0]), lsDistance)))[1]
                
    def Astar(self, targetPos): # A* algorithm
        dictGHF = dict({self.currentPosition : {'G': 0, 'H':0, 'F':0}})
        parent = dict({self.currentPosition : None})
        lsOpen = [self.currentPosition]
        lsClosed = []
            
        while len(lsOpen) > 0:
            choicePos = lsOpen[0]
            for pos in lsOpen:
                if dictGHF[pos]['F'] < dictGHF[choicePos]['F']:
                    choicePos = pos
            
            if choicePos == targetPos:
                path = []
                while choicePos != None:
                    path.append(choicePos)
                    choicePos = parent[choicePos]
                path.reverse()
                return path
        
            lsOpen.remove(choicePos)
            lsClosed.append(choicePos)
            
            for newPos in random.sample([(0, -1), (0, 1), (-1, 0), (1, 0)], k=4):
                neighborPos = (choicePos[0] + newPos[0], choicePos[1] + newPos[1])
                if neighborPos[0] < 0 or neighborPos[0] >= Agent.nbRow or neighborPos[1] < 0 or neighborPos[1] >= Agent.nbCol:
                    continue
                if neighborPos in lsClosed:
                    continue
                if neighborPos not in   Agent.agentDict:
                    newG = dictGHF[choicePos]['G'] + 1
                    newH = abs(neighborPos[0] - targetPos[0]) + abs(neighborPos[1] - targetPos[1])
                    newF = newG + newH
                else:
                    if Agent.agentDict[neighborPos] == Agent.messageStack[0].sender:
                        continue
                    difficulty = Agent.nbCol * Agent.nbRow
                    if Agent.agentDict[neighborPos].target == neighborPos:
                        difficulty += (max(Agent.nbCol, Agent.nbRow) * 2)
                    newG = dictGHF[choicePos]['G'] + difficulty
                    newH = abs(neighborPos[0] - targetPos[0]) + abs(neighborPos[1] - targetPos[1])
                    newF = newG + newH              
                    
                if neighborPos in lsOpen:
                    if dictGHF[neighborPos]['F'] > newF:
                        dictGHF[neighborPos] = dict({'G': newG, 'H': newH, 'F': newF})
                        parent[neighborPos] = choicePos
                else:
                    lsOpen.append(neighborPos)
                    dictGHF[neighborPos] = dict({'G': newG, 'H': newH, 'F': newF})
                    parent[neighborPos] = choicePos