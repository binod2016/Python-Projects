#============================================================
#This program allowes user to play "Guess the Number" game.
#------------------------------------------------------------
#Date:Jun-13/015  Class: Coursera/Fundamental_Computing_I/w3
#------------------------------------------------------------
#http://www.codeskulptor.org/#user40_KZ54uK0Fo8_28.py
#============================================================

#====================Import section ===============
import simplegui
import random
import math


#================Helper Functions =================


def new_game():
    
    global secret_num
    global num_range
    global trial
    global allowed_trial
   
    #---initiate global veriables -----
    num_range = 0
    secret_num = 0
    trial = 0
    allowed_trial = 0
    pass

def warning(x,num_range):
    if x > num_range:
        print "Warning:You crossed the range of Numbers!"
    pass
    

#===========  event handlers =======================
def range100():
    
    global num_range
    global secret_num
    global allowed_trial
    
    num_range = 100
    allowed_trial = 10
    print "New Game :  Range is from 0 to", num_range,"."
    secret_num = random.randint(0,num_range)
    pass


def range1000():
    global num_range
    global secret_num
    global allowed_trial
    
    num_range = 1000
    allowed_trial = 15
    print "New Game :  Range is from 0 to", num_range,"."
    secret_num = random.randint(0,num_range)
    pass
   
    
def input_guess(guess):
    global trial
    global num_range
    global secret_num
    global allowed_trial
    
    guess_num = int(guess)
    trial = trial+1
    
    if trial < allowed_trial+1:
            print "Guess was:", guess_num
            if guess_num > num_range:
                warning(guess_num,num_range)
            else:
                print"Number of remainin trial=",allowed_trial-trial
                if guess_num > secret_num:
                    print "Higher !"
                elif guess_num < secret_num:
                    print "Lower !"
                else:
                    print "Correct ! You are winner!"
    elif trial == allowed_trial+1:
            print "Sorry! You loose...Play next game!"
    pass

    
#===================== create frame =======================
frm = simplegui.create_frame("guess_the _number!",300,300)

#================= event handlers =========================
frm.add_button("Range is [0,100)",range100,200)
frm.add_button("Range is [0,1000)",range1000,200)
frm.add_input("Enter a guess",input_guess,200)


#============== call new_game =============================

new_game()

#====================<><><>================================
