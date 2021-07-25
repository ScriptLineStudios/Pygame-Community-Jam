import pygame, sys, math
pygame.init()

display = pygame.display.set_mode((800, 800))

clock = pygame.time.Clock()

ship_img = pygame.image.load("ship.png").convert()
ship_img.set_colorkey((255,255,255))

class Ship:
      def __init__(self, x, y):
            self.x = x
            self.y = y

      def main(self, display, angle):
            image = pygame.transform.rotate(ship_img, angle)
            display.blit(image, (self.x, self.y))

ship = Ship(300, 300)

while True:
      display.fill((0,0,0))
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()

      mouse_x, mouse_y = pygame.mouse.get_pos()
      rel_x, rel_y = mouse_x - ship.x, mouse_y - ship.y

      angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

      keys = pygame.key.get_pressed()

      if keys[pygame.K_w]:
            ship.y -= 5
      if keys[pygame.K_s]:
            ship.y += 5
      if keys[pygame.K_a]:
            ship.x -= 5
      if keys[pygame.K_d]:
            ship.x += 5

      ship.main(display, angle)

      pygame.display.update()
      clock.tick(60)
      
