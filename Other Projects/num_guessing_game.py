import random
import time

def number_guessing_game():
    # Display the welcome message only once at the beginning
    print(f"\nWelcome to the Number Guessing Game!")

    while True:
        # Set the range for the number
        lower_bound = 1
        upper_bound = 10
        number_to_guess = random.randint(lower_bound, upper_bound)

        print(f"\nI'm thinking of a number between {lower_bound} and {upper_bound}. Try to guess it!")

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
        if play_again not in ['yes', 'y', 'sure', 'yeah', 'ok', 'of course', 'ofc', 'alr']:
            print("\nThanks for playing! Goodbye!")
            break

# Start the game
number_guessing_game()
