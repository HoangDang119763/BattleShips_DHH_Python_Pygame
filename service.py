import pygame

SCREENWIDTH = 1530
SCREENHEIGHT = 775
NUMROWS = 10
NUMCOLS = 10
cellSizeY = (SCREENHEIGHT // 2) // (NUMROWS)
cellSizeX = (SCREENWIDTH // 2) // (NUMCOLS)
CELLSIZE = cellSizeY
STAGE = ['Main Menu', 'Deployment', 'Game Over']
TURNTIMER = pygame.time.get_ticks()
GAMESTATE = 'Main Menu'
GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Battle Ships')
icon = pygame.image.load(r'assets\images\background\icon.png')
pygame.display.set_icon(icon)
bg = pygame.image.load(r'assets\images\background\background.jpg')
bg = pygame.transform.scale(bg, (SCREENWIDTH, SCREENHEIGHT))



def load_image(path, size, rotate=False):
    """A function to import the images into memory"""
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    if rotate:
        img = pygame.transform.rotate(img, -90)
    return img

def load_animation_images(path, aniNum, size):
    """Load in stipulated number of images to memory"""
    imageList = []
    for num in range(aniNum):
        if num < 10:
            imageList.append(load_image(f'{path}00{num}.png', size))
        elif num < 100:
            imageList.append(load_image(f'{path}0{num}.png', size))
        else:
            imageList.append(load_image(f'{path}{num}.png', size))
    return imageList

def load_sprite_sheet_images(spriteSheet, rows, cols, newSize, size):
    image = pygame.Surface((128, 128))
    image.blit(spriteSheet, (0, 0), (rows * size[0], cols * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, (newSize[0], newSize[1]))
    image.set_colorkey((0, 0, 0))
    return image

def increase_animation_image(imageList, ind):
    return imageList[ind]

def updateGameScreen(window, game):
    GAMESCREEN.blit(bg, (0, 0))
    game.show_grid_onscreen(GAMESCREEN)
    game.show_ship_onscreen(GAMESCREEN, game.pFleet, game.pGameGrid)
    game.show_ship_onscreen(GAMESCREEN, game.cFleet, game.cGameGrid)
    game.show_button_onscreen(GAMESCREEN, game.button)

    pygame.display.update()

# def main_menu_screen(window):
#     window.fill((0, 0, 0))
#     window.blit(MAINMENUIMAGE, (0, 0))
#
#     for button in BUTTONS:
#         if button.name in ['Easy Computer', 'Hard Computer']:
#             button.active = True
#             button.draw(window)
#         else:
#             button.active = False
#
# def deployment_screen(window):
#     window.fill((0, 0, 0))
#
#     window.blit(BACKGROUND, (0, 0))
#     window.blit(PGAMEGRIDIMG, (0, 0))
#     window.blit(CGAMEGRIDIMG, (cGameGrid[0][0][0] - 50, cGameGrid[0][0][1] - 50))
#
#     #  Draws the player and computer grids to the screen
#     # showGridOnScreen(window, CELLSIZE, pGameGrid, cGameGrid)
#
#     #  Draw ships to screen
#     for ship in pFleet:
#         ship.draw(window)
#         ship.snapToGridEdge(pGameGrid)
#         ship.snapToGrid(pGameGrid)
#
#     displayShipNames(window)
#
#     for ship in cFleet:
#         # ship.draw(window)
#         ship.snapToGridEdge(cGameGrid)
#         ship.snapToGrid(cGameGrid)
#
#     for button in BUTTONS:
#         if button.name in ['Randomize', 'Reset', 'Deploy', 'Quit', 'Radar Scan', 'Redeploy']:
#             button.active = True
#             button.draw(window)
#         else:
#             button.active = False
#
#     computer.draw(window)
#
#     radarScan = displayRadarScanner(RADARGRIDIMAGES, INDNUM, SCANNER)
#     if not radarScan:
#         pass
#     else:
#         window.blit(radarScan, (cGameGrid[0][0][0], cGameGrid[0][-1][1]))
#         window.blit(RADARGRID, (cGameGrid[0][0][0], cGameGrid[0][-1][1]))
#
#     RBlip = displayRadarBlip(INDNUM, BLIPPOSITION)
#     if RBlip:
#         window.blit(RBlip, (cGameGrid[BLIPPOSITION[0]][BLIPPOSITION[1]][0],
#                             cGameGrid[BLIPPOSITION[0]][BLIPPOSITION[1]][1]))
#
#     for token in TOKENS:
#         token.draw(window)
#
#     updateGameLogic(pGameGrid, pFleet, pGameLogic)
#     updateGameLogic(cGameGrid, cFleet, cGameLogic)


# def update_game_screen(window, GAMESTATE):
#     if GAMESTATE == 'Main Menu':
#         main_menu_screen(window)
#     elif GAMESTATE == 'Deployment':
#         deployment_screen(window)
#     elif GAMESTATE == 'Game Over':
#         endScreen(window)
#
#     pygame.display.update()

# def endScreen(window):
#     window.fill((0, 0, 0))
#
#     window.blit(ENDSCREENIMAGE, (0, 0))
#
#     for button in BUTTONS:
#         if button.name in ['Easy Computer', 'Hard Computer', 'Quit']:
#             button.active = True
#             button.draw(window)
#         else:
#             button.active = False
