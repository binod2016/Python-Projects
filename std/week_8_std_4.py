  
# program template for Spaceship
import simplegui
import math
import random

# globals for user interface

WIDTH = 800
HEIGHT = 600
scores = 0
lives = 3


timeAngle=0

timeRock=0

signeAngle=0



class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0.05
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def shoot(self):
            global a_missile
            forward = angle_to_vector(self.angle)
            missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
            missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
            a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
            #return Sprite(self.pos, forward,self.angle, 0 , missile_image, missile_info,missile_sound)
        
    def draw(self,canvas):
        
        if self.thrust==True:
            x=self.image_center[0]+self.image_size[0]
            y=self.image_center[1]
        else:
            x=self.image_center[0]
            y=self.image_center[1]
        canvas.draw_image(self.image,[x,y],self.image_size,self.pos,self.image_size,self.angle)
    
  
    def update(self): 
        global timeAngle
        
       
        self.angle=self.angle+timeAngle*signeAngle*self.angle_vel
        if self.thrust==True:
            acceleration = angle_to_vector(self.angle)
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
            
        else:
            acceleration=[0,0]
            ship_thrust_sound.pause()
           
        self.vel[0]=0.98*self.vel[0]+0.1*acceleration[0]
        self.vel[1]=0.98*self.vel[1]+0.1*acceleration[1]
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        
            
        
            
       
            
        
            
    
# Sprite classv
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size)
    
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

           
def draw(canvas):
    global timeRock,a_rock,a_missile,lives,scores,WIDTH,HEIGHT
    
    # animiate background
    timeRock += 1
    wtime = (timeRock / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    
    #a_missile.update()
    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    WIDTH = 800

    message = "lives  "+str(lives)
    canvas.draw_text(message,(WIDTH/10,HEIGHT/6),35,"green")
    message = "scores  "+str(scores)
    canvas.draw_text(message,(8*WIDTH/10,HEIGHT/6),35,"green")
    
#key handler
def keyDown_handler(key):
    
    global timeAngle,signeAngle
    global my_ship
    #print 'key',key
    if key==37:
        timerAngle.start()
        signeAngle=-1
    if key==39:
        timerAngle.start()
        signeAngle=+1
    if key==40:
        my_ship.thrust=True
        
        
    if key==38 :
        my_ship.thrust=True
     
        
        
    if key==32:
        my_ship.shoot()
        
        
    
        
        
def keyUp_handler(key):        
    global timeAngle,timeThrust
    if (key==38) or (key==40):
        my_ship.thrust=False
        
    if (key==37) or (key==39):
        timerAngle.stop()
        timeAngle=0
    
            
# timer handler that spawns a rock    
def rock_spawner():
    global timeRock,a_rock
   
    timeRock=timeRock+1
    if timeRock % 4==0:
    
        y=random.randrange(1,WIDTH)
        x=random.randrange(1,HEIGHT)
        posRock=[x,y]
        scaleX=random.random()
        scaleY=random.random()
        velRock=[0.005*scaleX,0.005*scaleY]
        angle=random.random()*math.pi
        angleVel=random.random()
        a_rock=Sprite(posRock,velRock, angle,angleVel , asteroid_image, asteroid_info,)
      
def angle_spawner():
    global timeAngle
    timeAngle+=1 
    print timeAngle


    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
global my_ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

frame.set_draw_handler(draw)
frame.set_keydown_handler(keyDown_handler)
frame.set_keyup_handler(keyUp_handler)

timer = simplegui.create_timer(200.0, rock_spawner)
timerAngle = simplegui.create_timer(100.0, angle_spawner)
# get things rolling
timer.start()
frame.start()
