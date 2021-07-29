import pygame,math
import random as rd

pygame.init()
#from scripts.game import *
#ship class, bullet,space,star,planet

class ufoBullet:
      def __init__(self,pos,angle):
          self.pos = pos
          self.radius = 4
          self.color = (255,255,255)
          self.angle = angle

          self.surf = pygame.Surface((self.radius*2,self.radius*2))
          self.surf.fill((0,0,0))
          self.surf.set_colorkey((0,0,0))
          pygame.draw.circle(self.surf,self.color,(self.radius,self.radius),self.radius)
          self.mask = pygame.mask.from_surface(self.surf)

          self.bulletSpeed = 5

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
        
        self.bulletTimer = 100
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
        self.bulletTimer += 1
        if self.bulletTimer >= 100:
            self.bulletTimer = 0
            self.bullets.append(ufoBullet([self.pos[0]+self.image_size[0]//2,self.pos[1]+self.image_size[1]//2],bullAngle))

        for bull in self.bullets:
              bull.main(display)
      
    def ifCollide(self,rect):
        if self.rect.colliderect(rect):
            return True
        else:
            return False
    
#ufo = UFO([rd.choice([-32,display_size[0]]),rd.randint(0,763)],display_size)
