import pygame

from Utilities.menu import Menu
from Utilities.service import GAMESCREEN
pygame.init()

temp = Menu(GAMESCREEN)
temp.run()
