import math
import random
import othello
import game
import time
import copy

class extra(game.Player):
    def __init__(self, time_limit):
        super().__init__()
        self.time_limit = int(time_limit) / 1000 if time_limit else 0.1
        self.best_move = None
    
    def choose_move(self, state):
        start_time = time.time()
        time_elapsed = 0
        moves = state.generateMoves()
        if not moves:
            return None
        self.best_move = moves[0]
        
        player = state.nextPlayerToMove
        depth = 1
        
        #Want to search for 85% of the time limit
        #So we still have time to return the best move
        while time_elapsed < self.time_limit * 0.85:
            
            try:
                best_score = float('-inf')
                alpha = float('-inf')
                beta = float('inf')
                
                for move in moves:
                    next_state = state.applyMoveCloning(move)
                    score = self.alpha_beta(next_state, depth, alpha, beta, False, player, start_time)
                    
                    if score is not None and score > best_score:
                        best_score = score
                        self.best_move = move
                    
                    alpha = max(alpha, best_score)
                    time_elapsed = time.time() - start_time
                    if time_elapsed >= self.time_limit * 0.9:
                        break
                
                depth += 1
                
            except TimeoutError:
                break
            
            time_elapsed = time.time() - start_time
        
        return self.best_move
    
    def alpha_beta(self, state, depth, alpha, beta, is_max, original_player, start_time):
        if time.time() - start_time >= self.time_limit * 0.9:
            raise TimeoutError("Time limit exceeded")
        
        if depth == 0 or state.game_over():
            score = state.score()
            return score if original_player == othello.PLAYER1 else -score
        
        moves = state.generateMoves()
        if not moves:
            next_state = state.clone()
            next_state.nextPlayerToMove = othello.OTHER_PLAYER[next_state.nextPlayerToMove]
            return self.alpha_beta(next_state, depth - 1, alpha, beta, not is_max, original_player, start_time)
        
        if is_max:
            max_score = float('-inf')
            for move in moves:
                next_state = state.applyMoveCloning(move)
                score = self.alpha_beta(next_state, depth - 1, alpha, beta, False, original_player, start_time)
                if score is not None:
                    max_score = max(max_score, score)
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = float('inf')
            for move in moves:
                next_state = state.applyMoveCloning(move)
                score = self.alpha_beta(next_state, depth - 1, alpha, beta, True, original_player, start_time)
                if score is not None:
                    min_score = min(min_score, score)
                beta = min(beta, min_score)
                if beta <= alpha:
                    break
            return min_score