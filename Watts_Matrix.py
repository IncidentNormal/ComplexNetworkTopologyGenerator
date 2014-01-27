'''
Created on Jun 2, 2010

@author: duncantait
'''
import random as rnd
import numpy as np
import networkx as nx

class G():
    NUM_NODES = 10 #parameters, number of nodes
    MEAN_DEGREE = 4 #mean degree of node
    BETA = 0.99 #value of 'beta' (vital to algorithm)
    Clust=0
    Path=0

class Node(): #Have a node class - multiple instances may be created
    def __init__(self,ID):
        self.ID = ID #Has attribute 'ID' to identify nodes

class NetworkCreation(): #class to control the creation of network topology
    def __init__(self):
        self.graphMatrix = np.zeros((G.NUM_NODES,G.NUM_NODES)) #list of nodes (to be created and added to list)
    def createEdges(self): #Method to create the edges between the nodes
        for N1 in range(G.NUM_NODES):
            for N2 in range(G.NUM_NODES): #every node vs every other node in matrix
                if (N1-N2)%G.NUM_NODES<=G.MEAN_DEGREE/2 and N1!=N2: #see notes (also, make sure not a self loop)
                    self.graphMatrix[N1,N2] = 1 #create an edge by putting a 1 at the co-ordinate N1,N2 in matrix
        self.graphMatrix = self.graphMatrix + self.graphMatrix.conj().transpose() #make matrix symmetrical
        for N1 in range(G.NUM_NODES): #delete half the matrix to make it directional for next part:
            for N2 in range(G. NUM_NODES):
                if N2 < N1:
                    self.graphMatrix[N1,N2] = 0
    def rewireEdges(self): #Method to then rewire edges according to algorithm 
        for N in range(G.NUM_NODES): #iterate through all nodes
            row = self.graphMatrix[N]
            idx = [i for i, x in enumerate(row) if x==1]  #list of indices of edges for current node
            for E in idx: #iterate through all edges in newly created list
                rnd_x = rnd.random() #create random number (0-1)
                if rnd_x<G.BETA: #compare to 'beta' parameter
                    selectableEdges = [i for i in range(G.NUM_NODES) if i!=E and self.graphMatrix[i,E] ==0 and self.graphMatrix[E,i] ==0] 
                    #create list of all edges the node could reattach to (according to algorithm rules - see notes)
                    self.graphMatrix[N,E] = 0
                    rndSelect = rnd.randint(0,len(selectableEdges)-1) #select one randomly from this list
                    self.graphMatrix[N,selectableEdges[rndSelect]]=1 #replace old edge with this one
        self.graphMatrix = self.graphMatrix + self.graphMatrix.conj().transpose()
        for f1 in range(G.NUM_NODES): #Make all values 1 (some may have become 2's as a side effect of transposing)
            for f2 in range(G.NUM_NODES):
                if self.graphMatrix[f1,f2]>1:
                    self.graphMatrix[f1,f2]=1
        print self.graphMatrix
        nxG = nx.from_numpy_matrix(self.graphMatrix)
        res = nx.clustering(nxG)
        runningAve = 0
        for i in range(len(res)):
            runningAve += res[i]
        G.Clust += runningAve/len(res)
        
        res = nx.shortest_path_length(nxG)
        for k, v in res.items():
            for k1, v1 in v.items():
                G.Path += v1
        #print "Clustering Coefficient=", runningAve/len(res)
            

                    
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
        for i in range(1000):
            Net = NetworkCreation()
            Net.createEdges()
            Net.rewireEdges()
        print "coeff=", G.Clust
        print "shortest_path=", G.Path
#        V = Visualise(Net)
#        print Net.edgeList
        
R = RunMain() #run program      
        