# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    secret_number = range100()
    counter = 0
    max_guesses = 7

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global secret_number, max_guesses, counter
    secret_number = random.randrange(0,101)
    max_guesses = 7
    counter = 0
    print ""
    print "A new game has been started"
    print "The secret number is between 0 and 100"

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number, max_guesses, counter
    secret_number = random.randrange(0,1001)
    max_guesses = 10
    counter = 0
    print ""
    print "A new game has been started"
    print "The secret number is between 0 and 1000"
    
def input_guess(guess):
    # main game logic 
    global counter
    
    print "Guess was " + guess
    guess = int (guess)
    counter += 1
    
    if guess < secret_number:
        print "Higher"
        print "You have " + str(max_guesses - counter) + " guesses remaining"
    elif guess > secret_number:
        print "Lower"
        print "You have " + str(max_guesses - counter) + " guesses remaining"
    else:
        print "Correct. You win!"
        
    if max_guesses == counter:
        print "You have not guessed the secret number. You lose. Try again!"
        if max_guesses == 7:
            range100()
        else:
            range1000()
    else:
        print ""

    
# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200)

# register event handlers for control elements and start frame
range100button = frame.add_button("Range: 0 - 100", range100, 150)
range1000button = frame.add_button("Range: 0 - 1000", range1000, 150)
input = frame.add_input("My Guess:", input_guess, 50)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
