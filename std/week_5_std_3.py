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
LEFT = True
RIGHT = False

ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2 ,HEIGHT/2]
    ball_vel[1] = -random.randrange(60,180)/60.0
    if direction == LEFT:
        ball_vel[0] = -random.randrange(120, 240)/60.0
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)/60.0

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2]
    paddle2_pos = [WIDTH - 1 - HALF_PAD_WIDTH, HEIGHT/2]

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ## bouncing down
    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    ## bouncing up
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Yellow", "Yellow")
    
    # update paddle's vertical position, keep paddle on the screen   

    ## left paddle
    if paddle1_pos[1] + paddle1_vel <= HALF_PAD_HEIGHT:
         paddle1_pos[1] = paddle1_pos[1]
    elif paddle1_pos[1] + paddle1_vel >= HEIGHT - 1 - HALF_PAD_HEIGHT:
        paddle1_pos[1] = paddle1_pos[1]
    else:
        paddle1_pos[1] += paddle1_vel
       
    ## right paddle
    if paddle2_pos[1] + paddle2_vel <= HALF_PAD_HEIGHT:
         paddle2_pos[1] = paddle2_pos[1]
    elif paddle2_pos[1] + paddle2_vel >= HEIGHT - 1 - HALF_PAD_HEIGHT:
        paddle2_pos[1] = paddle2_pos[1]
    else:
        paddle2_pos[1] += paddle2_vel
       
    
    # draw paddles
    ## left
    p1_up = (paddle1_pos[0], paddle1_pos[1]- HALF_PAD_HEIGHT)
    p1_down = (paddle1_pos[0], paddle1_pos[1]+ HALF_PAD_HEIGHT)
    canvas.draw_line(p1_up, p1_down, PAD_WIDTH,"RED")
    ## right
    p2_up = (paddle2_pos[0], paddle2_pos[1]- HALF_PAD_HEIGHT)
    p2_down = (paddle2_pos[0], paddle2_pos[1]+ HALF_PAD_HEIGHT)
    canvas.draw_line(p2_up, p2_down, PAD_WIDTH,"CYAN")
    
    
    # determine whether paddle and ball collide    
    
    ## hitting the left paddle/gutter
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if (ball_pos[1] >= p1_up[1]) and (ball_pos[1] <= p1_down[1]):
            ball_vel[0] = - 1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score2 += 1
            spawn_ball(RIGHT)   
    ## hitting the right paddle/gutter
    elif ball_pos[0] >= (WIDTH - 1) - PAD_WIDTH - BALL_RADIUS:
        if (ball_pos[1] >= p2_up[1]) and (ball_pos[1] <= p2_down[1]):
            ball_vel[0] = - 1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH/4, HEIGHT/6), 36, "red")
    canvas.draw_text(str(score2), (3*WIDTH/4, HEIGHT/6), 36, "cyan")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 3
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 3
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", new_game, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
