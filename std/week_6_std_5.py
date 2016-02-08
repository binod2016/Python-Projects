# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global card_info, state, cards_up_idx,deck, turns
    state = 0
    turns = 0
    cards_up_idx = []
    card_info = []
    label.set_text("Turns = "+ str(turns))
    
        
    #Create the list of cards and shuffle them
    temp_deck1 = range(0,8)
    temp_deck2 = range(0,8)
    deck = temp_deck1 + temp_deck1
    random.shuffle(deck)
        
    #Create the horizontal positions (x axis) for all 16 cards using increments of 50
    cards_pos = range(0,751,50) # 0, 50,100,150, etc
    
    """Create a list of cards where each card has a position
    for drawing purposes, a side (up or down) and the number corresponding to the card"""
    #card_info = [0:position, 1:side, 2:number]
    for card_pos in cards_pos:
        card_info.append([card_pos,"down", deck[cards_pos.index(card_pos)]])
           

def color(side):
    """Returns a tuple for the color of the card depending on the side."""
    if side == "down":
        return "Brown","Green"
    else: return "Black", "Black"
     
# define event handlers
def mouseclick(pos):
    global card_info, cards_up, cards_up_idx,state, turns, label
    # add game state logic here
    for card in card_info:
        if pos[0] >= card[0] and pos[0] <= card[0] + 49:
            if state == 0 and card[1] == "down":
                card[1] = "up"
                state = 1
                cards_up_idx.append(card_info.index(card))                
            elif state == 1 and card[1] == "down":
                card[1] = "up"
                state = 2
                turns +=1
                label.set_text("Turns = "+ str(turns))
                cards_up_idx.append(card_info.index(card))
                #Check if cards match and leave them up if they do
                if card_info[cards_up_idx[0]][2] == card_info[cards_up_idx[1]][2]:
                    cards_up_idx=[]
                    state = 0
            elif state == 2 and card[1] == "down":
                card[1] = "up"
                state = 1                            
                #Put down the two cards that are up
                card_info[cards_up_idx.pop()][1] = "down" 
                card_info[cards_up_idx.pop()][1] = "down"
                #Record the index of the card that is fliped up
                cards_up_idx.append(card_info.index(card))
                            
                       
# cards are logically 50x100 pixels in size    
def draw(canvas):
    
    #card_info = [0:position, 1:side, 2:number]
    global card_info, deck
    for card in card_info:
        canvas.draw_polygon([[card[0], 0], [card[0] + 49, 0], [card[0] + 49, 100],
                            [card[0], 100]], 1, color(card[1])[0], color(card[1])[1]) 
        
        #If the Card is up then display the number
        if card[1] == "up":
            canvas.draw_text(str(card[2]), (10 + card[0], 65), 50, 'Red')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)



# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
label = frame.add_label("Turns = 0")

# get things rolling
new_game()
frame.start()



# Always remember to review the grading rubric
