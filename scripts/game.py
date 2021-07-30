import pygame,math
import random as rd
from scripts.spriteSheets import *
pygame.init()

#ship class, bullet,space,star,planet

def ifCollideMask(mask,mask1,pos,pos1):
    dist = [int(pos[0]-pos1[0]),int(pos[1]-pos1[1])]
    if mask.overlap(mask1,dist):
        return True
    else:
        return False

class ufoBullet:
      def __init__(self,pos,angle):
          self.pos = pos
          self.radius = 6
          self.color = (255,255,255)
          self.angle = angle

          self.surf = pygame.Surface((self.radius*2,self.radius*2))
          self.surf.fill((0,0,0))
          self.surf.set_colorkey((0,0,0))
          pygame.draw.circle(self.surf,self.color,(self.radius,self.radius),self.radius)
          self.mask = pygame.mask.from_surface(self.surf)

          self.bulletSpeed = 3

          self.rect = pygame.Rect(self.pos[0],self.pos[1],self.radius*2,self.radius*2)

      def main(self,display):
          self.rect = pygame.Rect(self.pos[0],self.pos[1],self.radius*2,self.radius*2)
          
          self.pos[0] -= math.cos(self.angle)*self.bulletSpeed
          self.pos[1] -= math.sin(self.angle)*self.bulletSpeed

          pygame.draw.circle(display,self.color,self.pos,self.radius)

      def ifCollide(self,rect):
            if self.rect.colliderect(rect):
                  return True
            else:
                  return False

      def ifCollideMask(self,mask,pos):
            dist = [int(self.pos[0]-pos[0]),int(self.pos[1]-pos[1])]

            if self.mask.overlap(mask,dist):
                  return True
            else:
                  return False
          
class UFO():
    def __init__(self,pos,dispSize):
        self.dispSize = dispSize
        self.pos = pos
        self.dir = {'left':False,'right':False}
        if self.pos[0] <= -32:
            self.dir['right'] = True
        elif self.pos[0] >= self.dispSize[0]:
            self.dir['left'] = True
        self.speed = 5

        self.bullets = []
        
        self.bulletTimer = 80
        self.image = pygame.image.load('assets/images/UFO.png')
        self.image_size = self.image.get_size()
        self.image.set_colorkey((0,0,0))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(topleft=self.pos)

        #self.sheet = pygame.image.load('assets/images/UFO.png')
        #self.anim = 0
    def main(self,display,ship):

        if self.dir['left'] == True:
              self.pos[0] -= self.speed
        else:
              self.pos[0] += self.speed

        self.rect.topleft = self.pos
        display.blit(self.image,self.pos)

        #ship and UFO angle
        dist = [self.pos[0]-ship.rect.center[0],self.pos[1]-ship.rect.center[1]]
        bullAngle = math.atan2(dist[1],dist[0])
        angleChoice = [bullAngle, rd.randint(1,359)]
        self.bulletTimer += 1
        if self.bulletTimer >= 80:
            self.bulletTimer = 0
            self.bullets.append(ufoBullet([self.pos[0]+self.image_size[0]//2,self.pos[1]+self.image_size[1]//2],rd.choice(angleChoice)))

        for bull in self.bullets:
              bull.main(display)
      
    def ifCollide(self,rect):
        if self.rect.colliderect(rect):
            return True
        else:
            return False

class bigAstPiece():
    def __init__(self,pos,sheet,cellSize,mask):
        self.pos = pos
        
        self.sheet = spriteSheet(sheet,cellSize)
        for sh in self.sheet:
            sh.set_colorkey((0,0,0))
            
        self.rect = self.image.get_rect(topleft=self.pos)

        self.angle = rd.randrange(0,360)
    
        self.mask = pygame.mask.from_surface(self.sheet[0])
        
    def main(self,display,planetRect,planet):
        ast_vector = pygame.Vector2(self.rect.center)
        planet_vector = pygame.Vector2(planetRect.center)
            
        try:
            towards = (planet_vector - ast_vector).normalize() * 2

            self.pos[0] += towards[0]
            self.pos[1] += towards[1]
        except:
            pass

        display.blit(pygame.transform.rotate(self.image, self.angle), (55, 50)),(self.pos[0],self.pos[1])

class bigAsteroid():
    def __init__(self,pos,sheet,cellSize,mask):
        self.pos = pos
        
        self.sheet = spriteSheet(sheet,cellSize)
        for sh in self.sheet:
            sh.set_colorkey((0,0,0))
            
        self.rect = self.image.get_rect(topleft=self.pos)

        self.angle = rd.randrange(0,360)
    
        self.mask = pygame.mask.from_surface(self.sheet[0])

        self.atan = 0
        self.pieces = []

        self.visible = True

    def main(self,display,planetRect):
        if self.visible == True:
            dist = [self.rect.center[0]-planetRect.center[0],self.rect.center[1]-planetRect.center[1]]
            
            self.atan = math.atan2(dist[1],dist[0])
            self.pos[0] += math.cos(self.atan)
            self.pos[1] -= math.sin(self.atan)


            display.blit(pygame.transform.rotate(self.image, self.angle), (55, 50)),(self.pos[0],self.pos[1])

    def addPieces(self):
        self.pieces.append([self.pos[0]+math.cos(self.atan)*30,self.pos[1]-math.sin(self.atan)*30])
