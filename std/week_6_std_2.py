# implementation of card game - Memory

import simplegui
import random

cards = range(8) + range(8) # Populate card deck - only needs to be done once

# helper function to initialize globals, shuffle deck and turn face-down
def new_game():
    global state, cards, faceup, turns, match
    state = 0
    turns = 0
    label.set_text("Turns = "+str(turns))
    match = False            
    random.shuffle (cards)
    faceup = [False]*16
     
# define event handlers
def mouseclick(pos):
    global state, cards, faceup, turns, card1, card2, match
    click_card = pos[0]/50					# get card number
    if faceup[click_card] == True:			# ignore mouse click if already face up
        return
    faceup[click_card] = True				# else turn face up
    if state == 1:							# game state logic changed from template (more efficient)
        card2 = click_card					# second card in turn stored
        match = cards[card1]==cards[card2]	# match = True when cards equal, else False
        turns += 1							# turn counter increments on second card flip
        label.set_text("Turns = "+str(turns))  # and label text updates
        state = 2							   # now 2 cards are exposed this turn
        return
    elif state == 2:
        faceup[card1] = faceup[card2] = match  # if previous cards matched, stay face-up
    card1 = click_card						   # runs on state = 0 and state = 2 (1st card flip)
    state = 1

# cards are logically 50x100 pixels in size
# draw green rectangle or card number with white border-line
def draw(canvas):
    for index in range(16):
        if faceup[index] == False:
            canvas.draw_line(((index*50)+25, 0), ((index*50)+25, 99), 50, "Green")
        else:
            canvas.draw_text(str(cards[index]), ((index*50)+10, 70), 60, "White")
        canvas.draw_line(((index*50)+50, 0), ((index*50)+50, 99), 1, "White")

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
