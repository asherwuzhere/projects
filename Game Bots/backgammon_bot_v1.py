import numpy as np

class Backgammon:
    def __init__(self):
        self.board = self.init_board()
        self.bar = {1: 0, -1: 0}  # 1: Player, -1: Opponent
        self.borne_off = {1: 0, -1: 0}
        self.turn = 1  # 1 for player, -1 for opponent
        self.dice = []
        self.roll_history = []
        self.doubling_cube = 1
        self.opponent_style = {"aggressive": 0, "conservative": 0}
    
    def init_board(self):
        board = np.zeros(24, dtype=int)
        board[0], board[23] = 2, -2
        board[5], board[18] = -5, 5
        board[7], board[16] = -3, 3
        board[11], board[12] = 5, -5
        return board
    
    def display_board(self):
        print("Current Board State:")
        print(self.board)
        print(f"Bar: {self.bar}")
        print(f"Borne Off: {self.borne_off}")
    
    def receive_dice_input(self, current_roll, opponent_last_roll, bot_last_roll):
        if all(1 <= die <= 6 for die in current_roll):
            self.dice = list(current_roll) * 2 if current_roll[0] == current_roll[1] else list(current_roll)
            self.roll_history.append((self.turn, current_roll, opponent_last_roll, bot_last_roll))
        else:
            raise ValueError("Invalid dice roll. Please enter values between 1 and 6.")
    
    def generate_legal_moves(self, player):
        moves = []
        for die in self.dice:
            for point in range(24):
                if self.board[point] * player > 0:
                    target = point + die * player
                    if 0 <= target < 24 and (self.board[target] * player >= -1):
                        moves.append((point, target))
        return sorted(moves, key=lambda m: self.evaluate_board_after_move(m, player), reverse=True)
    
    def evaluate_board(self, player):
        score = 0
        for i in range(24):
            if self.board[i] * player > 0:
                score += abs(self.board[i]) * (i if player == 1 else 23 - i)
        return score
    
    def evaluate_board_after_move(self, move, player):
        self.apply_move(move)
        score = self.evaluate_board(player)
        self.undo_move(move)
        return score
    
    def apply_move(self, move):
        start, end = move
        piece = np.sign(self.board[start])
        self.board[start] -= piece
        if self.board[end] == -piece:
            self.board[end] = 0
            self.bar[-piece] += 1
        self.board[end] += piece
    
    def best_move(self):
        legal_moves = self.generate_legal_moves(self.turn)
        return legal_moves[0] if legal_moves else None
    
    def undo_move(self, move):
        start, end = move
        piece = np.sign(self.board[end])
        self.board[end] -= piece
        self.board[start] += piece
    
    def decide_doubling(self):
        win_probability = self.evaluate_board(self.turn) / sum(abs(self.board))
        if win_probability > 0.75 and self.doubling_cube == 1:
            return "Double"
        return "No Double"
    
    def track_opponent_style(self, last_roll):
        if sum(last_roll) >= 10:
            self.opponent_style["aggressive"] += 1
        else:
            self.opponent_style["conservative"] += 1
    
    def play_turn(self, current_roll, opponent_last_roll, bot_last_roll):
        self.receive_dice_input(current_roll, opponent_last_roll, bot_last_roll)
        self.track_opponent_style(opponent_last_roll)
        move = self.best_move()
        if move:
            self.apply_move(move)
        doubling_decision = self.decide_doubling()
        self.turn *= -1
        return doubling_decision
    
if __name__ == "__main__":
    game = Backgammon()
    while max(game.borne_off.values()) < 15:
        game.display_board()
        current_roll = tuple(map(int, input("Enter dice roll (e.g., 3 5): ").split()))
        opponent_last_roll = tuple(map(int, input("Enter opponent's last roll (e.g., 2 6): ").split()))
        bot_last_roll = tuple(map(int, input("Enter bot's last roll (e.g., 4 4): ").split()))
        doubling_decision = game.play_turn(current_roll, opponent_last_roll, bot_last_roll)
        print(f"Doubling Decision: {doubling_decision}")
