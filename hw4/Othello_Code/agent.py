import math
import random
import othello

import game

class HumanPlayer(game.Player):

    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        # generate the list of moves:
        moves = state.generateMoves()

        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
        response = input('Please choose a move: ')
        return moves[int(response)]

class RandomAgent(game.Player):
    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        moves = state.generateMoves()
        if not moves:
            return None
        return random.choice(moves)


class MinimaxAgent(game.Player):
    def __init__(self, depth):
        super().__init__()
        #Default depth is 3 if no depth is provided
        self.depth = int(depth) if depth else 3
    
    def choose_move(self, state):
        moves = state.generateMoves()
        if not moves:
            return None
        
        best_score = float('-inf')
        best_move = moves[0]
        
        player = state.nextPlayerToMove
        
        for move in moves:
            next_state = state.applyMoveCloning(move)
            score = self.minimax(next_state, self.depth - 1, False, player)
            
            if score is not None and score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    #Used the website:
    #https://www.geeksforgeeks.org/mini-max-algorithm-in-artificial-intelligence/#
    #To help me understand the minimax algorithm and pseudocode for it.
    def minimax(self, state, depth, is_max, original_player):
        #Base case
        if depth == 0 or state.game_over():
            score = state.score()
            return score if original_player == othello.PLAYER1 else -score
        
        moves = state.generateMoves()
        
        if not moves:
            next_state = state.clone()
            next_state.nextPlayerToMove = othello.OTHER_PLAYER[next_state.nextPlayerToMove]
            return self.minimax(next_state, depth - 1, not is_max, original_player)
        
        if is_max:
            #If the current player is the original player, we want to maximize the score
            max_score = float('-inf')
            for move in moves:
                next_state = state.applyMoveCloning(move)
                score = self.minimax(next_state, depth - 1, False, original_player)
                if score is not None:
                    max_score = max(max_score, score)
            return max_score
        else:
            #If the current player is the opponent, we want to minimize the score
            min_score = float('inf')
            for move in moves:
                next_state = state.applyMoveCloning(move)
                score = self.minimax(next_state, depth - 1, True, original_player)
                if score is not None:
                    min_score = min(min_score, score)
            return min_score
            

class AlphaBeta(game.Player):
    def __init__(self, depth):
        super().__init__()
        #Default depth is 3 if no depth is provided
        self.depth = int(depth) if depth else 3
    
    def choose_move(self, state):
        moves = state.generateMoves()
        if not moves:
            return None
        
        best_score = float('-inf')
        best_move = moves[0]
        alpha = float('-inf')
        beta = float('inf')
        
        player = state.nextPlayerToMove
        
        for move in moves:
            next_state = state.applyMoveCloning(move)
            score = self.alpha_beta(next_state, self.depth - 1, alpha, beta, False, player)
            
            if score is not None and score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, best_score)
                
        return best_move
    
    
    #Used the website:
    #https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
    #To help me understand the alpha beta pruning and pseudocode for it.
    #Also this youtube video:
    #https://www.youtube.com/watch?v=l-hh51ncgDI&t=436s&ab_channel=SebastianLague
    def alpha_beta(self, state, depth, alpha, beta, is_max, original_player):
        #Base case
        if depth == 0 or state.game_over():
            score = state.score()
            return score if original_player == othello.PLAYER1 else -score
        
        #Get available moves for the current state
        moves = state.generateMoves()
        
        #If no moves are available, pass turn to opponent
        if not moves:
            next_state = state.clone()
            next_state.nextPlayerToMove = othello.OTHER_PLAYER[next_state.nextPlayerToMove]
            return self.alpha_beta(next_state, depth - 1, alpha, beta, not is_max, original_player)
        
        #If the current player is the original player, we want to maximize the score
        if is_max:
            max_score = float('-inf')
            for move in moves:
                next_state = state.applyMoveCloning(move)
                score = self.alpha_beta(next_state, depth - 1, alpha, beta, False, original_player)
                if score is not None:
                    max_score = max(max_score, score)
                #Alpha cutoff
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break
            return max_score
        else:
            #If the current player is the opponent, we want to minimize the score
            min_score = float('inf')
            for move in moves:
                next_state = state.applyMoveCloning(move)
                score = self.alpha_beta(next_state, depth - 1, alpha, beta, True, original_player)
                if score is not None:
                    min_score = min(min_score, score)
                #Beta cutoff
                beta = min(beta, min_score)
                if beta <= alpha:
                    break
            return min_score