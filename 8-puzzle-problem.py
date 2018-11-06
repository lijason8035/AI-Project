#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: JasonLi
"""

# Import Functions Needed for the Program
import copy
from collections import OrderedDict
import heapq

#Create Heuristic Function 
def hfunction(goal,array):
    #array = tuplearray[0]
    #Convert array into dictionary. Using Item as Key
    arrayd = {item: index for (index, item) in enumerate(array)}
    goald = {item: index for (index, item) in enumerate(goal)}
    total = 0;
    itemlist = list(arrayd.keys())
    #print (itemlist)
    itemlist.remove(0)
    #print (itemlist)
    #Calculate Sum of Manhattan distances of tiles from their goal position in a loop
    for item in itemlist:
        #print (goald.get(item),arrayd.get(item))
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
            #print (goald.get(item), arrayd.get(item), updown+leftright)
        else:
            updown = 0
            leftright = result
            #print (goald.get(item), arrayd.get(item), updown+leftright)
        total = total + updown+leftright
    return total

# Swap function for moving elements in the puzzle
def swap(dictS, orig, end):
    keys = list(dictS.keys())
    dictS[keys[orig]], dictS[keys[end]] = dictS[keys[end]], dictS[keys[orig]]
    return dictS

#Create eightpuzzle class
class eightpuzzle():
    def __init__(self,state1 = [],action1 = '',parent1 = None, hfun1 = 0,depth1 = 0):
        self.state = state1
        self.action = action1
        self.hfun = hfun1
        self.depth = depth1 #Keep track of g(n) which is also depth
        self.parent = parent1
    #Hashing tuple state in order to put into the dictionary later    
    def __hash__ (self):
        return hash(tuple(self.state))
    
    def __eq__(self, other):
        return (tuple(self.state) == tuple(other.state))
    
    def __ne__(self, other):
        return (tuple(self.state) != tuple(other.state))
    
    def __lt__(self,other):
        return (self.action<other.action)
    
    def state(self):
        return self.state

    def action(self):
        return self.action
    
    def hfun(self):
        return self.hfun
    
    def depth(self):
        return self.depth
    
    def parent(self):
        return self.parent
    
    def set_state(self,state2):
        self.state = state2
        
    def set_action(self,action2):
        self.action = action2
        
    def set_hfun(self, hfun2):
        self.hfun = hfun2
        
    def set_depth(self,depth2):
        self.depth = depth2
    
    def set_parent(self, parent2):
        self.parent = parent2

#Create 8 Puzzle Graph Search
class eightPuzzlegraph:
    def __init__(self):
        self.childarray = []#Children of current array
        self.element = None
        self.previous = -1 #Previous Position of X or zero
        
    
    def put(self,array):
        #Convert array into dictionary. Using Item as Key
        self.elements = {item: index for (index, item) in enumerate(array)}
        
    def get(self):
        return self.elements
    
    def child(self,eight):
        array= eight.state
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
                if abs(positionzero-ind)//3  + abs(positionzero-ind)%3  == 1:
                    movearray.append(ind)
        if self.previous in movearray: #If possible movement of X contains, previous position of X, then remove it
             movearray.remove(self.previous)
        #Create children arrays based on movearray and direction of X is moved
        #keep track of state
        for item in movearray:
            r = copy.deepcopy(self.elements)
            #list
            swapitem = swap(r, positionzero, item)
            childDict = OrderedDict(sorted(swapitem.items(), key=lambda x: x[1]))
            
            #action
            if (positionzero-item) == 3:
                resultd = 'U'
            elif (positionzero-item) == -3:
                resultd = 'D'
            elif (positionzero-item) == 1:
                resultd = 'L'
            elif (positionzero-item) == -1:
                resultd = 'R'
                
            r2 = eightpuzzle(list(childDict.keys()),resultd, eight)
            self.childarray.append(r2)
        self.previous = positionzero #Reset previous position of X or zero
        return self.childarray #Return Childarrays

#Create PriorityQueue for Graph Search
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def length(self):
        return len(self.elements)
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0) #Add starting array to queue
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    nodeindex = 0
    actions = []
    while not frontier.empty():
        current = frontier.get() #Get the current child
        if current == goal:
            actions.append(current.action)
            temp = current.parent
            while temp is not None:
                actions.append(temp.action)
                temp = temp.parent
            actions.remove('')
            nodeindex = nodeindex + 1
            break
        
        for next in graph.child(current): #Go through each Child
            new_cost = cost_so_far[current] +1
            if next not in cost_so_far or new_cost < cost_so_far[next]: #If child has not been visited or the cost is lower 
                cost_so_far[next] = new_cost
                next.set_depth(new_cost)
                priority = new_cost + hfunction(goal.state, next.state) 
                frontier.put(next, priority) #Add to the Queue
                next.set_hfun(priority)
                came_from[next] = current
                nodeindex = nodeindex + 1
    depthlevel = list(cost_so_far.keys())[-1].depth #Get the current element
    #Return depth, number of nodes and Actions taken in a string
    return depthlevel, nodeindex,' '.join(actions[::-1])


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
    inputfile = 'input4.txt'
    array, goal = readfile(inputfile)
    #print (array)
    #print (goal)
    ##################
    # Run A* Search #
    #################
    startnode = eightpuzzle(array)
    goalnode = eightpuzzle(goal)
    puzzle3 = eightPuzzlegraph()
    depth, numnode, actions = a_star_search(puzzle3, startnode,goalnode)
   # print (depth)
    #print (numnode)
    #print (actions)
    Outputfile = 'Output4.txt'
    write_to_file(Outputfile,array, goal,depth,numnode,actions)
 
    
if __name__== "__main__":
    main()