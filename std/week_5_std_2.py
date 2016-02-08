# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2] 
    if direction == RIGHT:
        ball_vel = [(random.randrange(120, 240)/50),-(random.randrange(60, 180)/50)]
    if direction == LEFT:
        ball_vel = [-(random.randrange(120, 240)/50),-(random.randrange(60, 180)/50)] 


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = 0
    paddle2_pos = 0
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)
    
def button_handler():
    new_game()



def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    score1_string = str(score1)
    score2_string = str(score2)
    
    #draw score
    canvas.draw_text(score1_string, (WIDTH/4 + 4, 50), 50, 'ORANGE')
    canvas.draw_text(score2_string, (WIDTH - WIDTH/4 , 50), 50, 'BLUE')

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # Update ball position
    # determine whether paddle2 and ball collide
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[0] < (0 + PAD_WIDTH + BALL_RADIUS):
        if ball_pos[1] > paddle1_pos and ball_pos[1] < paddle1_pos + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]*2
        else:
            spawn_ball(RIGHT)
            score2 += 1
    # determine whether paddle1 and ball collide        
    if ball_pos[0] > (WIDTH - PAD_WIDTH - BALL_RADIUS):
        if ball_pos[1] > paddle2_pos and ball_pos[1] < paddle2_pos + PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]*2
        else:
            spawn_ball(LEFT)
            score1 += 1
           
    if ball_pos[1] < (0 + BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] > (HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        
    print "ball" ,ball_pos
    print "paddle bottom", paddle1_pos + PAD_HEIGHT
    print "paddle top", paddle1_pos
    # Draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Green", "YELLOW")
    
    
    #update paddle 1 position and keep paddle on screen
    if paddle1_pos > 0:
        paddle1_pos += paddle1_vel
    elif paddle1_pos <= 0:
        paddle1_pos = 0
    if paddle1_pos < (HEIGHT - PAD_HEIGHT):
        paddle1_pos += paddle1_vel
    elif paddle1_pos >= (HEIGHT - PAD_HEIGHT):
        paddle1_pos = (HEIGHT - PAD_HEIGHT)
    print "paddle " , paddle1_pos
        
    #update paddle 2 position and keep paddle on screen
    if paddle2_pos > 0:
        paddle2_pos += paddle2_vel
    elif paddle2_pos <= 0:
        paddle2_pos = 0
    if paddle2_pos < (HEIGHT - PAD_HEIGHT):
        paddle2_pos += paddle2_vel
    elif paddle2_pos >= (HEIGHT - PAD_HEIGHT):
        paddle2_pos = (HEIGHT - PAD_HEIGHT)

    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos], [PAD_WIDTH, paddle1_pos], [PAD_WIDTH, paddle1_pos+PAD_HEIGHT], [0, paddle1_pos+PAD_HEIGHT]], 1, 'Yellow', 'ORANGE')
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos], [WIDTH, paddle2_pos], [WIDTH, paddle2_pos + PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT]], 1, 'Yellow', 'BLUE')
     

def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel += 5
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= 5
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel += 5
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= 5
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel -= 5
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel += 5
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel -= 5
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel += 5


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset_button = frame.add_button('RESET', button_handler)


# start frame
new_game()
frame.start()
