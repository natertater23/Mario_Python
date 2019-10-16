import pygame
from pygame.sprite import Sprite


class Goomba(Sprite):
    def __init__(self, settings, screen):
        super(Goomba, self).__init__()
        self. screen = screen
        self.settings = settings

        self.speed = 5
        self.direction = range(0,2)
        self.is_alive = True


        self.image = GOOMBA_SPRITES['0']
        self.index = 0
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)



        def blitme(self):
            self.screen.blit(self.image, self.rect)

        def upate(self):
            loop = True
            # Move left
            while loop:
                if self.direction == 0:
                    self.rect.x -= self.speed
                else:
                    self.rect.x += self.speed

                self.direction = range(0, 2)
                if not self.is_alive:
                    loop = False

