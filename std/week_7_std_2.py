# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Hit or stand?"
score = 0
deck = 0
player = 0
dealer = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card = []
        
            # create Hand object
            

    def __str__(self):
        s = "Hand contains "
        for card in range(len(self.card)):
            s += str(self.card[card]) + " "
        return s
            # return a string representation of a hand

    def add_card(self, card):
        self.card.append(card)
            # add a card object to a hand

    def get_value(self):
        value = 0
        get_ace = False
        for card in range(len(self.card)):
            rank = self.card[card].get_rank()
            if rank == RANKS[0]:
                get_ace = True
            value += VALUES[rank]
        if get_ace and value + 10 <= 21:
            value += 10
        return value
            
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
            # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for card in range(len(self.card)):
            self.card[card].draw(canvas, [pos[0] + CARD_SIZE[0] * card, pos[1]])
        # draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.card = []
        for suit in SUITS:
            for rank in RANKS:
                self.card.append(Card(suit, rank))
        # create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card)    # use random.shuffle()

    def deal_card(self):
        #self.shuffle()
        return self.card.pop(0)
            # deal a card object from the deck
    
    def __str__(self):
        s = "Deck contains "
        for card in self.card:
            s += str(card) + " " 
            # return a string representing the deck
        return s



#define event handlers for buttons
def deal():
    global outcome, in_play
    global player, deck, dealer
    # your code goes here
    in_play = True
    outcome = "Hit or stand?"
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    #outcome += "Player's hand: " + str(player) + " "
    #outcome += "Dealer's hand: " + str(dealer) + " "
    
    

def hit():
        # replace with your code below
    global in_play
    global player
    global score
    global deck
    global outcome
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            outcome = "You loses! New deal? "
            #outcome += '\n'
            #outcome += "You loses!"
            print "You have busted! "
            in_play = False
            score -= 1
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global player
    global dealer
    global outcome
    global deck
    global in_play
    global score
    
    if player.get_value() > 21:
        outcome = "You loses! New deal?"
        print "You have busted. You lose"
        in_play = False
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            outcome = "You wins! New deal?"
            print "Dealer has busted "
            score += 1
            in_play = False
        elif (player.get_value() <= dealer.get_value()):
            outcome = "You loses. New deal? "
            in_play = False
            score -= 1
        else:
            outcome = "You wins. New deal? "
            in_play = False
            score += 1
        
    
        # replace with your code below
    
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Player", [50, 180], 40, 'Black', 'sans-serif')
    player.draw(canvas, [50, 200])
    canvas.draw_text("Dealer", [50, 200 + CARD_SIZE[1] + 90], 40,  'Black', 'sans-serif')
    dealer.draw(canvas, [50, 400])
    canvas.draw_text(outcome, [200, 180], 40, 'Black', 'sans-serif')
    canvas.draw_text("Blackjack", [50, 100], 70, 'Red', 'sans-serif')
    canvas.draw_text("Score: " + str(score), [400, 100], 40, 'Black', 'sans-serif')
    if (in_play):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [50 + CARD_BACK_SIZE[0] / 2, 400 + CARD_BACK_SIZE[1] / 2], CARD_BACK_SIZE)
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
