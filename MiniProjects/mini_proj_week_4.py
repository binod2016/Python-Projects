
#============================================================
#This program allowes user to play "Stop Watch" game.
#------------------------------------------------------------
#Date:Jun-20/015  Class: Coursera/Fundamental_Computing_I/w4
#------------------------------------------------------------
#http://www.codeskulptor.org/#user40_zSySZy60JZ_9.py
#============================================================


'''=================Import section========================='''
import simplegui


'''============= initiate global variables ========='''

trial = 0  		#the number of games
win = 0		    #the number of games won
clock = 0		#timer
msec = 0		#millisecond


stop_it = False	



'''========== Event handler ===='''
def start():
    global stop_it
    
    if stop_it == False:
        timer.start()
        stop_it = True

def stop():
    global trial, win, stop_it
    
    if stop_it == True:
        timer.stop()
        stop_it = False
        
        trial = trial+1
        if msec == 0:
            win = win+1

def reset():
    global trial, win, clock, msec, stop_it
    
    if stop_it == True:
        timer.stop()
        stop_it = False
    
    trial = 0
    win = 0
    clock = 0
    msec = 0

'''============== Event handler for timer ===='''

def tick():
    global clock
    
    clock = clock+1
    if clock - clock // 1000 * 1000 == 600:
        clock = clock + 400
        
'''============== Helper function for draw handler  ==========='''        
def format(t):
    
    ''' This function sets timer into A:bc.D'''
    
    global msec
    minute = t // 1000
    sec = (t - minute * 1000) // 10
    msec = (t - minute * 1000) % 10
    
    if sec < 10:
        return str(minute) + ":0" + str(sec) + "." + str(msec)
    else:
        return str(minute) + ":" + str(sec) + "." + str(msec)

''' ===============  Draw handler =============================== '''

def draw(canvas):
    canvas.draw_text(str(win)+"/"+str(trial), [150, 20], 20, "Green")
    canvas.draw_text(format(clock),[70, 110], 28, "White")

'''================= Frame and timer ============================'''
frame = simplegui.create_frame("Stopwatch: The Game", 200, 200)
timer = simplegui.create_timer(100, tick)

'''================= Account  event handlers ============='''
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

'''=========Account draw handler============== '''   
frame.set_draw_handler(draw)

'''========== start frame=========='''
frame.start()

'''===============<><><>=============================='''



