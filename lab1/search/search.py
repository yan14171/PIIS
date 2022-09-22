
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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def leeAlgorithmSearch(problem: SearchProblem):
    frontier = util.Queue()

    state = (problem.getStartState(), {})
    node = None
    expandedNodes = set()
    path = list()

    frontier.push(state)

    while True:

        if frontier.isEmpty():
            return -1
        node = frontier.pop()
        if problem.isGoalState(node[0]):
            return node[1]
        if not node[0] in expandedNodes:
            expandedNodes.add(node[0])
            #use problem method to unfold next step
            successors = problem.getSuccessors(node[0])
            for n in successors:
                path = list(node[1])
                path.append(n[1])
                frontier.push((n[0],path))

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    endRoute = util.PriorityQueue()
    visited = []
    start_node = (problem.getStartState() , [] , 0)
    endRoute.push(start_node , 0)

    while not endRoute.isEmpty():
        (cur_state , Result , cur_cost) = endRoute.pop()
        if problem.isGoalState(cur_state):
            return Result
        if cur_state not in visited:
            visited.append(cur_state)
            for successor, action,stepcost in problem.getSuccessors(cur_state):
                new_cost = cur_cost + stepcost
                new_successor = (successor, Result+[action], new_cost)
                # actual cost + estimat(heuristic)
                cost = new_cost + heuristic(successor,problem)
                endRoute.push(new_successor , cost)

    util.raiseNotDefined()

def greedySearch(problem):
    start_point = problem.getStartState()
    pf_ucs = lambda state : state[2] 
    fringe = util.PriorityQueueWithFunction(priorityFunction=pf_ucs) 
    fringe.push((start_point, [], 0)) 

    visited = set()

    while(not fringe.isEmpty()):    

        curr = fringe.pop()

        if(problem.isGoalState(curr[0])):
            return curr[1]

        if(curr[0] not in visited):
            visited.add(curr[0])
            succ = problem.getSuccessors(curr[0])
            for s in succ:
                fringe.push((s[0], curr[1] + [s[1]], curr[2]+s[2])) 

    return []

# Abbreviations
astar = aStarSearch
greed = greedySearch
lee = leeAlgorithmSearch
