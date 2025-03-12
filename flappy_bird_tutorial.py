# What we need
# 1. We want a pipe
# 2. Multiple Birds
# 3. Ground

# Co-ordinates -> TOP-LEFT = 0,0
# i.e. moving up we need -ve velocity, and moving up takes +ve velocity
# Alo moving forward is +ve and moving backward is -ve


import pygame
import neat
import os
import random
import time

WIN_WIDTH = 600
WIN_HEIGHT = 800

# scale2x -> to double the size of the original size of the image
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))
    ]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 # Bird going up or down rotation
    ROT_VELO = 20 # How much do we rotate everytime we move the bird
    ANIMATION_TIME = 5 # How long we show each bird animation

    #Intial position of the bird
    def __init__(self, x ,y):
        self.x = x
        self.y = y
        self.tilt = 0 # Starting tilt of the bird
        self.vel = 0
        self.height = self.y
        self.img_count = 0 # To tell which image is being animated
        self. img = self.IMGS[0] # i.e. the birds1.jpg
        
    def jump(self):
        self.vel = -10.5 # Randome no. taken from expierience
        self.tick_count = 0 # When do we last jump, to calculate velocity and etc...
        self.height = self.y
        
    def move(self):
        self.tick_count +=1 # How many time we moved since last jump
        # S = ut + 1/2(at^2)     S is distance from the class 11 formulae
        # Initially, the velocity dominates, making the bird move upward.
        # As tick_count increases, the 1.5 * self.tick_count^2 term increases, causing the bird to slow down, stop, and then fall downward due to gravity.
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        if d>= 16:  # Terminal velocity i.e. the max. falling speed toward the gound 
            d = 16
        if d< 0: # if bord is moving up, make it move up faster
            d-=2
        self.y = self.y + d # d is the distance, but also has a role in the gravity dude also
        
        if d < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90: # to set the max. tilt down otherwise will rotate anit-clockwise till the user taps the jump
                self.tilt -= self.ROT_VEL
                
    def draw(self, win):
        """
        draw the bird
        :param win: pygame window or surface
        :return: None
        """
        self.img_count += 1
# +---------------------+----------------------------+
# |Frame (self.img_count) | Image Displayed          |
# +---------------------+----------------------------+
# | 1  →  5             | IMGS[0]                    |
# | 6  → 10             | IMGS[1]                    |
# | 11 → 15             | IMGS[2]                    |
# | 16 → 20             | IMGS[1]                    |
# | 21 → 21             | IMGS[0], then reset to 0   |
# +---------------------+----------------------------+

        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
            
# After this continue from here -> https://www.youtube.com/watch?v=ps55secj7iU&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2&index=2
# Do update Readme.md time to time