"""
    author: Arbuznikov Evgeniy
    mini-project: Spaceship
    browser: Chrome
"""

"""
    I USE BROWSER GOOGLE CHROME WHEN I WROTE THIS CODE. PLEASE USE THIS BROWSER WHEN YOU WILL CHECK MY CODE
    BIG THANKS
"""
# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

__CONST_VEL__ = [0.025, 0.025]
__CONST_ACCELERATION__ = 0.1
__CONST_COUNT_OF_ROCK__ = 5
__CONST_REMOVE_MISSILE__ = 5

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
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.cheet_shoot = False
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [130, 45], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        for i in range(2):
            self.pos[i] = (self.pos[i] + self.vel[i]) % (WIDTH if i == 0 else HEIGHT)
        
        # update velocity
        self.vel[0] *= (1 - __CONST_VEL__[0])
        self.vel[1] *= (1 - __CONST_VEL__[0])
        
        if self.thrust:
            forward = angle_to_vector(self.angle)
            for i in range(2):
                self.vel[i] += __CONST_ACCELERATION__ * forward[i]
            
    # increasing angle
    def angle_inc(self, angle_vel = None):
        self.angle_vel += .02 if angle_vel is None else angle_val
                
    # decreasing angle
    def angle_dec(self, angle_vel = None):
        self.angle_vel -= .02 if angle_vel is None else angle_vel
        
    # add sound for ship
    def change_thrust(self, thrust = False):
        self.thrust= thrust
        if thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            
    # shoot
    def shoot(self):
        global a_missile, __CONST_REMOVE_MISSILE__
        if self.cheet_shoot:
            __CONST_REMOVE_MISSILE__ = 10
            angle = -3.14
            while angle <= 3.14:
                forward = angle_to_vector(angle)
                pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
                vel = [self.vel[0] + 5 * forward[0], self.vel[1] + 5 * forward[1]]
                a_missile.append(Sprite(pos, vel, angle, 0, missile_image, missile_info, missile_sound, True))
                angle += 0.2
        else:
            __CONST_REMOVE_MISSILE__ = 5
            forward = angle_to_vector(self.angle)
            pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
            vel = [self.vel[0] + 5 * forward[0], self.vel[1] + 5 * forward[1]]
            a_missile.append(Sprite(pos, vel, self.angle, 0, missile_image, missile_info, missile_sound, True))
        
    def cheet(self):
        self.cheet_shoot = not(self.cheet_shoot)
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None, timer = False):
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
        if timer:
            self.timer_missile = simplegui.create_timer(5000.0, self.missile_spawner)
            self.timer_missile.start()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,self.angle)
    
    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % WIDTH    
    
    def missile_spawner(self):
        global a_missile
        try:
            missile = a_missile.pop(1)
            del missile
            self.timer_missile.stop()
        except IndexError:
            return 
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    #draw text and score
    canvas.draw_text('Lives: %d' % lives, (50, 50), 36, "White")
    canvas.draw_text('Score: %d' % score, (630, 50), 36, "White")

    # draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    
    # draw and update rock
    for i in range(len(a_rock)):
        a_rock[i].draw(canvas)
        a_rock[i].update()
    
    # draw and update missile shoot
    for i in range(len(a_missile)):
        a_missile[i].draw(canvas)
        a_missile[i].update()
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    a_rock = []
    for i in range(__CONST_COUNT_OF_ROCK__):
        a_rock.append(Sprite(
            [random.randrange(WIDTH), random.randrange(HEIGHT)],
            [random.choice([0.5, -1]) * random.random() * 2, random.choice([0.5, -1]) * random.random() * 2],
            1, 
            random.choice([0.5, -1]) * 0.05, 
            asteroid_image, 
            asteroid_info
        ))
    
# key down handler
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_dec()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_inc()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.change_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
# key up handler
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_inc()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_dec()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.change_thrust(False)
    elif key == simplegui.KEY_MAP['x']:
        my_ship.cheet()
        label.set_text('Cheet code: x - (use)' if my_ship.cheet_shoot else 'Cheet code: x - (not use)')
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.add_label('Author: Arbuznikov Evgeniy', 200)
frame.add_label('Mini-Project: Spaceship', 200)
frame.add_label('Date: Aug 2 2015', 200)
label = frame.add_label('Cheet code: x - (not use)', 200)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

a_rock = []
for i in range(__CONST_COUNT_OF_ROCK__):
    a_rock.append(Sprite(
            [random.randrange(WIDTH), random.randrange(HEIGHT)],
            [random.choice([0.5, -1]) * random.random() * 2, random.choice([0.5, -1]) * random.random() * 2],
            1, 
            random.choice([0.5, -1]) * 0.05, 
            asteroid_image, 
            asteroid_info
        ))
    
a_missile = [Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound, True)]

# register draw handlers
frame.set_draw_handler(draw)
# register keys handler
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer_rock = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer_rock.start()
frame.start()
