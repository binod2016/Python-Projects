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
check = False
outcome = ""
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
        self.hand = []	# create Hand object

    def __str__(self):
        ans = "Hand contains "
        for i in range(len(self.hand)):
            ans += (str(self.hand[i])+" ")
        return ans

    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        value = 0
        for cards in self.hand:
            value += VALUES.get(cards.rank)
        for cards in self.hand:
            if cards.rank == 'A':
                if value <= 11:
                    value +=10
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        return value	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        indexu = 0
        for card in self.hand:
            indexu +=1
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + indexu * CARD_SIZE[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
# draw a hand on the canvas, use the draw method for cards        
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit,rank)
                self.deck.append(card)
                # create a Deck object

    def shuffle(self):
        random.shuffle(self.deck) # shuffle the deck 
        pass    # use random.shuffle()

    def deal_card(self):
        return self.deck.pop()	# deal a card object from the deck
    
    def __str__(self):
        ans ="Deck contains "
        for i in range(len(self.deck)):
            ans += (str(self.deck[i])+" ")
        return ans  # return a string representing the deck


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score, check
    if in_play and check:
        score-=1
    deck = Deck()
    deck.shuffle()
    print deck
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    print deck
    print player_hand
    print dealer_hand
    outcome = "HIT OR STAND?"
    in_play = True
    check = False

def hit():
    global in_play, player_hand, deck, outcome, score, check
    check = True
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            print player_hand, player_hand.get_value()
        if player_hand.get_value() > 21:
            print "You done son! BUSTED GG"
            outcome = "BUSTED! YOU LOST!"
            in_play = False
            score -= 1
            
            
    pass	# replace with your code below
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play, player_hand, dealer_hand, deck, outcome, score, check
    check = True
    if in_play:
        if player_hand.get_value() > 21:
            print "You done son! BUSTED GG"
            outcome = "BUSTED! YOU LOST!"
            in_play = False
            score -= 1
            
        else:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
            print dealer_hand.get_value()
            if dealer_hand.get_value() > 21:
                print "This nigga busted! GG"
                outcome = "Dealer busted! YOU WON!"
                in_play = False
                score += 1
            else:
                if dealer_hand.get_value() >= player_hand.get_value():
                    in_play = False
                    print "EZ KATKA, son! YOU LOST!"
                    outcome = "YOU LOST!"
                    score -= 1
                else:
                    in_play = False
                    print "YOU ACTUALLY WON GG"
                    outcome = "YOU WON!"
                    score += 1
    pass	# replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    scorest = "Score: "+str(score)
    canvas.draw_text("Blackjack", (10, 50), 40, 'White', 'serif')
    canvas.draw_text(scorest, (10, 100), 40, 'White', 'serif')
    hand1 = player_hand
    hand2 = dealer_hand
    hand1.draw(canvas, [100, 400])
    hand2.draw(canvas, [100, 200])
    if in_play:
        canvas.draw_polygon([[172, 200], [172+CARD_SIZE[0], 200], [172+CARD_SIZE[0], 200+CARD_SIZE[1]], [172, 200+CARD_SIZE[1]]], 1, 'Yellow', 'Orange')
    else:
        canvas.draw_text(str(dealer_hand.get_value()), (100, 265), 30, 'White', 'serif')
        canvas.draw_text(str(player_hand.get_value()), (100, 465), 30, 'White', 'serif')
    canvas.draw_text(outcome, (172, 360), 30, 'White', 'serif')
#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])
    


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
