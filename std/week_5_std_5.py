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

ball_pos = [0,0]
time = 0
paddle_pos1 = [0,0]
paddle_pos2 = [WIDTH,HEIGHT]
paddle1_vel = 0
paddle2_vel = 0
c = 8
left_player = 0
right_player = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_vel = [0.1,0.1]
    if direction == "RIGHT":
        ball_vel[0] = random.randrange(120, 240)
        ball_vel[1] = -random.randrange(60, 180)
        
    elif direction == "LEFT":
        ball_vel[0] = -random.randrange(120, 240)
        ball_vel[1] = -random.randrange(60, 180)
    else:
        print "unknown direction of ball!" 
    ball_pos = [WIDTH/2, HEIGHT/2]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global left_player , right_player  # these are ints
    left_player = 0
    right_player = 0
    random_start = random.choice(["LEFT","RIGHT"])
    spawn_ball(random_start)
    
    
def tick():
    global time, ball_pos,ball_vel
    time = 0.01
    #print time,str(ball_pos[0]),str(ball_vel[0])

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, time,\
    paddle_pos1,HALF_PAD_WIDTH, paddle_pos2, HALF_PAD_HEIGHT, pa1, pa2, pb1, pb2,\
    left_player,right_player
    
    paddle_pos1[1] = paddle_pos1[1] + paddle1_vel
    paddle_pos2[1] = paddle_pos2[1] + paddle2_vel 
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle_pos1[1] <= HALF_PAD_HEIGHT:
        paddle_pos1[1] = HALF_PAD_HEIGHT
    elif paddle_pos1[1] >= HEIGHT-HALF_PAD_HEIGHT:
        paddle_pos1[1] = HEIGHT-HALF_PAD_HEIGHT
        
    if paddle_pos2[1] <= HALF_PAD_HEIGHT:
        paddle_pos2[1] = HALF_PAD_HEIGHT
    elif paddle_pos2[1] >= HEIGHT-HALF_PAD_HEIGHT:
        paddle_pos2[1] = HEIGHT-HALF_PAD_HEIGHT

    p1a1 = paddle_pos1[0] - HALF_PAD_WIDTH
    p1a2 = paddle_pos1[0] + HALF_PAD_WIDTH
    p1b1 = paddle_pos1[1] - HALF_PAD_HEIGHT
    p1b2 = paddle_pos1[1] + HALF_PAD_HEIGHT
    
    p2a1 = paddle_pos2[0] - HALF_PAD_WIDTH
    p2a2 = paddle_pos2[0] + HALF_PAD_WIDTH
    p2b1 = paddle_pos2[1] - HALF_PAD_HEIGHT
    p2b2 = paddle_pos2[1] + HALF_PAD_HEIGHT
  
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT-BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]        
            
    # draw ball
    ball_pos[0] = ball_pos[0] + time * ball_vel[0]
    ball_pos[1] = ball_pos[1] + time * ball_vel[1]
    canvas.draw_circle(ball_pos,BALL_RADIUS, 2, "Red", "White")

    # draw paddles
    canvas.draw_polygon([(p1a1, p1b1),(p1a1, p1b2), (p1a2, p1b1),(p1a2, p1b2)],8,"white")
    canvas.draw_polygon([(p2a1, p2b1),(p2a1, p2b2), (p2a2, p2b1),(p2a2, p2b2)],8,"white")
    
    # determine whether paddle and ball collide
    if ball_pos[0] <= BALL_RADIUS+PAD_WIDTH:
        if ball_pos[1] <= p1b2 and ball_pos[1] >= p1b1:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] = ball_vel[0]*1.1
            ball_vel[1] = ball_vel[1]*1.1
        else:
            # left side people lose
            # print "left lose"
            spawn_ball("RIGHT")
            right_player+=1
            
    if ball_pos[0]>=(WIDTH - PAD_WIDTH-BALL_RADIUS):
        if ball_pos[1] <= p2b2 and ball_pos[1] >= p2b1:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] = ball_vel[0]*1.5
            ball_vel[1] = ball_vel[1]*1.5
        else:
            # right side people lose
            # print "right lose"
            spawn_ball("LEFT")
            left_player+=1
    # draw scores
    # test 
    # print str(ball_vel[0]) 
    
    scores_disp = str(left_player) + ' / ' + str(right_player)
    # add scoring board
    canvas.draw_text(scores_disp, (255, 50), 50, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel,c
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = paddle1_vel + c
        #print str(paddle1_vel)
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = paddle1_vel - c
        
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = paddle2_vel + c
        #print str(paddle2_vel)
        
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = paddle2_vel - c 
        #print str(paddle2_vel)

def keyup(key):
    global paddle1_vel, paddle2_vel,c
    
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = paddle1_vel - c
        #print str(paddle1_vel)
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = paddle1_vel + c
        
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = paddle2_vel - c
        #print str(paddle2_vel)
        
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = paddle2_vel + c 
        #print str(paddle2_vel)
        
    #create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(100,tick)
button_two = frame.add_button("Reset the Game", new_game)
# start frame
new_game()
frame.start()
timer.start()
