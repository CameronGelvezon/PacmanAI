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
        score = 0
        food_list = newFood.asList()
        score -= len(food_list) * 2

        if newPos in food_list:
            score += 1
        else:
            score -= 1

        ghost_pos = []
        for ghost in newGhostStates:
            ghost_pos += [manhattanDistance(newPos, ghost.getPosition())]
        min_ghost = min(ghost_pos)
        if min_ghost <= 1:
            score -= 5

        if currentGameState.getWalls()[newPos[0]][newPos[1]] == True:
            score -= 1

        min_food = []
        for food in food_list:
            min_food += [manhattanDistance(newPos, food)]
        if len(min_food) != 0:
            score -= 0.1 * min(min_food)

        return score

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
        def value(state: GameState, agent, depth, action = []):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state), action
            
            if agent == 0:
                return max_value(state, agent, depth, action)
            
            else:
                return min_value(state, agent, depth, action)
            
        def max_value(state: GameState, agent, depth, action = []):
            v = float('-inf')
            temp = v

            for child in state.getLegalActions(agent):
                succ = state.generateSuccessor(agent, child)
                v = max(temp, value(succ, (agent + 1) % state.getNumAgents(), depth - 1)[0])

                if v > temp:
                    best = child
                    temp = v

            action.append(best)
            return v, action
        
        def min_value(state: GameState, agent, depth, action = []):
            v = float('inf')
            temp = v

            for child in state.getLegalActions(agent):
                succ = state.generateSuccessor(agent, child)
                v = min(temp, value(succ, (agent + 1) % state.getNumAgents(), depth - 1)[0])

                if v < temp:
                    best = child
                    temp = v

            action.append(best)
            return v, action
        
        return value(gameState, 0, self.depth * gameState.getNumAgents(), [])[1][0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def value(state: GameState, alpha, beta, agent, depth, action = []):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state), action
            
            if agent == 0:
                return max_value(state, alpha, beta, agent, depth, action)
            
            else:
                return min_value(state, alpha, beta, agent, depth, action)
            
        def max_value(state: GameState, alpha, beta, agent, depth, action = []):
            v = float('-inf')
            temp = v

            for child in state.getLegalActions(agent):
                succ = state.generateSuccessor(agent, child)
                v = max(temp, value(succ, alpha, beta, (agent + 1) % state.getNumAgents(), depth - 1)[0])
                
                if v > beta:
                    return v, action

                if v > temp:
                    best = child
                    temp = v

                alpha = max(alpha, v)

            action.append(best)
            return v, action
        
        def min_value(state: GameState, alpha, beta, agent, depth, action = []):
            v = float('inf')
            temp = v

            for child in state.getLegalActions(agent):
                succ = state.generateSuccessor(agent, child)
                v = min(temp, value(succ, alpha, beta, (agent + 1) % state.getNumAgents(), depth - 1)[0])

                if v < alpha:
                    return v, action
                if v < temp:
                    best = child
                    temp = v
                
                beta = min(beta, v)
                
            action.append(best)
            return v, action
        
        return value(gameState, float('-inf'), float('inf'), 0, self.depth * gameState.getNumAgents(), [])[1][0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def value(state: GameState, agent, depth, action = []):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state), action
            
            if agent == 0:
                return max_value(state, agent, depth, action)
            
            else:
                return exp_value(state, agent, depth, action)
            
        def max_value(state: GameState, agent, depth, action = []):
            v = float('-inf')
            temp = v

            for child in state.getLegalActions(agent):
                succ = state.generateSuccessor(agent, child)
                v = max(temp, value(succ, (agent + 1) % state.getNumAgents(), depth - 1)[0])

                if v > temp:
                    best = child
                    temp = v

            action.append(best)
            return v, action
        
        def exp_value(state: GameState, agent, depth, action = []):
            v = 0

            for child in state.getLegalActions(agent):
                succ = state.generateSuccessor(agent, child)
                p = 1/len(state.getLegalActions(agent))
                v += p * value(succ, (agent + 1) % state.getNumAgents(), depth - 1)[0]

            return v, action
        
        return value(gameState, 0, self.depth * gameState.getNumAgents(), [])[1][0]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
