import numpy as np

class Backgammon:
    def __init__(self, user_starts):
        self.board = self.init_board()
        self.bar = {1: 0, -1: 0}  # 1: User, -1: Opponent
        self.borne_off = {1: 0, -1: 0}
        self.user_is_player = user_starts
        self.turn = 1 if user_starts else -1
        self.dice = []
        self.roll_history = []
        self.doubling_cube = 1
        self.opponent_style = {"aggressive": 0, "conservative": 0}
        self.move_history = []  # Stores move history for analysis
    
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
    
    def receive_dice_input(self, dice_roll):
        if all(1 <= die <= 6 for die in dice_roll):
            self.dice = list(dice_roll) * 2 if dice_roll[0] == dice_roll[1] else list(dice_roll)
            self.roll_history.append(dice_roll)
        else:
            raise ValueError("Invalid dice roll. Please enter values between 1 and 6.")
    
    def generate_legal_moves(self, player):
        moves = []
        if self.bar[player] > 0:
            for die in self.dice:
                target = die - 1 if player == 1 else 24 - die
                if self.board[target] * player >= -1:
                    moves.append(("bar", target))
            return moves
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
        piece = 1 if self.board[start] > 0 else -1
        self.board[start] -= piece
        if self.board[end] == -piece:
            self.board[end] = 0
            self.bar[-piece] += 1
        self.board[end] += piece
        self.move_history.append(move)
    
    def best_moves(self):
        legal_moves = self.generate_legal_moves(self.turn)
        num_moves = 4 if len(self.dice) == 4 else 2
        return legal_moves[:num_moves] if legal_moves else []
    
    def undo_move(self, move):
        start, end = move
        piece = 1 if self.board[end] > 0 else -1
        self.board[end] -= piece
        self.board[start] += piece
    
    def decide_doubling(self):
        win_probability = self.evaluate_board(self.turn) / max(1, sum(abs(self.board)))
        if win_probability > 0.75 and self.doubling_cube == 1 and len(self.roll_history) > 2:
            return "Double"
        return "No Double"
    
    def play_turn(self, dice_roll):
        self.receive_dice_input(dice_roll)
        moves = self.best_moves()
        if moves:
            print("Bot suggests these moves:")
            for move in moves:
                print(f"Move from {move[0]} to {move[1]}")
            for move in moves:
                self.apply_move(move)
        doubling_decision = self.decide_doubling()
        self.turn *= -1
        return doubling_decision
    
    def apply_opponent_moves(self, moves):
        for start, end in moves:
            if start == "bar":
                self.bar[-1] -= 1
                start = 0 if self.user_is_player else 23
            piece = np.sign(self.board[start])
            self.board[start] -= piece
            if self.board[end] == -piece:
                self.board[end] = 0
                self.bar[-piece] += 1
            self.board[end] += piece
    
if __name__ == "__main__":
    user_first = input("Are you going first? (yes/no): ").strip().lower() == "yes"
    game = Backgammon(user_first)
    if not user_first:
        opponent_dice_roll = tuple(map(int, input("Enter opponent's dice roll (e.g., 3 5): ").split()))
        num_opponent_moves = 4 if len(opponent_dice_roll) == 4 else 2
        opponent_moves = []
        for _ in range(num_opponent_moves):
            move = tuple(map(int, input("Enter opponent's move (start and end point, e.g., 12 17): ").split()))
            opponent_moves.append(move)
        game.apply_opponent_moves(opponent_moves)
    print("This bot will help you make the best moves in Backgammon. Roll your dice and enter the result to get the best move suggestion.")
    while max(game.borne_off.values()) < 15:
        game.display_board()
        dice_roll = tuple(map(int, input("Enter your dice roll (e.g., 3 5): ").split()))
        doubling_decision = game.play_turn(dice_roll)
        print(f"Doubling Decision: {doubling_decision}")

