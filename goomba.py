import pygame
from pygame.sprite import Sprite


class Goomba(Sprite):
    def __init__(self, settings, screen):
        super(Goomba, self).__init__()
        self. screen = screen
        self.settings = settings

        self.image = GOOMBA_SPRITES['0']
        self.index = 0
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

        def blitme(self):
            self.screen.blit(self.image, self.rect)
