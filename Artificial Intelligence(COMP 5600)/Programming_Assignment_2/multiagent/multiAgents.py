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

        # Variable that represents the change to the successor state's score.
        change_in_score = 0

        # Find distance from pacman to nearest food on board
        distances_to_nearest_food = float("inf")
        for food_location in newFood.asList():
            distances_to_nearest_food = min(util.manhattanDistance(food_location, newPos), distances_to_nearest_food)

        # Adds the reciprocal of the distance to the nearest food times 10 to the change in score variable.
        # Incentivizes pacman to be near food.
        change_in_score += (10 / distances_to_nearest_food)

        # Find distance from pacman to nearest capsule on board
        distance_to_nearest_capsule = float("inf")
        for capsule_location in successorGameState.getCapsules():
            distance_to_nearest_capsule = min(util.manhattanDistance(capsule_location, newPos), distance_to_nearest_capsule)

        # Adds the reciprocal of the distance to the nearest capsule times 30 to the change in score variable.
        # Incentivizes pacman to be closer to power pellets.
        change_in_score += (30 / distance_to_nearest_capsule)

        # List of ghost positions in current state
        ghost_positions = currentGameState.getGhostPositions()

        # Iterate through the successor state's ghost positions
        for i in range(len(ghost_positions)):
            # Finds the distance from pacman to the current ghost
            distance_from_ghost = util.manhattanDistance(ghost_positions[i], newPos)
            # Checks to see if pacman has ate a power pellet
            if newScaredTimes[i] > 0:
                # Incentivise pacman to eat the ghosts
                change_in_score += (75 / distance_from_ghost)
            else:
                if distance_from_ghost < 3:
                    # Heavily penalize the successor state if pacman is near a ghost and it has not ate a power pellet
                    change_in_score -= 150
                else:
                    # Penalize succesor state by using distance to current ghost
                    change_in_score -= (5 / distance_from_ghost)

        # Return the sum of the successor state's score plus the change in score
        return successorGameState.getScore() + change_in_score

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

        # Recursive function for ghosts that tries to find the action that leads to the minimum score
        def min_ghost(current_depth, current_state, current_ghost):

            # Checks to see if the game is over
            # If it is, then this state is a terminal state and we return the score of this state
            if current_state.isWin() or current_state.isLose():
                return self.evaluationFunction(current_state)

            # Find the number of ghosts in the game currently
            number_of_current_ghosts = current_state.getNumAgents() - 1

            # Variable to keep track of minimum score found across all successor states
            minimum_score = float("inf")

            # Find the list of legal actions from this state
            legal_actions = current_state.getLegalActions(current_ghost)
            for legal_action in legal_actions:
                # Generate the successor state from the current state and legal action
                successor_state = current_state.generateSuccessor(current_ghost, legal_action)

                # If there are more ghosts in the game, recursively call the min ghost function again as
                # for every max function call there should be a min function call for each ghost
                if current_ghost < number_of_current_ghosts:
                    # If the successor state has a lower score than the current minimum score, update the minimum score
                    minimum_score = min(minimum_score, min_ghost(current_depth, successor_state, current_ghost + 1))
                # If there are no more ghosts to call, call the max pacman function
                else:
                    # If the successor state has a lower score than the current minimum score, update the minimum score
                    minimum_score = min(minimum_score, max_pacman(current_depth + 1, successor_state))

            return minimum_score

        # Recursive function for pacman that tries to find the action that leads to the maximum score
        def max_pacman(current_depth, current_state):

            # Checks to see if the game is over or if the algorithm exceeded its max depth.
            # If it is, then this state is a terminal state and we return the score of this state
            if current_state.isWin() or current_state.isLose() or current_depth > self.depth:
                return self.evaluationFunction(current_state)

            # Find the list of legal actions for pacman
            legal_actions = current_state.getLegalActions(0)

            # Keeps track of the maximum score found across all successor states
            maximum_score = float("-inf")
            # Keeps track of the best action that lead to the successor state with the best score
            best_action = None

            for legal_action in legal_actions:
                # Generate the successor state from the current state and legal action
                successor_state = current_state.generateSuccessor(0, legal_action)
                # Score for successor state
                score = min_ghost(current_depth, successor_state, 1)

                # Checks to see if this is the best score found so far,
                # if it is update maximum score and update best action
                if score > maximum_score:
                    maximum_score = score
                    best_action = legal_action

            # If the current depth is equal to 1, this means this is the root node and we return the best action
            # as we want to return the best action that leads to the best successor state for pacman.
            # If it is not the root node, we return the score.
            if current_depth == 1:
                return best_action
            else:
                return maximum_score


        # Call the max pacman function with the current depth at 1 and current game state
        return max_pacman(1, gameState)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # Recursive function for ghosts that tries to find the action that leads to the minimum score using alpha-beta pruning
        def min_ghost(current_depth, current_state, current_ghost, alpha, beta):

            # Checks to see if the game is over
            # If it is, then this state is a terminal state and we return the score of this state
            if current_state.isWin() or current_state.isLose():
                return self.evaluationFunction(current_state)

            # Find the number of ghosts in the game currently
            number_of_current_ghosts = current_state.getNumAgents() - 1

            # Variable to keep track of minimum score
            minimum_score = float("inf")

            # Find the list of legal actions from this state
            legal_actions = current_state.getLegalActions(current_ghost)
            for legal_action in legal_actions:
                # Generate the successor state from the current state and legal action
                successor_state = current_state.generateSuccessor(current_ghost, legal_action)

                # If there are more ghosts in the game, recursively call the min ghost function again as
                # for every max function call there should be a min function call for each ghost
                if current_ghost < number_of_current_ghosts:
                    # If the successor state has a lower score than the current min score, update the minimum score
                    minimum_score = min(minimum_score, min_ghost(current_depth, successor_state, current_ghost + 1, alpha, beta))
                # If there are no more ghosts to call, call the max pacman function
                else:
                    # If the successor state has a lower score than the current minimum score, update the minimum score
                    minimum_score = min(minimum_score, max_pacman(current_depth + 1, successor_state, alpha, beta))

                # If the minimum score is less than alpha, this means there is no point exploring the successor states any
                # further as the max node above this min node will not choose the action that will lead to this min node
                if minimum_score < alpha:
                    return minimum_score

                # Update beta in the case we found a state with a lower score than the existing beta
                beta = min(beta, minimum_score)

            return minimum_score

        # Recursive function for pacman that tries to find the action that leads to the maximum score
        def max_pacman(current_depth, current_state, alpha, beta):

            # Checks to see if the game is over or if the algorithm exceeded its max depth.
            # If it is, then this state is a terminal state and we return the score of this state
            if current_state.isWin() or current_state.isLose() or current_depth > self.depth:
                return self.evaluationFunction(current_state)

            # Find the list of legal actions for pacman
            legal_actions = current_state.getLegalActions(0)

            # Variable to keep track of maximum score
            maximum_score = float("-inf")
            # Keeps track of the best action that lead to the successor state with the maximum score
            best_action = None

            for legal_action in legal_actions:
                # Generate the successor state from the current state and legal action
                successor_state = current_state.generateSuccessor(0, legal_action)
                # Score for successor state
                score = min_ghost(current_depth, successor_state, 1, alpha, beta)

                # Checks to see if this is the best score found so far,
                # if it is update maximum score and update best action
                if score > maximum_score:
                    maximum_score = score
                    best_action = legal_action

                # If the maximum score is greater than beta, this means there is no point exploring the successor states any
                # further as the min node above this max node will not choose the action that will lead to this max node
                if maximum_score > beta:
                    return maximum_score

                # Update alpha in the case we found a state with a lower score than the existing alpha
                alpha = max(maximum_score, alpha)

            # If the current depth is equal to 1, this means this is the root node and we return the best action
            # as we want to return the best action that leads to the best successor state for pacman.
            # If it is not the root node, we return the maximum score found from a successor state.
            if current_depth == 1:
                return best_action
            else:
                return maximum_score

        # Call the max pacman function with the current depth at 1 and current game state
        return max_pacman(1, gameState, float("-inf"), float("inf"))

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

        # Recursive function for ghosts that finds the expected value of a state based on the legal moves from that state
        def expecti_ghost(current_depth, current_state, current_ghost):

            # Checks to see if the game is over
            # If it is, then this state is a terminal state and we return the score of this state
            if current_state.isWin() or current_state.isLose():
                return self.evaluationFunction(current_state)

            # Find the number of ghosts in the game currently
            number_of_current_ghosts = current_state.getNumAgents() - 1

            # Variable to keep track of the expected score of this state
            # Score is calculated by averaging the scores of the successor state as we assume the ghosts choose successor states at uniform random
            expected_score = 0

            # Find the list of legal actions from this state
            legal_actions = current_state.getLegalActions(current_ghost)
            for legal_action in legal_actions:
                # Generate the successor state from the current state and legal action
                successor_state = current_state.generateSuccessor(current_ghost, legal_action)

                # If there are more ghosts in the game, recursively call the expecti ghost function again as
                # for every max function call there should be a expecti ghost function call for each ghost
                if current_ghost < number_of_current_ghosts:
                    # Add the successor state's score divided by the number of actions to the expected score
                    expected_score += (expecti_ghost(current_depth, successor_state, current_ghost + 1) / len(legal_actions))
                # If there are no more ghosts to call, call the max pacman function
                else:
                    # Add the successor state's score divided by the number of actions to the expected score
                    expected_score += (max_pacman(current_depth + 1, successor_state) / len(legal_actions))

            return expected_score

        # Recursive function for pacman that tries to find the action that leads to the maximum score
        def max_pacman(current_depth, current_state):

            # Checks to see if the game is over or if the algorithm exceeded its max depth.
            # If it is, then this state is a terminal state and we return the score of this state
            if current_state.isWin() or current_state.isLose() or current_depth > self.depth:
                return self.evaluationFunction(current_state)

            # Find the list of legal actions for pacman
            legal_actions = current_state.getLegalActions(0)

            # Keeps track of the maximum score found across all successor states
            maximum_score = float("-inf")
            # Keeps track of the best action that lead to the successor state with the best score
            best_action = None

            for legal_action in legal_actions:
                # Generate the successor state from the current state and legal action
                successor_state = current_state.generateSuccessor(0, legal_action)
                # Score for successor state, adversary uses expected value to find score of a state
                score = expecti_ghost(current_depth, successor_state, 1)

                # Checks to see if this is the best score found so far,
                # if it is update maximum score and update best action
                if score > maximum_score:
                    maximum_score = score
                    best_action = legal_action

            # If the current depth is equal to 1, this means this is the root node and we return the best action
            # as we want to return the best action that leads to the best successor state for pacman.
            # If it is not the root node, we return the score.
            if current_depth == 1:
                return best_action
            else:
                return maximum_score

        # Call the max pacman function with the current depth at 1 and current game state
        return max_pacman(1, gameState)

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: I basically did exactly what I did in Question 1 where I used the nearest distance to food, nearest distance to capsule,
    ghost scared times, ghost distance, and the default score of the state. The only thing I changed is instead of evaluating a given successor
    state I am evaluating the current state. I wanted to run my previous implementation first to see if it would work, and it happened to pass
    the autograder's tests which is why I decided to reuse my previous implementation of the evaluation function.
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    current_pos = currentGameState.getPacmanPosition()
    current_food = currentGameState.getFood()
    current_ghost_states = currentGameState.getGhostStates()
    current_scared_times = [ghostState.scaredTimer for ghostState in current_ghost_states]

    "*** YOUR CODE HERE ***"

    # Variable that represents the change to the successor state's score.
    change_in_score = 0

    # Find distance from pacman to nearest food on board
    distances_to_nearest_food = float("inf")
    for food_location in current_food.asList():
        distances_to_nearest_food = min(util.manhattanDistance(food_location, current_pos), distances_to_nearest_food)

    # Adds the reciprocal of the distance to the nearest food times 10 to the change in score variable.
    # Incentivizes pacman to be near food.
    change_in_score += (10 / distances_to_nearest_food)

    # Find distance from pacman to nearest capsule on board
    distance_to_nearest_capsule = float("inf")
    for capsule_location in currentGameState.getCapsules():
        distance_to_nearest_capsule = min(util.manhattanDistance(capsule_location, current_pos), distance_to_nearest_capsule)

    # Adds the reciprocal of the distance to the nearest capsule times 30 to the change in score variable.
    # Incentivizes pacman to be closer to power pellets.
    change_in_score += (30 / distance_to_nearest_capsule)

    # List of ghost positions in current state
    ghost_positions = currentGameState.getGhostPositions()

    # Iterate through the successor state's ghost positions
    for i in range(len(ghost_positions)):
        # Finds the distance from pacman to the current ghost
        distance_from_ghost = util.manhattanDistance(ghost_positions[i], current_pos)
        # Checks to see if pacman has ate a power pellet
        if current_scared_times[i] > 0:
            # Incentivise pacman to eat the ghosts
            change_in_score += (75 / distance_from_ghost)
        else:
            if distance_from_ghost < 3:
                # Heavily penalize the successor state if pacman is near a ghost and it has not ate a power pellet
                change_in_score -= 150
            else:
                # Penalize succesor state by using distance to current ghost
                change_in_score -= (5 / distance_from_ghost)

    # Return the sum of the successor state's score plus the change in score
    return currentGameState.getScore() + change_in_score

# Abbreviation
better = betterEvaluationFunction
