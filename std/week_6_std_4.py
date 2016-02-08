# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards, exposed ,state, turns
    cards = range(0,8) + range(0,8)
    random.shuffle(cards)
    exposed = [0]*16
    state = 0
    turns = 0
    label.set_text("Turns = 0")
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, card1, card2,loc1,loc2, turns
    loc = list(pos)[0] // 50
    if exposed[loc] == False:
        if state == 0:
            if turns == 0:
                card1 = cards[loc]
                loc1 = loc
                exposed[loc] = True
            else:
                label.set_text("Turns = " + str(turns))
                if not (card1 == card2):
                    exposed[loc1] = False
                    exposed[loc2] = False
                card1 = cards[loc]
                loc1 = loc
                exposed[loc] = True
            state += 1
        elif state == 1:
            card2 = cards[loc]
            loc2 = loc
            exposed[loc] = True
            turns += 1
            state = 0
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    place = 25
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(cards[i]),(place-10,60),40,"Red")
        else:
            canvas.draw_line((place,0),(place,100),49,"Green")
        place += 50
    


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


# Always remember to review the grading rubric
