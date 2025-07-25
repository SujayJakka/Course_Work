# factorOperations.py
# -------------------
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

from typing import List
from bayesNet import Factor
import functools
from util import raiseNotDefined

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors: List[Factor], joinVariable: str):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        vars_on_left = [factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()]
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", vars_on_left)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()

########### ########### ###########
########### QUESTION 2  ###########
########### ########### ###########

def joinFactors(factors: List[Factor]):
    """
    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", intersect)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))

    "*** YOUR CODE HERE ***"

    # Sets to store the uncondtioned and conditioned variables across all factors
    unconditioned_variables = set()
    conditioned_variables = set()
    # Domain of the variables across all factors
    variable_domains_dict = {}

    # Loop through each factor and add their unconditioned and conditioned variables to our sets
    # Also set the variable domains dict to an arbitrary factor's variable domain dict as all factors have the same variable domain dict
    for factor in factors:
        unconditioned_variables = unconditioned_variables.union(factor.unconditionedVariables())
        conditioned_variables = conditioned_variables.union(factor.conditionedVariables())
        variable_domains_dict = factor.variableDomainsDict()

    # List to find which conditioned variables need to be removed
    conditioned_variables_to_remove = []

    # If a conditioned variable is also in the unconditioned variables set that means it no longer a conditioned variable
    # Remove the conditioned variable from the set of conditioned variables
    for conditioned_variable in conditioned_variables:
        if conditioned_variable in unconditioned_variables:
            conditioned_variables_to_remove.append(conditioned_variable)

    for conditioned_variable in conditioned_variables_to_remove:
        conditioned_variables.remove(conditioned_variable)

    # Create the resulting factor
    result_factor = Factor(unconditioned_variables, conditioned_variables, variable_domains_dict)

    # For each possible variables assignment find the probability by multiplying the probability across all factors given that variables assignment
    for assignment_dict in result_factor.getAllPossibleAssignmentDicts():
        assignment_prob = 1
        for factor in factors:
            assignment_prob *= factor.getProbability(assignment_dict)
        result_factor.setProbability(assignment_dict, assignment_prob)

    return result_factor

    "*** END YOUR CODE HERE ***"

########### ########### ###########
########### QUESTION 3  ###########
########### ########### ###########

def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor: Factor, eliminationVariable: str):
        """
        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        # Sets to store the uncondtioned and conditioned variables for the resulting factor
        unconditioned_variables = factor.unconditionedVariables()
        conditioned_variables = factor.conditionedVariables()
        # Dictionary to store the variable domains dict which is same across all factors that are part of the same bayes net
        variable_domains_dict = factor.variableDomainsDict()

        # Remove the elimination variable from the resulting factor's unconditioned variables
        unconditioned_variables.remove(eliminationVariable)

        # Create a new factor to return
        result_factor = Factor(unconditioned_variables, conditioned_variables, variable_domains_dict)

        # Marginalize by summing out the all possible values of the elimination variable for a given variables assignment in the resulting factor
        for assignment_dict in result_factor.getAllPossibleAssignmentDicts():
            prob = 0
            for value in variable_domains_dict[eliminationVariable]:
                assignment_dict[eliminationVariable] = value
                prob += factor.getProbability(assignment_dict)
            result_factor.setProbability(assignment_dict, prob)

        return result_factor

        "*** END YOUR CODE HERE ***"

    return eliminate

eliminate = eliminateWithCallTracking()

