# template for "Stopwatch: The Game"

import simplegui

# define global variables

# count the time in milliseconds
count = 0
# format in display
time = "0:00.0"
#results the games
result = "x/y"
#point the gamer
gamer = 0
#num stop
machine = 0
#color the message in display
color = "Black"
#message the total result
message = ""

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global time    
    A = t / 600
    B = t / 10
    D = t % 10
    
    if(A > 0):
        B = B - 60
        
    if(B > 60):
        B = B % 60
    
    if(B < 10):
        C = "0"
        time = str(A) + ":" + C + str(B) + "." + str(D)
    
    else:
        time = str(A) + ":" + str(B) + "." + str(D)
    
    return time


# define event handlers for buttons; "Start", "Stop", "Reset"

#pause the game
def stop():
    global result, gamer, machine, time
    mirror = timer.is_running()
    
    timer.stop()
    
    
    if(mirror == False):
        gamer = gamer
        machine = machine
        
    elif (int(time[-1] ) == 0):
        gamer = gamer + 1
        machine = machine + 1
        
    elif(mirror == True):
        machine = machine + 1
    
    result = str(gamer) + "/" + str(machine)
#start the game    
def start():
    global color 
    timer.start()
    color = "Black"

#reset the game    
def reset():
    global count, time, gamer, machine, result, color
    time = format(0)
    count = 0
    gamer = 0 
    machine = 0
    color = "Black"
    result = str(gamer) + "/" + str(machine)
    if(timer.is_running() == False):
        timer.start()

# see the results the game       
def results():
    global gamer, machine, color, message
    if(machine == 0):
        message = "please start first"
        total = 0
    else:    
        total = float(gamer)/float(machine)*100 
    
    message = "Your punctuation is the: " + str(int(total)) + "% " 
    #print message
    color = "White"
    return message

# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count = count + 1
    format(count)
  
 # define draw handler
def draw(canvas):
    canvas.draw_text(time, [100,110], 36, "White")
    canvas.draw_text(result, [220,40], 36, "Red") 
    canvas.draw_text(message, [20,160], 16, color) 
 
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)
frame.set_draw_handler(draw)
frame.add_button("stop", stop, 200)
frame.add_button("start", start, 200)
frame.add_button("reset", reset, 200)
frame.add_button("result", results, 200)

# register event handlers
timer = simplegui.create_timer(100, tick)

 
# start frame
frame.start()
timer.stop()


# Please remember to review the grading rubric
