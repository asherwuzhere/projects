# The main difference between dynamic points and static points is that the dynamic points is based on the remain possible wordle answers shown in wordle_words.txt while static points uses letter frequency in the English language

import random
from collections import Counter
# Load word list from file
with open("wordle_words.txt", "r") as file:
    word_list = [line.strip().lower() for line in file]

yes = [
    "yes", "yeah", "yep", "y", "ye", "yup", "sure", "ya", "absolutely", "affirmative",
    "of course", "certainly", "indeed", "right", "roger", "ok", "okay",
    "aye", "uh-huh", "yessir", "yesss", "for sure", "definitely", 
    "you bet", "without a doubt", "totally", "exactly", "correct", 
    "indubitably", "by all means", "agreed", "I concur", "naturally",
    "gladly", "of course", "unquestionably", "alright", "okie-dokie",
    "for real", "yass", "heck yes", "amen", "count me in", "true",
    "10-4", "copy that", "right on", "sounds good", "yup yup",
    "you got it", "that’s right", "sure thing", "obviously"
]

invalid = ["INVALID", "I", "IN", "E", "ERR"]
w = ["GGGGG", "W", "WIN", "WON", "DONE", "NEXT"]
vowels = {'a', 'e', 'i', 'o', 'u'}

def compute_letter_frequencies(word_list):
    """Recomputes letter frequencies based on the current possible words."""
    position_frequencies = [{}, {}, {}, {}, {}]  # One dict per letter position
    for word in word_list:
        for i, letter in enumerate(word):
            position_frequencies[i][letter] = position_frequencies[i].get(letter, 0) + 1
    # Normalize frequencies
    for pos in range(5):
        total = sum(position_frequencies[pos].values())  # Total letter occurrences
        for letter in position_frequencies[pos]:
            position_frequencies[pos][letter] /= total  # Convert to probability
    return position_frequencies

def calculate_word_score(word, letter_frequencies):
    """Assigns a score to a word based on letter frequency at each position."""
    score = sum(letter_frequencies[i].get(letter, 0) for i, letter in enumerate(word))
    # Penalize repeated letters
    letter_counts = Counter(word)
    if any(count == 2 for count in letter_counts.values()):
        score -= 50
    if any(count >= 3 for count in letter_counts.values()):
        score -= 100
    # Penalize too many vowels
    vowel_count = sum(1 for letter in word if letter in vowels)
    if vowel_count == 3:
        score -= 30
    elif vowel_count >= 4:
        score -= 50
    # Penalize words ending in 's'
    if word.endswith('s'):
        score -= 30
    return score

def rank_words(word_list):
    """Ranks words dynamically based on updated letter frequencies."""
    letter_frequencies = compute_letter_frequencies(word_list)
    return sorted(word_list, key=lambda word: calculate_word_score(word, letter_frequencies), reverse=True)

def filter_words(word_list, guess, feedback):
    """Filters the word list based on Wordle-style feedback."""
    filtered_words = []
    for word in word_list:
        match = True
        for i, (letter, feedback_type) in enumerate(zip(guess, feedback)):
            if feedback_type == 'G' and word[i] != letter:
                match = False
            elif feedback_type == 'Y' and (letter not in word or word[i] == letter):
                match = False
            elif feedback_type == 'B' and letter in word and guess.count(letter) <= word.count(letter):
                match = False
        if match:
            filtered_words.append(word)
    return filtered_words
# Game loop
while True:
    print("\nWelcome to Asher Lieberman's Wordle Bot!")
    #a = random.randint(1, 10)
    remaining_words = rank_words(word_list)  # Initial ranking based on full list
    print(f"\nLet's start today with {remaining_words[0]}")
    first_guess = remaining_words[0] if remaining_words else ""
    first_turn = True
    while remaining_words:
        if not first_turn:
            print(f"\nNext guess: {first_guess}")
        feedback = input("\nEnter feedback (G for Green, Y for Yellow, B for Black) or type 'INVALID' if the word is not valid: ").upper().strip()
        if feedback in invalid:
            print(f"Word '{first_guess}' is invalid. Trying another word...")
            remaining_words.remove(first_guess)
            if not remaining_words:
                print("No possible words left!")
                break
            first_guess = remaining_words[0]
            continue 
        if feedback in w:
            print("CONGRATULATIONS, YOU GOT IT!")
            break
        # Filter words based on feedback
        remaining_words = filter_words(remaining_words, first_guess, feedback)
        # Recalculate ranking based on remaining words
        if remaining_words:
            remaining_words = rank_words(remaining_words)
            first_guess = remaining_words[0]
        if len(remaining_words) == 1:
            print(f"The word is: {remaining_words[0]}")
            break
        elif len(remaining_words) == 0:
            print("No possible words found. Please check your feedback!")
            break
        first_turn = False
    play_again = input("\nDo you want to play another game? (yes/no): ").strip().lower()
    if play_again.casefold() not in yes:
        print("Thanks for playing! Goodbye!")
        break
