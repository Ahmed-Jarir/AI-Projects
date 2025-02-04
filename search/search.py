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

    """
    "*** YOUR CODE HERE ***"

    def getGoalPath(moves, goalState):
        movesToGoal = [goalState]
        while movesToGoal[0][0] > 1:
            movesToGoal.insert(0, moves[movesToGoal[0][0]])
        return movesToGoal

    currentState = problem.getStartState()
    stack = util.Stack()
    stack.push([0 , [currentState, None, None]])
    visited = []
    moves   = {}

    i = 0
    while not stack.isEmpty():
        currentState = stack.pop()
        visited.append(currentState[1][0])

        i += 1
        moves[i] = currentState
         
        if problem.isGoalState(currentState[1][0]):

            GoalPath = getGoalPath(moves, currentState)
            return list(filter(lambda item: item is not None, map(lambda state: state[1][1],GoalPath)))

        for successor in problem.getSuccessors(currentState[1][0]):
            if successor[0] not in visited:
                stack.push([i, successor])
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    def getGoalPath(moves, goalState):
        movesToGoal = [goalState]
        while movesToGoal[0][0] > 1:
            movesToGoal.insert(0, moves[movesToGoal[0][0]])
        return movesToGoal

    currentState = problem.getStartState()
    queue = util.Queue()
    queue.push([0 , [currentState, None, None]])
    visited = []
    moves   = {}

    i = 0
    while not queue.isEmpty():

        currentState = queue.pop()
        if currentState[1][0] in visited:
            continue
        visited.append(currentState[1][0])

        i += 1
        moves[i] = currentState
         
        if problem.isGoalState(currentState[1][0]):

            GoalPath = getGoalPath(moves, currentState)
            return list(filter(lambda item: item is not None, map(lambda state: state[1][1],GoalPath)))
            
        for successor in problem.getSuccessors(currentState[1][0]):
            if successor[0] not in visited:
                queue.push([i, successor])
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    def getGoalPath(moves, goalState):
        movesToGoal = [goalState]
        while movesToGoal[0][0] > 1:
            movesToGoal.insert(0, moves[movesToGoal[0][0]])
        return movesToGoal

    currentState = problem.getStartState()
    queue = util.PriorityQueue()
    queue.push([0 , [currentState, None, 0]], 0)
    visited = []
    moves   = {}

    i = 0
    while not queue.isEmpty():

        currentState = queue.pop()
        if currentState[1][0] in visited:
            continue
        visited.append(currentState[1][0])

        i += 1
        moves[i] = currentState
         
        if problem.isGoalState(currentState[1][0]):

            GoalPath = getGoalPath(moves, currentState)
            return list(filter(lambda item: item is not None, map(lambda state: state[1][1],GoalPath)))

            
        for nextState, move, cost in problem.getSuccessors(currentState[1][0]):

            newCost = cost + currentState[1][2]
            queue.push([i, (nextState, move, newCost)], newCost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    def getGoalPath(moves, goalState):
        movesToGoal = [goalState]
        while movesToGoal[0][0] > 1:
            movesToGoal.insert(0, moves[movesToGoal[0][0]])
        return movesToGoal

    currentState = problem.getStartState()
    queue = util.PriorityQueue()
    queue.push([0 , [currentState, None, 0]], 0)
    visited = []
    moves   = {}

    i = 0
    while not queue.isEmpty():

        currentState = queue.pop()
        if currentState[1][0] in visited:
            continue
        visited.append(currentState[1][0])

        i += 1
        moves[i] = currentState
         
        if problem.isGoalState(currentState[1][0]):

            GoalPath = getGoalPath(moves, currentState)
            return list(filter(lambda item: item is not None, map(lambda state: state[1][1],GoalPath)))

            
        for nextState, move, cost in problem.getSuccessors(currentState[1][0]):

            newCost = cost + currentState[1][2]
            queue.push([i, (nextState, move, newCost)], newCost + heuristic(nextState, problem))
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
