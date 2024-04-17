import pygame

from Utilities.menu import Menu
from Utilities.service import GAMESCREEN
pygame.init()

running = True

while running:
    temp = Menu(GAMESCREEN)
    temp.run()

    # Khi người dùng muốn thoát, nhấn Esc hoặc bất kỳ điều kiện khác
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

pygame.quit()
