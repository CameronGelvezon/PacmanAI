# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    closed_set = set()
    fringe = util.Stack()
    fringe.push(problem.getStartState())
    goal = False
    path_dictionary = {}
    if problem.isGoalState(problem.getStartState()):
        return []
    while not goal:
        node = fringe.pop()
        closed_set.add(node)
        if not problem.isGoalState(node):
            children = problem.getSuccessors(node)
            for child in children:
                if child[0] not in closed_set:
                    fringe.push(child[0])
                    path_dictionary[child[0]] = [node, child[1]]
        else:
            goal = True
   
    path = []
    while node != problem.getStartState():
        direct = path_dictionary[node][1]
        path.insert(0, direct)
        node = path_dictionary[node][0]
    return path

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    closed_set = set()
    fringe = util.Queue()
    fringe.push([problem.getStartState(), []])
    while True:
        if fringe.isEmpty():
            break
        node = fringe.pop()
        if problem.isGoalState(node[0]):
            break
        if node[0] not in closed_set:
            closed_set.add(node[0])
            children = problem.getSuccessors(node[0])
            for child in children:
                if child[0] not in closed_set:
                    fringe.push([child[0], node[1] + [child[1]]])
    path = node[1]
    return path

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    closed_set = set()
    fringe.push([problem.getStartState()], 0)
    path_dictionary = {}
    while True:
        if fringe.isEmpty():
            closed_set = set()
            break
        node = fringe.pop()
        if problem.isGoalState(node[0]):
            break
        if node[0] not in closed_set:
            closed_set.add(node[0])
            children = problem.getSuccessors(node[0])
            for child in children:
                if child[0] not in closed_set:
                    if node[0] == problem.getStartState():
                        fringe.update(child, child[2])
                        path_dictionary[child[0]] = [node[0], child[1], child[2]]
                    else:
                        fringe.update(child, path_dictionary[node[0]][2] + child[2])
                        if child[0] in path_dictionary and path_dictionary[child[0]][2] > path_dictionary[node[0]][2] + child[2]:
                            path_dictionary[child[0]] = [node[0], child[1], path_dictionary[node[0]][2] + child[2]]
                        elif child[0] not in path_dictionary:
                            path_dictionary[child[0]] = [node[0], child[1], path_dictionary[node[0]][2] + child[2]]
    path = []
    while node[0] != problem.getStartState():
        direct = path_dictionary[node[0]][1]
        path.insert(0, direct)
        node = path_dictionary[node[0]]
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    closed_set = set()
    fringe.push([problem.getStartState()], 0 + heuristic(problem.getStartState(), problem))
    path_dictionary = {}
    while True:
        if fringe.isEmpty():
            closed_set = set()
            break
        node = fringe.pop()
        if problem.isGoalState(node[0]):
            break
        if node[0] not in closed_set:
            closed_set.add(node[0])
            children = problem.getSuccessors(node[0])
            for child in children:
                cost = child[2] + heuristic(child[0], problem)
                if child[0] not in closed_set:
                    if node[0] == problem.getStartState():
                        fringe.update(child, cost)
                        path_dictionary[child[0]] = [node[0], child[1], child[2]]
                    else:
                        fringe.update(child, cost + path_dictionary[node[0]][2])
                        if child[0] in path_dictionary and path_dictionary[child[0]][2] > path_dictionary[node[0]][2] + cost:
                            path_dictionary[child[0]] = [node[0], child[1], path_dictionary[node[0]][2] + child[2]]
                        elif child[0] not in path_dictionary:
                            path_dictionary[child[0]] = [node[0], child[1], path_dictionary[node[0]][2] + child[2]]
    path = []
    while node[0] != problem.getStartState():
        direct = path_dictionary[node[0]][1]
        path.insert(0, direct)
        node = path_dictionary[node[0]]
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
