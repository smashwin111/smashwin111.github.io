#Created by rcastro2

import math,sys
from pygame.locals import *
from math import *
from random import randint

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

black, white, light_gray, gray, dark_gray = (0,0,0), (255,255,255), (170,170,170), (128,128,128), (85,85,85)
red, green, blue = (255,0,0), (0,255,0), (0,0,255)
yellow, magenta, cyan = (255,255,0), (255,0,255), (0,255,255)
orange, pink, brown = (255,128,0), (255,0, 128), (102,51,0)
N,NE,E,SE,S,SW,W,NW,C = 0,1,2,3,4,5,6,7,8

class Mouse(object):
	def __init__(self):
		self.x, self.y, self.visible, self.width, self.height, self.name = 0, 0, True, 4, 4, "mouse"
		self.rect = pygame.Rect(self.x-2,self.y-2,4,4)
		self.LeftClick, self.LeftClickable, self.LeftButton = False, True, None
		self.RightClick, self.RightClickable, self.RightButton = False, True, None
		self.collisionBorder = None 


class KeyBoard(object):
	def __init__(self):
		self.Down, self.Up, self.Pressed = None, None, pygame.key.get_pressed()

keys = KeyBoard()
mouse = Mouse()

class Font(object):
    def __init__(self, color = white, size = 24, shadowColor = None, family = None):
        self.color, self.size, self.shadowColor = color, size, shadowColor

        if family != None and family[-3:] == "ttf":
                self.family = family              
        elif family != None:
                self.findFont(family)
        else:
                self.family = None
        
    def findFont(self,newFont):
        self.family = pygame.font.match_font(newFont)

class Game(object):
    def __init__(self,w,h,title,time=0):
        self.width,self.height = w,h
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode([w,h])
        self.fps, self.time, self.clock = 20, time + 1, pygame.time.Clock()
        self.left, self.top, self.right, self.bottom = 0,0,w,h
        self.debug = True
        self.collisionBorder = None
        self.over = False
        self.score = 0
        self.font = Font()
        

    def clearBackground(self,color=(0,0,0)):
        self.screen.fill(color)
        
    def setBackground(self,bkGraphics):
        self.background = bkGraphics
        self.backgroundXY = [[],[],[]]
        for r in range(3):
             for c in range(3):
                  self.backgroundXY[r].append({"x":self.width * (c-1) + self.width / 2,"y":self.height * (r-1) + self.height / 2})
                  #print(f'({r},{c})-{self.backgroundXY[r][c]}  \t',end='')
             #print('')

    def scrollBackground(self,direction,amt = 2):
        if direction == "left":
            for r in range(3):
                 for c in range(3):
                      self.backgroundXY[r][c]["x"] -= amt
                      if self.backgroundXY[r][c]["x"] + self.background.width  / 2 <= 0:
                           self.backgroundXY[r][c]["x"] = self.backgroundXY[r][(c+2)%3]["x"] + self.background.width - amt
                      self.background.moveTo(self.backgroundXY[r][c]["x"],self.backgroundXY[r][c]["y"])
        elif direction == "right":
             for r in range(3):
                 for c in [2,1,0]:
                      self.backgroundXY[r][c]["x"] += amt
                      if self.backgroundXY[r][c]["x"] - self.background.width  / 2 >= self.width:
                           self.backgroundXY[r][c]["x"] = self.backgroundXY[r][(c-2)%3]["x"] - self.background.width + amt
                      self.background.moveTo(self.backgroundXY[r][c]["x"],self.backgroundXY[r][c]["y"])
        elif direction == "up":
            for c in range(3):
                 for r in range(3):
                      self.backgroundXY[r][c]["y"] -= amt
                      if self.backgroundXY[r][c]["y"] + self.background.height  / 2 <= 0:
                           self.backgroundXY[r][c]["y"] = self.backgroundXY[(r+2)%3][c]["y"] + self.background.height - amt
                      self.background.moveTo(self.backgroundXY[r][c]["x"],self.backgroundXY[r][c]["y"])
        elif direction == "down":
            for c in range(3):
                 for r in range(2,-1,-1):
                      self.backgroundXY[r][c]["y"] += amt
                      if self.backgroundXY[r][c]["y"] - self.background.height  / 2 >= self.height:
                           self.backgroundXY[r][c]["y"] = self.backgroundXY[(r-2)%3][c]["y"] - self.background.height + amt
                      self.background.moveTo(self.backgroundXY[r][c]["x"],self.backgroundXY[r][c]["y"])
        elif direction == "still":
            for r in range(3):
                 for c in range(3):    
                      self.background.moveTo(self.backgroundXY[r][c]["x"],self.backgroundXY[r][c]["y"])
                      
    def drawText(self,msg,x,y,newFont = None):
        if newFont == None:
             newFont = self.font
        try:
             textfont = pygame.font.Font(newFont.family,newFont.size)
        except:
             textfont = pygame.font.Font(pygame.font.match_font("arial"),24)
             
        if newFont.shadowColor != None:
             text = textfont.render(str(msg),True,newFont.shadowColor)
             self.screen.blit(text,[x+1,y+1]) 
        text = textfont.render(str(msg),True,newFont.color)
        self.screen.blit(text,[x,y])

    def update(self,fps=1):
        self.fps = fps
        if self.time > 0:
            self.time -= 1/fps
        mouse.LeftClick = False
        mouse.RightClick = False
        if mouse.collisionBorder == "circle" or self.collisionBorder == "circle":
                pygame.draw.circle(self.screen,red,(int(mouse.x),int(mouse.y)),int((mouse.width/2+mouse.height/2)/2),1)
        elif mouse.collisionBorder == "rectangle" or self.collisionBorder == "rectangle":
                pygame.draw.rect(self.screen,red,mouse.rect,1)
                
        pygame.display.flip()
        self.clock.tick(fps)

    def processInput(self):
        self.keysPressed = pygame.key.get_pressed()
        keys.Pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.debug:
                     self.over = True
                else:
                     pygame.quit()
                     sys.exit(0)
                
            if event.type == pygame.KEYDOWN:
                keys.Down = event.key
            else:
                keys.Down = None

            if event.type == pygame.KEYUP:
                keys.Up = event.key
            else:
                keys.Up = None

            pos = pygame.mouse.get_pos()
            mouse.x, mouse.y = pos
            button = pygame.mouse.get_pressed()
            mouse.LeftButton = button[0]
            mouse.RightButton = button[2]
            
            if mouse.LeftClickable and mouse.LeftButton:
                    mouse.LeftClick = True
                    mouse.LeftClickable = False
            if not mouse.LeftClickable and not mouse.LeftButton:
                    mouse.LeftClickable = True
                    
            if mouse.RightClickable and mouse.RightButton:
                    mouse.RightClick = True
                    mouse.RightClickable = False
            if not mouse.RightClickable and not mouse.RightButton:
                    mouse.RightClickable = True
            
            mouse.rect = pygame.Rect(mouse.x-2,mouse.y-2,4,4)
        
            pygame.mouse.set_visible(mouse.visible)


    def wait(self,key):
        while True:
            self.processInput()
            if self.keysPressed[key]:
                return

    def quit(self):
        pygame.quit()

class GameObject(object):
    def __init__(self,game):
        self.game = game
        self.x, self.y, self.dx, self.dy, self.dxsign, self.dysign = self.game.width/2,self.game.height/2,0,0,1,1
        self.angle, self.da = 0,0
        self.rotate,self.rotate_angle, self.rda = "still",0,0
        self.rect = None
        self.speed = 0
        self.bounce = False
        self.collisionBorder = None
        self.visible = True
                

class Image(GameObject):
    def __init__(self,path,game,use_alpha=True):
        GameObject.__init__(self,game)
        if not isinstance(path, str):
                self.image = path
        else:
                if use_alpha:
                        self.image = pygame.image.load(path).convert_alpha()
                else:
                        self.image = pygame.image.load(path).convert()
                        trans_color = self.image.get_at((0,0))
                        self.image.set_colorkey(trans_color)
                        
        self.width,self.original_width,self.oldwidth = self.image.get_width(),self.image.get_width(),self.image.get_width()
        self.height, self.original_height,self.oldheight = self.image.get_height(), self.image.get_height(), self.image.get_height()
        self.original, self.src = self.image, self.image
        self.flipV,self.flipH, self.offsetX, self.offsetY = False,False,0,0
        self.updateRect()

    def draw(self):
        if self.visible:
            self.image = self.original
            if self.width != self.oldwidth or self.height != self.oldheight:
                self.resizeTo(self.width,self.height)
            if self.flipV or self.flipH:
                self.image = pygame.transform.flip(self.image,self.flipV,self.flipH)
            if self.rotate == "left" or self.rotate == "right" or self.rotate == "to":
                self.image = pygame.transform.rotate(self.image,self.rotate_angle * 180 / math.pi)
                self.width,self.height = self.image.get_width(),self.image.get_height()
                self.oldwidth,self.oldheight = self.width,self.height
            self.game.screen.blit(self.image, [self.x - self.width/2 + self.offsetX,self.y - self.height/2 + self.offsetY])

        self.updateRect()
        self.displayCollisionBorder()
         
class Animation(Image):
    def __init__(self,path,sequence,game, width = 0, height = 0,frate = 1,use_alpha=True):
        self.f, self.frate, self.ftick, self.loop, self.once = 0,frate,0,True,True
        self.game = game
        self.playAnim = True
        self.images = []
        self.source = []
        if width == 0 and height == 0:
            Image.__init__(self,path + "1.gif",game)
            for i in range(sequence):
                self.images.append(pygame.image.load(path + str(i+1) + ".gif").convert_alpha())
                self.source.append(self.images[i])
        else:
            if use_alpha:
                self.sheet = pygame.image.load(path).convert_alpha()
            else:
                self.sheet = pygame.image.load(path).convert()
                trans_color = self.sheet.get_at((0,0))
                self.sheet.set_colorkey(trans_color)
                
            tmp = self.sheet.subsurface((0,0,width,height))
            Image.__init__(self,tmp,game)
            self.frame_width, self.frame_height = width, height
            self.frame_rect = 0,0,width,height
            try:
                self.columns = self.sheet.get_width() / width
            except:
                print("Wrong size sheet")
            for i in range(sequence):
                frame_x = (i % self.columns) * self.frame_width
                frame_y = (i // self.columns) * self.frame_height
                rect = ( frame_x, frame_y, self.frame_width, self.frame_height )
                frame_image = self.sheet.subsurface(rect)
                self.images.append(frame_image)
                self.source.append(frame_image)
                
    def play(self):
        self.playAnim = True
        
    def stop(self):
        self.playAnim = False
        
    def nextFrame(self):
        self.ftick += 1
        if self.ftick % self.frate == 0:
             self.f += 1
             self.ftick = 0
        if self.f > len(self.images)-1:
            self.f = 0
        self.draw()
        
    def prevFrame(self):
        self.ftick += 1
        if self.ftick % self.frate == 0:
             self.f -= 1
             self.ftick = 0
        if self.f < 0:
            self.f = len(self.images)-1
        self.draw()
        
    def draw(self, loop = True):
        if self.visible:
            Image.setImage(self, self.images[self.f % len(self.images)])
            Image.draw(self)
            self.ftick += 1
            if self.ftick % self.frate == 0 and self.playAnim:
                self.f += 1
                self.ftick = 0
            if not loop and self.f == len(self.images)-1:
                self.visible = False
                self.f = 0
            if self.f > len(self.images)-1:
                self.f = 0
                self.ftick = 0
