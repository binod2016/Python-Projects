# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
collide = False
collisions = 0
age = 0
explosion_group = set([])
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
asteroid_image2 = simplegui.load_image("https://dl.dropboxusercontent.com/u/17699684/asteroid_green.png")
asteroid_image3 = simplegui.load_image("https://dl.dropboxusercontent.com/u/17699684/asteroid_purple.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
explosion_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png")

# spaceship image
spaceship_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/17699684/spaceship_blue2.png")

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

def process_sprite_group(group, canvas):
    for item in set(group):
        if not item.update():
            item.update()
            item.draw(canvas)
        else:
            group.remove(item)
            
def group_group_collide(group1, group2):
    collisions = 0
    for item in set(group1):
        if group_collide(group2, item):
            group1.discard(item)
            collisions += 1
    return collisions

def group_collide(group, other_object):
    explosion_imgs = [explosion_image, explosion_image2, explosion_image3]
    collisions = 0
    for item in set(group):
        if item.collide(other_object):
            explosion_group.add(Sprite(item.pos, [-2, -1], 0, 0, random.choice(explosion_imgs), explosion_info, explosion_sound))
            group.remove(item)
            collisions += 1
    return collisions > 0

# Ship class
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

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))


# Sprite class
class Sprite:
    global lives
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
        global time
        if started == True and self.animated == False:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                self.pos, self.image_size, self.angle)
        if self.animated:
            center = [64, 64]
            center[0] = self.image_center[0] + self.image_size[0] * self.age
            canvas.draw_image(explosion_image, center, self.image_size,
                              self.pos, self.image_size, self.angle) 
            time += 1
#            
    def update(self):
        if lives > 0:
            # update angle
            self.angle += self.angle_vel

            # update position
            self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
            self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

            self.age += 1
            # check if spite age is past lifespan
            if self.age >= self.lifespan:
                return True
            else:
                return False
#        	return self.age >= self.lifespan
        
    def collide(self, other_object):
        self.other_object = other_object
        obj_dist = dist(self.pos, other_object.pos)
        if obj_dist <= self.radius + other_object.radius:
            return True
        else:
            return False

# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handler resets UI
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        my_ship.pos = [WIDTH // 2, HEIGHT // 2]
        soundtrack.rewind()
        soundtrack.play()

def draw(canvas):
    global time, started, lives, score, rock_group, my_ship
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    if group_collide(rock_group, my_ship):
        lives -= 1
        if lives <= 0:
            started = False
            rock_group = set([])
            collisions = 0
            age = 0
            soundtrack.pause()
            
    score += group_group_collide(rock_group, missile_group)
    
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "#E3C3FF", "serif")
    canvas.draw_text("Score", [680, 50], 22, "#E3C3FF", "serif")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    if lives <= 0:
        canvas.draw_text("Game Over", [288, 50], 46, "White", "serif") 
        canvas.draw_text("You scored " + str(score) + " points!",
                         [290, 84], 24, "White", "serif")
        canvas.draw_image(spaceship_image, [78, 36.5], [156, 73], (wtime + WIDTH / 3, HEIGHT / 2), (WIDTH, HEIGHT))
                          
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship and sprites
    my_ship.update()
    
    # draw splash screen if not started
    if not started or lives <= 0:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        

# timer handle spawns a rock    
def rock_spawner():
    global rock_group, rock, lives
    asteroid_imgs = [asteroid_image, asteroid_image2, asteroid_image3]  
    if started == True:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1
        # spawn rock only if not on top of ship
        rock_dist = dist(rock_pos, my_ship.pos)
        if not rock_dist <= (rock.radius + 25) + (my_ship.radius + 25):
            rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel,
                            random.choice(asteroid_imgs), asteroid_info))
            if score >= 25:
                rock.vel[0] += rock.vel[0] * 1.1
                rock.vel[1] += rock.vel[1] * 1.1
            if score >= 55:
                rock.vel[0] += rock.vel[0] * 2.1
                rock.vel[1] += rock.vel[1] * 2.1
                
        for rock in set(rock_group):
            if len(rock_group) >= 11:   
                rock_group.remove(rock)

# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
missile_group = set([])


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
label = frame.add_label('label')
label.set_text("************************ \
                You have 3 lives. Loose a life if you hit an asteroid...\n \
                mothership is watching!")

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()