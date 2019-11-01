from data import main
from data import menu
from data import settings as s
import pygame as pg
import os
import sys


class Game:
    def __init__(self):
        self.menu = None
        self.main = None

    def run(self):
        self.menu = menu.Menu() 
        self.menu.menu_loop()
        if self.menu.quit_state == 'play':   # Check whether to continue to game or quit app
            self.main = main.Main()
            self.main.main_loop()
            if self.main.quit_state == 'menu':
                os.execl(sys.executable, sys.executable, *sys.argv)  # Restart game


if __name__ == '__main__':
    pg.init()  # Initialize pygame module
    s.screen = pg.display.set_mode((s.SCREEN_SIZE.x, s.SCREEN_SIZE.y))
    pg.display.set_caption(s.CAPTION)
    s.clock = pg.time.Clock()

    game = Game()
    game.run()

    pg.quit()
