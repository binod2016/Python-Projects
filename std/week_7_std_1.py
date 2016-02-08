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
outcome = ""
outcome_score = "" #Variable for priting Score
outcome_dealer_hand = ""
outcome_player_hand = ""
score = 0
position=[0,0]
displayed = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

#*********************************************************************************************************************
# define card class
#*********************************************************************************************************************
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
        

        
#*********************************************************************************************************************
# define hand class
#*********************************************************************************************************************
class Hand:
    def __init__(self):
        self.hand = []	# create Hand object      

    def __str__(self):
        s = ''
        for card in self.hand:
            #print "card = ", card
            s += (str(card.get_suit()) + str(card.get_rank())) + " "
        return "Hand contains " + str(s)

    def add_card(self, card):
        self.hand.append(card)
        #self.draw(card,position)
        # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace,
        # then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        sum = 0
        acein = False
        localvalue=0
        for card in self.hand:
            #print card.get_rank()
            if card.get_rank()=='A':
                acein += 1
        #if (acein>1):
            #print "**************"
            #print "More than one Ace"
            #print dealer
            #print dealer.get_value()
            #print "**************"
        for card in self.hand:
            localvalue= int(VALUES[card.get_rank()])
            if (acein>1 & localvalue==1):
                sum += 11
            else:
                sum += localvalue
        return sum
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        #self.pos = pos
        #self.canvas = canvas
        #for card in self.hand:
        #    card.draw(self.canvas, self.pos)
        #    print type(card)
        for c in self.hand:
            i += 1
            x = pos[0]
            y = pos[1]            
            c.draw(canvas, [(x * i + CARD_SIZE[0]),y])
            #if (i==1):
            #    print x * i + CARD_SIZE[0]
        #x = pos[0]
        #y = pos[1]
        #for i in range(len(self.hand)):
        #    self.hand[i].draw(canvas, (x * i + CARD_SIZE[0], y))
            
            
            
            
            


#*********************************************************************************************************************        
# define deck class 
#*********************************************************************************************************************
class Deck:
    def __init__(self):
        global SUITS, RANKS
        self.deck = []	# create a Deck object
        for i in SUITS:
            for j in RANKS:
                #self.deck.append(i+j)
                self.deck.append(Card(i,j))
        

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        self.dealt = self.deck.pop()
        #print "Dealt = ", self.dealt
        return self.dealt # deal a card object from the deck
    
    def __str__(self):
        #return str(self.deck)	# return a string representing the deck
        y = ''
        for card in self.deck:
            y += (str(card.get_suit()) + str(card.get_rank())) + " "
        return "Deck Contains : " + str(y)



#*********************************************************************************************************************
#define event handlers for buttons
#*********************************************************************************************************************
def deal():
    global outcome, in_play, score
    # your code goes here
    global playingdeck, player, dealer
    global outcome, outcome_dealer_hand, outcome_player_hand

    if (in_play==False):
        playingdeck = Deck()
        player = Hand()
        dealer = Hand()

        #print playingdeck
        playingdeck.shuffle()
        #print playingdeck

        outcome = "Hit        or        Stand"
        #Cards for Player
        for i in (1,2):
            #newcard = playingdeck.deal_card()
            #print "*******************************"
            #print "newcard " + str(i) + " = ", newcard
            #player.add_card(newcard)
            player.add_card( playingdeck.deal_card())
            #print "player : ", player

            #Cards for Dealer
        for j in (1,2):
            #newcard = playingdeck.deal_card()
            #print "*******************************"
            #print "newcard for dealer" + str(i) + " = ", newcard
            dealer.add_card(playingdeck.deal_card())
            #print "Dealer : ", dealer
        outcome_dealer_hand = "Hidden"
        outcome_player_hand = player.get_value()
        in_play = True
    else:
        outcome = "You have again clicked Deal. Player loses"
        score -= 1
        in_play = False
    #code ends
    

#*********************************************************************************************************************
# hit buttons
#*********************************************************************************************************************
def hit():
    global in_play, outcome, score, outcome_player_hand
    if(in_play):
        # replace with your code below
        onhand = player.get_value()
        print "Currently on hand : ", onhand
        # if the hand is in play, hit the player
        if(onhand<=21):
            player.add_card(playingdeck.deal_card())
        onhand = player.get_value()
        outcome_player_hand = onhand
        print "New on hand : ", onhand
        #outcome = "Players hand value = " + str(onhand)
        if(onhand>21):
            #print "You are busted"
            outcome = "You are Busted"
            score -= 1
            in_play = False
        # if busted, assign a message to outcome, update in_play and score
       

#*********************************************************************************************************************
# Stand Buttons
#*********************************************************************************************************************
def stand():
    # replace with your code below
    global outcome, score, 	outcome_dealer_hand, in_play
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if (in_play):
        print " "
        #hit the dealer
        #get dealer current value
        while(dealer.get_value()<=17):
            print "Current players hand : ",player.get_value()
            print "Current Dealers hand : ",dealer.get_value()
            dealer.add_card(playingdeck.deal_card())
            print "New Dealers hand : ",dealer.get_value()
            print "Dealer : ", dealer
            print 
        outcome_dealer_hand = dealer.get_value()

        if(dealer.get_value()>21):
            print "Dealer is busted"
            outcome = "Dealer is busted. Player Wins"
            score += 1
            outcome_dealer_hand = dealer.get_value()
        elif(dealer.get_value()>=player.get_value()):
            print "Dealer wins the hand"
            outcome = "Dealer wins the hand"
            score -= 1
            outcome_dealer_hand = dealer.get_value()
        else:
            print "Player wins the hand"
            outcome = "Player wins the hand"
            score += 1
            outcome_dealer_hand = dealer.get_value()
        # of <=17 keep hitting        
    else:
        print "You are already busted mister."
        print "Your hand value was : ", player.get_value()       
        outcome = "You are already busted mister. "
    in_play = False
    # assign a message to outcome, update in_play and score

#*********************************************************************************************************************
# draw handler 
#*********************************************************************************************************************   
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global in_play, position, outcome, score, displayed
    global outcome_player_hand, outcome_dealer_hand

    player.draw(canvas, [50, 175])      
    dealer.draw(canvas, [50, 375])   
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [122 + CARD_BACK_CENTER[0], 375 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    canvas.draw_text("Player's Hand", [50, 150], 20, 'White')

    
    canvas.draw_text("Dealer's Hand", [50, 350], 20, 'White')
    #playingdeck.draw(canvas,[0,0])
    #player.draw(canvas,position)
    if displayed:
        canvas.draw_text(outcome, [200, 100], 20, 'White')
    canvas.draw_text("Blackjack", [200, 50], 50, 'White')
    canvas.draw_text("Score = " + str(score), [250, 550], 20, 'White')
    canvas.draw_text("Player's Hand Value= " + str(outcome_player_hand), [300, 150], 20, 'White')
    canvas.draw_text("Dealer's Hand Value =  " + str(outcome_dealer_hand), [300, 350], 20, 'White')
    
    #card.draw(canvas, position)

def timer_handler():
    global displayed
    displayed = not displayed


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, timer_handler)


# get things rolling
deal()
frame.start()
timer.start()

# remember to review the gradic rubric
