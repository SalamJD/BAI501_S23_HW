import heapq
import itertools


class PuzzleNode:
    def __init__(self, state, parent=None, move=None, depth=0, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost


def heuristic_manhattan(current_state, goal_state):
    total_distance = 0
    for i in range(3):
        for j in range(3):
            value = current_state[i][j]
            if value != 0:
                goal_position = divmod(value - 1, 3)
                total_distance += abs(i - goal_position[0]) + abs(j - goal_position[1])
    return total_distance


def heuristic_misplaced_tiles(current_state, goal_state):
    return sum(current != goal for current, goal in zip(itertools.chain(*current_state), itertools.chain(*goal_state)))


def get_neighbors(node):
    neighbors = []
    zero_row, zero_col = next((i, j) for i, row in enumerate(node.state) for j, val in enumerate(row) if val == 0)

    for i, j in [(zero_row, zero_col - 1), (zero_row, zero_col + 1), (zero_row - 1, zero_col),
                 (zero_row + 1, zero_col)]:
        if 0 <= i < 3 and 0 <= j < 3:
            new_state = [row.copy() for row in node.state]
            new_state[zero_row][zero_col], new_state[i][j] = new_state[i][j], new_state[zero_row][zero_col]
            neighbors.append(
                PuzzleNode(new_state, parent=node, move=(zero_row, zero_col), depth=node.depth + 1, cost=0))

    return neighbors


def print_puzzle(state):
    for row in state:
        print(row)
    print()


def solve_puzzle(initial_state, goal_state, heuristic_func):
    initial_node = PuzzleNode(initial_state)
    goal_node = PuzzleNode(goal_state)

    open_set = [initial_node]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)
        if current_node.state == goal_node.state:
            path = []
            while current_node.parent:
                path.append(current_node.move)
                current_node = current_node.parent
            path.reverse()
            return path

        closed_set.add(tuple(map(tuple, current_node.state)))

        for neighbor in get_neighbors(current_node):
            if tuple(map(tuple, neighbor.state)) not in closed_set:
                neighbor.cost = neighbor.depth + heuristic_func(neighbor.state, goal_node.state)
                heapq.heappush(open_set, neighbor)

    return None


def apply_moves(initial_state, moves):
    current_state = [row.copy() for row in initial_state]
    path_states = [current_state]

    for move in moves:
        zero_row, zero_col = move
        current_state[zero_row][zero_col], current_state[zero_row][zero_col - 1] = current_state[zero_row][
            zero_col - 1], current_state[zero_row][zero_col]
        path_states.append([row.copy() for row in current_state])

    return path_states


# Example usage:
initial_state = [
    [1, 2, 3],
    [5, 6, 0],
    [7, 8, 4]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

path_misplaced_tiles = solve_puzzle(initial_state, goal_state, heuristic_misplaced_tiles)

print("Initial State:")
print_puzzle(initial_state)

print("Solution using misplaced tiles:")
print("Moves to solve:")
print_puzzle(initial_state)

for i, move in enumerate(path_misplaced_tiles):
    print(f"Move {i + 1}:")
    print_puzzle(apply_moves(initial_state, path_misplaced_tiles[:i + 1])[-1])
