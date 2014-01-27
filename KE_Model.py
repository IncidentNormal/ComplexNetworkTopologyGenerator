'''
Created on Jun 2, 2010

@author: duncantait
'''
import numpy as np
import random as rnd

class G():
    NUM_INITIAL_NODES = 10
    NUM_GEN_NODES = 90
    MEAN_DEGREE = 4
    MU = 0.2

class Node():
    def __init__(self,ID):
        self.ID = ID
        self.active = False

class NetworkCreation():
    def __init__(self):
        self.nodeList = []
        self.edgeList = []
    def createInitialNodes(self):
        for i in range(G.NUM_INITIAL_NODES):
            N = Node(i)
            N.active = True
            self.nodeList.append(N)
    def createGenNodes(self):
        for i in range(G.NUM_GEN_NODES):
            N = Node(i+G.NUM_INITIAL_NODES)
            print N.ID
            self.createGenEdges(N)
            N.active == True
            self.nodeList.append(N)
        activeList = [N for N in self.nodeList if N.active==True]
        for aN in activeList:
            rndDeac = rnd.randint(0,len(activeList)-1)
            activeList[rndDeac].active=False
            #randomly deactivate one, with variable probabilities.
            
    def createInitialEdges(self):
        for N1 in self.nodeList:
            for N2 in self.nodeList:
                if N1>N2:
                    addEdge = [N1.ID,N2.ID]
                    self.edgeList.append(addEdge)
                    
    def createGenEdges(self,node):
        activeList = [N for N in self.nodeList if N.active==True]
        for N in activeList:
            rndX = rnd.random()
            print rndX
            if rndX < G.MU:
                rndEdge=rnd.randint(0,len(self.nodeList)-1)
                newEdge=[node.ID,rndEdge]
                self.edgeList.append(newEdge)
            else:
                newEdge=[node.ID,N.ID]
                self.edgeList.append(newEdge)
                    
class RunMain():
    def __init__(self):
        Net = NetworkCreation()
        Net.createInitialNodes()
        Net.createInitialEdges()
        print Net.edgeList
        Net.createGenNodes()
        print Net.edgeList
        
R = RunMain()