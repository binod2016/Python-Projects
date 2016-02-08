# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 0
time = 0
started=False   
bestscore=0

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
missile_sound.set_volume(0)
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
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def thruster(self,thrust):
        if thrust:
            self.image_center[0] = 135
        else:
            self.image_center[0] = 45
            
    def draw(self,canvas):
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size, self.angle)

    def update(self):
        self.vel[0]*=.967
        self.vel[1]*=.967
        forward = angle_to_vector(self.angle)
        if thrust:
            self.vel[0]+=forward[0]/4
            self.vel[1]+=forward[1]/4
        self.pos = [(self.pos[0]+self.vel[0])%WIDTH,(self.pos[1]+self.vel[1])%HEIGHT]
        self.angle+=self.angle_vel
        
    def newangle(self,direction):
        if direction=='left':
            self.angle_vel -= .04
        elif direction=='right':
            self.angle_vel += .04
        else:
            self.angle_vel=0
            
    def shoot(self):
        forward = angle_to_vector(self.angle)
        norm = math.sqrt(forward[0]**2+forward[1]**2)/45
        pos0 = self.pos[0]+forward[0]/norm
        pos1 = self.pos[1]+forward[1]/norm
        vel0 = self.vel[0]/2+forward[0]
        vel1 = self.vel[1]/2+forward[1] 
        velnorm=math.sqrt(vel0**2+vel1**2)
        vel0=16*vel0/velnorm
        vel1=16*vel1/velnorm
        return [[pos0,pos1],[vel0,vel1]]
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None, age=0):
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
        self.age = age
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size, self.angle)
        else:            
            canvas.draw_image(self.image,[self.image_center[0]+self.age*128,self.image_center[1]],self.image_size,self.pos,self.image_size, self.angle)
            self.age+=1
            
    def update(self):
        if self.animated:
            self.age=0
        else:
            self.angle += (0.005*self.angle_vel)
            if self.lifespan<10000:
                self.pos[0] = (self.pos[0] + self.vel[0]/2.0)
                self.pos[1] = (self.pos[1] + self.vel[1]/2.0)
                self.age+=1
            else:
                self.pos[0] = (self.pos[0] + self.vel[0]/2.0)%WIDTH
                self.pos[1] = (self.pos[1] + self.vel[1]/2.0)%HEIGHT
            if self.age<self.lifespan:
                return False
            else:
                return True
        
    def collide(self,sprite):
        d=math.sqrt((self.pos[0]-sprite.pos[0])**2+(self.pos[1]-sprite.pos[1])**2)
        if d<=(self.radius+sprite.radius):
            return True
        else:
            return False    
def draw(canvas):
    global time,started,bestscore
    if lives==0:
        started=False
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    if started:
        # draw ship and sprites
        for rock in rocks:
            rock.draw(canvas)
            rock.update()
        my_ship.draw(canvas)
        my_ship.update()
        try:
            for i in range(3):
                expo.draw(canvas)
        except:
            pass
        for missile in list(missiles):
            missile.draw(canvas)
            up=missile.update()
            if up:
                missiles.remove(missile)
        
        ship_collision(set([my_ship]),rocks)    
        missile_collision(missiles,rocks)
        try:
            explosion.draw(canvas)
        except:
            pass
    else:
        canvas.draw_image(splash_image,splash_info.center,splash_info.size,[WIDTH/2,HEIGHT/2],splash_info.size)
        soundtrack.rewind()
        
    # drawing text
    canvas.draw_text("Lives: "+str(lives), [20,30], 32, "yellow")
    if score>bestscore:
        bestscore=score
    canvas.draw_text("Best Score: "+str(bestscore), [616-16*(len(str(bestscore))),30], 32, "White")
    canvas.draw_text("Your Score: "+str(score), [616-16*(len(str(score))),60], 32, "White")
    
# angle handler
direction=''
thrust = False
def key_down(key):
    global direction,thrust,a_missile
    if key==37:
        direction='left'
        my_ship.newangle(direction)
    elif key==39:
        direction='right' 
        my_ship.newangle(direction)
    elif key==38:
        thrust=True
        my_ship.thruster(thrust)
        ship_thrust_sound.play()    
    elif key==32:
        missile_spawner(my_ship)

def missile_spawner(ship):
    global missiles
    [pos,vel] = ship.shoot()
    missile = Sprite(pos, vel, 1, 1, missile_image, missile_info, missile_sound)
    missiles.add(missile)
    
def key_up(key):
    global direction, thrust
    if key==37 or key==39:
        direction=""
        my_ship.newangle(direction)
    elif key==38:
        thrust=False
        my_ship.thruster(thrust)
        ship_thrust_sound.rewind()
        
def mouse_handler(pos):
    global started,score,lives, missile_sound,soundtrack,my_ship
    if not started:
        if (pos[1]>312) and (pos[1]<363) and (pos[0]>275) and (pos[0]<525):
            started=True
            lives=3
            score=0
            missile_sound.set_volume(0)
            soundtrack.play()
            my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], -1.57, ship_image, ship_info)

# timer handler that spawns a rock    
def rock_spawner():
    global rocks, lives
    ang = 0
    ang_vel = random.randrange(20,50)/10.0
    vel = [(random.randrange(5,25)-15)/8.0,(random.randrange(5,25)-15)/8.0]
    pos = [random.randrange(20,780),random.randrange(20,580)]
    rock = Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info)
    if rock.collide(my_ship):
        pos[0]+=120
        rock = Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info)
    if len(rocks)<12 and lives>0:
        rocks.add(rock)

# collision handlers

def ship_collision(ships,Rocks):
    global lives,expo
    for ship in ships:
        l=len(Rocks)
        rock_collision(ship,rocks)
        if l>len(rocks):
            if lives>1:
                lives-=1
            else:
                l=list(Rocks)
                for r in l:
                    Rocks.remove(r)
                lives=0
            pos=my_ship.pos
            expo=Sprite(pos, [0,0], 0, 0, explosion_image, explosion_info,explosion_sound,age=0)
            
def rock_collision(ship,Rocks):
    global explosion
    for rock in list(Rocks):
        if rock.collide(ship):
            Rocks.remove(rock)
            pos=rock.pos
            explosion=Sprite(pos, [0,0], 0, 0, explosion_image, explosion_info,explosion_sound,age=0)

               
                
def missile_collision(Missiles,Rocks):
    global score
    for missile in list(Missiles):
        l=len(Rocks)
        rock_collision(missile,Rocks)
        if l>len(Rocks):
            Missiles.remove(missile)
            score+=10
            
            
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], -1.57, ship_image, ship_info)
rocks=set([])
missiles=set([])

# register handlers
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

frame.set_mouseclick_handler(mouse_handler)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1200.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
