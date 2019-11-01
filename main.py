from . import settings as s
from . import level
from . import sprites
from . import sounds
from .types import Camera, Vector2, Rectangle, Digit_System
import pygame as pg
from .components import mario


class Main:
    # Main loop handler
    def __init__(self):
        s.camera = Camera(Vector2(), s.SCREEN_SIZE.x, s.SCREEN_SIZE.y)
        s.mario = mario.Mario(Rectangle(s.MARIO_START_POSITION, 36, 48))

        pg.mixer.music.load(sounds.main_theme)
        pg.mixer.music.play()

        self.quit_state = None
        self.out_of_time = False

        self.score_system = Digit_System(Vector2(66, 49), 6) #Displays total score on screen
        self.coin_score = Digit_System(Vector2(306, 49), 2) #Displays collected coins on screen
        self.time = Digit_System(Vector2(610, 49), 3, 300) #Displays time on screen
        self.timer = 0 #timer for counting down the in-game time

    def draw(self):
        # Main draw method
        s.screen.fill(s.BACKGROUND_COLOR)
        self.draw_background()
        
        for item in (level.coins + level.super_mushrooms):
            if item.deployed:
                item.draw()

        for tile in level.dynamic_colliders:
            if s.camera.contains(tile.rect):
                view_pos = s.camera.to_view_space(tile.pos)
                tile.draw(view_pos)

        for enemy in level.enemies:
            if enemy.is_active:
                enemy.draw()

        for fragment in level.brick_fragments:
            fragment.draw()

        s.flagpole.draw_flag()

        s.mario.draw()

        self.draw_foreground()
        self.draw_digit_systems()

    def draw_background(self):
        s.screen.blit(sprites.background,
                      (0, 0), 
                      (s.camera.pos.x, s.camera.pos.y, s.SCREEN_SIZE.x, s.SCREEN_SIZE.y))

    def draw_foreground(self):
        view_pos = s.camera.to_view_space(s.FOREGROUND_POS)
        if view_pos.x < s.camera.pos.x + s.SCREEN_SIZE.x:
            s.screen.blit(sprites.foreground, (view_pos.x, view_pos.y))
        s.screen.blit(sprites.text_image, (0,0))

    def draw_digit_systems(self):
        # Draws Numbers
        self.score_system.draw()
        self.coin_score.draw()
        self.time.draw()

    def handle_digit_systems(self):
        # Numbers
        if not s.mario.current_mario_state == 'Dead_Mario':
            self.handle_time()
            self.score_system.update_value(s.total_score)
            self.coin_score.update_value(s.collected_coins)

    def handle_time(self):
        # Timer
        # Count down the timer
        self.timer += s.var_time
        if not s.final_count_down and self.timer > 14 * s.var_time:
            self.time.update_value(self.time.total_value - 1)
            self.timer = 0

        # Timer is lower than 100, play out of time music
        if not s.mario.current_mario_state == 'Win_State':
            if not s.final_count_down and self.time.total_value < 100 and not self.out_of_time:
                pg.mixer.music.stop()
                pg.mixer.music.set_endevent(s.OUT_OF_TIME_END)
                pg.mixer.music.load(sounds.out_of_time)
                pg.mixer.music.play()
                self.out_of_time = True

        # If the timer runs out and mario has not won, kill mario
        if not s.final_count_down and self.time.total_value == 0:
            s.mario.mario_states.on_event('dead')

        # If mario has won and time is still > 0, count down and add score
        if s.final_count_down and self.time.total_value > 0:
            self.time.update_value(self.time.total_value - 1)
            s.total_score += s.TIME_SCORE
            sounds.count_down.play()
            sounds.count_down.set_volume(0.15)
            if self.time.total_value == 0:
                sounds.count_down.stop()
                sounds.coin.play()

    def update_level(self):
        # Update Objects
        s.mario.update()
        s.mario.physics_update()
        s.camera.update()
        for tile in level.dynamic_colliders:
            tile.update()

        for item in (level.coins + level.super_mushrooms):
            if item.deployed:
                item.update()

        if not s.mario.freeze_movement:
            for enemy in level.enemies:
                if enemy.pos.x < s.camera.pos.x + s.SCREEN_SIZE.x:
                    enemy.is_active = True
                enemy.update()

        for fragment in level.brick_fragments:
            fragment.update()

        s.flagpole.update()

    def check_for_quit(self):
        # Lose/Quit- does not exactly work
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            
            if event.type == s.WIN_SONG_END and self.time.total_value == 0:
                self.quit_state = 'menu'
                return False

            if event.type == s.DEATH_SONG_END:
                self.quit_state = 'menu'
                return False

            if event.type == s.OUT_OF_TIME_END:
                pg.mixer.music.stop()
                pg.mixer.music.load(sounds.main_theme_sped_up)
                pg.mixer.music.play()

        if s.mario.to_menu:
            self.quit_state = 'menu'
            return False

        if s.keys[pg.K_ESCAPE]:
            return False
        return True

    def main_loop(self):
        # draws main frame
        while True:
            s.var_time = s.clock.tick(60)
            s.keys = pg.key.get_pressed()

            self.update_level()
            self.handle_digit_systems()
            self.draw()

            if not self.check_for_quit():
                break

            pg.display.update()