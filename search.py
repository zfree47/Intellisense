"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors:
Zachary Freeman, Kalanika Weerasinghe
"""

import sys
import json
from collections import defaultdict

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: Search for and output winning sequence of moves
    # ...
    # Exits: Red = (3, -3) to (3, 0), green = (-3, 3) to (0, 3), blue = (0, -3) to (-3, 0)
    """
    TODO:
    1. Make sure pieces don't step on each other
    2. Get them to their closest exit
    4. Move simultaneously
    """

    # Square grid board configuration
    board = [[None, None, None, 0, 0, 0, 0],
            [None, None, 0, 0, 0, 0, 0],
            [None, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, None],
            [0, 0, 0, 0, 0, None, None],
            [0, 0, 0, 0, None, None, None]]

    # Enter data into board_dict configuration to print it: board_dict = {(0,0): "RED", (1,0): "GREEN", (2,-1): "B"}
    board_dict = defaultdict()
    for piece in data['pieces']:
        board_dict[tuple(piece)] = data['colour'].upper()
    for block in data['blocks']:
        board_dict[tuple(block)] = "BLOCK"
        # Put the blocks on the square grid board
        q = block[0] + 3
        r = block[1] + 3
        board[r][q] = 1
    print_board(board_dict, debug=True)

    # Find paths to exit
    paths = []
    for piece in data['pieces']:
        end = ()
        if data['colour'] == 'red':
            end = (3, -3)
        elif data['colour'] == 'green':
            end = (-3, 3)
        else:
            end = (0, -3)
        path = a_star(board, tuple(piece), end)
        paths.append(path)
    for piece, path in enumerate(paths):
        print("Piece number {}. || Path to exit: {}".format(piece+1, path))


def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.

    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using
    the axial coordinate system outlined in the project specification) and the
    values are formatted as strings and placed in the drawing at the corres-
    ponding location (only the first 5 characters of each string are used, to
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}|
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}|
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}|
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}|
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}|
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}|
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} |
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


def a_star(board, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Convert to grid coordinates
    offset = 3
    start_q = start[0] + offset
    start_r = start[1] + offset
    end_q = end[0] + offset
    end_r = end[1] + offset

    # Create start and end node (row is accessed first in 2D array)
    if board[start_r][start_q] is not None:
        start_node = Node(None, [start_r, start_q])
        start_node.g = start_node.h = start_node.f = 0
    else:
        return "Start position doesn't exist."

    if board[end_r][end_q] is not None:
        end_node = Node(None, [end_r, end_q])
        end_node.g = end_node.h = end_node.f = 0
    else:
        return "End position doesn't exist."

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):  # Could use a priority queue here
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:

                # Convert to hex coordinates
                output_r = current.position[0] - offset
                output_q = current.position[1] - offset
                output = [output_q, output_r]
                path.append(output)

                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = generate_children(board, current_node)

        # Loop through children
        for child in children:

            # Don't change g, h, f values if it's a closed position
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values.
            child.g = current_node.g + 1
            # current heuristic: pythagoras
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + \
                      ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Don't add to open list if it's already in it with a smaller true cost value
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def generate_children(board, current_node):

    children = []

    for new_position in [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]:  # Adjacent squares
        # Get node position
        node_position = [current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]

        board_max_dim = len(board) - 1
        r = node_position[0]  # row
        q = node_position[1]  # column

        # If r or q is off the board, move on to the next position
        '''if r > board_max_dim or r < 0 or \
                q > (len(board[board_max_dim]) - 1) or q < 0 or board[r][q] is None:
            continue'''
        if out_of_bounds(board, r, q):
            continue

        # Check if it's a blocked position
        if board[r][q] != 0:
            # Check if the following position is walkable
            jump_position = [r + new_position[0], q + new_position[1]]
            jump_r = jump_position[0]
            jump_q = jump_position[1]
            if not out_of_bounds(board, r, q):
                    # If it is, add it to the children (g only increments once)
                    node_position = jump_position
            else:
                continue

        # Create new node with parent and position
        new_node = Node(current_node, node_position)

        # Add to children
        children.append(new_node)

    return children


def out_of_bounds(board, r, q):
    board_max_dim = len(board) - 1
    return r > board_max_dim or r < 0 or q > len(board[board_max_dim]) - 1 \
    or q < 0 or board[r][q] is None


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
