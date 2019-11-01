import pygame as pg
from os import path

pg.init()
pg.mixer.pre_init(44100, 16, 2, 4096)

folder = path.join(path.dirname(__file__), 'resources/sounds')

# Game Sounds
brick_smash = pg.mixer.Sound(path.join(folder, 'brick_smash.wav'))
kick = pg.mixer.Sound(path.join(folder, 'kick.wav'))
flagpole_sound = pg.mixer.Sound(path.join(folder, 'flagpole.wav'))
count_down = pg.mixer.Sound(path.join(folder, 'count_down.wav'))
pipe = pg.mixer.Sound(path.join(folder, 'pipe.wav'))
small_jump = pg.mixer.Sound(path.join(folder, 'small_jump.wav'))
big_jump = pg.mixer.Sound(path.join(folder, 'big_jump.wav'))
bump = pg.mixer.Sound(path.join(folder, 'bump.wav'))
power_up_appears = pg.mixer.Sound(path.join(folder, 'powerup_appears.wav'))
power_up = pg.mixer.Sound(path.join(folder, 'powerup.wav'))
coin = pg.mixer.Sound(path.join(folder, 'coin.wav'))
stomp = pg.mixer.Sound(path.join(folder, 'stomp.wav'))

# Music
main_theme = path.join(folder, 'main_theme.wav')
stage_clear = path.join(folder, 'stage_clear.wav')
death = path.join(folder, 'death.wav')
out_of_time = path.join(folder, 'out_of_time.wav')
main_theme_sped_up = path.join(folder, 'main_theme_sped_up.wav')
