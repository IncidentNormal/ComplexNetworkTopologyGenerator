'''
Created on Jun 2, 2010

@author: duncantait
'''
import random as rnd
import math
import visual as v

class G():
    NUM_NODES = 20 #parameters, number of nodes
    MEAN_DEGREE = 4 #mean degree of node
    BETA = 0.2 #value of 'beta' (vital to algorithm)

class Node(): #Have a node class - multiple instances may be created
    def __init__(self,ID):
        self.ID = ID #Has attribute 'ID' to identify nodes

class NetworkCreation(): #class to control the creation of network topology
    def __init__(self):
        self.nodeList = [] #list of nodes (to be created and added to list)
        self.edgeList = [] #list of edges (ditto)
    def createNodes(self): #Method to create nodes
        for i in range(G.NUM_NODES): #Iteratively create nodes and append to list   
            N = Node(i)
            self.nodeList.append(N)
    def createEdges(self): #Method to create the edges between the nodes
        for N1 in self.nodeList:
            for N2 in self.nodeList: #every node vs every other node in list
                if (N1.ID-N2.ID)%G.NUM_NODES<=G.MEAN_DEGREE/2 and N1!=N2: #see notes (also, make sure not a self loop)
                    tupleEdge = [N1.ID,N2.ID] #create an edge in the form of a list of 2
                    self.edgeList.append(tupleEdge) #add this edge to the list 
    def rewireEdges(self): #Method to then rewire edges according to algorithm 
        for N in self.nodeList: #iterate through all nodes
            edges = [E for E in self.edgeList if E[0]==N.ID] #create list of edges currently attached to node
            for E in edges: #iterate through all edges in newly created list
                rnd_x = rnd.random() #create random number (0-1)
                if rnd_x<G.BETA: #compare to 'beta' parameter
                    selectableEdges = [i for i in range(G.NUM_NODES) if i!=N.ID and (N.ID,i) not in self.edgeList]
                    #create list of all edges the node could reattach to (according to algorithm rules - see notes)
                    rndSelect = rnd.randint(0,len(selectableEdges)-1) #select one randomly from this list
                    E[1]=selectableEdges[rndSelect] #replace old edge with this one
                    
class Visualise(): #class to visualise the nodes and edges created - circular structure.
    def __init__(self,net):
        self.sphereList = [] #list to hold the nodes (as vPython spheres)
        self.rodList = [] #list to hold the edges (as vPython cylinders)
        self.Net = net #NetworkCreation instance passed by reference
        print 'Start visualising'
        
        r = 1.0 #radius of circle that nodes are in
        delta_theta = (2.0*math.pi) / len(self.Net.nodeList) #calculate angle between nodes
        theta = 0 #start 'counter' theta at zero
         
        for N in self.Net.nodeList:
            sph = v.sphere(pos=v.vector(r*math.cos(theta),r*math.sin(theta),0),radius=0.015, color=v.color.green)
            #for each node create a sphere in a position on the circumference of the circle
            self.sphereList.append(sph) #add this sphere to the list
            theta += delta_theta #increment the angle by the calculated delta_theta
        for E in self.Net.edgeList: #for each edge...
            pos1 = self.sphereList[E[0]].pos #take positions of the corresponding nodes from the sphereList
            pos2 = self.sphereList[E[1]].pos
            rod = v.cylinder(pos=pos1,axis=pos2-pos1,radius=0.0025,color=v.color.white) 
            #create a vPython cylinder that stretches between the two nodes 
            self.rodList.append(rod) #add this cylinder to list
                    
class RunMain(): #class to run program in correct order
    def __init__(self):
        Net = NetworkCreation()
        Net.createNodes()
        Net.createEdges()
        Net.rewireEdges()
        V = Visualise(Net)
        print Net.edgeList
        
R = RunMain() #run program
                    
                    
                    
                
            
            
                    
                
                    
        
        

        
        