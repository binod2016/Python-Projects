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
        self.cards = []

    def __str__(self):
        ans = "Hand contains"
        for card in self.cards:
            ans += " " + str(card)
        return ans

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        val = 0
        contains_aces = False
        for card in self.cards:
            rank = card.get_rank()
            val += VALUES[rank]
            if rank == "A":
                contains_aces = True
        if val <= 10 and contains_aces:
            val += 10
        return val
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 85
            
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        ans = "Deck contains"
        for card in self.cards:
            ans += " " + str(card)
        return ans



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, score
    # your code goes here
    if in_play:
        print "Player lost due to re-deal. New deal?"
        outcome = "Player lost due to re-deal. New deal?"
        score -= 1
        in_play = False
    else:
        print "Hit or stand?"
        outcome = "Hit or stand?"
        deck = Deck()
        deck.shuffle()
        dealer_hand = Hand()
        player_hand = Hand()
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        print "Dealer:", dealer_hand
        print "Player:", player_hand
        in_play = True

def hit():
    global outcome, in_play, score
 
    # if the hand is in play, hit the player
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())

        # if busted, assign a message to outcome, update in_play and score
        elif player_hand.get_value() > 21:
            print "You have busted. New deal?"
            outcome = "You have busted. New deal?"
            in_play = False
            score -= 1

def stand():
    global outcome, in_play, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
    print "Dealer:", dealer_hand
    if dealer_hand.get_value() > 21:
        print "Dealer busted. Player wins! Play again?"
        outcome = "Dealer busted. Player wins! Play again?"
        score += 1
    else:
        if dealer_hand.get_value() >= player_hand.get_value() or player_hand.get_value() > 21:
            print "Dealer wins! New deal?"
            outcome = "Dealer wins! New deal?"
            score -= 1
        else:
            print "Player wins! New deal?"
            outcome = "Player wins! Play again?"
            score += 1
    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome
    dealer_hand.draw(canvas, [60, 150])
    player_hand.draw(canvas, [60, 350])
    canvas.draw_text(outcome, [60, 100], 25, "White")
    canvas.draw_text("BLACKJACK", [160, 50], 50, "Yellow")
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (96, 198), CARD_BACK_SIZE)
    canvas.draw_text("SCORE: " + str(score), [60, 500], 25, "White")
    # card = Card("S", "A")
    # card.draw(canvas, [300, 300])


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
