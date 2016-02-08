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
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = []
paddle_1_pos = [[0, HEIGHT/2 + HALF_PAD_HEIGHT], [0, HEIGHT/2 - HALF_PAD_HEIGHT], [PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT], [PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]]
paddle_2_pos = [[WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT], [WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT], [WIDTH-PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT], [WIDTH-PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]]    
paddle2_vel = 0
paddle1_vel = 0
score1 = 0
score2 = 0
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == LEFT:
        ball_vel = [(float(random.randrange(120, 240))/100 * -1), (float(random.randrange(60, 180))/100 * -1)]
    elif direction == RIGHT :
        ball_vel = [(float(random.randrange(120, 240))/100), (float(random.randrange(60, 180))/100 * -1)]
         


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle_1_pos = [[0, HEIGHT/2 + HALF_PAD_HEIGHT], [0, HEIGHT/2 - HALF_PAD_HEIGHT], [PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT], [PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]]
    paddle_2_pos = [[WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT], [WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT], [WIDTH-PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT], [WIDTH-PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]]
    direction = random.choice([True, False])
    score1 = 0
    score2 = 0
    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    
    if ball_pos[1] >= HEIGHT - BALL_RADIUS or ball_pos[1] <= 0 + BALL_RADIUS:
        ball_vel[1] = ball_vel[1] * -1
      
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')
    # update paddle's vertical position, keep paddle on the screen
    if (paddle_2_pos[0][1] < HEIGHT and paddle2_vel == 2) or (paddle_2_pos[1][1] > 0 and paddle2_vel == -2):
        paddle_2_pos[0][1] += paddle2_vel
        paddle_2_pos[1][1] += paddle2_vel
        paddle_2_pos[2][1] += paddle2_vel
        paddle_2_pos[3][1] += paddle2_vel
    if (paddle_1_pos[0][1] < HEIGHT and paddle1_vel == 2) or (paddle_1_pos[1][1] > 0 and paddle1_vel == -2):
        paddle_1_pos[0][1] += paddle1_vel
        paddle_1_pos[1][1] += paddle1_vel
        paddle_1_pos[2][1] += paddle1_vel
        paddle_1_pos[3][1] += paddle1_vel
    # determine whether paddle and ball collide    
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS and (ball_pos[1] + BALL_RADIUS >= paddle_1_pos[1][1] and ball_pos[1] - BALL_RADIUS <= paddle_1_pos[0][1]):
        ball_vel[0] = ball_vel[0] * -1
        ball_vel[0] += 0.1 * ball_vel[0]
        ball_vel[1] += 0.1 * ball_vel[1]
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS and (ball_pos[1] + BALL_RADIUS >= paddle_2_pos[1][1] and ball_pos[1] - BALL_RADIUS <= paddle_2_pos[0][1]):
        ball_vel[0] = ball_vel[0] * -1
        ball_vel[0] += 0.1 * ball_vel[0]
        ball_vel[1] += 0.1 * ball_vel[1]
    elif ball_pos[0] >= WIDTH - BALL_RADIUS:
        spawn_ball(LEFT)
        score1 +=1
    elif ball_pos[0] <= 0 + BALL_RADIUS:
        spawn_ball(RIGHT)
        score2 +=1

    # draw paddles
    canvas.draw_polygon(paddle_1_pos, 1, 'White', 'White')
    canvas.draw_polygon(paddle_2_pos, 1, 'White', 'White')
    # determine whether paddle and ball collide    

    # draw scores
    canvas.draw_text(str(score1), (120, 150), 80, 'White')
    canvas.draw_text(str(score2), (450, 150), 80, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    print key
    if key == 40:
        paddle2_vel = 2
    elif key == 38:
        paddle2_vel = -2
    elif key == 83:
        paddle1_vel = 2
    elif key == 87:
        paddle1_vel = -2
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle2_vel = 0
    paddle1_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

button = frame.add_button('Restart', new_game, 200)
# start frame
new_game()
frame.start()
