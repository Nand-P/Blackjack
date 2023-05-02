'''

This project is the human-versus-computer version of the card game "Blackjack". 
The "Player" will be the human while the "Dealer" will be the computer.
It uses object-oriented programming as the foundation of the game.

Author: Nand Patel
Date: April 19, 2023
Current Version: v1.2

HISTORY:
v1.00 - Created global variables to store all possible card data to improve organization.
v1.01 - Added custom print methods to make debugging easier in Card and Deck classes.
v1.1 - Altered adjust_for_ace method in Hand class to automatically adjust the value of aces without user intervention
v1.11 - Edge-case accounted for by using the hit() function if the player or dealer is dealt two aces from the beginning
v1.12 - Reformatted text to make it more user-friendly.
v1.2 - Added functionality to retain chips amount across rounds instead of resetting to the default value every game.
'''

#Imported to shuffle deck.
import random

#Global variables defined to create cards and decks. The Ace card can have a value of 1 or 11, but has been set to 11 by default.
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
game_values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

#Boolean defined to keep the game running.
game_active = True

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.game_value = game_values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit
    
class Deck:
    
    def __init__(self):
        #Empty list created to hold card objects.
        self.deck = []

        #Created every possible card in deck and saved to empty list.
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    #Prints out every card using the __str__ method from the Card class.
    def __str__(self):
        for card in self.deck:
            print(card)

    #Shuffles deck using imported library.
    def shuffle(self):
        return random.shuffle(self.deck)
    
    #Returns a removed card from the "bottom" of the deck.
    def deal_one(self):
        return self.deck.pop()
    
class Hand:

    def __init__(self):
        self.cards = []  #Holds Card objects in hand
        self.hand_value = 0 #Stores the total game value of all of the cards in the hand.
        self.default_aces = 0 #Keeps track of how many ace cards have retained their default value of 11.
    
    def add_card(self,card):
        self.cards.append(card)
        self.hand_value += card.game_value

        if card.rank == 'Ace':
            self.default_aces += 1
    
    def adjust_for_ace(self):
        while (self.hand_value > 21) & (self.default_aces != 0): #The total value of the hand must be over 21 to prevent unneccessary changes and there must be at least one unchanged ace
            self.hand_value -= 10
            self.default_aces -= 1
            
class Chips:

    def __init__(self):
        self.total = 100 #Default number of chips set the amount here.
        self.bet = 0
    
    def win_bet(self): #Adds chips in bet to total if won.
        self.total += self.bet
        self.bet = 0

    def lose_bet(self): #Subtracts chips in bet from total if lost.
        self.total -= self.bet
        self.bet = 0

#Asks user how many chips they would like to bet and verifies if the input was valid.
def take_bet(chips): 

    print(f"You currently have {chips.total} chips.")

    while True:
        try:
            chips.bet = int(input("Please enter a positive integer for how many chips you would like to bet: "))
            
        except ValueError:
            print("That was not an integer.")

        else:
            if chips.bet < 0:   
                print("Please enter a positive value.")
            
            elif chips.bet > chips.total:
                print("You do not have enough chips. Please choose a lower amount.")

            else:
                break #Exits the function if there were no issues with the input.

def hit(deck, hand):
    dealt_card = deck.deal_one() #Taking a card from the deck.

    hand.add_card(dealt_card) #Adding the dealt card to the hand.
    hand.adjust_for_ace() #Adjusting as necessary if the dealt card was an ace.

def hit_or_stand(deck, hand):
    global playing

    while True:
        player_choice = input("\nWould you like to hit or stand? Enter h or s: ")

        if player_choice == 'h':
            hit(deck, hand)
        
        elif player_choice == 's':
            print("The player stands. Dealer's turn.")
            playing = False
            
        else:
            print("You have not entered valid input. Please try again.")
            continue #Prevents the loop from exiting and asks the user to enter h or s again.

        break

#Shows one of the dealer's cards and all of the player's cards. 
def show_some(player, dealer):

    print("\nDealer's Hand: ")
    print("First card has been hidden.")
    print(dealer.cards[1])

    print("\nPlayer's Hand: ")
    for card in player.cards:
        print(card)

#Shows all cards for both the dealer and player as well as their respective hand values.
def show_all(player, dealer):

    print("\nDealer's Hand: ")
    for card in dealer.cards:
        print(card)

    print(f"Dealer's Hand Value: {dealer.hand_value}")

    print("\nPlayer's Hand: ")
    for card in player.cards:
        print(card) 

    print(f"Player's Hand Value: {player.hand_value}")

#The following functions account for end-game scenarios.
def player_busts(player, dealer, chips):
    print("PLAYER BUSTS!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("PLAYER WINS! DEALER BUSTS!")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("PLAYER BUSTS! DEALER WINS!")
    chips.lose_bet()

#If both the player and dealer have a hand with a value of 21, there will be a tie. No bets will lost or won.
def push(player, dealer):
    print("PLAYER AND DEALER BOTH REACHED 21. PUSH!")

################# MAIN #################

#Initial setup for game logic control.
print("Welcome to Blackjack!")
first_game = True
playing = True

while True:
    
    print("\nNew Round!")

    #Creates deck and shuffles it.
    deck = Deck()
    deck.shuffle()

    #The following two blocks of code create the player and dealer hands and adds two cards to each of them from the deck.
    dealer = Hand()
    hit(deck, dealer)
    hit(deck, dealer)

    player = Hand()
    hit(deck, player)
    hit(deck, player)

    #If this is the first round, the player's chips will set to the default amount of 100.
    if first_game == True:
        player_chips = Chips()
        first_game = False

    take_bet(player_chips)

    show_some(player, dealer)

    #Loop will continue running as long as the player has not finished hitting.
    while playing:

        hit_or_stand(deck, player)

        show_some(player, dealer)

        #If the player's hand has a value over 21, they will lose the amount they bet.
        if player.hand_value > 21:
            player_busts(player, dealer, player_chips)
            playing = False
    
    if player.hand_value <= 21: 
        #Dealer will continue hitting while their hand has a value under 17.
        while dealer.hand_value < 17:
            hit(deck, dealer)

        show_all(player, dealer)

        #The following block of code handles end-game scenarios.
        if dealer.hand_value > 21:
            dealer_busts(player, dealer, player_chips)

        elif dealer.hand_value > player.hand_value:
            dealer_wins(player, dealer, player_chips)
        
        elif dealer.hand_value < player.hand_value:
            player_wins(player, dealer, player_chips)

        else:
            push(player, dealer)
    
    print(f"Player's total chips are at: {player_chips.total}")

    new_game = input("Would you like to play a new game? Enter y for yes or any other character for no.")

    if new_game == 'y':
        playing = True
        continue

    else:
        print("Thank you for playing!")
        break
