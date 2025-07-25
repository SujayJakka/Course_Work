# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        "*** YOUR CODE HERE ***"

        # Loop through each iteration
        for i in range(self.iterations):
            # Create a new dictionary to update the new values for each state
            new_values = self.values.copy()
            # Iterate through each state in the MDP
            for state in self.mdp.getStates():

                # Continue if its a Terminal State as their utilities are always 0 as there are no actions to take from that state
                if self.mdp.isTerminal(state):
                    continue

                # Initialize negative infinity as the best Q-value seen so far
                best_Q_value = float("-inf")
                # Iterate through each legal action from the state
                for action in self.mdp.getPossibleActions(state):
                    # Find the Q-value for that state and action
                    Q_value = self.computeQValueFromValues(state, action)
                    # Update the best Q-value seen so far for this state across actions
                    best_Q_value = max(best_Q_value, Q_value)

                # Set this best Q-value as the new Q-value for this state in this iteration
                new_values[state] = best_Q_value

            self.values = new_values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        Q_value = 0

        # Iterate through all the successor states and the associated transition probabilities
        for successor_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            # Get the previous value of the successor state
            prev_value_successor_state = self.getValue(successor_state)
            # Get the reward for transitioning to this successor state with the current state and action
            reward = self.mdp.getReward(state, action, successor_state)
            # Append this expression to the Q-value sum, this is in accordance to the Value Iteration formula
            Q_value += (prob * (reward + (self.discount * prev_value_successor_state)))

        return Q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        # Return None if terminal state
        if self.mdp.isTerminal(state):
            return None

        best_action = None
        best_Q_value = float("-inf")

        # Iterate through all the actions, and find the Q-value for the current state and each action
        # Save the action as the best action if it yields the highest Q-value seen
        for action in self.mdp.getPossibleActions(state):
            Q_value = self.computeQValueFromValues(state, action)
            if Q_value > best_Q_value:
                best_action = action
                best_Q_value = Q_value

        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
