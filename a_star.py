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

    board = [[None, None, None, 0, 0, 0, 0],
            [None, None, 0, 0, 0, 0, 0],
            [None, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, None],
            [0, 0, 1, 0, 0, None, None],
            [0, 1, 0, 0, None, None, None]]

    # (q/column, r/row)
    start = (0, -1)
    end = (0, 3)
    print("start: {}, {}, end: {}, {}".format(*start, *end))

    path = a_star(board, start, end)
    print(path)


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
        if r > board_max_dim or r < 0 or \
                q > (len(board[board_max_dim]) - 1) or q < 0 or board[r][q] is None:
            continue

        # Check if it's a blocked position
        if board[r][q] != 0:
            # Check if the following position is walkable
            jump_position = [r + new_position[0], q + new_position[1]]
            jump_r = jump_position[0]
            jump_q = jump_position[1]
            if board[jump_r][jump_q] == 0:
                # If it is, add it to the children (g only increments once)
                node_position = jump_position
            else:
                continue

        # Create new node with parent and position
        new_node = Node(current_node, node_position)

        # Append
        children.append(new_node)

    return children

if __name__ == '__main__':
    main()
