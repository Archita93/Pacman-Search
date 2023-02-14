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

def depthFirstSearch(problem):
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
    frontier = util.Stack() # LIFO

    # Stores all the explored states 
    explored = [] 

    # Frontier node contains the state and the path leading to the goal state
    frontier.push((problem.getStartState(),[])) 

    while True:
        if frontier.isEmpty():
            raise Exception("No solution")
        
        # Initial node is removed to check            
        (state,nextAction) = frontier.pop()

        # Path is returned, if the state is a goal state
        if(problem.isGoalState(state)):
            return nextAction
        
        else:
            # State is added to keep track of the explored states
            explored.append(state)

            # Succesors of the explored state are found
            successors = problem.getSuccessors(state)

            for s in successors:

                # Successor is added to the frontier if not explored yet
                if(not s[0] in explored):
                    frontier.push((s[0],nextAction + [s[1]]))

    util.raiseNotDefined()


    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue() # FIFO
    
    # Lists initialised to keep the explored and visited states in check
    explored = [] 

    visited = []
    
    # Initial node is added to the frontier, which contains a start state, a path and the total cost of action
    frontier.push((problem.getStartState(),[],0)) 

    explored.append(problem.getStartState())

    while True:

        if frontier.isEmpty():
            raise Exception("No solution")

        # Initial node is removed             
        (state,nextAction,nextCost) = frontier.pop()

        # Path is returned, if the removed state is a goal state
        if(problem.isGoalState(state)):
            return nextAction

        else:

            # State is added to visited
            visited.append(state)

            # Successors are found for that particular state
            successors = problem.getSuccessors(state)
            for s in successors:

                # Added in the frontier if the state is unvisited and not explored
                if ((not s[0] in visited) and (not s[0] in explored)): 
                    frontier.push((s[0],nextAction + [s[1]],nextCost+s[2]))
                    explored.append(s[0])

    util.raiseNotDefined()    



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()

    visited = []   

    explored = []

    # Intial node contains the start state, path leading to the goal, and the total cost, prioritized by the cost of actions
    frontier.push((problem.getStartState(),[],0),0) 

    explored.append(problem.getStartState())

    while not frontier.isEmpty():

        (state,nextAction,nextCost) = frontier.pop()
         
        # Initial node is popped out of the frontier to check if its the goal state or not
        if(problem.isGoalState(state)):
            return nextAction
        
        if not state in visited:
            visited.append(state)
            successors = problem.getSuccessors(state)

            for s in successors:

                # Successor is added if it is not visited
                if(not s[0] in visited):    # CHOOSE SMALLEST COST
                    frontier.push((s[0],nextAction +[s[1]],nextCost+s[2]),nextCost+s[2])
                    explored.append(s[0])
                
                # Successor node is updated with the new cost if it is explored, but the new cost is less than the previous cost
                elif(s[0] in explored and s[2]> nextCost):
                    frontier.update((s[0],nextAction,nextCost),nextCost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    visited = []    # visisted states
     
    # Initial node contains a subnode (start state and path leading to the goal) and the heuristic
    frontier.push((problem.getStartState(),[]),heuristic(problem.getStartState(),problem))

    while not frontier.isEmpty():

        # Node is removed to check if goal state is reached or to find its successors
        (state,nextAction) = frontier.pop()
   
        if(problem.isGoalState(state)):
            return nextAction
        
        
        if not state in visited:

            visited.append(state)
            successors = problem.getSuccessors(state)
           
            for s in successors:

                # Successors' heuristic consists of the previous state's heuristic and the cost of next Action
                f_value = heuristic(s[0],problem) + problem.getCostOfActions(nextAction +[s[1]])
                
                # If its unvisited, successor is added
                if(not s[0] in visited):    # CHOOSE SMALLEST COST
                    frontier.push((s[0],nextAction +[s[1]]),f_value)

                # Successor is updated with the smaller f_value, if the new f_value is less than the previous one
                elif(s[2]> f_value):
                    frontier.update((s[0],nextAction),f_value)
                    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch