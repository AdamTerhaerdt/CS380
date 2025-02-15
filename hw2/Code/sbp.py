import sys
import random
from queue import Queue
from stack import Stack
from priority_queue import PriorityQueue
import time

#CONSTANTS
GOAL = -1
EMPTY_CELL = 0
WALL = 1
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

#GLOBAL VARIABLES
ROWS = 0
COLS = 0

def random_walk(board, n):
    moves_made = 0
    while moves_made < n:
        available_moves = get_available_moves(board)
        if not available_moves:
            print("No moves available!")
            break
        move = random.choice(available_moves)
        piece, direction = move
        print(f"Move {moves_made + 1}: ({piece}, {direction})")
        apply_move(board, move)
        normalize_board(board)
        #print_board(board)
        #print()
        if check_solution(board):
            print("Goal reached!")
            break
            
        moves_made += 1

def swap_indices(idx1, idx2, board):
    for i in range(ROWS):
        for j in range(COLS):
            if int(board[i][j]) == idx1:
                board[i][j] = str(idx2)
            elif int(board[i][j]) == idx2:
                board[i][j] = str(idx1)
    return board

def normalize_board(board):
    next_idx = 3
    for i in range(ROWS):
        for j in range(COLS):
            current = int(board[i][j])
            if current == next_idx:
                next_idx += 1
            elif current > next_idx:
                board = swap_indices(next_idx, current, board)
                next_idx += 1 
    return board

def compare_boards(board1, board2):
    if len(board1) != len(board2) or len(board1[0]) != len(board2[0]):
        return False
    
    for i in range(len(board1)):
        for j in range(len(board1[0])):
            if board1[i][j] != board2[i][j]:
                return False
    return True

def apply_move(board, move):
    if not isinstance(move, tuple) or len(move) != 2:
        print("Error: Invalid move")
        sys.exit(1)
        
    piece, direction = move
    
    if not isinstance(piece, int) or not isinstance(direction, str):
        print("Error: Invalid move")
        sys.exit(1)
        
    coords = find_piece_coordinates(board, piece)
    
    if direction not in DIRECTIONS:
        print("Error: Invalid move")
        sys.exit(1)
        
    dx, dy = DIRECTIONS[direction]
    new_coords = [(x + dx, y + dy) for x, y in coords]
    
    new_board = [row[:] for row in board]
        
    for x, y in coords:
        new_board[y][x] = str(EMPTY_CELL)
          
    for x, y in new_coords:
        new_board[y][x] = str(piece)
        
    return new_board

def parse_move(move_str):
    # Remove parentheses and split by comma
    move_str = move_str.strip('()')
    piece, direction = move_str.split(',')
    return (int(piece), direction.strip().upper()) 

def find_piece_coordinates(board, piece):
    coords = []
    for i in range(ROWS):
        row = board[i]
        for j in range(COLS):
            if int(row[j]) == piece:
                coords.append((j, i))
    return coords

def is_valid_move(board, piece_coords, direction, piece):
    dx, dy = DIRECTIONS[direction]
    new_coords = [(x + dx, y + dy) for x, y in piece_coords]
    
    # First, get the set of current piece coordinates to ignore them
    current_piece_coords = set((x, y) for x, y in piece_coords)
    
    # Check if any new coordinates are out of bounds
    for x, y in new_coords:
        if x < 0 or x >= COLS or y < 0 or y >= ROWS:
            return False
            
        # Skip if this coordinate is part of the current piece
        if (x, y) in current_piece_coords:
            continue
            
        # Check if wall - no piece should ever move into a wall
        if int(board[y][x]) == WALL:
            return False
        
        # Check if new position is empty or if piece 2 moving to goal
        cell_value = int(board[y][x])
        if cell_value != EMPTY_CELL:
            # Only allow piece 2 to move into goal, and ALL cells must be valid
            if piece == 2 and cell_value == GOAL:
                continue  # Check other cells
            return False
    return True

def get_new_coords(piece_coords, direction):
    dx, dy = DIRECTIONS[direction]
    return [(x + dx, y + dy) for x, y in piece_coords]

def get_specific_piece_moves(board, piece):
    moves = []
    coords = find_piece_coordinates(board, piece)
    for direction in DIRECTIONS:
        if is_valid_move(board, coords, direction, piece):
            moves.append((piece, direction))
    
    return moves

def get_available_moves(board):
    moves = []
    pieces = sorted(set(int(cell) for row in board 
                   for cell in row 
                   if int(cell) != EMPTY_CELL and int(cell) != WALL and int(cell) != GOAL), 
               reverse=True)  # Process larger piece numbers first

    for piece in pieces:
        piece_moves = []
        for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            coords = find_piece_coordinates(board, piece)
            if is_valid_move(board, coords, direction, piece):
                piece_moves.append((piece, direction))
        moves.extend(piece_moves)
    
    return moves

def check_solution(board):
    for row in board:
        for cell in row:
            if int(cell) == GOAL:
                return False
    return True

def print_board(board):
    print(str(COLS) + ", " + str(ROWS))
    for row in board:
        print(' ' + ', '.join(f"{int(cell):2d}" for cell in row))

def load_board(filename):
    global ROWS, COLS
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            dimensions = [int(x) for x in lines[0].strip().split(',') if x]
            COLS, ROWS = dimensions[0], dimensions[1]
            board = []
            for line in lines[1:]:
                row = [int(cell) for cell in line.strip().split(',') if cell]
                board.append(row)
            return board
            
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        sys.exit(1)
    except IOError:
        print(f"Error: Could not read file '{filename}'")
        sys.exit(1)
        
def calculate_heuristic(board):
    goal_position = None
    for i in range(ROWS):
        for j in range(COLS):
            if int(board[i][j]) == GOAL:
                goal_position = (j, i)
                break
        if goal_position:
            break
    
    if not goal_position:
        return 0 
    
    piece_coords = find_piece_coordinates(board, 2)
    if not piece_coords:
        print("Error: No piece 2 found")
        sys.exit(1)
    
    min_distance = float('inf')
    for coord in piece_coords:
        distance = calculate_manhattan_distance(
            coord[0], coord[1],
            goal_position[0], goal_position[1]
        )
        #print("DISTANCE: " + str(distance))
        min_distance = min(min_distance, distance)
    
    return min_distance

def calculate_manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def search(board, data_structure, depth_limit=None):
    start_time = time.time()
    nodes_explored = 1
    board = normalize_board(board)
    inital = calculate_heuristic(board)
    current_depth = 1 if depth_limit is not None else None

    while True:
        if depth_limit is not None:
            data_structure = Stack()
        data_structure.push([board, []], inital)
        visited = set()
        while not data_structure.is_empty():
            result = data_structure.pop()
            if isinstance(result, tuple) and len(result) == 2:
                current_board = result[0][0]
                current_moves = result[0][1]
                priority = result[1]
            else:
                current_board, current_moves = result
                priority = None
            #print(f"Current board: {current_board}")
            #print(f"Current moves: {current_moves}")
            current_depth_of_node = len(current_moves)
            
            if check_solution(current_board):
                #print("\nSOLUTION FOUND!")
                end_time = time.time()
                solution_length = len(current_moves)
                for piece, direction in current_moves:
                    print(f"({piece},{direction})")
                print()
                print_board(current_board)
                print()
                print(nodes_explored)
                print(f"{(end_time - start_time):.2f}")
                print(solution_length)
                return

            if depth_limit is not None and len(current_moves) >= current_depth:
                #print(f"Skipping - reached depth limit {current_depth}")
                continue

            board_tuple = tuple(tuple(int(cell) for cell in row) for row in current_board)
            if board_tuple in visited:
                #print("Skipping - already visited")
                continue
                
            visited.add(board_tuple)
            if depth_limit is None or len(current_moves) + 1 == current_depth:
                nodes_explored += 1
            
            if depth_limit is None or len(current_moves) < current_depth:
                available_moves = get_available_moves(current_board)
                #print(f"Available moves: {available_moves}")
                for move in available_moves:
                    new_board = [row[:] for row in current_board]
                    new_board = apply_move(new_board, move)
                    new_board = normalize_board(new_board)
                    if priority is not None:
                        new_priority = priority + 1
                        new_h_cost = calculate_heuristic(new_board)
                        new_f_cost = new_priority + new_h_cost
                    else:
                        new_f_cost = None
                    data_structure.push([new_board, current_moves + [move]], new_f_cost)
        
        if current_depth is None:
            end_time = time.time()
            print(nodes_explored)
            print(f"{(end_time - start_time):.2f}")
            print("No solution found")
            return
            
        current_depth += 1
        if current_depth > 1000:
            end_time = time.time()
            print(nodes_explored)
            print(f"{(end_time - start_time):.2f}")
            print("No solution found")
            return

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 sbp.py <command> [<optional-argument>]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    match command:
        case "print":
            if len(sys.argv) != 3:
                print("Error: Board file required for print command")
                sys.exit(1)
            filename = sys.argv[2]
            board = load_board(filename)
            print_board(board)
        case "done":
            if len(sys.argv) != 3:
                print("Error: Board file required for done command") 
                sys.exit(1)
            filename = sys.argv[2]
            board = load_board(filename)
            result = check_solution(board)
            print(result)
        case "availableMoves":
            if len(sys.argv) != 3:
                print("Error: Board file required for availableMoves command")
                sys.exit(1)
            filename = sys.argv[2]
            board = load_board(filename)
            available_moves = get_available_moves(board)
            for piece, direction in available_moves:
                print(f"({piece}, {direction})")
        case "applyMove":
            if len(sys.argv) != 4:
                print("Error: Board file and move required for applyMove command")
                sys.exit(1)
            filename = sys.argv[2]
            board = load_board(filename)
            move = parse_move(sys.argv[3])
            board = apply_move(board, move)
            print_board(board)
        case "compare":
            if len(sys.argv) != 4:
                print("Error: Two board files required for comparison")
                sys.exit(1)
            board1 = load_board(sys.argv[2])
            board2 = load_board(sys.argv[3])
            result = compare_boards(board1, board2)
            print(result)
        case "norm":
            if len(sys.argv) != 3:
                print("Error: Board file required for norm command")
                sys.exit(1)
            filename = sys.argv[2]
            board = load_board(filename)
            normalized_board = normalize_board(board)
            print_board(normalized_board)
        case "random":
            if len(sys.argv) != 4:
                print("Error: Board file required for random command")
                sys.exit(1)
            filename = sys.argv[2]
            n_moves = int(sys.argv[3])
            board = load_board(filename)
            #print_board(board)
            random_walk(board, n_moves)
        case "bfs":
            if len(sys.argv) != 3:
                print("Error: Board file required for bfs command")
                sys.exit(1)
            filename = sys.argv[2]  
            board = load_board(filename)
            search(board, Queue())
        case "dfs":
            if len(sys.argv) != 3:
                print("Error: Board file required for dfs command")
                sys.exit(1)
            filename = sys.argv[2]
            board = load_board(filename)
            search(board, Stack())
        case "ids":
            if len(sys.argv) != 3:
                print("Error: Board file required for ids command")
                sys.exit(1)
            filename = sys.argv[2]
            board = load_board(filename)
            search(board, Stack(), 1)
        case "astar":
            if len(sys.argv) != 3:
                print("Error: Board file required for astar command")
                sys.exit(1)
            filename = sys.argv[2]
            board = load_board(filename)
            search(board, PriorityQueue())
        case _:
            print(f"Error: Unknown command '{command}'")
            sys.exit(1)

if __name__ == "__main__":
    main()
