#===================================================================
# This program Draws the RiceRock which can shoot missile!
#===================================================================
#Date: 2015-Aug-8
#http://www.codeskulptor.org/#user40_R8EBdh1wTl_4.py
#===================================================================

import simplegui
import math
import random

'''========= globals for user interface ================'''

WIDTH = 800
HEIGHT = 600
best_score = 0
score = 0
lives = 3
time = 0.5
started = False
rockSet = set()
explosionSet = set()
missileSet = set()


'''================================== Class Info ===================================='''

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
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris1_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

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
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def sprite_holder(spriteGroup, canvas):
    removeSet = set()
    for sprite in spriteGroup:
        sprite.draw(canvas)
        if sprite.update():
            removeSet.add(sprite)
    if removeSet:
        spriteGroup.difference_update(removeSet)

def collider(spriteGroup, otherSprite):
    removeSet = set()
    for sprite in spriteGroup:
        if sprite.collide(otherSprite):
            removeSet.add(sprite)
            explosionSet.add(Sprite(sprite.get_position(), sprite.get_velocity(), 0, 0, explosion_image, explosion_info, explosion_sound))
    if removeSet:
        spriteGroup.difference_update(removeSet)
    return len(removeSet)

def megha_collider(group_one, group_two):
    removeSet = set()
    for sprite in group_one:
        if collider(group_two, sprite) > 0:
            removeSet.add(sprite)
    if removeSet:
        group_one.difference_update(removeSet)
    return len(removeSet)


'''========================= Ship class =============================='''

class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
        
        self.vel[0] *= .99
        self.vel[1] *= .99

    def thruster(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    
    def omega_plus(self):
        self.angle_vel += .05
    
    def omega_minus(self):
        self.angle_vel -= .05
    
    def shooter(self):
        global missile_group

        ''' initialize missile'''
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missileSet.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    

'''============================= Sprite class   ============================='''

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
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.age % self.lifespan * self.image_size[0],
                                           self.image_center[1]], self.image_size, self.pos, self.image_size)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    
    def update(self):
        ''' update angle'''
        self.angle += self.angle_vel
    
        ''' update position'''
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        ''' increment the age of the sprite'''
        if self.lifespan:
            if self.age > self.lifespan:
                return True
            else:  
                self.age += 1
        return False
    
    def get_position(self):
        return self.pos
    
    def get_velocity(self):
        return self.vel
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        return dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius()
    
    

'''=================== key handlers to control ship  =======================''' 


def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.omega_minus()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.omega_plus()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thruster(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shooter()

def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.omega_plus()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.omega_minus()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thruster(False)

''' mouseclick handlers '''
def clicker(pos):
    global score, lives, time, started

    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        ''' start new game'''
        score = 0
        lives = 3
        time = 0.5
        soundtrack.rewind()
        missile_sound.rewind()
        ship_thrust_sound.rewind()
        explosion_sound.rewind()
        soundtrack.play()
        started = True
        
'''====================== Draw ===================='''

def draw(canvas):
    global my_ship, best_score, score, lives, time, started, rock_group, explosion_group, missile_group
    
    ''' animiate background'''
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])
    
    ''' draw UI'''
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    
    ''' draw and update ship and sprites'''
    my_ship.draw(canvas)
    my_ship.update()
    sprite_holder(rockSet, canvas)
    sprite_holder(explosionSet, canvas)
    sprite_holder(missileSet, canvas)
    
    ''' ship - rocks collides'''
    numb_collide = collider(rockSet, my_ship)
    if numb_collide > 0:
        lives -= numb_collide
    if lives <= 0:
        ''' stop game'''
        if best_score < score:
            best_score = score
        started = False
        rock_group = set([])
        explosion_group = set([])
        missile_group = set([])
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
        my_ship.vel = [0, 0]
        my_ship.thrust = False
        my_ship.angle = 0
        my_ship.angle_vel = 0
        soundtrack.pause()
    
    ''' missiles - rocks collides'''
    score += megha_collider(missileSet, rockSet)

    ''' draw splash screen if not started'''
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

    label.set_text("Best score: " + str(best_score))
    

'''============== timer handler to spawns a rock ====================''' 

def rock_spawner():
    global rock_group
    
    # initialize rock
    if random.random() < 0.5:
        negative_h = -1
    else:
        negative_h = 1
    if random.random() < 0.5:
        negative_v = -1
    else:
        negative_v = 1
    rock_vel = [random.random() * .6 - .3 + score / 40 * negative_h, random.random() * .6 - .3 + score / 40 * negative_v]
    rock_avel = random.random() * .2 - .1
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    if started and len(rockSet) < 12 and dist(rock_pos, my_ship.get_position()) > 75:
        rockSet.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))

'''================= initialize stuff==========================='''
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

'''================== initialize ship========================================='''
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

'''===================== register handlers  ================'''
label = frame.add_label("Best score: ")
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(clicker)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

'''============= get things rolling================='''
timer.start()
frame.start()
'''=================<><><>================'''



