from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
    
class ReflexAgent(Agent):
    def getAction(self, gameState):
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        BestScore = 0

        # Current food list
        currentFood = currentGameState.getFood().asList()

        for i in range(len(newGhostStates)):
            distanceAWay = manhattanDistance(
                newPos, newGhostStates[i].getPosition())

            # Eat Food >> Good
            if newPos in currentFood:
                BestScore += 1

            # Eat ghost
            if distanceAWay <= newScaredTimes[i]:
                BestScore += distanceAWay

            # Run away
            if distanceAWay < 2:
                BestScore -= 2

            # Add minimum distance to the nearest food using euclideanDistance to improve score
            FoodDistance = []
            for pos in currentFood:
                howFar = util.euclideanDistance(newPos, pos)
                FoodDistance.append(howFar)

            BestScore -= min(FoodDistance)

        return BestScore

def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        legal_actions = gameState.getLegalActions(0)
        max_val = float("-inf")
        ans = None

        for action in legal_actions:
            current_successor = gameState.generateSuccessor(0, action)
            action_value = self.getvalue(current_successor, 1, 0)

            if action_value > max_val:
                max_val = action_value
                ans = action

        return ans

    def Maximizer(self, gameState, agent, depth):
        legal_actions = gameState.getLegalActions(agent)
        maxi = float("-inf")
        for action in legal_actions:
            current_successor = gameState.generateSuccessor(agent, action)
            maxi = max(maxi, self.getvalue(current_successor, 1, depth))

        return maxi

    def Minimizer(self, gameState, agent, depth):
        legal_actions = gameState.getLegalActions(agent)
        mini = float("inf")
        for action in legal_actions:
            current_successor = gameState.generateSuccessor(agent, action)
            if agent + 1 == gameState.getNumAgents():
                mini = min(mini, self.getvalue(current_successor, 0, depth + 1))
            else:
                mini = min(mini, self.getvalue(current_successor, agent + 1, depth))

        return mini

    def getvalue(self, gameState, agent, depth):
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState) # end game state

        # If agent is 0, Maximizer
        if agent == 0:
            return self.Maximizer(gameState, agent, depth)

        # if agentindex > 0, Minimizer
        if agent > 0:
            return self.Minimizer(gameState, agent, depth)

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        legal_actions = gameState.getLegalActions(0)
        max_val = float("-inf")
        ans = None
        alpha = float("-inf")
        beta = float("inf")

        for action in legal_actions:
            current_successor = gameState.generateSuccessor(0, action)
            action_value = self.getvalue(current_successor, 1, 0, alpha, beta)

            if action_value > max_val:
                max_val = action_value
                alpha = action_value
                ans = action

        return ans

    def Maximizer(self, gameState, agent, depth, alpha, beta):
        legal_actions = gameState.getLegalActions(agent)
        maxi = float("-inf")
        for action in legal_actions:
            current_successor = gameState.generateSuccessor(agent, action)
            maxi = max(maxi, self.getvalue(current_successor, 1, depth, alpha, beta))
            if maxi > beta:
                return maxi
            alpha = max(alpha , maxi)

        return maxi

    def Minimizer(self, gameState, agent, depth, alpha, beta):
        legal_actions = gameState.getLegalActions(agent)
        mini = float("inf")
        for action in legal_actions:
            current_successor = gameState.generateSuccessor(agent, action)
            if agent + 1 == gameState.getNumAgents():
                mini = min(mini, self.getvalue(current_successor, 0, depth + 1 , alpha, beta))
            else:
                mini = min(mini, self.getvalue(current_successor, agent + 1, depth, alpha, beta))
            if mini < alpha:
                return mini
            beta = min(beta , mini)
            
        return mini

    def getvalue(self, gameState, agent, depth, alpha , beta):
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # pacman should maximize the outcome
        if agent == 0:
            return self.Maximizer(gameState, agent, depth, alpha , beta)

        # ghosts should minimize the outcome
        if agent > 0:
            return self.Minimizer(gameState, agent, depth, alpha, beta)

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):


    def getAction(self, gameState):
        legal_actions = gameState.getLegalActions(0)
        max_val = float("-inf")
        ans = None

        for action in legal_actions:
            current_successor = gameState.generateSuccessor(0, action)
            action_value = self.getvalue(current_successor, 1, 0)

            if action_value > max_val:
                max_val = action_value
                ans = action

        return ans

    def Maximizer(self, gameState, agent, depth):   
        legal_actions = gameState.getLegalActions(agent)
        maxi = float("-inf")
        for action in legal_actions:
            current_successor = gameState.generateSuccessor(agent, action)
            maxi = max(maxi, self.getvalue(current_successor, 1, depth))

        return maxi

    def Exp(self, gameState, agent, depth):
        legal_actions = gameState.getLegalActions(agent)
        ans = 0
        for action in legal_actions:
            current_successor = gameState.generateSuccessor(agent, action)
            if agent + 1 == gameState.getNumAgents():
                ans += self.getvalue(current_successor, 0, depth+1)
            else:
                ans += self.getvalue(current_successor, agent + 1, depth)

        return ans/len(legal_actions)

    def getvalue(self, gameState, agent, depth):
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent == 0:
            return self.Maximizer(gameState, agent, depth)
        if agent > 0:
            return self.Exp(gameState, agent, depth) #use avg exp when counting ghost moves
            
        util.raiseNotDefined()
