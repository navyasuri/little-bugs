#CS FINAL PROJECT WORK
#by Berwin Gan (wqg203) and Navya Suri (ns3774)
# The objective of the game is to reach the golden box without touching the little bugs
# Score is increased as time passes. You get bonus scores for passing levels
# Friendly warning - the game is not Easy
# We hope you enjoy playing

import pygame
import sys
import random
import math, time


BLUE = (0, 0, 255)
DARK_BLUE = (0,0,240)
RED = (255, 0, 0)
DARK_RED = (240,0,0)
GREEN = (0, 255, 0)
DARK_GREEN = (0,240,0)


PURPLE = (255, 0, 255)
WHITE = (255,255,255)
BLACK = (0, 0, 0)


#global detect function

def detectcollision(x1,y1,w1,h1,x2,y2,w2,h2):
        if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2): 
            return True
        elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2): 
            return True
        elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2): 
            return True
        elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2): 
            return True
        else: 
            return False

#The class that defines the working of the Goal or the golden box
class Goal:
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.color = PURPLE
        self.width = 30
        self.height = 30
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)

    def display(self, screen):
        screen.blit(goalImage, (self.box.x, self.box.y))

    def win(self, level):
        print('you win')

# Donkey class defines the working of the doors from where the little bugs spawn
class Donkey:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = GREEN
        self.size = 30
        self.box = pygame.Rect(self.x, self.y, self.size, self.size)
    
    def display(self, screen):
        screen.blit(donkeyImage, (self.box.x, self.box.y))
    
# The Barrel Class defines the wokring of the little bugs including their movement and interaction
class Barrel:
    def __init__(self, donkey):
        self.x = donkey.box.left
        self.y = donkey.box.top
        self.velocity = 0
        self.falling = True
        self.onground = False
        self.xDir = 1
        self.width = 10
        self.height = 10
        self.color = PURPLE
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)
    
    
    def display(self, screen, e_count):
        pygame.draw.rect(screen, self.color, self.box)
        if self.xDir == 1:
            screen.blit(enemy_right[e_count], (self.box.x, self.box.y))
        else:
            screen.blit(enemy_left[e_count], (self.box.x, self.box.y))
            
            
    # The code for the movement of the little bugs is almost the same as movement of the main player
    
    def move(self, gravity, blocklist):
        if self.velocity <0:
            self.falling = True
        else:
            self.falling = False
            
        collision = False
        blockY= 0
        
        for i in blocklist:
            collision = detectcollision(self.x,self.y,self.width,self.height,i.xPos,i.yPos,i.width,i.height)
            if collision == False:
                self.onground == False
            if collision == True:
                blockY= i.yPos
                break
        
        if collision == True:
            if self.falling == True:
                self.falling = False
                self.onground = True
                self.velocity = 0
                self.y = blockY - self.height

        if collision == False:
            self.xDir = -self.xDir if random.randint(0, 5)==0 else self.xDir
            self.falling = True
            self.onground = False
            
    
        if self.onground == False:
            self.velocity += gravity    
            
        
        self.x+=self.xDir    
        self.y -= self.velocity
        self.box = pygame.Rect(self.x,self.y,self.height,self.width)

## this global is used for the gravity simulation in player
gravity = - 0.5

#The player class conmtains the main code for the movement and interaction of the player, including gravity simulation and interaction with the little bugs   
class Player:
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.color = BLUE
        self.width =width
        self.height = height
        self.velocity = 0
        self.falling = True
        self.onground = False
        self.box = pygame.Rect(self.x,self.y,self.width,self.height)
    
    def detectcollision(self,x1,y1,w1,h1,x2,y2,w2,h2):
        if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2): 
            return True
        elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2): 
            return True
        elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2): 
            return True
        elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2): 
            return True
        else: 
            return False
        
        
#interaction between player and other elements
#the self.falling and self.velocity is used to simulated an increasing gravity as time passes like in real life
    def update(self,gravity, blocklist,ladderlist):
        if self.velocity <0:
            self.falling = True
        else:
            self.falling = False
            
        collision = False
        blockY= 0
        
        for i in blocklist:
            collision = self.detectcollision(self.x,self.y,self.width,self.height,i.xPos,i.yPos,i.width,i.height)
            if collision == False:
                self.onground == False
            if collision == True:
                blockY= i.yPos
                break
        
        if collision == True:
            if self.falling == True:
                self.falling = False
                self.onground = True
                self.velocity = 0
                self.y = blockY - self.height
        
        
        if collision == False:
            self.falling = True
            self.onground = False
            
        
        
        for i in ladderlist:
            collision_ladder = self.detectcollision(self.x,self.y,self.width,self.height,i.x,i.y,i.width,i.height)
#            if collision_ladder and self.velocity<0: #falling from a jump 
            
            if collision_ladder and pygame.key.get_pressed()[pygame.K_UP]:
                self.y += -5  
                self.veloctiy = 0
                self. onground = True
            if collision_ladder and pygame.key.get_pressed()[pygame.K_DOWN]:
                self.y += 5
                self.veloctiy = 0
                self. onground = True
                
            
        if self.onground == False:
            self.velocity += gravity  
            
                
        
        self.y -= self.velocity
        self.box = pygame.Rect(self.x,self.y,self.width,self.height)
        
        
        
    def display(self,screen):
        self.box = pygame.Rect(self.x,self.y,self.width,self.height)    
        
    def jump(self, ladderList):
        for i in ladderList:
            collision_ladder = self.detectcollision(self.x,self.y,self.width,self.height,i.x,i.y,i.width,i.height)
            if collision_ladder:
                self.onground =True
                self.velocity = 0
                return 
            
        
        if self.onground ==False:
            return 
        self.velocity = 8
        self.onground = False
        
        
        

        

# The ledge class is used to create platforms on which the bugs and player moves. They are stationary    
class Ledge:
    def __init__(self, xPos, yPos, width=None):
        self.height =  30
        self.xPos = xPos
        self.yPos = yPos
        if width != None:
            self.width = width
        else:
            self.width = 40
        self.color = RED
        self.box = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        
    def display(self, screen):
        # pygame.draw.rect(screen, self.color, self.box)
        screen.blit(ledgeImage, (self.box.x, self.box.y))
    
# Used to make instances of ladder blocks
class Ladder:
    def __init__(self,x,y,width = None ,height = None):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = GREEN
        self.box = pygame.Rect(self.x,self.y,self.width,self.height)
    
    def display(self,screen):
        # pygame.draw.rect(screen,self.color,self.box)
        screen.blit(ladderImage, (self.box.x, self.box.y))
    


pygame.init()
            

screen = pygame.display.set_mode((1600, 800))
clock = pygame.time.Clock()

# The leftBorder and rightBorder rectangles prevent the player and the bugs from moving out of the screen
leftBorder = pygame.Rect(0, 0, 0, screen.get_height())
rightBorder = pygame.Rect(screen.get_width(), 0, 0, screen.get_height())
pygame.draw.rect(screen, (255,0,255), leftBorder)
pygame.draw.rect(screen, (0,0,0), rightBorder)


def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


#this button is used only for the Go event to start the gamne

def button(msg,x,y,width,height,ic,ac,size, action=None):
      a = None
      score =None
      lc = None
      mouse = pygame.mouse.get_pos()
      click = pygame.mouse.get_pressed()
      
        
      if x+width > mouse[0] >x and y+height >mouse[1] >y:
          pygame.draw.rect(screen,ac,(x,y,width,height))
          if click[0] == 1 and action != None:
              if action == 'play':
              	#the a (dead or win check), score and lc (lifecounter) is given a sperate storage in order to carry on 
                #into the next level while remaining in the same linear code
                #a will return 'a' if the player lifeCounter==0 and 'b' if player wins
              	#this 'a' is obtain form the actual_game() function called
                  a, score, lc = actual_game(screen,levelone,sprite_sheet,enemy_sprite,lifeCounter,levelCounter,scoreCounter)
                  if a!= 'a':
                      score +=500
                      lc+=3
                      a, score,lc = actual_game(screen,leveltwo,sprite_sheet,enemy_sprite,lc,levelCounter,score)
                  if a!= 'a':
                      lc+=3
                      score +=1000
                      a, score, lc = actual_game(screen,levelthree,sprite_sheet,enemy_sprite,lc,levelCounter,score)
           
      else:
          pygame.draw.rect(screen,ic,(x,y,width,height))
        
      smallText = pygame.font.Font('freesansbold.ttf',size)
      textSurf , textRect = text_objects(msg,smallText)
      textRect.center = (x+ (width/2),y + (height/2))
      screen.blit(textSurf,textRect)
      
      return a,score
     
  
def game_intro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        screen.blit(introbgImage, (0,0))
        largeText = pygame.font.Font('freesansbold.ttf',40)
        TextSurf, TextRect = text_objects('A CS101 Kinda Game With Tiny Bugs',largeText)
        TextRect.center = ((screen.get_width()/2),((screen.get_height()/2)-200))
        LextSurf, LextRect = text_objects("There are three levels, Don't hit the bugs",largeText)
        LextRect.center = ((screen.get_width()/2),((screen.get_height()/2)-120))
        PextSurf, PextRect = text_objects('Chocolate if you clear all levels!',largeText)
        PextRect.center = ((screen.get_width()/2),((screen.get_height()/2)-40))
        screen.blit(TextSurf, TextRect)
        screen.blit(LextSurf, LextRect)
        screen.blit(PextSurf, PextRect)
        
        a, score = button('Go!',(screen.get_width()/2)-150,(screen.get_height()/2)+200,300,70,DARK_GREEN,GREEN,50,'play')
        pygame.display.update()
        clock.tick(15)
        # a is only 'a' or 'b' if you died or win
        if a:
            break
        
    game_result(a,score)
        
#called in the game_inro() after the button which contains the actual_game() is done 

def game_result(a,score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(introbgImage, (0,0))
        largeText = pygame.font.Font('freesansbold.ttf',40)
        if a == 'a':
            
            TextSurf, TextRect = text_objects('You Died my friend',largeText)
            TextRect.center = ((screen.get_width()/2),((screen.get_height()/2)-200))
            screen.blit(TextSurf, TextRect)
        else:
            TextSurf, TextRect = text_objects('You are a winner !',largeText)
            TextRect.center = ((screen.get_width()/2),((screen.get_height()/2)-200))
            screen.blit(TextSurf, TextRect)
            
        LextSurf, LextRect = text_objects('Score:'+ str(score),largeText)
        LextRect.center = ((screen.get_width()/2),((screen.get_height()/2)+200))
        
        screen.blit(TextSurf, TextRect)
        screen.blit(LextSurf, LextRect)
        
        pygame.display.update()
        clock.tick(15)
             
#Level defintons are in the form of matrices which are read in a function and then the corresponding objects are displayed on the screen.            
    
leveltwo =[
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'D',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,'G',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,2],
    [0,0,0,0,'F',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [0,0,1,2,1,1,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,2],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'E',0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [0,0,0,1,1,1,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,1,1,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,2,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,'P',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

]


levelthree = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'F',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'G',0,0,0,0,0,0,0],
    [0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,'E',0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0],
    [0,0,0,0,1,2,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,2,1,0,0],
    [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0],
    [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'D',0,2,0,0,0],
    [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0],
    [0,1,1,2,1,1,1,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'P',0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

]

levelone = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,'D',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'E',0,0,0,0,0,0,0,0,0,0,0,2,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,'G',0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,2,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'F',0,0,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,1,2,1,1,1,1,1,0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'P',0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

]

    

#A general class that allows us to get a specific part of the image from a larger spritesheet
class SpriteSheet():
    
    sprite_sheet = None

    def __init__(self, file):
        
        self.sprite_sheet = pygame.image.load(file)
        
    def getImage(self, xPos, yPos, width, height):
        
        img = pygame.Surface([width, height]).convert()
        
        img.blit(self.sprite_sheet, (0,0), (xPos, yPos, width, height))
        
        img.set_colorkey(BLACK)
        
        return img


sprite_sheet = SpriteSheet('download.png')
enemy_sprite = SpriteSheet('enemySprites.png')
platform_sprite = SpriteSheet('platforms.png')
bg_sprite = SpriteSheet('bg1.png')
intro_bg_sprite = SpriteSheet('introbg.png')

ladderImage = platform_sprite.getImage(280, 80, 40, 40)
ledgeImage = platform_sprite.getImage(120, 0, 40, 40)
bgImg = bg_sprite.getImage(0, 0, 1600, 800)
donkeyImage = platform_sprite.getImage(40, 0, 40, 40)
goalImage = platform_sprite.getImage(0, 400, 40, 40)
introbgImage = intro_bg_sprite.getImage(0, 0, 1600, 800)

move_left = []
move_right = []
enemy_left = []
enemy_right = []
for x in range(2):
    img = enemy_sprite.getImage((x*40)+8, 0, 16, 16)
    enemy_left.append(img)

for x in range(2, 4):
    img = enemy_sprite.getImage((x*40)+8, 0, 16, 16)
    enemy_right.append(img)

for x in range(9):
    img = sprite_sheet.getImage((x*64)+14, 9*64, 64-30, 64)
    move_left.append(img)
for x in range(9):
    img = sprite_sheet.getImage((x*64)+14, 11*64, 64-30, 64)
    move_right.append(img)

lifeCounter = 3
levelCounter = 1
scoreCounter = 0

#called by the button in game_intro()
def actual_game(screen,level,sprite_sheet,enemy_sprite,lifeCounter,levelCounter,scoreCounter):
      
    ledgeList = []
    ladderList=[]
    
    #The levels are read using the below lines of code
    
    for y in range(0,len(level)):
        for x in range(0,len(level[y])):
            if level[y][x] == 1:
                ledgeList.append(Ledge(x*40,y*40))
            elif level[y][x] == 2:
                ladderList.append(Ladder(x*40,y*40))
            elif level[y][x] == 'D':
                donkey1 = Donkey(x*40,y*40)
            elif level[y][x] == 'E':
                donkey2 = Donkey(x*40,y*40)
            elif level[y][x] == 'F':
                donkey3 = Donkey(x*40,y*40)
            elif level[y][x] == 'P':
                start_x =x*40
                start_y =y*40
                player = Player(x*40,y*40,34,64)
                
            elif level[y][x] == 'G':
                goal = Goal(x*40, y*40)
                
            
    image = move_right[0]

    
    barrelList = []
    then = time.time()
    sThen = time.time()

		#The variables below are used to give a lag between the images displayed of the player and the bugs
    e_counter = 0
    counter = 0
    
    #The main game loop!
    while True:
        
        if counter==44:
            counter = 0
        else:
            counter += 1
    
        count = counter//5

        if e_counter == 9:
            e_counter = 0
        else:
            e_counter+=1
        e_count = e_counter//5
    
        screen.fill(0)
        screen.blit(bgImg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump(ladderList)
                
        goal.display(screen)

        rn = time.time()
        if rn - sThen> 4:
            scoreCounter += 10
            sThen = rn
        

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            player.x += 3
            image = move_right[count]

        if pygame.key.get_pressed()[pygame.K_LEFT]:    
            player.x -=3
            image = move_left[count]

        if player.box.colliderect(leftBorder):
            player.x+=3
        if player.box.colliderect(rightBorder):
            player.x-=3

        for i in ledgeList:
            i.display(screen)

        for i in ladderList:
            i.display(screen)
    
        player.update(gravity,ledgeList,ladderList)        
        player.display(screen)

    
        donkey1.display(screen) 
        donkey2.display(screen) 
        donkey3.display(screen) 
        now = time.time()   
        
        #The if condidtion below makes the bugs spawn every 4 seconds 
        if now - then >4:
            then = now
            now = time.time()
            barrelList.append(Barrel(donkey1))
            barrelList.append(Barrel(donkey2))
            barrelList.append(Barrel(donkey3))
            
        for i in barrelList:
            i.display(screen, e_count) 
            i.move(gravity, ledgeList)
            if i.box.colliderect(leftBorder) or i.box.colliderect(rightBorder):
                i.xDir = -i.xDir
            if i.box.colliderect(player.box):
                print('ded')
                lifeCounter -=1
                player.x = start_x
                player.y = start_y
                if lifeCounter == 0:
                    return 'a', scoreCounter, 0
                

        if player.box.colliderect(goal.box):
            return 'b', scoreCounter, lifeCounter
       
        screen.blit(image, (player.box.x, player.box.y))
                     
        clock.tick(200)
        button('Life'+'='+str(lifeCounter),1450,30,50,50,DARK_GREEN,GREEN,15)
        button('Score' + '=' +str(scoreCounter),1500,30,90,50,RED,DARK_RED,15)
        
	#The if condidtion below makes sure that at any given time, there are only 25 bugs on the screen 
        if len(barrelList)>25:
            newBarrels = barrelList[len(barrelList)-25:]
            barrelList = newBarrels

        pygame.display.update()
        
#the actual game function which is called by python, in it there is a while loop which contains a button in which if 
#pressed will called the actual_game() level by level, at the end, the game_result() is used to show the score
game_intro()  