import pygame, sys, math
pygame.init()

display = pygame.display.set_mode((800, 800))

clock = pygame.time.Clock()

ship_img = pygame.image.load("ship.png").convert()
ship_img.set_colorkey((255,255,255))

def rotate(rotatedImage, rect):
    rect = rotatedImage.get_rect(center=rect.center)
    return rect


class Ship:
      def __init__(self, x, y):
            self.x = x
            self.y = y
            self.size = ship_img.get_size()
            self.angle = 0

            self.rect = ship_img.get_rect(topleft=(self.x,self.y))

            self.speed = [0,0]
            

      def main(self, display):
            
            self.rect = ship_img.get_rect(topleft=(self.x,self.y))
            image = pygame.transform.rotate(ship_img, self.angle)
            display.blit(image, rotate(image,self.rect).topleft)#rotate(image,self.rect) - rotate from center
            

ship = Ship(300, 300)

while True:
      display.fill((0,0,0))
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
            ship.angle -= 5
      if keys[pygame.K_d]:
            ship.x += 5

      ship.angle = angle
      ship.main(display)

      pygame.display.update()
      clock.tick(60)
