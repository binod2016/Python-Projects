# template for "Stopwatch: The Game"
import simplegui

# define global variables
time = 0
sum = 0
isStopped = False
success = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    if (t < 10):
        min = 0
        sec = 0
        ms  = t
    elif (t >= 10 and t < 600):
        min = 0
        sec = t / 10
        ms = (t % 10)
    else:
        min = t / 600
        sec = (t % 600) / 10
        ms = t % 10
    return '%02d:%02d.%1d' % (min, sec, ms) 

def checktime(t):
    global success
    if not t % 10:
        success = success + 1
    return success    

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    print 'Start timer'
    global isStopped
    isStopped = True
    timer.start()
    isStopped = False
    
def stop_button():
    print 'Stop timer'
    global time
    global sum
    global isStopped
    timer.stop()
    print isStopped
    if not isStopped:
       sum = sum + 1
    isStopped = True
    checktime(time)
    
def reset_button():
    global time
    global sum
    global success
    global isStopped
    time = 0
    sum = 0
    isStopped = True
    success = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time = time + 1
    print time
    
# define draw handler
def draw_handler(canvas):
    global time
    global sum
    global success
    canvas.draw_text(format(time), (50, 100), 30, 'Blue')
    canvas.draw_text(str(success) + '/' + str(sum) , (130,20), 20, 'Yellow')
    
                     
# create frame
f = simplegui.create_frame('My timer', 200, 200)

# register event handlers
timer    = simplegui.create_timer(100, timer_handler)
startbtn = f.add_button('Start', start_button, 120)
stopbtn  = f.add_button('Stop', stop_button, 120)
rstbtn   = f.add_button('Reset', reset_button, 120)

# start frame
f.set_draw_handler(draw_handler)
f.start()
timer.start()

# Please remember to review the grading rubric
