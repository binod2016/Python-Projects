# implementation of card game - Memory

import simplegui
import random

cardlist = [0, 1, 2, 3, 4, 5, 6, 7]
cards = cardlist + cardlist
exposedlist = [False, False, False, False, False, False, False, False]
exposed = exposedlist + exposedlist
state = 0
turns = 0

#print cards

# helper function to initialize globals
def new_game():
    global cards
    global exposed
    global state, turns
    cards = cardlist+cardlist
    exposed = exposedlist+exposedlist
    state = 0
    turns = 0
    random.shuffle(cards)
    #print cards
    #print exposed

     
# define event handlers
def mouseclick(pos):
    global exposed, firstclick, secondclick, turns, state
    # add game state logic here
    #
    # First determine if we've clicked on a box
    #
    # Rule out any that aren't in the correct Y coordinate range or to the left of the first breen box
    #
    (x, y) = pos
    if (y < 70 or y >80 or x < 45 or x > 760):
        pass
    else:
        # Now see if it's within one of the X coordinate ranges for a box
        index =    (x / 45) - 1
        position = (x % 45)
        #print index, position
        #
        # Now, we know the index where the thing was clicked
        # If the position is less than the width of the box, then we must have
        # clicked in a box
        #
        if (position < 10 and exposed[index] == False):
            #
            # Then we've clicked in an area where a box is unturned
            #
            exposed[index] = True
           
            state += 1
            #print state
            
            if (state == 3):
                turns += 1
                #
                # We've already clicked on two numbers and are clicking
                # clicking on a third now
                #
                if cards[firstclick] != cards[secondclick]:
                    exposed[firstclick] = False
                    exposed[secondclick] = False
                state = 1
                
            if (state == 1):
                firstclick = index
            elif (state == 2):
                secondclick = index

                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global frame, turns, label
 
    for i in range(0, len(cards)):
        canvas.draw_text(str(i), (45+45*i, 50), 16, 'White')
        if exposed[i] == True:
            canvas.draw_text(str(cards[i]), (45+45*i, 80), 16, 'White')
        else:
            canvas.draw_polygon([(45+45*i, 70), (55+45*i, 70),(55+45*i, 80), (45+45*i, 80)], 4, 'Green', 'Green') 
            
    label.set_text("Turns = " + str(turns))

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
