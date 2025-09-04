# The main difference between dynamic points and static points is that the dynamic points is based on the remain possible wordle answers shown in wordle_words.txt while static points uses letter frequency in the English language

from collections import Counter

with open("wordle_words.txt", "r") as file:
    word_list = [line.strip() for line in file]

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
w = ["GGGGG", "w", "win", "won", "done", "next"]

# Estimated letter frequencies (scores)
letter_scores = {
    'e': 7.7, 'r': 5.1, 'a': 8.5, 'o': 5.15, 't': 4.1, 
    'i': 5, 'l': 4.2, 's': 6.5, 'c': 2.7, 'n': 4, 
    'u': 3.4, 'p': 2.3, 'd': 2.8, 'b': 2.05, 'y': 2.45, 
    'g': 2, 'h': 2.3, 'm': 2.4, 'f': 1.3, 'k': 1.8, 
    'w': 1.2, 'v': 1, 'x': 0.5, 'z': 0.65, 'j': 0.5, 'q': 0.2
}

vowels = {'a', 'e', 'i', 'o', 'u'}

def calculate_word_score(word):
    score = sum(letter_scores.get(letter, 0) for letter in word)
    letter_counts = Counter(word)
    
    if any(count == 2 for count in letter_counts.values()):
        score -= 5
    if any(count >= 3 for count in letter_counts.values()):
        score -= 10
    
    vowel_count = sum(1 for letter in word if letter in vowels)
    if vowel_count == 3:
        score -= 3
    elif vowel_count >= 4:
        score -= 5
    
    return score

sorted_words = sorted(word_list, key=calculate_word_score, reverse=True)

def filter_words(word_list, guess, feedback):
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

while True:
    print("\nWelcome to Asher Lieberman's Wordle Bot!")
    print("\nFirst guess: crane.")
    
    remaining_words = sorted_words
    first_guess = "crane"
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
            print("\nCONGRATULATIONS, YOU GOT IT!")
            break
        
        remaining_words = filter_words(remaining_words, first_guess, feedback)
        
        if len(remaining_words) == 1:
            print(f"The word is: {remaining_words[0]}")
            break
        elif len(remaining_words) == 0:
            print("No possible words found. Please check your feedback!")
            break
        
        first_guess = remaining_words[0]
        first_turn = False
    
    play_again = input("\nDo you want to play another game? (yes/no): ").strip().lower()
    if play_again.casefold() not in yes:
        print("Thanks for playing! Goodbye!")
        break
