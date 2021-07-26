import pygame, sys, math
import random as rd
from pygame.locals import *
from scripts.spriteSheets import *

pygame.init()

display = pygame.display.set_mode((800, 800))

clock = pygame.time.Clock()

ship_img = pygame.image.load("ship.png").convert()
ship_img.set_colorkey((255,255,255))

def rotate(rotatedImage, rect):
      rect = rotatedImage.get_rect(center=rect.center)
      return rect

class planet():
      def __init__(self,pos,planetImage):#
          self.pos = pos#init pos
          self.planetImgs = spriteSheet(planetImage,(200,200))#slice planet spritesheet planet generated with planet generator: https://deep-fold.itch.io/pixel-planet-generator
          self.planetRect = self.planetImgs[0].get_rect(topleft=self.pos)# get rect from image
          self.planetAnim = 0
          self.maxAnim = 198

      def main(self,display):#main function(draw planet frames
          if self.planetAnim >= self.maxAnim:
              self.planetAnim = 0# animatoin loop
          self.planetAnim += 0.75
        
          display.blit(self.planetImgs[round(self.planetAnim)],self.pos)
      def ifCollide(self,rect):
          if self.planetRect.colliderect(rect):
                return True
          else:
                return False

planetSheet = pygame.image.load('planet.png').convert()
planetSheet.set_colorkey()
planetSize = [200,200]#planetFrameSize
mainPlanet = planet([display.get_width()//2-planetSize[0]//2,display.get_height()//2-planetSize[1]//2],planetSheet)#atribute0 - centering position, atribute1 - planet scpritesheet

class star():
      def __init__(self,pos,radius,color):
          self.pos = pos
          self.radius = radius
          self.color = color

      def draw(self,display):
          pygame.draw.circle(display,self.color,self.pos,self.radius)

class space():#basic space generator
      def __init__(self,starNum):
          self.stars = []
          self.colors = [(255,255,255),(192,192,192),(128,128,128),(255, 184, 69),(251, 121, 116),(249, 118, 152),(163, 72, 166)]
          for st in range(starNum):
              #append star
              self.stars.append(star([rd.randint(0,800),rd.randint(0,800)],rd.randint(1,5),rd.choice(self.colors)))

      def draw(self,display):
          for st in self.stars:
              st.draw(display)#draw stars

spaceBG = space(30)

class Ship:
      def __init__(self, x, y):
            self.x = x
            self.y = y
            self.size = ship_img.get_size()
            self.angle = 0

            self.rect = ship_img.get_rect(topleft=(self.x,self.y))

            self.speed = [0,0]
            self.speedIncrease = 1.0

      def main(self, display):
            
            self.rect = ship_img.get_rect(topleft=(self.x,self.y))
            image = pygame.transform.rotate(ship_img, self.angle)
            display.blit(image, rotate(image,self.rect).topleft)#rotate(image,self.rect) - rotate from center
            

ship = Ship(300, 300)

while True:
      display.fill((0,0,0))
      
      spaceBG.draw(display)
      
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()
    
      mouse_x, mouse_y = pygame.mouse.get_pos()
      rel_x, rel_y = mouse_x - (ship.x+ship.size[0]//2), mouse_y - (ship.y+ship.size[1]//2)

      angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

      #mouse controlls
      mp = pygame.mouse.get_pos()#get mouse position
      mc = pygame.mouse.get_pressed()#get mouse press event

      mainPlanet.main(display)


      keys = pygame.key.get_pressed()
      if mc[0] == True:
            ship.y -= math.sin(math.radians(angle))*5
            ship.x += math.cos(math.radians(angle))*5
      elif mc[2] == True:
            ship.y += math.sin(math.radians(angle))*5
            ship.x -= math.cos(math.radians(angle))*5
            
      if keys[pygame.K_w]:
            ship.y -= 5
      if keys[pygame.K_s]:
            ship.y += 5

      if keys[pygame.K_a]:
            ship.x -= 5
      if keys[pygame.K_d]:
            ship.x += 5

      ship.angle = angle
      ship.main(display)

      pygame.display.update()
      clock.tick(60)
