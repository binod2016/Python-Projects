# template for "Stopwatch: The Game"
import simplegui
import time

# define global variables
time_in_tenths = 0
stop_cnt = 0
success_cnt = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    
    # how many minutes
    A = t//600
    
    # how many tens of seconds
    # //10 drops the tenths
    # %60 drops the minutes
    # //10 drops the seconds
    B = ((t//10)%60)//10
    
    # how many seconds
    # //10 drops the tenths
    # %60 drops the minutes
    # %10 drops the tens of seconds
    C = ((t//10)%60)%10
    
    # how many tenths of seconds
    # %10 drops the seconds
    D = t%10
    
    return str(A) + ":" + str(B) + str(C) + "." + str(D)

# define event handlers for buttons; "Start", "Stop", "Reset"
def button_start():
    timer.start()

def button_stop():
    global stop_cnt
    global success_cnt
    
    if timer.is_running():
        timer.stop()
        stop_cnt += 1
        
        # count successful stops at whole seconds
        #i.e. no tenths
        if (time_in_tenths %10) == 0:
            success_cnt += 1
    
def button_reset():
    global time_in_tenths
    global stop_cnt
    global success_cnt
    
    timer.stop()
    time_in_tenths = 0    
    stop_cnt = 0
    success_cnt = 0
        
# define event handler for timer with 0.1 sec interval
def tick():
    global time_in_tenths
    time_in_tenths += 1    
    
# define draw handler
def draw(canvas):
    f_time = format(time_in_tenths)
    canvas.draw_text(str(f_time), (150, 275), 100, "Red")
    canvas.draw_text(str(success_cnt) + "/" + str(stop_cnt), (410, 40), 40, "Red")
    
# create frame
frame = simplegui.create_frame("Stop Watch Game", 500, 500)
button1 = frame.add_button('Start', button_start, 120)
button2 = frame.add_button('Stop', button_stop, 120)
button3 = frame.add_button('Reset', button_reset, 120)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw)

# start frame
frame.start()

