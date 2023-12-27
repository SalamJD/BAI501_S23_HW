import heapq
import itertools
import random


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


def is_solvable(puzzle):
    inversion_count = 0
    flattened_puzzle = list(itertools.chain(*puzzle))
    for i in range(len(flattened_puzzle) - 1):
        for j in range(i + 1, len(flattened_puzzle)):
            if flattened_puzzle[i] and flattened_puzzle[j] and flattened_puzzle[i] > flattened_puzzle[j]:
                inversion_count += 1
    return inversion_count % 2 == 0


def solve_and_print_ebf(initial_state, goal_state):
    while not is_solvable(initial_state):
        initial_state = generate_random_puzzle()

    def solve_puzzle(heuristic_func):
        initial_node = PuzzleNode(initial_state)
        goal_node = PuzzleNode(goal_state)

        open_set = [initial_node]
        closed_set = set()
        visited_nodes = 0
        discovered_nodes = 1

        while open_set:
            current_node = heapq.heappop(open_set)
            visited_nodes += 1

            if current_node.state == goal_node.state:
                path = []
                while current_node.parent:
                    path.append(current_node.move)
                    current_node = current_node.parent
                path.reverse()
                depth_of_solution = len(path)
                discovered_nodes_at_solution_depth = len([n for n in open_set if n.depth == depth_of_solution])
                if discovered_nodes_at_solution_depth != 0:
                    ebf = (visited_nodes / discovered_nodes_at_solution_depth) ** (1 / depth_of_solution)
                else:
                    ebf = float('inf')
                return round(ebf, 4)

            closed_set.add(tuple(map(tuple, current_node.state)))

            for neighbor in get_neighbors(current_node):
                if tuple(map(tuple, neighbor.state)) not in closed_set:
                    discovered_nodes += 1
                    neighbor.cost = neighbor.depth + heuristic_func(neighbor.state, goal_node.state)
                    heapq.heappush(open_set, neighbor)

        return float('inf')

    # Solve and print EBF for the current state using Manhattan distance and misplaced tiles
    ebf_manhattan = solve_puzzle(heuristic_manhattan)
    ebf_misplaced_tiles = solve_puzzle(heuristic_misplaced_tiles)

    # Print the EBF values for the current state
    print(f"EBF (Manhattan): {ebf_manhattan}, EBF (Misplaced Tiles): {ebf_misplaced_tiles}\n")


def generate_random_puzzle():
    numbers = list(range(9))
    random.shuffle(numbers)
    return [numbers[i:i + 3] for i in range(0, 9, 3)]


# Set the goal state
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Print EBF for 100 random puzzles
for i in range(100):
    initial_state = generate_random_puzzle()
    print(f"State: {i + 1}")
    solve_and_print_ebf(initial_state, goal_state)
