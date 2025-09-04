class BlackjackStrategyBot:
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    
    def calculate_probability(self, player_hand, dealer_card):
        remaining_deck = self.deck.copy()
        for card in player_hand + [dealer_card]:
            if card in remaining_deck:
                remaining_deck.remove(card)
        
        hit_wins, stand_wins, busts = 0, 0, 0
        
        for new_card in remaining_deck:
            new_hand = player_hand + [new_card]
            score = self.calculate_score(new_hand)
            if score > 21:
                busts += 1
            elif score >= 17:
                hit_wins += 1
            else:
                stand_wins += 1
        
        return {"hit_win_chance": hit_wins / len(remaining_deck),
                "stand_win_chance": stand_wins / len(remaining_deck),
                "bust_chance": busts / len(remaining_deck)}
    
    def calculate_score(self, hand):
        score = sum(hand)
        ace_count = hand.count(11)
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        return score
    
    def is_soft_hand(self, hand):
        return 11 in hand and sum(hand) <= 21
    
    def get_best_move(self, player_hand, dealer_card):
        probabilities = self.calculate_probability(player_hand, dealer_card)
        
        if self.is_soft_hand(player_hand) and sum(player_hand) >= 18:
            return "Stand"
        elif probabilities["bust_chance"] > 0.5:
            return "Stand"
        elif probabilities["hit_win_chance"] > probabilities["stand_win_chance"]:
            return "Hit"
        else:
            return "Stand"
    
    def recommend_action(self, player_hand, dealer_card):
        if self.is_soft_hand(player_hand) and sum(player_hand) < 18:
            return "Hit"
        if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
            return "Split"
        elif sum(player_hand) == 11:
            return "Double Down"
        else:
            return self.get_best_move(player_hand, dealer_card)
    
    def get_card_input(self, prompt):
        while True:
            card = input(prompt).strip().lower()
            if card in ["a", "ace", "1", "11"]:
                return 11
            try:
                card_value = int(card)
                if card_value in range(1, 12):
                    return card_value
            except ValueError:
                pass
            print("Invalid input! Please enter a number between 1-11 or 'A'/'Ace'.")
    
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
        print("Welcome to Asher Lieberman's Blackjack Bot!")
        
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
    bot.play_interactive()
