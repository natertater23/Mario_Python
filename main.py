from pygame import *
from pygame.sprite import Sprite
import sys
from os.path import abspath, dirname

directory_path = abspath(dirname(__path__))
images_path = directory_path + '/images/'
sounds_path = directory_path + '/sounds/'
fonts_path = directory_path + '/fonts'

SCREEN = display.set_mode(800, 600)

FIREBALL_JUMP_HEIGHT = 40

# general use sounds

SOUNDS = {}
for sound_name in []:
    SOUNDS[sound_name] = mixer.Sound(
        sounds_path + '{}.wav'.format(sound_name))
    SOUNDS[sound_name].set_volume(0.2)

# general use images

images = []
IMAGES = {name: (images_path + '{}.png'.format(name)).convert_alpha()
          for name in images}

# mario specific sprites and images
# format for use -> state + order of img in sprite. VERY IMPORTANT TO FOLLOW THIS FORMAT

mario_images = []
MARIO_SPRITES = {name: (images_path + '{}.png'.format(name)).convert_alpha()
                 for name in mario_images}


class superMario():
    def __init__(self):
        mixer.pre_init(44100, -16, 1, 4096)
        init()
        self.clock = time.clock()
        self.game_over = False
        self.main_screen = True
        self.startGame = False
        self.display_caption = display.set_caption('Super Mario')
        self.screen = SCREEN
        self.should_exit = False
        self.lives_amount = 3

    def reset(self):
        self.player = Mario(1)
        self.player_fireballs = sprite.Group()
        self.enemies = sprite.Group()
        self.terrain = sprite.Group()
        self.allsprites = sprite.Group(self.player, self.enemies, self.terrain)
        # self.makeWorld()

    def check_input(self):
        super(Mario, self).__init__()
        self.keys = key.get_pressed()
        for e in pygame.event.get():
            if self.should_exit:
                sys.exit()
            if event.type == KEYDOWN:
                if e.key == K_SPACE and Mario.current_state == Mario.marioStates[2] and Mario.is_alive:
                    fireball = Player_fireball(Mario.direction)
                    self.player_fireballs.add(fireball)
                    self.allsprites.add(self.player_fireballs)

        """
    def check_collisons(self):
        # When terrain is ready, load a group terrain in the supermario class w/ bounceable objects
        # this section will handle fireball collisions and physics with any sprites in that group

        for fireball, object in sprite.groupcollide(self.player_fireballs, self.terrain, False, False):
            if fireball.rect.left == object.rect.right or fireball.rect.right == object.rect.left:
                hit.direction *= -1
            if fireball.rect.bottom == object.rect.top:
                fireball.baseY = fireball.rect.bottom

        for mario, powerup in sprite.groupcollide(self.player, self.powerup, false, true):
            if powerup.type == 'mushroom' and mario.currentState == 'mini':
                mario.currentState = 'normal'
            if powerup.type == 'fire_flower' and mario.currentState != 'fire':
                mario.currentState = 'fire'

        for mario, enemy in groupcollide(self.player, self.enemies, false, false):
            if mario.currentState != 'mini':
                mario.currentState = mario.marioStates[mario.currentState - 1]
            else:
                if self.lives_amount > 0:
                    self.lives_amount -= 1
                    self.reset()
                else:
                    self.game_over = True;
        """

    def main(self):
        self.reset()
        # while True:
        # self.checkCollisions()


class Player_fireball(Sprite):
    def __init__(self, direction):
        super(Mario, self).__init__()
        self.direction = direction
        self.bounces = 0
        self.baseY = Mario.rect.bottom
        self.up = False
        self.speed = 1
        self.jump_amount = 1
        self.timer = time.get_ticks()
        self.moveTimer = 100
        self.play_sound = True
        self.shoot = SOUNDS[0]

        # LOAD ALL NEEDED FIREBALL IMAGES HERE from the image section

        self.images = []
        self.index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(topright=(Mario.rect.topleft, Mario.rect.topleft))

    def update(self, current_time):
        if current_time - self.timer > self.moveTimer:
            if self.bounces > 3:
                self.kill()
            if self.play_sound:
                self.shoot.play()
                self.play_sound = False
            if self.rect.y - self.baseY <= FIREBALL_JUMP_HEIGHT:
                self.rect.y += self.jump_amount
            else:
                self.rect.y -= self.jump_amount
            if self.direction == 1:
                self.rect.x += 1
            else:
                self.rect.x -= 1
            self.image = self.images[self.index]
            if self.index >= len(self.images):
                self.index = 0


class Mario(Sprite):
    def __init__(self):
        self.image = MARIO_SPRITES['0']
        self.index = 0
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.speed = 5
        self.direction = 1
        self.jumping = False
        self.ducking = False
        self.marioStates = {0: 'mini', 1: 'normal', 2: 'fire'}
        self.current_state = self.marioStates[0]
        self.is_alive = True

    def update(self, keys):
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x -= self.speed
        if keys[K_UP] and not self.jumping:
            self.jumping = True
        if keys[K_DOWN]:
            self.ducking = True
        if self.ducking:
            game.screen.blit(IMAGES[self.current_state + '_Ducking'], self.rect)
            self.index = 0
        else:
            game.screen.blit(IMAGES[self.current_state + ('{}'.format(self.index))], self.rect)
            if self.index >= len(mario_images):
                self.index = 0


if __name__ == 'main':
    game = superMario()
    game.main()
