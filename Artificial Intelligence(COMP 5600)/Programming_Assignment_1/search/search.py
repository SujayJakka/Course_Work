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
from game import Directions
from typing import List

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
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

    # Set to keep track of explored states
    explored = set()
    # Stack for frontier for iterative approach
    dfs_stack = util.Stack()
    # Stack that keeps track of a path for each state added to the frontier
    paths = util.Stack()

    # Add start state to the dfs stack
    dfs_stack.push(problem.getStartState())

    # Push empty path(actions) for the start state
    paths.push([])

    # Loop until either the goal state has been found or the frontier is empty
    while not dfs_stack.isEmpty():

        # Pop the current state off of the frontier(stack) and its corresponding path of actions
        current_state = dfs_stack.pop()
        path = paths.pop()

        # If this state is the goal state return the path of actions
        if problem.isGoalState(current_state):
            return path

        # Add the current state to the explored set
        explored.add(current_state)

        # Add successor states and their corresponding paths to the stack if they have not already been explored
        for successor_state, action, cost in problem.getSuccessors(current_state):
            if successor_state not in explored:
                dfs_stack.push(successor_state)
                paths.push(path + [action])


def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # Set to keep track of explored states
    explored = set()
    # Queue for frontier for states
    queue = util.Queue()
    # Queue for the corresponding paths of the states added onto the frontier
    paths = util.Queue()

    # Add the start state to the explored set
    explored.add(problem.getStartState())
    # Push the start state to the queue
    queue.push(problem.getStartState())
    # Push an empty path of actions for the start state
    paths.push([])

    # Loop until either the goal state has been found or the frontier is empty
    while not queue.isEmpty():
        # Pop the current state and its corresponding path of actions
        current_state = queue.pop()
        path = paths.pop()

        # If the current state is the start state return its corresponding path of actions
        if problem.isGoalState(current_state):
            return path

        # If a successor state has not been explored push it onto the queue
        for successor_state, action, cost in problem.getSuccessors(current_state):
            if successor_state not in explored:
                # Add successor states to the explored set, so we can avoid the risk of
                # the same state being pushed onto the frontier multiple of times
                explored.add(successor_state)
                queue.push(successor_state)
                paths.push(path + [action])

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # Set to keep track of explored states
    explored = set()
    # Priority queue for frontier
    priority_queue = util.PriorityQueue()

    # Keeps track of the path of actions to each state
    # Key is State, Value is Path of Actions
    path_to_state = {problem.getStartState(): []}
    # Keeps track of the cost to each state
    # Key is State, Value is Cost
    cost_to_state = {problem.getStartState(): 0}

    # Push the start state onto the frontier
    priority_queue.push(problem.getStartState(), 0)

    # Loop until either the goal state has been found or the frontier is empty
    while not priority_queue.isEmpty():
        # Pop the current state from the priority queue
        current_state = priority_queue.pop()

        # If the current state is the goal state return the path of actions with the LEAST cost
        if problem.isGoalState(current_state):
            return path_to_state[current_state]

        # Add the current state to the explored set
        explored.add(current_state)

        # Loop through all successor states from the current state
        for successor_state, action, cost in problem.getSuccessors(current_state):
            # Only consider successor states that have not been explored yet
            if successor_state not in explored:
                # Calculate the cost to this successor state from the CURRENT STATE
                cost_to_succesor_state = cost_to_state[current_state] + cost

                # Checks to see if this is the minimum cost path to this successor state
                if successor_state not in cost_to_state or cost_to_succesor_state < cost_to_state[successor_state]:
                    # If it is, the cost dictionary and path dictionary updates for that successor state
                    # Furthermore, we will then update the successor states priority key in the priority queue
                    path_to_state[successor_state] = path_to_state[current_state] + [action]
                    cost_to_state[successor_state] = cost_to_state[current_state] + cost
                    priority_queue.update(successor_state, cost_to_state[successor_state])


def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # Set to keep track of explored states
    explored = set()
    # Priority queue for frontier
    priority_queue = util.PriorityQueue()
    # Keeps track of the path of actions to each state
    path_to_state = {problem.getStartState(): []}
    # Keeps track of the cost to each state
    cost_to_state = {problem.getStartState(): 0}

    # Push the start state onto the frontier
    priority_queue.push(problem.getStartState(), 0)

    # Loop until either the goal state has been found or the frontier is empty
    while not priority_queue.isEmpty():
        # Pop the current state from the priority queue
        current_state = priority_queue.pop()

        # If the current state is the goal state return the path of actions with the LEAST cost
        if problem.isGoalState(current_state):
            return path_to_state[current_state]

        # Add a tuple of current state and its path to get there to the explored st
        # States may need to be explored multiple times to find the optimal path to the goal state
        explored.add((current_state, cost_to_state[current_state]))

        # Loop through all successor states from the current state
        for successor_state, action, cost in problem.getSuccessors(current_state):
            # If this successor state with this path has not already been explored continue
            if (successor_state, cost_to_state[current_state] + cost) not in explored:
                # Calculate the cost to this successor state from the CURRENT STATE
                cost_to_successor_state = cost_to_state[current_state] + cost

                # If the new cost of the successor state is the less than a previously seen cost of the successor state,
                # the cost dictionary and path dictionary updates for that successor state path as a better path has been found
                if successor_state not in cost_to_state or cost_to_successor_state < cost_to_state[successor_state]:
                    path_to_state[successor_state] = path_to_state[current_state] + [action]
                    cost_to_state[successor_state] = cost_to_state[current_state] + cost
                    # Update priority queue to reflect this new-found path plus the heuristic
                    priority_queue.update(successor_state, cost_to_successor_state + heuristic(successor_state, problem))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
