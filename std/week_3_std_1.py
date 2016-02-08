#Guess the number game

import simplegui
import random

secret_number = 0
numberOfGuesses = 0
pendingGuess = 0
rangeLow=0
rangeHigh=100
inputTextObj=None

def calculateNumOfGuess(low,high):
    """
        Function calculates the number of guesses user is allowed 
        for a given range.
        The lower bound and upperbound of the range is expected to be
        passed as input parameters.
        
        2**n >= high-low+1, n is the number of guesses allowed.
    """
    temp = high-low +1
    guess=0
    for i in range(0,high):
        if 2**i >= temp:
            guess=i
            break
    return guess
            
# 
def new_game():
    """
        helper function to start and restart the game
        This functions initializes global variables used in the game.
        Determines the secret number, the number of guesses allowed for the
        chosen range and initializes the pending number of guesses.
    """
    global secret_number, numberOfGuesses, pendingGuess
    clear_text(inputTextObj)
    secret_number = random.randrange(rangeLow,rangeHigh)
    numberOfGuesses = calculateNumOfGuess(rangeLow,rangeHigh)
    pendingGuess = numberOfGuesses
    print "\nChosen game range is %d to %d."%(rangeLow,rangeHigh)
    print "Please guess a number in this range by entering it in the text box"
    print "You have %d guesses to go. Good Luck!" % pendingGuess

def validate_guess(guess):
    """
        Function takes the number guessed by user as input and determines if
        secret number matches this or if it is lower or higher than guessed number
        and displays message to user.
        It returns True if the guess is correct else False
    """
    global pendingGuess
    ret = False
    pendingGuess-=1
    if secret_number == guess:
        print "Congrats you have guessed the number correctly!"
        ret = True
        pendingGuess = 0
    elif secret_number > guess:
        print "Secret number is HIGHER than your guess"
    else:
        print "Secret number is LOWER than your guess"
    return ret

# define event handlers for control panel
def range100():
    """
        Event handler for button that sets the range to [0,100) and
        starts a new game 
    """
    global rangeHigh
    rangeHigh = 100
    new_game()

def range1000():
    """
        Event handler for button that sets the range to [0,1000) and 
        starts a new game     
    """
    global rangeHigh
    rangeHigh = 1000
    new_game()

def clear_text(textObject):
    """
        clear the text box
        input is the text box object
    """
    textObject.set_text("")
        

def input_guess(guess):
    """
        Event handler for the input box.
        When user enters the number and presses enter, this function calls validate_guess
        to determine if the number has been guessed correctly.
        In case the number has not been guessed, the user is expected to enter 
        another guess until they run out of guesses.
        If user runs out of guess or has won, then a new game is started using the same
        range as the last game.
    """
    global pendingGuess
    if guess.isdigit():
        guessNum = int(guess)
        if rangeLow <= guessNum <= (rangeHigh-1):
            print "\nYour guess is:",guessNum
            newGame=False
            isDone = validate_guess(guessNum)
            if not(isDone) and pendingGuess:
                if pendingGuess == 1:
                    print "You have %d more guess to go." %  pendingGuess
                else:
                    print "You have %d guesses to go." %  pendingGuess
            elif not(isDone) and not(pendingGuess):
                print "No more guesses left.\nSorry you have lost the game. Better luck next time."
                print "The secret number was %d" % secret_number
                newGame=True
            elif isDone:
                newGame=True
                
            if newGame:
                print "Starting a new Game with the same range as last one..."
                new_game()
        else:
            print "\nError:Please enter number between %d and %d inclusive"%(rangeLow,rangeHigh-1)
            clear_text(inputTextObj)
    else:
        print "\nError:Please enter a valid number in the selected range"
        clear_text(inputTextObj)

# create frame
newframe = simplegui.create_frame("Guess the number", 300,300)
# register event handlers for control elements and start frame
inputTextObj = newframe.add_input("Enter the number:",input_guess,50) 
newframe.add_button("Range [0,100)",range100,105)
newframe.add_button("Range [0,1000)",range1000)
newframe.start()
# call new_game 
print "\t\tWelcome to \"Guess the number\" game"
new_game()
