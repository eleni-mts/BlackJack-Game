from IPython.core.display import clear_output
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


# **Step 2: Create a Card Class**<br>
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


# **Step 3: Create a Deck Class**
class Deck:
    # Create a bunch of cards, like 52 card-class together

    def __init__(self):
        self.deck = []  # start with an empty list

        for suit in suits:
            for rank in ranks:  # Define every card in this deck
                created_card = Card(suit, rank)
                # make a bunch of 52 cards (4 suits *12 ranks)

                self.deck.append(created_card)

    def __str__(self):
        return f"Our deck has still these cards: {', '.join(str(card) for card in self.deck)}"

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

# **Step 4: Create a Hand Class**<br>
class Hand:

    def __init__(self):

        self.hand_cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def calculate_value(self):
        self.value = 0
        self.aces = 0

        for card in self.hand_cards:
            rank = card.rank
            self.value += values[rank]

            if rank == 'Ace':
                self.aces += 1

        # Adjust the value if there are aces in the hand
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
    def add_card(self, new_card):

        if type(new_card) == type([]):
            # add more than one cards to hand
            self.hand_cards.extend(new_card)
        else:
            # add one only card to hand
            self.hand_cards.append(new_card)

    def display(self):

        for card in self.hand_cards:
            print(card)

# **Step 5: Create a Chips Class**<br>
class Chips:

    def __init__(self):

        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):

        self.total = self.total + (self.bet * 2)

    def lose_bet(self):

        if self.bet <= self.total:
            self.total = self.total - self.bet
        else:
            print("No chips available!")

    def __str__(self):

        return f" Your total chips are {self.total}"

# **Step 6: Write a function for taking bets**<br>
def take_bet():
    bet = "Chips"

    while not bet.isdigit():
        bet = input("How many chips you want to bet? Your bet is: ")
    return int(bet)


# **Step 7: Write a function for taking hits**
def hit(deck, hand):  # black_deck,player

    deck = Deck()
    hand = Hand()
    hand.calculate_value()

    hand.add_card(black_deck.deal())


# **Step 8: Write a function prompting the Player to Hit or Stand**<br> If the Player Hits, employ the hit() function
# above. If the Player Stands, set the playing variable to False - this will control the behavior of a
# <code>while</code> loop later on in our code.

# def hit_or_stand(deck,hand):
#     global playing  # to control an upcoming while loop
#     
#     hand = Hand()
#     deck = Deck()
#     choice = 'wrong'
#     
#     while choice not in ["Hit", "Stand"]:
#         choice = input("Do you want to 'Hit' or 'Stand'? Your choice is.... ")
#     
#     if choice == "Hit":
#         return True
#     elif choice == "Stand":
#         return False

def hit_or_stand():
    global playing  # to control an upcoming while loop
    choice = 'wrong'

    while choice not in ["Hit", "Stand"]:
        choice = input("Do you want to 'Hit' or 'Stand'? Your choice is.... ")

    return choice


# **Step 9: Write functions to display cards**<br>

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print("", dealer.hand_cards[1])  # Show only the second card of the dealer's hand
    print("\nPlayer's Hand:", *player.hand_cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.hand_cards, sep='\n ')
    print("Dealer's Hand value:", dealer.value)
    print("\nPlayer's Hand:", *player.hand_cards, sep='\n ')
    print("Player's Hand value:", player.value)


# ### And now on to the game!!

black_deck = Deck()
black_deck.shuffle()
while True:

    # Create & shuffle the deck, deal two cards to each player
    player = Hand()

    player.add_card(black_deck.deal())
    player.add_card(black_deck.deal())

    dealer = Hand()

    dealer.add_card(black_deck.deal())
    dealer.add_card(black_deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    player_chips.bet = take_bet()

    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        player.calculate_value()
        dealer.calculate_value()

        decision = hit_or_stand()
        if decision == "Stand":
            while not dealer.value == 17:
                dealer.add_card(black_deck.deal())
                break
        else:
            player.add_card(black_deck.deal())
            show_some(player, dealer)

        player.calculate_value()
        dealer.calculate_value()

        decision = hit_or_stand()
        if decision == "Stand":
            while not dealer.value == 17:
                dealer.add_card(black_deck.deal())
                break
        else:
            player.add_card(black_deck.deal())

            # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)

        player.calculate_value()
        dealer.calculate_value()

        show_all(player, dealer)

        # Run different winning scenarios
        if player.value == 21 or player.value > dealer.value and not player.value > 21:
            print("Player wins!")
            player_chips.win_bet()
            playing = False
        elif dealer.value == 21 or player.value < dealer.value and not dealer.value > 21:
            print("Dealer wins!")
            player_chips.lose_bet()
            playing = False
        elif player.value > 21:
            print("Player Busted!")
            player_chips.lose_bet()
            playing = False
        elif dealer.value > 21:
            print("Dealer Busted!")
            playing = False
        elif dealer.value == player.value:
            print("It is a PUSH!")
            playing = False

            # Inform Player of their chips total
        print(player_chips)
        break

    # Ask to play again
    play_game = input("Do you want to play again? Yes or No?  ")
    if play_game == "Yes":
        clear_output()
        playing = True
        continue
    else:
        print("See you next time!")
        playing = False
        break
