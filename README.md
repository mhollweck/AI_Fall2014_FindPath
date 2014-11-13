AI_Fall2014
===========

Source Code Infos

(1) General functions and classes
>>> Enum state: indicated all the different states we have at the fields
	state.g = goal state
	state.s = start state
	state.e = not visited field
	state.v = visited field, but not in the end path
	state.x = visited field within the end path
	state.o = obstacle
The state Enum is used for making it easier to compare between the different states.

>>> def parseArena(arena): converts the arena from string indications to the Enum state indications, f.e. state " " will be state.e or state "g" will be state.g
	
>>> def location(graph, st): return the location of a specific field (f.e. start field location or end field location) based on the input arena
param graph: arena
	param st: state which we want to find
	

>>> setArena(n, graph, i): marks the final path within the input graph with recursion
param n: current node (has the next node as argument)
param graph: arena
param i: dedicates the index of the next node at the n argument

>>> printArena(graph): creates a string with the final arena (included the final path and all the visited fields)

	
(4) A* functions
>>> contains(x, y, list): checks if the x,y node is within the input list	
>>> lowestOpenCost(openlist): returns the node with the lowest cost within the input list (used for openlist in A*)
>>> locToGoal(xs, ys, xg, yg): returns the estimated distance between two points with "Manhattan"-calculation

