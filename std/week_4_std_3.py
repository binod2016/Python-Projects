# template for "Stopwatch: The Game"
import simplegui

# define global variables
tenth = 0
second = 0
minute = 0
correct = 0
countstart = 0
countstop = 0
x = 0
y = 0
status = "false"


# define helper function format that converts integer
# counting tenths of seconds into formatted string A:BC.D

def attempt(y):
        y = str(correct)+"/"+str(countstop)
        return y

def format(x):
    minute = str(tenth//600)
    x = str(tenth % 10)
    second = tenth//10
    if second < 10:
        second = "0"+str(tenth//10)
    else:
        second = str(tenth//10)
    return minute+":"+second+"."+x+" "

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global countstart, status
    if status == "false":
        countstart += 1
        status = "true"
        timer.start()
    
def stop():
    global countstop, status, correct
    if status == "true":
        status = "false"
        countstop += 1
        timer.stop()
        if tenth % 10 == 0:
            correct +=1

def reset():
    global minute, second, status, x, tenth, countstart, countstop, correct
    tenth = 0
    second = 0
    minute = 0
    correct = 0
    countstart = 0
    countstop = 0
    x = 0
    y = 0
    status = "false"
    timer.stop()

# define event handler for timer with 0.1 sec interval
def tick():
    global tenth
    tenth += 1

def draw(canvas):
    canvas.draw_text(format(x), [230,200], 48, "Orange")
    canvas.draw_text(attempt(y), [520,50], 40, "Green")

# create frame
frame = simplegui.create_frame("Stopwatch The Game", 600, 400)

# register event handlers
f = frame.add_button("Start", start, 150)
f = frame.add_button("Stop", stop, 150)
f = frame.add_button("Reset", reset, 150)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)

# start timer and frame
frame.start()
#timer.start()

# remember to review the grading rubric
