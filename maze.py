# Python implementation of the directed graph puzzle described by the
# book "Maze" by Christopher Manson, 1985.  The goal is to travel from
# room 1 to room 45 (the center) and back to room 1 by the shortest
# path.  The author says this should be achievable in 16 steps.
#
# While I have extracted the graph of the maze, I have not captured much
# of the intrigue and excitement of the whole puzzle as most of that
# lies in the illustrations of the rooms and the "clues" they contain as
# well as the narrative of the maze's "guide".  Perhaps you can find
# these aspects at your local library.
#
# Copyright (c) 2015 Aubrey Barnard.  This is free, open-source software
# released under the MIT license.  See the LICENSE file for details.

import heapq


# This is the directed graph of all the passages between rooms by just
# going through the book and taking down the numbers of all the obvious
# doorways.  I have listed the doorways in a natural order from left to
# right and then top to bottom.
passages = {
    1: (20, 26, 41, 21),
    2: (29, 22, 12),
    3: (33, 9, 18),
    4: (44, 29, 15, 11, 16, 24, 43),
    5: (43, 22, 30, 20),
    6: (40,),
    7: (33, 36, 16),
    8: (31, 6, 29, 12),
    9: (3, 18),
    10: (34, 41, 14),
    11: (40, 24),
    12: (2, 21, 8, 39),
    13: (27, 18, 25),
    14: (10, 43, 24),
    15: (30, 37, 3),
    16: (36, 7),
    17: (6, 45, 33),
    18: (13, 3),
    19: (31, 11),
    20: (5, 27, 1),
    21: (44, 24, 31),
    22: (43, 38),
    23: (28, 8, 45, 19),
    24: (),
    25: (34, 13, 35),
    26: (30, 36, 38, 1),
    27: (13, 9),
    28: (23, 43, 45, 32), # cf. 12
    29: (8, 40, 35, 2),
    30: (42, 34, 5, 15),
    31: (44, 19, 21),
    32: (11, 6, 28, 16),
    33: (3, 35, 7),
    34: (10, 25),
    35: (33,),
    36: (7, 16),
    37: (15, 10, 42, 20),
    38: (40, 22, 43),
    39: (11, 4, 12),
    40: (11, 6, 38),
    41: (1, 35, 10, 38),
    42: (22, 30, 4, 25, 37),
    43: (22, 38),
    44: (21, 18),
    45: (28, 17, 36, 19, 23),
}

def path_from_backpointers(backpointers, start, end):
    """
    """
    node = end
    path = [node]
    while node != start:
        if node in backpointers:
            node = backpointers[node]
        else:
            return None
        path.append(node)
    return path

def shortest_path(digraph, start, end):
    """
    """
    # Create a priority (min) queue where each entry is a (distance,
    # node) pair.  Start at the start, of course.
    queue = [(0, start)]
    # These are the shortest paths in reverse
    backpointers = {}
    visited = set()
    # Search for the end
    while queue:
        # Visit the next node
        dist, node = heapq.heappop(queue)
        visited.add(node)
        # If this node is the end return the found path
        if node == end:
            # Construct path from back pointers
            path = path_from_backpointers(backpointers, start, end)
            if path is None:
                raise Exception("No path found from {} pointing back to {}.".format(end, start))
            return list(reversed(path)), visited, backpointers
        # Get the node's neighbors
        neighbors = digraph[node]
        # Enqueue unvisited neighbors by distance (uniformly 1)
        dist += 1
        for neighbor in neighbors:
            if neighbor not in visited:
                heapq.heappush(queue, (dist, neighbor))
                # Add back pointer for this neighbor
                backpointers[neighbor] = node
    # No path found
    return None, visited, backpointers

# >>> import maze
# >>> path, visited, bkptrs = maze.shortest_path(maze.passages, 1, 45)
#
# There is no path from 1 to 45.  Which nodes are not visited?
#
# >>> unvisited = set(range(1, 46)) - visited

def parents(digraph, nodes):
    """
    """
    nodes = set(nodes)
    parents = set()
    for parent, children in digraph.items():
        if nodes & set(children):
            parents.add(parent)
    return parents

# Do a little bidirectional search by hand.
#
# >>> parents = maze.parents(maze.passages, (45,))
# >>> parents |= maze.parents(maze.passages, parents)
# >>> parents |= maze.parents(maze.passages, parents) # parents same as previous
#
# The set of parents has not expanded which means that there are no
# in-links to the transitive set of parents of 45.  (The transitive set
# of parents should keep expanding and eventually include 1 if there is
# a path from 1 to 45.)  This means that there is no solution to the
# puzzle or that I have missed passages.  I should investigate the rooms
# for links to the set of parents of 45.

# I found a hidden passage from room 29 to room 17.
hidden_passages = dict(passages)
hidden_passages[29] += (17,)

# >>> path, visited, bkptrs = maze.shortest_path(maze.hidden_passages, 1, 45)
# >>> len(path)
#
# A path now exists.  It has 8 steps.
#
# What about the return path?
#
# >>> path, visited, bkptrs = maze.shortest_path(maze.hidden_passages, 45, 1)
# >>> len(path)
#
# A return path exists.  It has 10 steps.  We have solved the maze but
# not in the shortest way (18 vs. 16 steps).  Perhaps something else is
# missing.
