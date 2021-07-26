import pygame, sys, math
import random as rd
from pygame.locals import *
from scripts.spriteSheets import *

pygame.init()

display = pygame.display.set_mode((800, 800))
display_size = display.get_size()
clock = pygame.time.Clock()

ship_img = pygame.image.load("assets/images/ship1.png").convert()
ship_img.set_colorkey((0,0,0))

asteroid_img = pygame.image.load("assets/images/ast.png").convert()
asteroid_img.set_colorkey((255,255,255))

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

          self.mask = pygame.mask.from_surface(self.planetImgs[0])
          
      def main(self,display):#main function(draw planet frames
          if self.planetAnim >= self.maxAnim:
              self.planetAnim = 0# animatoin loop
          self.planetAnim += 0.75
        
          display.blit(pygame.transform.scale(self.planetImgs[round(self.planetAnim)], (128, 128)),self.pos)
      def ifCollide(self,rect):
          #if planet rect collide with other rect
          if self.planetRect.colliderect(rect):
                return True
          else:
                return False

      
planetSheet = pygame.image.load('assets/images/planet.png').convert()
planetSheet.set_colorkey()
planetSize = [128,128]#planetFrameSize
mainPlanet = planet([display_size[0]//2-planetSize[0]//2,display_size[1]//2-planetSize[1]//2],planetSheet)#atribute0 - centering position, atribute1 - planet scpritesheet

class star:
      def __init__(self,pos,radius,color):
          self.pos = pos
          self.radius = radius
          self.color = color

      def draw(self,display):
          pygame.draw.circle(display,self.color,self.pos,self.radius)

class Asteroid:
      def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = None
            self.angle = rd.randrange(0,360)
      def main(self, display):

            display.blit(pygame.transform.scale(pygame.transform.rotate(asteroid_img, self.angle), (55, 50)), (self.x, self.y))
            #pygame.draw.rect(display, (255, 255, 255), (self.x, self.y, 50,50))
            self.rect = pygame.Rect(self.x, self.y, 55, 50)

            ast_vector = pygame.Vector2(self.rect.center)
            planet_vector = pygame.Vector2(planetRect.center)

            try:
                  towards = (planet_vector - ast_vector).normalize() * 2
            except:
                  pass

            self.x += towards[0]
            self.y += towards[1]



class space:#basic space generator
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

            self.centered = [0,0]

            self.hitbox = None

      def main(self, display):
            self.hitbox = pygame.Rect(self.x, self.y, 45, 45)
            self.x += self.speed[0]*self.speedIncrease
            self.y -= self.speed[1]*self.speedIncrease
            self.rect = ship_img.get_rect(topleft=(self.x,self.y))
            image = pygame.transform.rotate(ship_img, self.angle)

            self.centered = rotate(image,self.rect).topleft
            display.blit(image, self.centered)#rotate(image,self.rect) - rotate from center
   
#Would be cool if we add mask collision(pixel perfect), but for now rects
bullets = []
class bullet:
      def __init__(self,pos,angle):
          self.pos = pos
          self.radius = 5
          self.color = (255,255,255)
          self.angle = angle

          self.bulletSpeed = 5

          self.rect = pygame.Rect(self.pos[0],self.pos[1],self.radius*2,self.radius*2)

      def main(self,display):
          self.rect = pygame.Rect(self.pos[0],self.pos[1],self.radius*2,self.radius*2)
          
          self.pos[0] += math.cos(math.radians(self.angle))*self.bulletSpeed
          self.pos[1] -= math.sin(math.radians(self.angle))*self.bulletSpeed

          pygame.draw.circle(display,self.color,self.pos,self.radius)

shootTimer = 20

ship = Ship(300, 300)

asteroids = []

planetRect = pygame.Rect(display_size[0]//2-planetSize[0]//2,display_size[1]//2-planetSize[1]//2, 128, 128)

asteroid_spawn_cooldown = 0

rand_spawns = [[0, rd.randrange(0, 800)], [850, rd.randrange(0, 800)], [rd.randrange(0, 800), 850], [rd.randrange(0, 800), 0]]

while True:
      display.fill((0,0,0))
      
      spaceBG.draw(display)

      if shootTimer < 20:
            shootTimer += 1
      
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()

            if event.type == KEYDOWN:
                  if event.key == K_SPACE and shootTimer == 20:
                        shootPos = [ship.rect.center[0]+math.cos(math.radians(ship.angle))*(ship.size[0]//2),ship.rect.center[1]-math.sin(math.radians(ship.angle))*(ship.size[1]//2)]
                        bullets.append(bullet(shootPos,ship.angle))
                        shootTimer = 0

      if asteroid_spawn_cooldown == 0:
            choice = rd.choice(rand_spawns)
            asteroids.append(Asteroid(choice[0], choice[1]))
            rand_spawns = [[0, rd.randrange(0, 800)], [850, rd.randrange(0, 800)], [rd.randrange(0, 800), 850], [rd.randrange(0, 800), 0]]
            asteroid_spawn_cooldown = 75
      else:
            asteroid_spawn_cooldown -= 1

    
      mouse_x, mouse_y = pygame.mouse.get_pos()
      rel_x, rel_y = mouse_x - (ship.x+ship.size[0]//2), mouse_y - (ship.y+ship.size[1]//2)

      angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

      #mouse controlls
      mp = pygame.mouse.get_pos()#get mouse position
      mc = pygame.mouse.get_pressed()#get mouse press event

      mainPlanet.main(display)


      keys = pygame.key.get_pressed()
      if mc[0] == True:
            ship.speed[0] = math.cos(math.radians(angle))*5
            ship.speed[1] = math.sin(math.radians(angle))*5
            if ship.speedIncrease < 1.5:
                  ship.speedIncrease += 0.1
      else:
          if ship.speedIncrease > 0:
              ship.speedIncrease -= 0.005
          else:
              ship.speedIncrease = 0
              
      if mc[2] == True:
            ship.speed[0] = -math.cos(math.radians(angle))*3
            ship.speed[1] = -math.sin(math.radians(angle))*3
            if ship.speedIncrease < 1.5:
                  ship.speedIncrease += 0.1
      else:
          if ship.speedIncrease > 0:
              ship.speedIncrease -= 0.02
          else:
              ship.speedIncrease = 0
            
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


      for bull in bullets:
            bull.main(display)

      for asteroid in asteroids:
            asteroid.main(display)

            if asteroid.rect.colliderect(planetRect):
                  asteroids.remove(asteroid)
      #pygame.draw.circle(display,(255,0,0),,5)

      pygame.display.update()
      clock.tick(60)
