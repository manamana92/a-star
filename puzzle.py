#!/bin/python3
import argparse

## Helper Functions


def min_score(open_list):
    """
    On input the list of Tile Objects, will output the object
    that has the minimal score.
    """
    minimum = open_list[0].score
    min_idx = 0
    for i in range(1, len(open_list)):
        if open_list[i].score < minimum:
            min_idx = i
            minimum = open_list[i].score
    return open_list[min_idx]

##-----------Heuristic Functions---------------
def dist_manhattan(curr, goal):
    """
    On input a list representing the current tile
    configureation and the goal list, shall output
    the Sum of the Manhattan distance for each tile.
    """
    tot_dist = 0
    glist = goal.list_l
    for i in glist:
        # for each tile, compute the horizontal
        # and vertical distance between the two
        # states and add to the sum, d
        h_dist = abs(curr.index(i)%3 - i%3)
        v_dist = abs(curr.index(i)//3 - i//3)
        tot_dist = tot_dist + h_dist + v_dist
    return tot_dist

def dist_null(curr, goal):
    """
    The Null heuristic function. Needs to still take
    two list to keep the same form of a heuristic function.
    """
    return 0

##----------General 8 problem functions-----------
def reconstruct_path(end_node):
    """
    On input a end node, will traverse the previous
    nodes, until it finds the start node. Then
    returns the list of nodes allong the way.
    """
    curr = end_node
    ret_path = []
    while curr.prev_tile is not None:
        ret_path.insert(0, curr)
        curr = curr.prev_tile
    ret_path.insert(0, curr)
    return ret_path

def print_arrangement(in_list):
    """
    On input a list to be printed in 3-column format,
    prints the values in 3 collumns.
    """
    for i in range(len(in_list)):
        if in_list[i] == 0:
            print("_ ", end=' ')
        else:
            print("{0} ".format(in_list[i]), end=' ')
        if i % 3 == 2:
            print("")

##---Objects for the graph, nodes, and Tiles---
class Tile:
    """
    A Tile object that maintains the list that
    represents the Tile and its current cost
    and score.
    """
    def __init__(self, in_list, cost, score):
        self.list_l = in_list
        self.cost = cost
        self.score = score

class Node:
    """
    A Node object is represented by a Tile
    object and its neighbors.
    """
    def __init__(self, tile_obj, prev_tile):
        self.tile = tile_obj
        self.prev_tile = prev_tile
        self.neighs = neighbor_list(tile_obj.list_l)

class A_Graph:
    """
    A graph is represented by a list of Node
    objects.
    """
    def __init__(self):
        self.curr = None
        self.nodes = []

    def add_node(self, node):
        """
        Creates a node, and sets that to
        the current node.
        """
        self.curr = Node(node, self.curr)
        self.nodes.append(self.curr)

    def set_curr(self, tile):
        """
        Searches the list of nodes that
        represent the graph until it finds
        the tile instance that matches.
        """
        for i in self.nodes:
            if i.tile == tile:
                self.curr = i
                break
            else:
                self.curr = None

##------Functions for finding Neighbors--------
def switch(list, i, j):
    """
    On input a list, return a copy of the list
    with the values at index i and j swapped.
    This is used for finding neighbors.
    """
    retl = list.copy()
    swap = retl[i]
    retl[i] = retl[j]
    retl[j] = swap
    return retl

def neighbor_list(cur_list):
    """
    On input a list, find the neighbors, and return
    a list of their Tile Objects. Any time there is
    a tile above, below, to the right or left, then
    that is a neighbor of the current tile
    configuration.
    """
    n_list = []
    curr_0 = cur_list.index(0)
    # Any time there is a neighbor above, below,
    # to the left or right, there is a neighbor
    # configuration.
    if curr_0 %3 != 0:
        # If there is a tile below the blank.
        n_list.append(Tile(switch(cur_list, curr_0, curr_0 -1), 0, 0))
    if curr_0 %3 != 2:
        # If there is a tile above the blank.
        n_list.append(Tile(switch(cur_list, curr_0, curr_0 + 1), 0, 0))
    if curr_0 // 3 != 0:
        # If there is a tile to the left of the blank.
        n_list.append(Tile(switch(cur_list, curr_0, curr_0 - 3), 0, 0))
    if curr_0 // 3 != 2:
        # If there is a tile to the right of the blank.
        n_list.append(Tile(switch(cur_list, curr_0, curr_0 + 3), 0, 0))
    return n_list

def goal_check(curr_node, goal_node):
    """
    On input two nodes,that are Tile objects
    outputs if they are the same tile.
    """
    return curr_node.list_l == goal_node.list_l

##---------------A*functions-------------------
def a_star_8(graph, start, goal, h):
    """
    On input a graph (here it is empty), start and goal objects
    or nodes, and a heuristic function, performs the A*search
    procedure and returns a path of nodes as the solution.
    Some print statements are commented out, but provide
    some insight into the execution of A*.
    """
    open_l = []
    open_l.append(start)

    closed = []
    curr = None
    ret_path = None
    while len(open_l) > 0:
        curr = min_score(open_l)
        graph.set_curr(curr)
        if goal_check(curr, goal):
            ret_path = reconstruct_path(graph.curr)
            break
        closed.append(curr)
        open_l.remove(curr)
        ## print("Processing for ")
        ## print_arrangement(curr.list_l)
        for neigh in graph.curr.neighs:
            cost = curr.cost + 1
            ret_fetched = closed.count(neigh)
            heur = h(neigh.list_l, goal)
            ## print("Exploring neighbor")
            ## print_arrangement(neigh.list_l)
            ## print("With a cost of {0} and Heuristic Value of {1}\n".format(cost, heur))
            if ret_fetched == 0:
                neigh.cost = cost
                neigh.score = cost + heur
                open_l.append(neigh)
                graph.add_node(neigh)
            elif cost < neigh.cost:
                neigh.cost = cost
                neigh.score = cost + heur
                open_l.append(neigh)
                closed.remove(neigh)
            graph.set_curr(curr)
    return ret_path

def input_parser(in_val):
    ret_val = None
    if in_val == "_":
        ret_val = 0
    else:
        ret_val = int(in_val)
    return ret_val

def valid_tile(tile_list):
    ret_bool = True
    for i in range(0, 9):
        ret_bool = ((tile_list.count(i) == 1) and ret_bool)
    return ret_bool

if __name__ == "__main__":
    ## Main
    parser = argparse.ArgumentParser()
    parser.add_argument('start_list', type=input_parser, nargs=9)
    args = parser.parse_args()

    GOAL_LIST = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    if valid_tile(args.start_list):
        goal = Tile(GOAL_LIST, 0, 0)
        start = Tile(args.start_list, 0, dist_manhattan(args.start_list, goal))

        eight_graph = A_Graph()
        eight_graph.add_node(start)


        path = a_star_8(eight_graph, start, goal, dist_manhattan)

        print("Path starting at:\n")
        for node in path:
            print_arrangement(node.tile.list_l)
            #print("With a score of {0}".format(node.tile.score))
            print("\n   |\n   |\n   V\n")
    else:
        print("Invalid input list")
