# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    open = util.Stack()

    # Add a tuple that stores both the node, and the path to get to the node
    open.push((problem.getStartState(), []))
    closed = []

    while (not open.isEmpty()):
        # Remove the top node and add it to the closed list
        currentNode = open.pop()
        closed.append(currentNode[0])

        # If we are at the goal, return the path we took to the goal
        if problem.isGoalState(currentNode[0]):
            return currentNode[1]

        successors = problem.getSuccessors(currentNode[0])

        # For each node in the successors, check if it is in the closed list, and if not, put it on the stack
        for node in successors:
            if (node[0] not in closed):
                newEntry = (node[0],currentNode[1] + [node[1]])
                open.push(newEntry)

    return
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    open = util.Queue()

    # Add a tuple that stores both the node, and the path to get to the node
    open.push((problem.getStartState(), []))
    closed = []

    while (not open.isEmpty()):
        # Take the currentNode out of the Queue, then add the node to the closed list
        currentNode = open.pop()
        closed.append(currentNode[0])


        # If we reached our goal, return the path we took to get there
        if problem.isGoalState(currentNode[0]):
            return currentNode[1]

        successors = problem.getSuccessors(currentNode[0])

        # For each successor node, check if it is in the closed list, and if it is not,
        # then place the successor in the closed list, and add the new one to the closed list
        for node in successors:
            if (node[0] not in closed):
                newEntry = (node[0], currentNode[1] + [node[1]])
                closed.append(newEntry[0])
                open.push(newEntry)
    return
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    open = util.PriorityQueue()

    # Add a tuple that stores node, path to node, and cost to get to node
    open.push((problem.getStartState(), [], 0), 0)
    closed = []

    while (not open.isEmpty()):
        currentNode = open.pop()

        # If we are at the goal, return the path that got us there
        if problem.isGoalState(currentNode[0]):
            return currentNode[1]

        # Check if the currentNode is in closed, then if not, append it to closed
        # Then, add the children to the open list, if they are not already in the closed list
        if currentNode[0] not in closed:
            closed.append(currentNode[0])
            successors = problem.getSuccessors(currentNode[0])
            for node in successors:
                if node[0] not in closed:
                    newEntry = (node[0], currentNode[1] + [node[1]], currentNode[2] + node[2])
                    open.push(newEntry, newEntry[2])

    return
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    open = util.PriorityQueue()

    # Add a tuple that stores node, path to node, and cost to get to node. Cost in this case is UCS + Heuristic
    h = heuristic(problem.getStartState(), problem)
    # No cost for the start state
    g = 0
    # Combination of the Cost and the Heuristic, from class notes
    f = g + h

    # Push the starting node to the cue based on its f value. Note, we could replace f with 'h' at this starting point
    open.push((problem.getStartState(), [], f), f)
    closed = []

    while (not open.isEmpty()):
        currentNode = open.pop()

        # If we are at the goal, return the path that got us there
        if problem.isGoalState(currentNode[0]):
            return currentNode[1]

        # Check if node is closed, then if not, append it to the closed, and for each child,
        # determine if it is in closed, and if not, add it to the P-Queue based on its f function value
        if currentNode[0] not in closed:
            closed.append(currentNode[0])
            successors = problem.getSuccessors(currentNode[0])
            for node in successors:
                if node[0] not in closed:
                    h = heuristic(node[0], problem)
                    g = currentNode[2] + node[2]
                    f = h + g
                    newEntry = (node[0], currentNode[1] + [node[1]], g)
                    open.push(newEntry, f)

    return
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch