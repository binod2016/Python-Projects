#============================================================
#This program allowes user to play "classic arcade game Pong".
#------------------------------------------------------------
#Date:Jun-27/015  Class: Coursera/Fundamental_Computing_I/w5
#============================================================




''' ===========Import========================'''

import simplegui
import random

'''======= initialize globals - pos and vel =================='''
WIDTH = 1000
HEIGHT = 600       
BALL_RADIUS = 10
PAD_WIDTH = 20
PAD_HEIGHT = 200
SIDE = True



def spawn_ball(right):
    
    ''' helper function that spawns a ball by updating the ball's
    position vector and velocity vector if right is True, the ball's
    velocity is upper right,else upper left'''

    global ball_pos, ball_vel
    ball_pos = [WIDTH/2, HEIGHT/2]
    if right == True:
        ball_vel = [random.randrange(5, 10),-random.randrange(5, 10)]
    else:
        ball_vel = [-random.randrange(5, 10),-random.randrange(5, 10)]
    
    
'''============== event handlers============='''

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel,\
           paddle2_vel,score1, score2, SIDE
    paddle1_pos, paddle2_pos = (HEIGHT - PAD_HEIGHT)/2,\
                               (HEIGHT - PAD_HEIGHT)/2
    paddle1_vel = paddle2_vel = 0
    score1, score2 = 0, 0
    SIDE = not SIDE
    spawn_ball(SIDE)
    
'''=============function to update ball and paddle=============='''

def Updator():
    
        global score1, score2, paddle1_pos,\
               paddle2_pos, ball_pos, ball_vel,\
               paddle1_pos, paddle2_pos,\
                paddle1_vel, paddle2_vel
        
        ''' update ball's position and velocity'''
        
        if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
            if paddle1_pos <= ball_pos[1] <= (paddle1_pos+PAD_HEIGHT):
                ball_vel[0] = - 1.1 * ball_vel[0]
            else:
                spawn_ball(True)
                score2 += 1
        if ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
            if paddle2_pos <= ball_pos[1] <= (paddle2_pos+PAD_HEIGHT):
                ball_vel[0] = - 1.1 * ball_vel[0]
            else:
                spawn_ball(False)
                score1 += 1
        if ball_pos[1] <= BALL_RADIUS:
            ball_vel[1] = - ball_vel[1]
        if ball_pos[1] >= (HEIGHT - BALL_RADIUS):
            ball_vel[1] = - ball_vel[1]

        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
        
        
        ''' update paddle's vertical position, keep paddle on the screen'''
        
        if 0 <= (paddle1_pos + paddle1_vel) <= HEIGHT - PAD_HEIGHT:
            paddle1_pos += paddle1_vel
        if 0 <= (paddle2_pos + paddle2_vel) <= HEIGHT - PAD_HEIGHT:
            paddle2_pos += paddle2_vel   
       
        
'''=========== handler function to draw canvas ===================='''  


def draw(canvas):
    
    global score1, score2, paddle1_pos,\
           paddle2_pos, ball_pos, ball_vel,\
           paddle1_pos, paddle2_pos,\
            paddle1_vel, paddle2_vel
    
    
    '''----------Constant Config-------'''
    
    '''draw text and text-box'''
    canvas.draw_text(str(score1), (460, 40), 40, "yellow")
    canvas.draw_text(str(score2), (520, 40), 40, "yellow")
    canvas.draw_line([450,0],[450,50], 2, "yellow")
    canvas.draw_line([450,50],[500,50], 2,  "yellow")
    canvas.draw_line([500,50],[550,50], 2,  "yellow")
    canvas.draw_line([550,0],[550,50], 2,  "yellow")
    
    '''draw mid line and gutters'''
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 5, "orange")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 5, "red")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH\
                      - PAD_WIDTH, HEIGHT], 5, "red")
    
    '''draw paddles'''
    canvas.draw_line([PAD_WIDTH/2, paddle1_pos],[PAD_WIDTH/2,\
                    paddle1_pos+PAD_HEIGHT], PAD_WIDTH, "blue")
    canvas.draw_line([WIDTH - PAD_WIDTH/2, paddle2_pos],\
                     [WIDTH- PAD_WIDTH/2, paddle2_pos+PAD_HEIGHT],\
                      PAD_WIDTH, "blue")
    
    
    '''----------Dynamic Config-------'''
    
    '''update ball and paddle calling Updator function'''
    Updator()
    ''' draw ball and scores'''
    def colr():
        ''' function changes the color of ball'''
        col = ["red","blue","white","yellow"]
        cl = col[random.randint(0,3)]
        return cl
    canvas.draw_circle(ball_pos, BALL_RADIUS, 0.1,colr(),colr())
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 20
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -vel   
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -vel   
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0   
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0  
        
def restart_handler():
    new_game()

'''========= create frame============================='''
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background("green")
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart_handler, 100)

'''==============start frame========================'''
frame.start()
new_game()
'''=============== <><> End of Code <><> ===================='''






