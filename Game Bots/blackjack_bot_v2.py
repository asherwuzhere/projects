'''class BlackjackStrategyBot:
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4

    def calculate_score(self, hand):
        score = sum(hand)
        ace_count = hand.count(11)
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        return score

    def is_soft_hand(self, hand):
        return 11 in hand and sum(hand) <= 21

    def recommend_action(self, player_hand, dealer_card):
        player_total = self.calculate_score(player_hand)
        dealer_up = dealer_card
        
        if len(player_hand) == 2 and player_hand[0] == player_hand[1]:  # Check for pairs
            pair_card = player_hand[0]
            if pair_card == 11:
                return "Split"
            if pair_card == 10:
                return "Stand"
            if pair_card == 9 and dealer_up in [2, 3, 4, 5, 6, 8, 9]:
                return "Split"
            if pair_card == 8:
                return "Split"
            if pair_card == 7 and dealer_up in range(2, 8):
                return "Split"
            if pair_card == 6 and dealer_up in range(2, 7):
                return "Split"
            if pair_card == 5 and dealer_up in range(2, 10):
                return "Double Down"
            if pair_card == 4 and dealer_up in [5, 6]:
                return "Split"
            if pair_card in [2, 3] and dealer_up in range(2, 8):
                return "Split"
            return "Hit"
        
        if self.is_soft_hand(player_hand):  # Soft totals
            if player_total == 20:
                return "Stand"
            if player_total == 19:
                return "Double Down" if dealer_up == 6 else "Stand"
            if player_total == 18:
                if dealer_up in range(2, 7):
                    return "Double Down"
                if dealer_up in range(9, 12):
                    return "Hit"
                return "Stand"
            if player_total == 17 and dealer_up in range(3, 7):
                return "Double Down"
            if player_total in [16, 15] and dealer_up in range(4, 7):
                return "Double Down"
            if player_total in [14, 13] and dealer_up in [5, 6]:
                return "Double Down"
            return "Hit"
        
        # Hard totals
        if player_total >= 17:
            return "Stand"
        if player_total == 16 and dealer_up in range(2, 7):
            return "Stand"
        if player_total == 15 and dealer_up in range(2, 7):
            return "Stand"
        if player_total == 14 and dealer_up in range(2, 7):
            return "Stand"
        if player_total == 13 and dealer_up in range(2, 7):
            return "Stand"
        if player_total == 12 and dealer_up in range(4, 7):
            return "Stand"
        if player_total == 11:
            return "Double Down"
        if player_total == 10 and dealer_up in range(2, 10):
            return "Double Down"
        if player_total == 9 and dealer_up in range(3, 7):
            return "Double Down"
        return "Hit"

    def get_card_input(self, prompt):
        while True:
            card = input(prompt).strip().lower()
            if card in ["a", "ace", "1", "11"]:
                return 11
            try:
                card_value = int(card)
                if card_value in range(2, 12):
                    return card_value
            except ValueError:
                pass
            print("Invalid input! Please enter a number between 2-11 or 'A'/'Ace'.")

    def play_hand(self, player_hand, dealer_card):
        while True:
            action = self.recommend_action(player_hand, dealer_card)
            print(f"\nRecommended action: {action}")
            if action == "Hit":
                new_card = self.get_card_input("\nEnter the new card drawn: ")
                player_hand.append(new_card)
            else:
                break
        print(f"\nFinal hand: {player_hand}, Final Score: {self.calculate_score(player_hand)}")

    def play_interactive(self):
        print("Welcome to the Blackjack Strategy Bot!")
        
        while True:
            try:
                dealer_card = self.get_card_input("\nEnter the dealer's visible card: ")
                print()
                
                card1 = self.get_card_input("Enter your first card: ")
                card2 = self.get_card_input("Enter your second card: ")
                
                if card1 == card2:
                    print("You have chosen to split!")
                    hand1 = [card1]
                    hand2 = [card2]
                    hand1.append(self.get_card_input("Enter the second card for first hand: "))
                    hand2.append(self.get_card_input("Enter the second card for second hand: "))
                    
                    print("Playing first hand:")
                    self.play_hand(hand1, dealer_card)
                    print("Playing second hand:")
                    self.play_hand(hand2, dealer_card)
                else:
                    player_hand = [card1, card2]
                    self.play_hand(player_hand, dealer_card)
                
                play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
                if play_again not in ["y", "yes", "yeah", "sure"]:
                    print("\nThank you for playing! Goodbye.")
                    break
            
            except ValueError:
                print("Invalid input! Please enter numeric values for cards.")

if __name__ == "__main__":
    bot = BlackjackStrategyBot()
    bot.play_interactive()'''
class BlackjackStrategyBot:
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4

    def calculate_score(self, hand):
        score = sum(hand)
        ace_count = hand.count(11)
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        return score

    def is_soft_hand(self, hand):
        return 11 in hand and sum(hand) <= 21

    def recommend_action(self, player_hand, dealer_card):
        player_total = self.calculate_score(player_hand)
        dealer_up = dealer_card

        # Handle Pair Splitting
        if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
            pair_card = player_hand[0]
            if pair_card == 11:  # Aces
                return "Split"
            if pair_card == 10:  # Tens
                return "Stand"
            if pair_card == 9 and dealer_up in [2, 3, 4, 5, 6, 8, 9]:
                return "Split"
            if pair_card == 8:  # Eights
                return "Split"
            if pair_card == 7 and dealer_up in range(2, 8):
                return "Split"
            if pair_card == 6 and dealer_up in range(2, 7):
                return "Split"
            if pair_card == 5 and dealer_up in range(2, 10):
                return "Double Down"
            if pair_card == 4 and dealer_up in [5, 6]:
                return "Split"
            if pair_card in [2, 3] and dealer_up in range(2, 8):
                return "Split"
            return "Hit"

        # Handle Soft Totals
        if self.is_soft_hand(player_hand):
            if player_total == 20:  # A,9
                return "Stand"
            if player_total == 19:  # A,8
                return "Double Down" if dealer_up == 6 else "Stand"
            if player_total == 18:  # A,7
                if dealer_up in range(2, 7):
                    return "Double Down"
                if dealer_up in range(9, 12):
                    return "Hit"
                return "Stand"
            if player_total == 17 and dealer_up in range(3, 7):
                return "Double Down"
            if player_total in [16, 15] and dealer_up in range(4, 7):
                return "Double Down"
            if player_total in [14, 13] and dealer_up in [5, 6]:
                return "Double Down"
            return "Hit"

        # Handle Hard Totals
        if player_total >= 17:
            return "Stand"
        if player_total == 16:
            if dealer_up in range(2, 7):
                return "Stand"
            if dealer_up in [9, 10, 11]:
                return "Surrender"
            return "Hit"
        if player_total == 15:
            if dealer_up in range(2, 7):
                return "Stand"
            if dealer_up == 10:
                return "Surrender"
            return "Hit"
        if player_total == 14 and dealer_up in range(2, 7):
            return "Stand"
        if player_total == 13 and dealer_up in range(2, 7):
            return "Stand"
        if player_total == 12:
            if dealer_up in range(4, 7):
                return "Stand"
            return "Hit"
        if player_total == 11:
            return "Double Down"
        if player_total == 10 and dealer_up in range(2, 10):
            return "Double Down"
        if player_total == 9 and dealer_up in range(3, 7):
            return "Double Down"
        return "Hit"

    def get_card_input(self, prompt):
        while True:
            card = input(prompt).strip().lower()
            if card in ["a", "ace", "1", "11"]:
                return 11
            try:
                card_value = int(card)
                if card_value in range(2, 12):
                    return card_value
            except ValueError:
                pass
            print("Invalid input! Please enter a number between 2-11 or 'A'/'Ace'.")

    def play_hand(self, player_hand, dealer_card):
        while True:
            action = self.recommend_action(player_hand, dealer_card)
            print(f"\nRecommended action: {action}")
            if action == "Hit":
                new_card = self.get_card_input("\nEnter the new card drawn: ")
                player_hand.append(new_card)
            elif action == "Surrender":
                print("You chose to surrender. Half your bet is returned.")
                break
            else:
                break
        print(f"\nFinal hand: {player_hand}, Final Score: {self.calculate_score(player_hand)}")

    def play_interactive(self):
        print("Welcome to the Blackjack Strategy Bot!")

        while True:
            try:
                dealer_card = self.get_card_input("\nEnter the dealer's visible card: ")
                print()

                card1 = self.get_card_input("Enter your first card: ")
                card2 = self.get_card_input("Enter your second card: ")

                player_hand = [card1, card2]
                self.play_hand(player_hand, dealer_card)
                
                '''if card1 == card2:
                    print("You have chosen to split!")
                    hand1 = [card1]
                    hand2 = [card2]
                    hand1.append(self.get_card_input("Enter the second card for first hand: "))
                    hand2.append(self.get_card_input("Enter the second card for second hand: "))

                    print("Playing first hand:")
                    self.play_hand(hand1, dealer_card)
                    print("Playing second hand:")
                    self.play_hand(hand2, dealer_card)
                else:
                    player_hand = [card1, card2]
                    self.play_hand(player_hand, dealer_card)'''

                play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
                if play_again not in ["y", "yes", "yeah", "sure"]:
                    print("\nThank you for playing! Goodbye.")
                    break

            except ValueError:
                print("Invalid input! Please enter numeric values for cards.")

if __name__ == "__main__":
    bot = BlackjackStrategyBot()
    bot.play_interactive()
