# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
from backend import ReplayMemory

import nn
import model
import backend
import gridworld


import random,util,math
import numpy as np
import copy

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent
      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update
      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"

        # Dictionary that has a default value of 0
        self.Q_values = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"

        # Returns the corresponding Q-value for the given state and action
        return self.Q_values[(state, action)]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legal_actions = self.getLegalActions(state)

        # If there are no legal actions, it is a terminal state and return 0
        if not legal_actions:
            return 0

        # Initialize the best Q-value to negative infinity
        best_Q_value = float("-inf")

        # Find the max Q-Value across all actions
        for action in legal_actions:
            best_Q_value = max(best_Q_value, self.getQValue(state, action))

        # Return the best Q-Value
        return best_Q_value

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legal_actions = self.getLegalActions(state)

        # If there are no legal actions, this is a terminal state so return None
        if not legal_actions:
            return None

        # Variables to keep track of the best Q-Value and best action
        best_Q_value = float("-inf")
        best_action = None

        # Iterate through all legal actions
        for action in legal_actions:

            # Find Q-Value of the state and current action
            Q_value = self.getQValue(state, action)

            # If the Q-value best seen so far update best Q-value and best action
            if Q_value > best_Q_value:
                best_action = action
                best_Q_value = Q_value
            # If the Q-value equals the best seen so far randomly choose between the best action and current action
            elif Q_value == best_Q_value:
                best_action = random.choice([best_action, action])

        return best_action

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"

        # If this is a terminal state, return None
        if not legalActions:
            return action

        # With a probability of epsilon, choose a random legal action
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        # Otherwise take the action with the best Q-Value
        else:
            return self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward: float):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"

        # Find max Q-value across all actions from the successor state
        best_Q_value_successor_state = self.computeValueFromQValues(nextState)
        # Find the sample by adding the reward to the product of the discount and utility value of the successor state
        sample = reward + (self.discount * best_Q_value_successor_state)
        # Update the Q value of the state and action
        self.Q_values[(state, action)] = ((1 - self.alpha) * self.getQValue(state, action)) + (self.alpha * sample)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action

class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent
       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"

        # Return the Q-Value of the state, action pair using util.Counter() dot product
        return self.getWeights() * self.featExtractor.getFeatures(state, action)

    def update(self, state, action, nextState, reward: float):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"

        # Find feature vector
        feature_vector = self.featExtractor.getFeatures(state, action)

        # Find difference according to the equation provided in the assignment details
        difference = (reward + (self.discount * self.computeValueFromQValues(nextState))) - self.getQValue(state, action)

        # Iterate through each feature and update its weight according to the equation provided in the assignment details
        for feature in feature_vector:
            self.weights[feature] += (self.alpha * difference * feature_vector[feature])

    def final(self, state):
        """Called at the end of each game."""
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
