import random

# Define card values and suits
suits = ['h', 'd', 'c', 's']
values = ['2', '3', '4', '5', '6', '7', '8', '9', 't', 'j', 'q', 'k', 'a']
chen_points = {'a': 10, 'k': 8, 'q': 7, 'j': 6, 't': 5, '9': 4.5, '8': 4, '7': 3.5, '6': 3, '5': 2.5, '4': 2, '3': 1.5, '2': 1}

# Generate a deck of cards
def generate_deck():
    return [f"{value}{suit}" for value in values for suit in suits]

# Validate player input
def validate_hand_input(hand):
    deck = generate_deck()
    return bool(hand) and len(hand) == len(set(hand)) and all(card in deck for card in hand)

# Get player's hand input
def get_player_hand():
    while True:
        hand = input("Enter your hand (e.g., 'ah kc'): ").lower().split()
        if len(hand) == 2 and validate_hand_input(hand):
            return hand
        print("Invalid hand. Please enter valid cards.")

# Get community cards input
def get_community_cards(stage):
    while True:
        cards = input(f"Enter the {stage} (e.g., 'ah kc td'): ").lower().split()
        expected = 3 if stage == "flop" else 1
        if len(cards) == expected and validate_hand_input(cards):
            return cards
        print("Invalid input. Please enter valid cards.")

# Compute Chen formula score
def chen_formula(hand):
    ranks = sorted([card[:-1] for card in hand], key=lambda x: values.index(x), reverse=True)
    suits = [card[-1] for card in hand]
    
    high_card = ranks[0]
    low_card = ranks[1]
    score = max(chen_points[high_card], 5)  # Highest card
    
    if high_card == low_card:
        score *= 2  # Pair bonus
        if high_card == '5':
            score += 1  # 55 gets an extra point
    
    if suits[0] == suits[1]:
        score += 2  # Suited bonus
    
    gap = abs(values.index(high_card) - values.index(low_card))
    if gap == 1:
        score -= 1
    elif gap == 2:
        score -= 2
    elif gap == 3:
        score -= 4
    elif gap >= 4:
        score -= 5
    
    if (gap <= 1) and (values.index(high_card) < values.index('q')):
        score += 1  # Bonus for making higher straights
    
    return max(score, 0)

# Provide pre-flop advice based solely on Chen score
def pre_flop_advice(score):
    if score >= 10:
        return "Bet aggressively. You have a strong hand."
    elif score >= 7:
        return "Raise. You have a solid hand."
    elif score >= 5:
        return "Call or check. Play cautiously."
    else:
        return "Fold. Your hand is weak."

# Evaluate hand strength with community cards
def evaluate_hand_with_community(hand, community):
    full_hand = hand + community
    ranks = [card[:-1] for card in full_hand]
    suits = [card[-1] for card in full_hand]
    unique_ranks = set(ranks)
    unique_suits = set(suits)

    rank_counts = sorted((ranks.count(rank) for rank in unique_ranks), reverse=True)
    if rank_counts[0] >= 4:
        return "Very Strong Hand"
    elif rank_counts[0] == 3 or rank_counts.count(2) >= 2:
        return "Strong Hand"
    elif max(suits.count(suit) for suit in unique_suits) >= 4:
        return "Flush or Flush Draw"
    elif rank_counts[0] == 2:
        return "Pair or Two Pair"
    return "Weak Hand"

# Poker advice function
def poker_advice(hand, community):
    evaluation = evaluate_hand_with_community(hand, community)
    bluff_chance = random.randint(1, 5)
    
    if evaluation == "Very Strong Hand":
        return "Bet aggressively. You are in a dominant position."
    elif evaluation == "Strong Hand":
        return "Raise or bet. You have a solid hand."
    elif evaluation == "Flush or Flush Draw":
        return "Consider semi-bluffing. Your flush draw is strong."
    elif evaluation == "Pair or Two Pair":
        return "Call or raise if needed. You have a decent hand."
    elif bluff_chance == 5:
        return "Bluff! Use aggressive play strategically based on opponent tendencies."
    else:
        return "Fold. Your hand is too weak to continue."

# Simulate a game round
def play_poker():
    while True:
        hand = get_player_hand()
        community = []
        chen_score = chen_formula(hand)
        
        print("Your hand:", hand)
        print("Chen formula score:", chen_score)
        advice = pre_flop_advice(chen_score)
        print("Pre-flop action:", advice)
        
        if "Fold" in advice:
            continue
        
        # Flop
        community = get_community_cards("flop")
        print("Flop:", community)
        advice = poker_advice(hand, community)
        print("Flop action:", advice)
        
        if "Fold" in advice:
            continue
        
        # Turn
        community.append(get_community_cards("turn")[0])
        print("Turn:", community)
        advice = poker_advice(hand, community)
        print("Turn action:", advice)
        
        if "Fold" in advice:
            continue
        
        # River
        community.append(get_community_cards("river")[0])
        print("River:", community)
        advice = poker_advice(hand, community)
        print("Final action:", advice)
        
        if "Fold" in advice:
            continue
        
        restart = input("Enter 'r' to restart or any other key to exit: ").lower()
        if restart != 'r':
            break

if __name__ == "__main__":
    play_poker()
