import pygame, sys, math
import random as rd
from pygame.locals import *
from scripts.spriteSheets import *

pygame.init()

display = pygame.display.set_mode((800, 800))
display_size = display.get_size()
clock = pygame.time.Clock()

ship_img = pygame.image.load("assets/images/ship1.png").convert()
ship_img.set_colorkey((255,255,255))

asteroid_imgs = spriteSheet(pygame.image.load("assets/images/asteroids.png").convert(),[100,100])
asteroidMasks = []
for astimg in asteroid_imgs:
      astimg.set_colorkey((255,255,255))
      asteroidMasks.append(pygame.mask.from_surface(astimg))

asteroid_bit_imgs_ = [pygame.image.load("assets/images/bit1.png"), pygame.image.load("assets/images/bit2.png"),
                     pygame.image.load("assets/images/bit3.png"), pygame.image.load("assets/images/bit4.png"),
                     pygame.image.load("assets/images/bit5.png")]

asteroid_bit_imgs = []

for img in asteroid_bit_imgs_:
      img.set_colorkey((255,255,255))
      img = pygame.transform.scale(img, (8,8))
      asteroid_bit_imgs.append(img)

fire_particles_ = [pygame.image.load("assets/images/fire_particle.png"), pygame.image.load("assets/images/fire_particle_1.png")
                   , pygame.image.load("assets/images/fire_particle_2.png")]

fire_particles = []

for img in fire_particles_:
      img.set_colorkey((255,255,255))
      img = pygame.transform.scale(img, (8,8))
      fire_particles.append(img)

            
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

          self.planetImgs[0].set_colorkey((0,0,0))
          self.mask = pygame.mask.from_surface(pygame.transform.scale(self.planetImgs[0],(128,128)))

          self.center = [800//2,800//2]
          
          self.boundTimer = 0
          self.maxBoundTimer = 20
          self.transparency = 0
          self.Bound = pygame.image.load('assets/images/bound.png')
          self.Bound.set_colorkey((255,255,255))
          
      def main(self,display):#main function(draw planet frames
          if self.planetAnim >= self.maxAnim:
              self.planetAnim = 0# animatoin loop
          self.planetAnim += 0.75
          
          display.blit(pygame.transform.scale(self.planetImgs[round(self.planetAnim)], (128, 128)),self.pos)
          #display.blit(self.mask.to_surface(),self.pos) #draw mask
      def ifCollide(self,rect):
          #if planet rect collide with other rect
          if self.planetRect.colliderect(rect):
                return True
          else:
                return False

      def ifCollideMask(self,mask,maskPos):
            distance = [int(maskPos[0]-self.pos[0]),int(maskPos[1]-self.pos[1])]#distance between two masks
            if self.mask.overlap(mask,distance):
                  return True
            else:
                  return False

      def drawBound(self,display):
            if self.boundTimer < self.maxBoundTimer//2:
                  self.transparency -= 20
            else:
                  self.transparency += 20
            bound = self.Bound.copy()
            bound.set_alpha(self.transparency)

            display.blit(bound,self.pos)
      
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
      def __init__(self, x, y, image,mask):
            self.x = x
            self.y = y
            self.rect = None
            self.angle = rd.randrange(0,360)

            self.image = image
            self.mask = mask #mask will help with pixel perfect collision
      def main(self, display):
            
            display.blit(pygame.transform.scale(pygame.transform.rotate(self.image, self.angle), (55, 50)), (self.x, self.y))
            self.mask = pygame.mask.from_surface(pygame.transform.scale(pygame.transform.rotate(self.image, self.angle), (55, 50)))
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

            self.mask = pygame.mask.from_surface(ship_img)

      def main(self, display):
            self.hitbox = pygame.Rect(self.x, self.y, 45, 45)
            self.x += self.speed[0]*self.speedIncrease
            self.y -= self.speed[1]*self.speedIncrease
            self.rect = ship_img.get_rect(topleft=(self.x,self.y))
            image = pygame.transform.rotate(ship_img, self.angle)

            self.centered = rotate(image,self.rect).topleft
            self.mask = pygame.mask.from_surface(image)
            display.blit(image, self.centered)#rotate(image,self.rect) - rotate from center
   
#Would be cool if we add mask collision(pixel perfect), but for now rects
bullets = []
class bullet:
      def __init__(self,pos,angle):
          self.pos = pos
          self.radius = 5
          self.color = (255,255,255)
          self.angle = angle


          self.surf = pygame.Surface((self.radius*2,self.radius*2))
          self.surf.fill((0,0,0))
          self.surf.set_colorkey((0,0,0))
          pygame.draw.circle(self.surf,(255,255,255),[self.radius,self.radius],self.radius)
                             
          self.mask = pygame.mask.from_surface(self.surf)

          self.bulletSpeed = 10

          self.rect = pygame.Rect(self.pos[0],self.pos[1],self.radius*2,self.radius*2)

      def main(self,display):
          self.rect = pygame.Rect(self.pos[0],self.pos[1],self.radius*2,self.radius*2)
          
          self.pos[0] += math.cos(math.radians(self.angle))*self.bulletSpeed
          self.pos[1] -= math.sin(math.radians(self.angle))*self.bulletSpeed

          pygame.draw.circle(display,self.color,self.pos,self.radius)

class particle(object):
    def __init__(self, x, y, x_vel, y_vel, radius, color, gravity_scale, images, lifetime):
        self.x = x 
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.gravity = 1
        self.radius = radius
        self.color = color
        self.lifetime = lifetime
        self.gravity_scale = gravity_scale
        self.img = rd.choice(images)

    def draw(self, display):
        self.lifetime -= 1
        self.gravity -= self.gravity_scale
        self.x += self.x_vel
        self.y += self.y_vel * self.gravity
        display.blit(self.img, (int(self.x), int(self.y)))
        #pygame.draw.circle(display, self.color, (int(self.x), int(self.y)), self.radius)

shootTimer = 20
ship = Ship(300, 300)
asteroids = []
planetRect = pygame.Rect(display_size[0]//2-planetSize[0]//2,display_size[1]//2-planetSize[1]//2, 128, 128)
asteroid_spawn_cooldown = 0
rand_spawns = [[0, rd.randrange(0, 800)], [850, rd.randrange(0, 800)], [rd.randrange(0, 800), 850], [rd.randrange(0, 800), 0]]
particles = []

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
            ImageIndex = rd.randint(0,len(asteroid_imgs)-1)
            choice = rd.choice(rand_spawns)
            asteroids.append(Asteroid(choice[0], choice[1],asteroid_imgs[ImageIndex],asteroidMasks[ImageIndex]))
            rand_spawns = [[0, rd.randrange(0, 800)], [850, rd.randrange(0, 800)], [rd.randrange(0, 800), 850], [rd.randrange(0, 800), 0]]
            asteroid_spawn_cooldown = 100
      else:
            asteroid_spawn_cooldown -= 1

      mouse_x, mouse_y = pygame.mouse.get_pos()
      rel_x, rel_y = mouse_x - (ship.x+ship.size[0]//2), mouse_y - (ship.y+ship.size[1]//2)

      angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

      #mouse controlls
      mp = pygame.mouse.get_pos()#get mouse position
      mc = pygame.mouse.get_pressed()#get mouse press event

      mainPlanet.main(display)
      if mainPlanet.boundTimer > 0:
            mainPlanet.drawBound(display)
            mainPlanet.boundTimer -= 1
            
      keys = pygame.key.get_pressed()
      #event check

      if mainPlanet.ifCollideMask(ship.mask,[ship.x,ship.y]):
            PlanetShipDist = [mainPlanet.center[0]-ship.centered[0],mainPlanet.center[1]-ship.centered[1]]
            ang = math.atan2(PlanetShipDist[1],PlanetShipDist[1])
            ship.speed[0] = -ship.speed[0]-math.cos(math.radians(ang))*10
            ship.speed[1] = -ship.speed[1]+math.sin(math.radians(ang))*10
            ship.speedIncrease = 0.7
            mainPlanet.boundTimer = mainPlanet.maxBoundTimer
            mainPlanet.transparency = 0
            
      elif mc[0] == True:
            particles.append(particle(ship.rect.center[0], ship.rect.center[1], rd.randrange(-3, 3), rd.randrange(-1, 1), 4, (163, 167, 194), 0, fire_particles, rd.randrange(20, 30)))
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
            
      #if keys[pygame.K_w]:
        #    ship.y -= 5
      #if keys[pygame.K_s]:
       #     ship.y += 5

      #if keys[pygame.K_a]:
       #     ship.x -= 5
      #if keys[pygame.K_d]:
       #     ship.x += 5

      #partincles
      for par in particles:
            if par.lifetime > 0:
                  par.draw(display)
            else:
                  particles.remove(par)

      ship.angle = angle
      ship.main(display)

      #bullets loop
      for bull in bullets:
            bull.main(display)
            try:
                  if bull.pos[0] < 0 or bull.pos[0] > display_size[0]:
                        bullets.pop(bullets.index(bull))

                  if bull.pos[1] < 0 or bull.pos[1] > display_size[1]:
                        bullets.pop(bullets.index(bull))

                  for ast in asteroids:
                        if ast.rect.colliderect(bull.rect):
                              for i in range(15):
                                 particles.append(particle(bull.pos[0], bull.pos[1], rd.randrange(-10, 10), rd.randrange(-10, 0), 4, (163, 167, 194), 0.1, asteroid_bit_imgs, 100))

                              asteroids.remove(ast)

                  if bull.rect.colliderect(planetRect):
                        if mainPlanet.ifCollideMask(bull.mask,(bull.pos[0],bull.pos[1])):
                              bullets.remove(bull)
            except:
                  pass

      #asteroids
      for asteroid in asteroids:
            asteroid.main(display)

            if asteroid.rect.colliderect(planetRect):
                  if mainPlanet.ifCollideMask(asteroid.mask,(asteroid.x,asteroid.y)):
                        asteroids.remove(asteroid)

      pygame.display.update()
      clock.tick(60)
