# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"

        prevFoodList = currentGameState.getFood().asList()
        newFoodList = newFood.asList()
        GhostDist = sum(list(map(lambda x,y : 0 if manhattanDistance(x.getPosition(), newPos) >= 2 or y > 1 else 9999 , newGhostStates, newScaredTimes)))

        if successorGameState.isWin() and GhostDist == 0:
            return float("inf")
        foodDist = 0 if len(newFoodList) == 0 else min(list(map(lambda x: manhattanDistance(x, newPos), newFoodList)))
        foodEaten = len(prevFoodList) - len(newFoodList)
        return successorGameState.getScore() -(GhostDist + (foodEaten if foodEaten == 1 else foodDist))

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimaxHelp(agentIdx, depth, state, AgentsNum):
            actions = state.getLegalActions(agentIdx)

            if depth == 0 or len(actions) == 0:
                return self.evaluationFunction(state)
            scores = []
            for action in actions:
                successor = state.generateSuccessor(agentIdx, action)
                nextIdx = (agentIdx+1)%AgentsNum
                newDepth = depth - (1 if nextIdx == 0 else 0)
                recScore = minimaxHelp(nextIdx, newDepth, successor, AgentsNum)
                scores.append(((recScore[0] if type(recScore) == tuple else recScore), action))


            return (min if agentIdx > 0 else max)(scores, key=lambda x: x[0])
        return minimaxHelp(0, self.depth, gameState,gameState.getNumAgents())[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minimaxHelp(agentIdx, depth, state, AgentsNum, alpha, beta):
            actions = state.getLegalActions(agentIdx)
            
            if depth == 0 or len(actions) == 0:
                return self.evaluationFunction(state)
            scores = []
            if agentIdx == 0:
                v = float('-inf')
                for action in actions:
                    successor = state.generateSuccessor(agentIdx, action)
                    nextIdx = (agentIdx+1)%AgentsNum
                    newDepth = depth - (1 if nextIdx == 0 else 0)
                    recScore = minimaxHelp(nextIdx, newDepth, successor, AgentsNum, alpha, beta)
                    recScore = recScore[0] if type(recScore) == tuple else recScore
                    v =  max(v, recScore)
                    if v>beta:
                        return (v,action)
                    alpha = max(alpha, v)
                    scores.append((recScore, action))

            else:
                v = float('inf')
                for action in actions:
                    successor = state.generateSuccessor(agentIdx, action)
                    nextIdx = (agentIdx+1)%AgentsNum
                    newDepth = depth - (1 if nextIdx == 0 else 0)
                    recScore = minimaxHelp(nextIdx, newDepth, successor, AgentsNum, alpha, beta)
                    recScore = recScore[0] if type(recScore) == tuple else recScore
                    v =  min(v, recScore)
                    if v<alpha:
                        return (v,action)
                    beta = min(beta, v)
                    scores.append((recScore, action))

            return (min if agentIdx > 0 else max)(scores, key=lambda x: x[0])
        return minimaxHelp(0, self.depth, gameState,gameState.getNumAgents(), float('-inf'), float('inf'))[1]
class ExpectimaxAgent(MultiAgentSearchAgent):
    """4.0
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def avg(lst):
            lst = list(map(lambda l: l[0],lst))
            return sum(lst) / len(lst) 
        def minimaxHelp(agentIdx, depth, state, AgentsNum):
            actions = state.getLegalActions(agentIdx)

            # print(agentIdx)
            # print(depth)
            if depth == 0 or len(actions) == 0:
                return self.evaluationFunction(state)
            scores = []
            for action in actions:
                successor = state.generateSuccessor(agentIdx, action)
                nextIdx = (agentIdx+1)%AgentsNum
                newDepth = depth - (1 if nextIdx == 0 else 0)
                recScore = minimaxHelp(nextIdx, newDepth, successor, AgentsNum)
                scores.append(((recScore[0] if type(recScore) == tuple else recScore), action))

            if agentIdx == 0:
                return max(scores, key=lambda x: x[0])
            return avg(scores)
        
        return minimaxHelp(0, self.depth, gameState,gameState.getNumAgents())[1]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostDist = sum(list(map(lambda x,y : 0 if manhattanDistance(x.getPosition(), pacmanPos) > 3 or y >2 else 9999 , ghostStates, scaredTimes)))
    if currentGameState.isWin() and ghostDist == 0:
        return float("inf")
    foodList = currentGameState.getFood().asList()
    score = currentGameState.getScore()
    minDistToFood = 0 if len(foodList) == 0 else min(list(map(lambda x: manhattanDistance(x, pacmanPos), foodList)))
    foodLeft = len(foodList)
    return  score - (minDistToFood + foodLeft + ghostDist)
# Abbreviation
better = betterEvaluationFunction
