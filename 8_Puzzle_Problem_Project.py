#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 17:54:31 2018

@author: JasonLi
"""
# Import Functions Needed for the Program
import copy
from collections import OrderedDict
import heapq
#import numpy as np

#Create Heuristic Function 
def hfunction(goal,tuplearray):
    array = tuplearray[0]
    #Convert array into dictionary. Using Item as Key
    arrayd = {item: index for (index, item) in enumerate(array)}
    goald = {item: index for (index, item) in enumerate(goal)}
    total = 0;
    itemlist = list(arrayd.keys())
    itemlist.remove(0)
    #Calculate Sum of Manhattan distances of tiles from their goal position in a loop
    for item in itemlist:
        result = abs(goald.get(item)-arrayd.get(item))
        if result >= 3:
            """
            Ex: Going from index 6 to 0
                move up/down: (6-0)//3 = 2
                move left/right = (6-0)%3 = 0
                Total Move will be 2 
            """
            updown = result//3
            leftright = result%3
        else:
            updown = 0
            leftright = result
        total = total + updown+leftright
    return total

# Swap function for moving elements in the puzzle
def swap(dictS, orig, end):
    keys = list(dictS.keys())
    dictS[keys[orig]], dictS[keys[end]] = dictS[keys[end]], dictS[keys[orig]]
    return dictS

#Create PriorityQueue for Graph Search
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]
    
#Create 8 Puzzle Graph Search
class eightPuzzlegraph:
    def __init__(self):
        self.elements = {} #Elements of the current array
        self.childarray = [] #Children of current array
        self.previous = 0 #Previous Position of X or zero
        self.direction = [] #Possible Movement of X or zero of the Children
        
    def empty(self):
        return len(self.elements) == 0
    
    def put(self,array):
        #Convert array into dictionary. Using Item as Key
        self.elements = {item: index for (index, item) in enumerate(array)}
        
    def get(self):
        return self.elements
    
    def child(self,tuplearray):
        array= tuplearray[0]
        self.elements = {item: index for (index, item) in enumerate(array)}
        positionzero = self.elements[0] #Find where X or zero is in the puzzle
        movearray = [] #Index of possible movement of X or zero of the children in the puzzle
        self.childarray = [] 
        self.direction = []
        for ind in range(0,9):
            #Find the possible movement of X or zero is only equal to 1
            if abs(positionzero-ind) == 1:
                if positionzero > ind:
                    if positionzero %3 != 0:
                        movearray.append(ind)
                elif positionzero < ind:
                    if ind %3 != 0:
                        movearray.append(ind)
            else:
          #      temp = abs(positionzero-ind)//3 
            #    temp2 = abs(positionzero-ind)%3 
                if abs(positionzero-ind)//3  + abs(positionzero-ind)%3  == 1:
                    movearray.append(ind)
        if self.previous in movearray: #If possible movement of X contains, previous position of X, then remove it
             movearray.remove(self.previous)
        #Create children arrays based on movearray and direction of X is moved
        for item in movearray:
            r = copy.deepcopy(self.elements)
            if (positionzero-item) == 3:
                resultd = 'U'
            elif (positionzero-item) == -3:
                resultd = 'D'
            elif (positionzero-item) == 1:
                resultd = 'L'
            elif (positionzero-item) == -1:
                resultd = 'R'
            swapitem = swap(r, positionzero, item)
            childDict = OrderedDict(sorted(swapitem.items(), key=lambda x: x[1]))
            self.childarray.append((list(childDict.keys()),resultd))
        self.previous = positionzero #Reset previous position of X or zero
        return self.childarray #Return Childarrays

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put((start,None), 0) #Add starting array to queue
    depthnode = 0 #Keep track of g(n) which is also depth
    f_cost = {} #Keep track of the total cost f(n)
    nodeindex = 0 #Number of Node generated
    f_cost[nodeindex] = 0 #f(n) is set to 0. It will be updated in the node
    actions = [] #Keep track of Actions Performed
    visited = {} #Keep track of visited node
    visited[nodeindex] = (start,None) #Add the first node as visited
    while not frontier.empty():
        current = frontier.get() #Get the current child
        #print(depthnode)
        #print(np.matrix(to_matrix(current[0]))) #Printing current matrix
        #print ('\n')
        actions.append(current[1]) #Adding action taken in the current node
        if current[0] == goal:
            nodeindex = nodeindex +1 #Since we started with node 0, total number will be: nodeindex +1
            break
        
        for next in graph.child(current): #Go through each Child
            f_cost[nodeindex] = depthnode
            new_cost = f_cost[nodeindex]+ 1
            if next not in visited.values() or new_cost < f_cost[nodeindex]: #If child has not been visited or the cost is lower 
                priority = new_cost + hfunction(goal, next) 
                f_cost[nodeindex] = priority #Add F_cost for the child
                frontier.put(next, priority) #Add to the Queue
                nodeindex = nodeindex + 1
                visited[nodeindex] = next #Add to visited dictionary
        depthnode = depthnode+1
    return depthnode, nodeindex,' '.join(actions[1::]) #Return depth, number of nodes and Actions taken in a string

###################
# Read Input File #
##################
def stringToarray(stringarray):
    array = []
    for item in stringarray:
        item = item.replace(" ", "")
        item2 = [x.strip() for x in item]
        for ind in range(0,3):
            array.append(int(item2[ind]))
    return array

def readfile(filename):
    with open(filename) as file:
        content = file.readlines()
    content = [x.strip() for x in content] 
    array = stringToarray(content[0:3])
    goal = stringToarray(content[4:8])
    file.close()
    return array, goal

#####################
# Write Output File #
#####################
def to_matrix(l):
    return [l[i:i+3] for i in range(0, len(l), 3)]

def write_to_file(filename,array, goal, depthlevel,numnodes,actionstaken):
    file = open(filename,'w')
    arrayMatrix = to_matrix(array)
    goalMatrix = to_matrix(goal)

    for item in range(0,3):
        result = ' '.join(str(x) for x in arrayMatrix[item])
        file.write(result+'\n') 
    file.write('\n')

    for item in range(0,3):
        result = ' '.join(str(x) for x in goalMatrix[item])
        file.write(result+'\n') 
    
    file.write('\n')
    file.write(str(depthlevel)+'\n')
    file.write(str(numnodes)+'\n')
    file.write(actionstaken+'\n')
    file.close()
    
def main():
    inputfile = 'input2.txt'
    array, goal = readfile(inputfile)
    ##################
    # Run A* Search #
    #################
    puzzle3 = eightPuzzlegraph()
    depth, nodes, actions = a_star_search(puzzle3, array,goal)
    outputfile = 'Output2.txt'
    write_to_file(outputfile,array,goal,depth,nodes,actions)
 
    
if __name__== "__main__":
    main()