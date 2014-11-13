__author__ = "Maria Hollweck"
__email__ = "mh3478@columbia.edu"

import sys
sys.setrecursionlimit(1500)

#MH3478 START enum "state" for internal representation of states
from enum import Enum
from _overlapped import NULL
class state(Enum):
    e = 0
    s = 1
    o = 2
    g = 3
    x = 4
    v = 5

##### ARENA FUNCTIOONS ######
def parseArena(arena):
    graph = list()
    for i in arena:
        inner = list()
        for j in i:
            if j == " ":
                inner.append(state.e)
            elif j == "s":
                inner.append(state.s)
            elif j == "g":
                inner.append(state.g)
            elif j == "o":
                inner.append(state.o)
        graph.append(inner)
    return graph

def setArena(n, graph, i):
    while n[i] != 0:
        graph[n[0]][n[1]] = state.x
        return setArena(n[i], graph, i)
    
def printArena(graph):
    println = "" 
    pathcost = 0;
    for i in graph:
        for j in i:
            if j == state.e:
                println += " "
            elif j == state.g:
                println += "g"
            elif j == state.x:
                println += "*"
                pathcost += 1
            elif j == state.s:
                println += "s"
            elif j == state.o:
                println += "#"
            elif j == state.v:
                println += "v"
        println += "\n"
    return println, pathcost
#MH3478 END


# gets the point of a specific state, f.e. start or endpoint for the arena (indicated with state.)
def location(graph, st):
    a = 0
    for s in graph:
        a = a + 1
        b = 0
        for r in s:
            b = b + 1
            if r == st:
                return a - 1, b - 1 
   
    return 0, 0

#helperfunctions for ASTAR:

#locToGoal gets the estimated distance between two points with "Manhattan"-calculation
def locToGoal(xs, ys, xg, yg):
    return  ((abs(xg - xs)) + abs(yg - ys))    

#lowestOpenCost returns the lowest cost within a specific list (in astar used for openlist)
def lowestOpenCost(openlist):
    openlist = sorted(openlist, key=lambda o: o[2])
    return openlist, openlist[0];

def contains(x, y, list):
    for l in list:
        if l[0] == x and l[1] == y:
            return True
    return False
     
def dfs (x, y, graph):    
    numrows = len(graph)
    numcols = len(graph[0])
    
    # check the size of graph
    if x >= numrows or y >= numcols:
        return False

    # check if we're at the final position
    if graph[x][y] == state.g:
        #GOAL
        return True 
    
    noRows = 0;
    # 1st: right, 2nd: left, 3rd: up, 4th: down
    for i in [[x, y + 1, ],  [x, y - 1], [x - 1, y],  [x + 1, y]]:
            noRows += 1
            if i[0] < numrows and i[0] >= 0 and i[1] < numcols and i[1] >= 0:
                                     
                if graph[i[0]][i[1]] != state.o and graph[i[0]][i[1]] != state.x and graph[i[0]][i[1]] != state.v and graph[i[0]][i[1]] != state.s:
                    
                    if graph[i[0]][i[1]] == state.g:
                        #GOAL
                        return True 
                    
                    if graph[i[0]][i[1]] != state.s:  
                        graph[i[0]][i[1]] = state.x
                        
                    if dfs(i[0], i[1], graph): 
                        return True
    
    #if i visited all the 4 neighbours and there is no way to go on, mark as visited to prevent a loop
    if noRows == 4:
        graph[x][y] = state.v
        
    
from collections import deque        
def bfs (x, y, graph):
    
    #general initiatializing of variabls
    numrows = len(graph)
    numcols = len(graph[0])
    
    #queue for my items
    itemsQueue = deque()
    itemsQueue.append([x, y, NULL])
    
    while len(itemsQueue) > 0:
        n = itemsQueue.popleft()
        x = int(n[0])
        y = int(n[1])
        nState = graph[x][y]
        
        if nState == state.g:
            #GOAL
            return True
        
        # searching for the next item near to our current item (up, down, right, left)
        for i in [[x, y + 1], [x, y - 1], [x - 1, y], [x + 1, y]]:
            
            # check if the next item is still in our arena 
            if i[0] < numrows and i[0] >= 0 and i[1] < numcols and i[1] >= 0:
                # visit the node only if the node is no obstacle and has not been visited yet
                if graph[i[0]][i[1]] != state.o and graph[i[0]][i[1]] != state.v and graph[i[0]][i[1]] != state.s:
                    # when a goal was find, return true to stop the function
                    if graph[i[0]][i[1]] == state.g:
                        #GOAL
                        setArena(n, graph, 2)
                        return True 
                    
                    # if the goal was not find, we're setting the state to x (visited) and add the item to our graph
                    graph[i[0]][i[1]] = state.v
                    itemsQueue.append([i[0], i[1], n])
      
def astar(x, y, v, w, graph):
    
    open = list()
    closed = list()
    
    startX = x
    startY = y
   
    # estimated minimum costs without walls
    min = locToGoal(x, y, v, w)
    
    numrows = len(graph)
    numcols = len(graph[0])
    
    open.append([x, y, min, 0])
    
    while len(open) > 0:
        #setting the current node to the node with the lowest cost in our open list
        #AND sorting the open list from the smallest cost to the biggest cost
        open, current = lowestOpenCost(open)
        result = list()
        
        x = current[0]
        y = current[1]
         
        
        # is current location the goal?
        if graph[x][y] == state.g:
            #GOAL
            return True  
          
        if graph[x][y] != state.s:
            graph[x][y] = state.v
      
        #remove the item with the lowest cost 
        lastOpen = open.pop(0)
        closed.append([lastOpen[0], lastOpen[1]])
        
        #go through all the neighbours
        for i in [[x, y + 1, ], [x, y - 1], [x - 1, y], [x + 1, y]]:
            
            #and check if the index is okay in general
            if i[0] < numrows and i[0] >= 0 and i[1] < numcols and i[1] >= 0:
                  
                #but just in case there is no obstacle                           
                if graph[i[0]][i[1]] != state.o:
                    
                    #and my closed list doesn't contain my current object
                    if contains(i[0], i[1], closed) == False:
                        
                        if graph[i[0]][i[1]] == state.g:
                            #GOAL
                            v = [x, y, 0, current[3]]
                            setArena(v, graph, 3)
                            return True
                        
                        #calculating g and f cost
                        gCost = lastOpen[2] + 1
                        fCost = locToGoal(i[0], i[1], v, w)
                        
                        #check again if our current elemtn is not in the closed list
                        if contains(i[0], i[1], open) == False:
                            open.append([i[0], i[1], (gCost),current ])
     
                            
import argparse
parser = argparse.ArgumentParser(description='Robot Path Planning | HW 1 | COMS 4701')
parser.add_argument('-bfs', action="store_true", default=False , help="Run BFS on the map")
parser.add_argument('-dfs', action="store_true", default=False, help="Run DFS on the map")
parser.add_argument('-astar', action="store_true", default=False, help="Run A* on the map")
parser.add_argument('-all', action="store_true", default=False, help="Run all the 3 algorithms")
parser.add_argument('-m', action="store", help="Map filename")

results = parser.parse_args()

if results.m == "" or not(results.all or results.astar or results.bfs or results.dfs):
    print "Check the parameters : >> python hw1_UNI.py -h"
    exit()

if results.all:
    results.bfs = results.dfs = results.astar = True

# Reading of map given and all other initializations
try:
    with open(results.m) as f:
        arena = f.read()
except:
    print "Error in reading the arena file."
    exit()


#MH3478 START: for each called algorithm an own graph to safe capacity 
#graph will be edited with the path
    
if results.astar: 
    arenaAStar = parseArena(arena.split("\n")[:-1])
if results.dfs:
    arenaDFS = parseArena(arena.split("\n")[:-1])
if results.bfs:
    arenaBFS = parseArena(arena.split("\n")[:-1])

arena = arena.split("\n")[:-1]

#MH3478 END
  
# Internal representation  
print arena 

print "The arena of size " + str(len(arena)) + "x" + str(len(arena[0]))
print "\n".join(arena)


try:
    with open("output.txt", "a") as file:

        if results.bfs:
            # Call / write your BFS algorithm
        
            #x, y are our start location
            x, y = location(arenaBFS, state.s)
            bfs(x, y, arenaBFS)
            BFSout, BFScost = printArena(arenaBFS)
            file.write("BFS: " + str(BFScost) +"\n")
            file.write(BFSout)
    
        if results.dfs:
            # Call / write your DFS algorithm
            
            #x, y are our start location
            x, y = location(arenaDFS, state.s)
            dfs(x, y, arenaDFS)
            DFSOut, DFSCost = printArena(arenaDFS)
            file.write("\n\nDFS: " + str(DFSCost))
            file.write(DFSOut)
        
        if results.astar:
            # Call / write your A* algorithm
            
            #x, y are our start location
            x, y = location(arenaAStar, state.s)
            
            #v, z are our goal location
            v, w = location(arenaAStar, state.g)
            astar(x, y, v, w, arenaAStar)
            AStarOut, AStarCost = printArena(arenaAStar)
            file.write("\n\nAStar: " + str(AStarCost))
            file.write(AStarOut)   
                 
except IOError:
    print "IO error"
    
    
    

