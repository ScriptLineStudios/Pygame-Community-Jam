import pygame, sys, math
import random as rd
from pygame.locals import *
from scripts.spriteSheets import *
from scripts.game import *
from scripts.UI import *
import time
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

display = pygame.display.set_mode((800, 800))
display_size = display.get_size()
clock = pygame.time.Clock()

pygame.display.set_caption("Asteroids!")

cursor_imgs = [pygame.image.load("assets/images/cursor.png"), pygame.image.load("assets/images/cursor1.png")]

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
      img = pygame.transform.scale(img, (14,14))
      img.set_colorkey((255,255,255))
      asteroid_bit_imgs.append(img)

fire_particles_ = [pygame.image.load("assets/images/fire_particle.png"), pygame.image.load("assets/images/fire_particle_1.png")
                   , pygame.image.load("assets/images/fire_particle_2.png")]

fire_particles = []

for img in fire_particles_:
      img.set_colorkey((255,255,255))
      img = pygame.transform.scale(img, (8,8))
      fire_particles.append(img)

earth_particles_ = [pygame.image.load("assets/images/planet_particle.png"), pygame.image.load("assets/images/planet_particle_1.png")
                   , pygame.image.load("assets/images/planet_particle_2.png")]

earth_particles = []

for img in earth_particles_:
      img.set_colorkey((255,255,255))
      img = pygame.transform.scale(img, (8,8))
      earth_particles.append(img)

ufo_particles_ = [pygame.image.load("assets/images/ufo_particle.png"), pygame.image.load("assets/images/ufo_particle_1.png")
                   , pygame.image.load("assets/images/ufo_particle_2.png")]
ufo_particles = []
for img in ufo_particles_:
      img.set_colorkey((255,255,255))
      img = pygame.transform.scale(img, (8,8))
      ufo_particles.append(img)

ship_particles_ = [pygame.image.load("assets/images/ship_particle.png"), pygame.image.load("assets/images/ship_particle_1.png")
                   , pygame.image.load("assets/images/ship_particle_2.png")]
ship_particles = []
for img in ship_particles_:
      img.set_colorkey((255,255,255))
      img = pygame.transform.scale(img, (8,8))
      ship_particles.append(img)

pygame.mixer.music.load("assets/GamePlay.mp3")

game_over_sound = pygame.mixer.Sound("assets/GameOver.wav")

asteroid_sound_effects = [pygame.mixer.Sound("assets/Soundeffects/Space-SFX-DestroyAsteroid1.wav"),
                          pygame.mixer.Sound("assets/Soundeffects/Space-SFX-DestroyAsteroid2.wav")
                          ,pygame.mixer.Sound("assets/Soundeffects/Space-SFX-DestroyAsteroid3.wav")]

for asteroid_sound in asteroid_sound_effects:
      asteroid_sound.set_volume(0.5)

player_sound_effects = [pygame.mixer.Sound("assets/Soundeffects/Space-SFX-Shoot1.wav"),
                          pygame.mixer.Sound("assets/Soundeffects/Space-SFX-Shoot2.mp3")]

for player_sound in player_sound_effects:
      player_sound.set_volume(0.5)

player_jet_sound = pygame.mixer.Sound("assets/Soundeffects/jetsound.wav")
player_jet_sound.set_volume(0.1)
            
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


#Init menu
mainMen = mainMenu(display_size)
transit = cubeTrans(display,display,display_size)
startTrans = False


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

                  self.x += towards[0]
                  self.y += towards[1]
            except:
                  pass




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
   
bullets = []
class bullet:
      def __init__(self,pos,angle, rot_img_angle):
          self.pos = pos
          self.radius = 5
          self.color = (95,255,66)
          self.angle = angle
          self.bullet_image = None
          self.img = pygame.image.load("assets/images/bullet.png")


          self.surf = pygame.Surface((self.radius*2,self.radius*2))
          self.surf.fill((0,0,0))
          self.surf.set_colorkey((0,0,0))
          pygame.draw.circle(self.surf,(255,255,255),[self.radius,self.radius],self.radius)
                             
          self.mask = pygame.mask.from_surface(self.surf)

          self.bulletSpeed = 10

          self.rect = pygame.Rect(self.pos[0],self.pos[1],self.radius*2,self.radius*2)

          self.rot_img_angle = rot_img_angle

      def main(self,display):
          self.rect = pygame.Rect(self.pos[0],self.pos[1],self.radius*2,self.radius*2)
          
          self.pos[0] += math.cos(math.radians(self.angle))*self.bulletSpeed
          self.pos[1] -= math.sin(math.radians(self.angle))*self.bulletSpeed
          
          self.first_loop = False

          #Wanted to swap circles for rotating rect but couldnt get rotations working
          self.bullet_image = pygame.transform.rotate(self.img, self.rot_img_angle)
          display.blit(self.bullet_image, self.pos)

          #pygame.draw.circle(display,self.color,self.pos,self.radius)

      def ifCollideMask(self,mask,pos):
            dist = [int(self.pos[0]-pos[0]),int(self.pos[1]-pos[1])]

            if self.mask.overlap(mask,dist):
                  return True
            else:
                  return False
class particle(object):
    def __init__(self, x, y, x_vel, y_vel, radius, color, gravity_scale, images, lifetime, must_decrease_size):
        self.x = x 
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.gravity = 1
        self.radius = radius
        self.color = color
        self.lifetime = lifetime
        self.gravity_scale = gravity_scale
        self.must_decrease_size = must_decrease_size
        try:
              self.img = rd.choice(images)
        except:
              pass
        self.size = 16
        self.size_cooldown = 0

    def draw(self, display):
        self.lifetime -= 1
        self.gravity -= self.gravity_scale
        self.x += self.x_vel
        self.y += self.y_vel * self.gravity
        try:
              if self.must_decrease_size:
                    display.blit(pygame.transform.scale(self.img, (self.size, self.size)), (int(self.x), int(self.y)))
                    if self.size > 0:
                          if self.size_cooldown == 0:
                                self.size -= 1
                                self.size_cooldown = 2
                          else:
                                self.size_cooldown -= 1
              else:
                    display.blit(self.img, (int(self.x), int(self.y)))
        except:
           pygame.draw.circle(display, self.color, (int(self.x), int(self.y)), self.radius)

shootTimer = 20
ship = Ship(300, 300)
asteroids = []
planetRect = pygame.Rect(display_size[0]//2-planetSize[0]//2,display_size[1]//2-planetSize[1]//2, 128, 128)
asteroid_spawn_cooldown = 0
rand_spawns = [[0, rd.randrange(0, 800)], [850, rd.randrange(0, 800)], [rd.randrange(0, 800), 850], [rd.randrange(0, 800), 0]]
particles = []


font = pygame.font.Font('assets/font/Laser_1.otf', 64)
text = font.render('Score: 0', True, (255,255,255))
scoretextRect = text.get_rect()
scoretextRect.center = (180, 40)

font_large = pygame.font.Font('assets/font/Laser_1.otf', 80)



game_over_text = font_large.render('Game Over!', True, (255,255,255))
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (400, 350)

final_score_text = font_large.render('Score: ', False, (255,255,255))
final_score_text_rect = final_score_text.get_rect()
final_score_text_rect.center = (325, 410)

font_large_menu = pygame.font.Font('assets/font/menu.ttf', 40)
font_small_menu = pygame.font.Font('assets/font/menu.ttf', 30)

score = 0

circles = []

game_stop = True
game_over = False

difficulty = 110

difficulty_increases = [False, False, False, False, False]
#The difficulty will increase when the score reaches these numbers
difficulty_figures = [10, 20, 30, 40, 50]
difficulty_index = 0


UFO_timer = 300
UFOs = []

has_loaded_game_music = False
has_loaded_menu_music = False

how_to_play_menu = False

text_to_render = [["Watch Out!"], ["You planet is being"],
                  ["attacked by Asteroids!"], [" "], [" "],["Hold left mouse"],
                  ["in the direction you"], ["would like to move"], [" "], [" "],
                  ["Press space to shoot"], [" "], [" "], ["Avoid UFOs at all cost!"], [" "], [" "],
                  ["ENTER: Return to Menu"]]
text_list = []

for i, text in enumerate(text_to_render):
      text_to_append = font_small_menu.render(text[0], True, (255,255,255))
      textRect = text_to_append.get_rect()
      textRect.center = (400, 200+i*30)
      text_list.append([text_to_append, textRect])

print(text_list)

in_game = False

while True:
      pygame.mouse.set_visible(False)
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
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        rel_x, rel_y = mouse_x - ship.x, mouse_y - ship.y
                        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
                        sound = rd.choice(player_sound_effects)
                        sound.play()
                        shootPos = [ship.rect.center[0]+math.cos(math.radians(ship.angle))*(ship.size[0]//2),ship.rect.center[1]-math.sin(math.radians(ship.angle))*(ship.size[1]//2)]
                        bullets.append(bullet(shootPos,ship.angle, angle))
                        circles.append([shootPos[0],shootPos[1], 10, 3, (0, 155, 0)])
                        #particles.append(particle(shootPos[0], shootPos[1], rd.randrange(-10, 10), rd.randrange(-10, 0), 4, (0, 255, 0), rd.random()/2, None, 100))

                        shootTimer = 0

                  if event.key == K_RETURN:
                        if game_over:
                              pygame.mixer.Sound.stop(game_over_sound)
                              pygame.mixer.music.play(-1)
                              score = 0
                              asteroids = []
                              game_over = False
                              difficulty = 100
                              difficulty_increases = [False, False, False]
                              difficulty_figures = [10, 20, 30]
                              difficulty_index = 0
                        
                  if event.key == K_SPACE:
                        startTrans = True

                  if event.key == K_RETURN and not in_game:
                        how_to_play_menu = not how_to_play_menu
                        
      if asteroid_spawn_cooldown == 0:
            if not game_over:
                  if game_stop == False:
                        ImageIndex = rd.randint(0,len(asteroid_imgs)-1)
                        choice = rd.choice(rand_spawns)
                        asteroids.append(Asteroid(choice[0], choice[1],asteroid_imgs[ImageIndex],asteroidMasks[ImageIndex]))
                        rand_spawns = [[0, rd.randrange(0, 800)], [850, rd.randrange(0, 800)], [rd.randrange(0, 800), 850], [rd.randrange(0, 800), 0]]
                        asteroid_spawn_cooldown = difficulty
      else:
            asteroid_spawn_cooldown -= 1

      if difficulty_index < len(difficulty_figures):
            if score == difficulty_figures[difficulty_index] and difficulty_increases[difficulty_index] == False:
                  difficulty -= 10
                  difficulty_increases[difficulty_index] = True
                  print(difficulty_increases)

                  difficulty_index += 1
                  print(difficulty_index)

      mouse_x, mouse_y = pygame.mouse.get_pos()
      rel_x, rel_y = mouse_x - (ship.x+ship.size[0]//2), mouse_y - (ship.y+ship.size[1]//2)

      angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

      #mouse controlls
      mp = pygame.mouse.get_pos()#get mouse position
      mc = pygame.mouse.get_pressed()#get mouse press event

      if not game_over:

            mainPlanet.main(display)
            if mainPlanet.boundTimer > 0:
                  mainPlanet.drawBound(display)
                  mainPlanet.boundTimer -= 1

            if mainPlanet.ifCollideMask(ship.mask,[ship.x,ship.y]):
                  PlanetShipDist = [mainPlanet.center[0]-ship.rect.center[0],mainPlanet.center[1]-ship.rect.center[1]]#distance between planet center and ship center
                  ang = math.atan2(PlanetShipDist[1],PlanetShipDist[1])#getting angle from hypotenuse
                        
                  ship.speed[0] = -ship.speed[0]-math.cos(ang)*10#reject ship from planet
                  ship.speed[1] = -ship.speed[1]+math.sin(ang)*10#
                  ship.speedIncrease = 0.7
                  mainPlanet.boundTimer = mainPlanet.maxBoundTimer
                  mainPlanet.transparency = 0
            
      keys = pygame.key.get_pressed()
      #event check

      mouse_x, mouse_y = pygame.mouse.get_pos()
      
      if mc[0] == True and mainPlanet.boundTimer == 0:
            display.blit(cursor_imgs[1], (mouse_x, mouse_y))
            player_jet_sound.play()
            for x in range(2):
             particles.append(particle(ship.rect.center[0], ship.rect.center[1], rd.randrange(-3, 3), rd.randrange(-1, 1), 4, (163, 167, 194), 0, fire_particles, rd.randrange(20, 100), True))
            ship.speed[0] = math.cos(math.radians(angle))*5
            ship.speed[1] = math.sin(math.radians(angle))*5
            if ship.speedIncrease < 1.5:
                  ship.speedIncrease += 0.1
      else:
          display.blit(cursor_imgs[0], (mouse_x, mouse_y))
          player_jet_sound.stop()
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

      #particles
      for par in particles:
            if par.lifetime > 0:
                  par.draw(display)
            else:
                  particles.remove(par)

      for circle in circles:
        circle[2] += 8
        if circle[2] > 30:
            circle[3] -= 1
        if circle[3] > 0:
            pygame.draw.circle(display, circle[4], (circle[0], circle[1]), circle[2], circle[3])

      ship.angle = angle

      if not game_over:
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
      
                              circles.append([ast.rect.center[0]+rd.randrange(-30, 30), ast.rect.center[1]+rd.randrange(-30, 30), 10, 12, (163, 167, 194)])

                              score += 1
                              for i in range(rd.randrange(30, 60)):
                                 particles.append(particle(bull.pos[0], bull.pos[1], rd.randrange(-10, 10), rd.randrange(-10, 0), 4, (163, 167, 194), rd.random()/2, asteroid_bit_imgs, 100, False))

                              sound = rd.choice(asteroid_sound_effects)
                              sound.play()
                              asteroids.remove(ast)
                              bullets.remove(bull)

                  if bull.rect.colliderect(planetRect):
                        if mainPlanet.ifCollideMask(bull.mask,(bull.pos[0],bull.pos[1])):
                              bullets.remove(bull)
            except Exception as e:
                  pass

      #asteroids
      for asteroid in asteroids:
            asteroid.main(display)
            #particles.append(particle(asteroid.rect.center[0], asteroid.rect.center[1], rd.randrange(-3, 3), rd.randrange(-1, 1), 4, (163, 167, 194), 0, fire_particles, 50))
            if asteroid.rect.colliderect(planetRect):
                  if mainPlanet.ifCollideMask(asteroid.mask,(asteroid.x,asteroid.y)):
                              asteroids = []
                              ufos = []
                              #game_over_sound.play()
                              pygame.mixer.music.fadeout(1000)
                              pygame.mixer.music.stop()

                              for x in range(5):
                                circles.append([mainPlanet.planetRect.center[0]+rd.randrange(-40, 40), mainPlanet.planetRect.center[1]+rd.randrange(-40, 40), 25, 12, (99, 171, 163)])

                              for i in range(50):
                                    particles.append(particle(mainPlanet.pos[0], mainPlanet.pos[1], rd.randrange(-20, 20), rd.randrange(-10, 0), 4, (163, 167, 194), rd.uniform(-1, 1)/2, earth_particles, 100, False))
                              game_over_sound.play()
                              game_over = True
                              #asteroids.remove(asteroid)

      if game_over == False:
            if game_stop == False:
                  if len(UFOs) == 0:
                        UFO_timer -= 1

      for uf in UFOs:
            uf.main(display,ship)

            for bull in bullets:
                  if bull.rect.colliderect(uf.rect):
                        try:
                              bullets.pop(bullets.index(bull))
                              UFOs.pop(UFOs.index(uf))
                              for i in range(15):
                                 particles.append(particle(bull.pos[0], bull.pos[1], rd.randrange(-10, 10), rd.randrange(-10, 0), 4, (163, 167, 194), rd.random()/2, ufo_particles, 100, False))
                        except:
                              pass
                        score += 1                              
            for ufBull in uf.bullets:
                  if ufBull.ifCollide(ship.rect):
                        try:
                              uf.bullets.pop(uf.bullets.index(ufBull))
                        except:
                              pass
                        asteroids = []
                        ufos = []
                        pygame.mixer.music.fadeout(10000)
                        pygame.mixer.music.stop()
                        game_over_sound.play()
                        
                        for i in range(50):
                              particles.append(particle(ship.rect.center[0], ship.rect.center[1], rd.randrange(-10, 10), rd.randrange(-10, 0), 4, (163, 167, 194), rd.random()/2, ship_particles, 100, False))
                        game_over = True
            if uf.dir['left'] == True:
                  if uf.pos[0] < 0:
                        UFOs.pop(UFOs.index(uf))
            if uf.dir['right'] == True:
                  if uf.pos[0] > display_size[0]+uf.image_size[0]:
                        UFOs.pop(UFOs.index(uf))
      
      
      if score >= 25:
            if UFO_timer < 0:
                  UFO_timer = 300
                  if len(UFOs) == 0:
                        if ship.y > 400:
                              UFOs.append(UFO([rd.choice([-32,display_size[0]]),rd.randint(0,400)],display_size))
                        else:
                              UFOs.append(UFO([rd.choice([-32,display_size[0]]),rd.randint(400,750)],display_size))
                        #game over
      if game_over:
            final_score_text = font_large.render('Score: ' + str(score), True, (255,255,255))
            display.blit(game_over_text, game_over_text_rect)
            display.blit(final_score_text, final_score_text_rect)

      else:
            text = font.render('Score: ' + str(score), True, (255,255,255))
            display.blit(text, scoretextRect)

      #draw MAIN MENU
      if startTrans == False:
            if not has_loaded_menu_music:
              pygame.mixer.music.unload()
              pygame.mixer.music.load("assets/Menu.mp3")
              pygame.mixer.music.play(-1)
              has_loaded_menu_music = True
            mainMen.main(display)
            transit.disp1 = mainMen.disp
      
      if startTrans == True:

              
              transit.disp2 = display
              transit.main(display)

              if not has_loaded_game_music:
                    pygame.mixer.music.fadeout(10000)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("assets/GamePlay.mp3")
                    pygame.mixer.music.play(-1)
                    has_loaded_game_music = True
                    in_game = True
              if transit.transEnd == True:
                    game_stop = False


      if how_to_play_menu:
            
            how_to_play_text = font_large_menu.render("How To Play:", True, (255,255,255))
            textRect = how_to_play_text.get_rect()
            textRect.center = (400, 100)



            pygame.draw.rect(display, (0,0,0), (0,0,800, 800))
            display.blit(how_to_play_text, textRect)

            for text in text_list:
                  display.blit(text[0], text[1])
 
            
      pygame.display.update()
      clock.tick(60)
