# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck, exposed, state, attempts
    # Initialize the deck
    deck = range(0,8)+range(0,8)
    random.shuffle(deck)
    # Some auxiliary variables
    state = 0
    attempts = 0
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False] 
    
# define event handlers
def mouseclick(pos):
    global state, first, second, attempts
    # Recognize the chosen card
    clicked = pos[0]//50
    # Stage machine
    if not exposed[clicked]:
        exposed[clicked] = True
        if state == 0:
            first = clicked
            state = 1
        elif state == 1:
            second = clicked
            attempts = attempts + 1
            state = 2
        else:
            if deck[first] != deck[second]:
                exposed[first] = False
                exposed[second] = False
            first = clicked    
            state = 1
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck
    # Plot cards
    for i in range(0,16):
        if exposed[i]:
            canvas.draw_text(str(deck[i]), [10+i*50, 70], 70, 'Green')
        else:
            canvas.draw_polygon([(7+i*50, 5), (7+i*50, 100), (43+i*50, 100), (43+i*50, 5)], 12, 'Green', 'Green')
    #Draw attempts
    label.set_text('Turns = '+str(attempts))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
