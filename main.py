import pygame
import pygame.display

from battle_ship_type_one import BattleShips_TypeOne
from service import load_image, GAMESCREEN, CELLSIZE, bg, SCREENWIDTH, SCREENHEIGHT, cellSizeY, cellSizeX, NUMROWS, NUMCOLS, GAMESTATE, updateGameScreen

pygame.init()

game = BattleShips_TypeOne()
game.create_grid()
game.create_fleet()
game.create_button()
game.randomize_ship_positions(game.cFleet, game.cGameGrid)
RUNGAME = True

while RUNGAME:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNGAME = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for ship in game.pFleet:
                    if ship.rect.collidepoint(pygame.mouse.get_pos()):
                        ship.active = True
                        #game.sort_fleet(ship, game.pFleet)
                        ship.select_ship_and_move(game.pFleet, game, GAMESCREEN)

                for button in game.button:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.action_on_press(game)


            elif event.button == 3:
                    for ship in game.pFleet:
                        if ship.rect.collidepoint(pygame.mouse.get_pos()) and not ship.check_for_rotate_collisions(game.pFleet):
                            ship.rotate_ship(True)
    updateGameScreen(GAMESCREEN, game)

pygame.quit()