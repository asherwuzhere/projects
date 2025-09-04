import random

def print_board(board, first_move=False):
    if first_move:
        num_board = [[str(r * 3 + c + 1) for c in range(3)] for r in range(3)]
    else:
        num_board = board
    
    for row in num_board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def number_to_coords(number):
    return ((number - 1) // 3, (number - 1) % 3)

def find_winning_move(board, player):
    for row in range(3):
        if board[row].count(player) == 2 and " " in board[row]:
            return (row, board[row].index(" "))
    for col in range(3):
        col_values = [board[row][col] for row in range(3)]
        if col_values.count(player) == 2 and " " in col_values:
            return (col_values.index(" "), col)
    main_diag = [board[i][i] for i in range(3)]
    if main_diag.count(player) == 2 and " " in main_diag:
        return (main_diag.index(" "), main_diag.index(" "))
    anti_diag = [board[i][2 - i] for i in range(3)]
    if anti_diag.count(player) == 2 and " " in anti_diag:
        return (anti_diag.index(" "), 2 - anti_diag.index(" "))
    return None

def check_opposite_corners(board, human):
    if board[0][0] == human and board[2][2] == human:
        return [(0, 1), (1, 0), (1, 2), (2, 1)]
    if board[0][2] == human and board[2][0] == human:
        return [(0, 1), (1, 0), (1, 2), (2, 1)]
    return None

def bot_move(board, turn, human, bot):
    if turn == 1:
        if board[1][1] == human:
            return random.choice([(0, 0), (0, 2), (2, 0), (2, 2)])
        return (1, 1)
    win_move = find_winning_move(board, bot)
    if win_move:
        return win_move
    block_move = find_winning_move(board, human)
    if block_move:
        return block_move
    corner_block = check_opposite_corners(board, human)
    if turn == 3 and corner_block:
        for move in corner_block:
            if board[move[0]][move[1]] == " ":
                return move
    moves = get_available_moves(board)
    return random.choice(moves)

def play_tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    human = "X"
    bot = "O"
    
    print("Welcome to Tic Tac Toe!")
    print_board(board, first_move=True)
    
    for turn in range(9):
        if turn % 2 == 0:
            move = int(input("Enter your move (1-9): "))
            row, col = number_to_coords(move)
            while (row, col) not in get_available_moves(board):
                print("Invalid move, try again.")
                move = int(input("Enter your move (1-9): "))
                row, col = number_to_coords(move)
            board[row][col] = human
        else:
            row, col = bot_move(board, turn, human, bot)
            print(f"Bot chooses: {row * 3 + col + 1}")
            board[row][col] = bot
        
        print_board(board)
        
        if check_winner(board, human):
            print("You win!")
            return
        elif check_winner(board, bot):
            print("Bot wins!")
            return
    
    print("It's a draw!")

if __name__ == "__main__":
    play_tic_tac_toe()
