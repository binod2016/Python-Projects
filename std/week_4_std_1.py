# template for "Stopwatch: The Game"
import simplegui

# define global variables
stop = True
interval = 100
width = 400
height = 200
time = 0
whole_game = 0
win_game = 0
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D = t % 10
    A = t / 600
    tmp = (t % 600 - D) / 10
    C = tmp % 10
    B = tmp / 10
    return str(A)+":"+str(B)+str(C)+"."+str(D)   

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global stop, whole_game, win_game
    stop = False
    timer.start()

def stop_handler():
    global stop, whole_game, win_game
    stop = True
    whole_game += 1
    if(time % 10 == 0):
        win_game += 1
    timer.stop()
    
def reset_handler():
    global stop, whole_game, win_game, time
    time = 0
    whole_game = 0
    win_game = 0
    timer.stop()
    
# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time = time + 1

def full():
    global whole_game, win_game       
    return str(win_game)+"/"+str(whole_game)
# define draw handler
def draw(canvas):
    canvas.draw_text(format(time), [100, 130], 60, "white")
    canvas.draw_text(full(), [350, 20], 20, "white")
    
# create frame
frame = simplegui.create_frame("StopWatch", width, height)
frame.set_canvas_background("green")
timer = simplegui.create_timer(interval, tick)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start_handler, 100)
frame.add_button("Stop", stop_handler, 100)
frame.add_button("Reset", reset_handler, 100)

# start frame
frame.start()
# Please remember to review the grading rubric
