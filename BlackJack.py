import pygame
from sys import exit
from IPython.core.display import clear_output
import random
game = True

# SET UP THE GAME
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


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
        single_card = self.deck.pop()
        return single_card


class Hand:

    def __init__(self):

        self.hand_cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def calculate_value(self):

        # Adjust the value if there are aces in the hand
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def add_card(self, new_card):

        self.hand_cards.append(new_card)
        self.value += values[new_card.rank]
        if new_card.rank == 'Ace':
            self.aces += 1


class Chips:

    def __init__(self):

        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):

        self.total = self.total + self.bet

    def lose_bet(self):

        if self.bet <= self.total:
            self.total = self.total - self.bet
        else:
            print("No chips available!")

    def __str__(self):

        return f" Your total chips are {self.total}"


def take_bet():
    bet = "Chips"

    while not bet.isdigit():
        bet = input("How many chips you want to bet? Your bet is: ")
    return int(bet)


def hit(deck, hand):  # black_deck,player

    hand.add_card(deck.deal())
    hand.calculate_value()


def show_some(player, dealer):
    dealer_x = 1100
    player_x = 30

    # Show the dealer's facedown card
    card_back = pygame.image.load("Game_Pictures/PNG_cards/card_back.png")
    card_back_rect = card_back.get_rect()
    card_back_rect.topright = (dealer_x, 110)
    screen.blit(card_back, card_back_rect)

    # Show the second card of the dealer's hand
    dealer_x += card_back_rect.width - 120
    dealer_card = dealer.hand_cards[1]
    dealer_card_image = card_images[(dealer_card.suit, dealer_card.rank)]
    dealer_card_rect = dealer_card_image.get_rect()
    dealer_card_rect.topright = (dealer_x, 110)
    screen.blit(dealer_card_image, dealer_card_rect)

    # Show all the player's cards
    for i, player_card in enumerate(player.hand_cards):
        player_card_image = card_images[(player_card.suit, player_card.rank)]
        player_card_rect = player_card_image.get_rect()
        player_card_rect.topleft = (player_x + i * (player_card_rect.width - 120), 110)  # Adjust positions as needed
        screen.blit(player_card_image, player_card_rect)

    pygame.display.flip()


def show_all(player, dealer):
    dealer_x = 1100
    player_x = 30

    # Show all the dealer's cards
    for i, dealer_card in enumerate(dealer.hand_cards):
        dealer_card_image = card_images[(dealer_card.suit, dealer_card.rank)]
        dealer_card_rect = dealer_card_image.get_rect()
        dealer_card_rect.topright = (dealer_x + i * (dealer_card_rect.width - 120), 110)  # Adjust positions as needed
        screen.blit(dealer_card_image, dealer_card_rect)

    # Show all the player's cards
    for i, player_card in enumerate(player.hand_cards):
        player_card_image = card_images[(player_card.suit, player_card.rank)]
        player_card_rect = player_card_image.get_rect()
        player_card_rect.topleft = (player_x + i * (player_card_rect.width - 120), 110)  # Adjust positions as needed
        screen.blit(player_card_image, player_card_rect)

    pygame.display.flip()


# INITIALIZE PYGAME & SET UP THE MENU PART
pygame.init()
screen = pygame.display.set_mode((1440, 768))
pygame.display.set_caption("BlackJack Game")
clock = pygame.time.Clock()
playing = False

menu_music = pygame.mixer.Sound("Game_Music/Fast-start.mp3")
menu_music.set_volume(0.5)  # Adjust the volume as needed
menu_music.play(loops=-1)  # Play in a loop (-1 means loop indefinitely)

button_music = pygame.mixer.Sound("Game_Music/click-menu-app.mp3")
button_music.set_volume(0.4)

game_music = pygame.mixer.Sound("Game_Music/ready to start.mp3")
game_music.set_volume(0.2)

hit_button = pygame.mixer.Sound("Game_Music/ping.mp3")
hit_button.set_volume(2.0)

stand_button = pygame.mixer.Sound("Game_Music/select_denied_.mp3")
stand_button.set_volume(2.0)

image_1 = pygame.image.load("Game_Pictures/BlackJack_title1.png").convert()
imagerect = image_1.get_rect()
imagerect.center = ((1440 // 2, 768 // 2))

play_image = pygame.image.load("Game_Pictures/play_button.png").convert_alpha()
play_image_rect = play_image.get_rect()
play_image_rect.center = ((550, 642))

exit_image = pygame.image.load("Game_Pictures/exit_button.png").convert_alpha()
exit_image_rect = exit_image.get_rect()
exit_image_rect.center = ((850, 647))

exit_image2 = pygame.image.load("Game_Pictures/exit_button.png").convert_alpha()
exit_image2_rect = exit_image2.get_rect()
exit_image2_rect.center = ((110, 700))
exit_image2 = pygame.transform.scale(exit_image2,(150,150))

main_image = pygame.image.load("Game_Pictures/Green_Wallpapers.png").convert()

menu_image = pygame.image.load("Game_Pictures/menu_button.png").convert_alpha()
menu_image_rect = menu_image.get_rect()
menu_image_rect.center = ((110, 600))
menu_image = pygame.transform.scale(menu_image,(150,150))

reset_image = pygame.image.load("Game_Pictures/reset_button.png").convert_alpha()
reset_image_rect = reset_image.get_rect()
reset_image_rect.center = ((1270,647))
reset_image = pygame.transform.scale(reset_image,(150,150))

hit_image = pygame.image.load("Game_Pictures/hit_button.png").convert_alpha()
hit_image_rect = hit_image.get_rect()
hit_image_rect.center = ((870, 647))

stand_image = pygame.image.load("Game_Pictures/stand_button.png").convert_alpha()
stand_image_rect = stand_image.get_rect()
stand_image_rect.center = ((550, 647))


def display_message(message):
    font = pygame.font.Font(None, 45)  # Choose a font and size
    text_surface = font.render(message, True, (255, 255, 255))  # Render the text
    text_rect = text_surface.get_rect(center=(1440 // 2, 768 // 2))  # Position the text
    screen.blit(text_surface, text_rect)  # Display the text on the screen


card_images = {}
for suit in suits:
    for rank in ranks:
        card_name = f"{rank}_of_{suit}.png"
        original_card_image = pygame.image.load(f'Game_Pictures/PNG_cards/{card_name}')
        resized_card_image = pygame.transform.scale(original_card_image, (250, 363))  # Replace width and height with your desired dimensions
        card_images[(suit, rank)] = resized_card_image

game_active = True
playing = False

while game_active:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('white')
    screen.blit(image_1, imagerect)
    screen.blit(play_image, play_image_rect)
    screen.blit(exit_image, exit_image_rect)
    mouse_pos = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if exit_image_rect.collidepoint(event.pos):
            button_music.play()
            pygame.quit()
            exit()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if play_image_rect.collidepoint(event.pos):
            button_music.play()
            playing = True
            black_deck = Deck()
            black_deck.shuffle()

            while playing:
                menu_music.stop()
                game_music.play(loops=-1)
                screen.blit(main_image, (0, 0))
                screen.blit(exit_image2, exit_image2_rect)
                screen.blit(menu_image, menu_image_rect)
                screen.blit(hit_image, hit_image_rect)
                screen.blit(stand_image, stand_image_rect)
                screen.blit(reset_image,reset_image_rect)


                # LET'S PLAY!

                if menu_image_rect.collidepoint(event.pos):
                    button_music.play()
                    game_active = True
                    playing = False

                if exit_image2_rect.collidepoint(event.pos):
                    button_music.play()
                    pygame.quit()
                    exit()

                while game:
                    player = Hand()
                    dealer = Hand()

                    player.add_card(black_deck.deal())
                    dealer.add_card(black_deck.deal())
                    player.add_card(black_deck.deal())
                    dealer.add_card(black_deck.deal())

                    show_some(player, dealer)
                    pygame.display.flip()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if hit_image_rect.collidepoint(event.pos):
                            hit_button.play(loops=1)
                            player.add_card(black_deck.deal())
                            show_some(player, dealer)
                            pygame.display.flip()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if stand_image_rect.collidepoint(event.pos):
                            stand_button.play(loops=1)
                            dealer.calculate_value()
                            while not dealer.value == 17:
                                dealer.add_card(black_deck.deal())
                                pygame.display.flip()

                    player.calculate_value()
                    dealer.calculate_value()
                    pygame.display.flip()

                    # Determine the winner and handle game outcomes
                    if player.value > 21:
                        # Handle player bust
                        game = False
                        display_message("Player Busts!")
                    elif dealer.value > 21:
                        # Handle dealer bust
                        game = False
                        display_message("Dealer Busts! Player Wins!")
                    elif player.value > dealer.value:
                        # Handle player win
                        game = False
                        display_message("Player Wins!")
                    elif dealer.value > player.value:
                        # Handle dealer win
                        game = False
                        display_message("Dealer Wins!")
                    else:
                        # Handle push (tie)
                        game = False
                        display_message("It's a Tie!")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_image_rect.collidepoint(event.pos):
                        game = True
                        continue
                else:
                    break


    pygame.display.flip()
    # set a maximum frame rate
    clock.tick(60)
