import random
import time

# Rock, Paper, Scissors
def rock_paper_scissors():
    print("Welcome to Rock, Paper, Scissors!")
    choices = ["rock", "paper", "scissors"]
    
    while True:
        user_choice = input("Enter rock, paper, or scissors (or 'exit' to quit): ").lower()
        if user_choice == 'exit':
            print("Thanks for playing! Goodbye!")
            break
        if user_choice not in choices:
            print("Invalid choice, please try again.")
            continue

        computer_choice = random.choice(choices)
        print(f"Computer chose: {computer_choice}")
        
        if user_choice == computer_choice:
            print("It's a tie!")
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "scissors" and computer_choice == "paper") or \
             (user_choice == "paper" and computer_choice == "rock"):
            print("You win!")
        else:
            print("Computer wins!")

# Tic-Tac-Toe
def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_win(board, player):
    # Check rows, columns, and diagonals
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or \
       all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    turn = 0

    print("Welcome to Tic-Tac-Toe!")
    while True:
        print_board(board)
        print(f"Player {players[turn % 2]}'s turn.")
        
        row = int(input("Enter row (0, 1, 2): "))
        col = int(input("Enter column (0, 1, 2): "))
        
        if board[row][col] != " ":
            print("Cell already taken, try again.")
            continue
        
        board[row][col] = players[turn % 2]
        
        if check_win(board, players[turn % 2]):
            print_board(board)
            print(f"Player {players[turn % 2]} wins!")
            break
        
        if all(cell != " " for row in board for cell in row):
            print_board(board)
            print("It's a tie!")
            break

        turn += 1

# Hangman
def hangman():
    words = ["pickle", "galaxy", "quokka", "umbrella", "zeppelin", "marshmallow", "tornado", "sphinx", "noodle", "kazoo", "turtle", "whisker", "jalapeño", "fireworks", "avalanche", "platypus", "banjo", "spaghetti", "narwhal", "bubble", "mongoose", "cupcake", "yodel", "popsicle", "sloth", "zebra", "tofu", "giraffe", "lollipop", "cactus", "pogo", "doodle", "iguana", "maracas", "sundae", "hammock", "penguin", "trombone", "koala", "pineapple"]
    word_to_guess = random.choice(words)
    guessed_word = ["_"] * len(word_to_guess)
    attempts = 6
    guessed_letters = []

    print("Welcome to Hangman!")
    
    while attempts > 0:
        print("\n" + " ".join(guessed_word))
        guess = input(f"Guess a letter (Attempts left: {attempts}): ").lower()
        
        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue
        
        if guess not in word_to_guess:
            attempts -= 1
            print(f"Wrong guess! {attempts} attempts left.")
        else:
            for i in range(len(word_to_guess)):
                if word_to_guess[i] == guess:
                    guessed_word[i] = guess
        
        guessed_letters.append(guess)

        if "_" not in guessed_word:
            print(f"\nCongratulations! You've guessed the word: {word_to_guess}")
            break
    else:
        print(f"\nGame Over! The word was: {word_to_guess}")

# Word Scramble
def word_scramble():
    words = ["python", "java", "javascript", "ruby", "html"]
    word_to_guess = random.choice(words)
    scrambled_word = "".join(random.sample(word_to_guess, len(word_to_guess)))

    print(f"Scrambled word: {scrambled_word}")
    guess = input("Guess the word: ").lower()

    if guess == word_to_guess:
        print("Congratulations! You guessed the word correctly!")
    else:
        print(f"Wrong guess! The correct word was {word_to_guess}.")

# Number Guessing Game
def number_guessing_game():
    print(f"\nWelcome to the Number Guessing Game!\n")

    while True:
        # Set the range for the number
        lower_bound = 1
        upper_bound = 10
        number_to_guess = random.randint(lower_bound, upper_bound)

        print(f"I'm thinking of a number between {lower_bound} and {upper_bound}. Try to guess it!")

        attempts = 0

        # Game loop
        while True:
            user_guess = input("\nEnter your guess: ")

            # Ensure the input is a valid integer
            try:
                user_guess = int(user_guess)
            except ValueError:
                print("Please enter a valid number.")
                continue

            # Check if the guess is within the valid range
            if user_guess < lower_bound or user_guess > upper_bound:
                print(f"Your guess is out of range! Please guess a number between {lower_bound} and {upper_bound}.")
                continue

            attempts += 1

            # Check the guess
            if user_guess < number_to_guess:
                print("Too low! Try again.")
            elif user_guess > number_to_guess:
                print("Too high! Try again.")
            else:
                print(f"\nCongratulations! You've guessed the number {number_to_guess} in {attempts} attempts.")
                break

        # Wait for 2 seconds before asking to play again
        time.sleep(2)

        # Ask if the user wants to play again
        play_again = input("\nDo you want to play again? : ").lower()
        if play_again not in ['yes', 'y', 'sure', 'yeah', 'ok', 'of course', 'ofc','alr']:
            print("\nThanks for playing! Goodbye!")
            break

# Main Menu
def main_menu():
    while True:
        print("\nWelcome to the Game Hub! Choose a game to play:")
        print("1. Rock, Paper, Scissors")
        print("2. Tic-Tac-Toe")
        print("3. Hangman")
        print("4. Word Scramble")
        print("5. Number Guessing Game")
        print("6. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == '1':
            rock_paper_scissors()
        elif choice == '2':
            tic_tac_toe()
        elif choice == '3':
            hangman()
        elif choice == '4':
            word_scramble()
        elif choice == '5':
            number_guessing_game()
        elif choice == '6':
            print("\nThanks for playing! Goodbye!")
            break
        else:
            print("\nInvalid choice, please try again.")

# Start the Game Hub
main_menu()
