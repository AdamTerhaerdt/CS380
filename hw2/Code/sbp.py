import sys
import random

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
    available_moves = get_available_moves(board)
    
    if move not in available_moves:
        print("Error: Invalid move")
        sys.exit(1)
        
    # Clear old positions
    for x, y in coords:
        board[y][x] = EMPTY_CELL
    # Set new positions  
    for x, y in new_coords:
        board[y][x] = piece
    return board

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
    
    for x, y in new_coords:
        # Check if wall
        if int(board[y][x]) == WALL:
            #print("NOT ALLOWED WALL")
            return False
        
        # Check if new position is empty or if piece 2 moving to goal
        if int(board[y][x]) != EMPTY_CELL and int(board[y][x]) != piece:
            if piece == 2 and int(board[y][x]) == GOAL:
                #print("ALLOWED NOT EMPTY TO GOAL")
                return True
            #print("NOT ALLOWED NOT EMPTY")
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
    #Set to get unique pieces
    pieces = set()
    for row in board:
        for cell in row:
            if int(cell) != EMPTY_CELL and int(cell) != WALL and int(cell) != GOAL:
                pieces.add(int(cell))
    # Get moves for each piece
    for piece in pieces:
        piece_moves = get_specific_piece_moves(board, piece)
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
        case _:
            print(f"Error: Unknown command '{command}'")
            sys.exit(1)

if __name__ == "__main__":
    main()
