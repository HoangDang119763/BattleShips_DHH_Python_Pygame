import random

from battle_ships import BattleShips
from ship import Ship
from service import SCREENWIDTH, SCREENHEIGHT, load_image, load_animation_images, load_sprite_sheet_images, \
    increase_animation_image
from button import Button
import pygame


class BattleShips_TypeOne(BattleShips):
    def __init__(self, numrows=None, numcolumns=None, cellsize=None, pos=None):
        if numrows is not None and numcolumns is not None and cellsize is not None and pos is not None:
            super().__init__(numrows, numcolumns, cellsize, pos)
            cellSizeY = (SCREENHEIGHT // 2) // self.numRows
            cellSizeX = (SCREENWIDTH // 2) // self.numColums
            self.cellSize = cellSizeY
            self.cellSize1 = cellSizeX
            self.pos = (cellSizeX, cellSizeX)
            self.deployment = True
            self.scanner = False
            self.indnum = 0
            self.blipposition = None
            self.cFleet = []
            self.pFleet = []
            self.button = []
            self.tokens = []
            self.status = True
        else:
            cellSizeY = (SCREENHEIGHT // 2) // 10
            cellSizeX = (SCREENWIDTH // 2) // 10
            self.cellSize1 = cellSizeX
            super().__init__(10, 10, cellSizeY, (cellSizeX, cellSizeX))
            self.deployment = True
            self.scanner = False
            self.indnum = 0
            self.blipposition = None
            self.cFleet = []
            self.pFleet = []
            self.button = []
            self.tokens = []
            self.status = True

    def create_grid(self):
        startx = self.pos[0]
        starty = self.pos[1]

        for row in range(self.numRows):
            rowx = []
            for col in range(self.numColums):
                rowx.append((startx, starty))
                startx += self.cellSize
            self.pGameGrid.append(rowx)
            startx = self.pos[0]
            starty += self.cellSize

        startx = SCREENWIDTH - (self.numRows * self.cellSize) - self.pos[0]
        starty = self.pos[1]
        for row in range(self.numRows):
            rowxc = []
            for col in range(self.numColums):
                rowxc.append((startx, starty))
                startx += self.cellSize
            self.cGameGrid.append(rowxc)
            startx = SCREENWIDTH - (self.numRows * self.cellSize) - self.pos[0]
            starty += self.cellSize

    def create_logic(self):
        for row in range(self.numRows):
            rowX = []
            for col in range(self.numColums):
                rowX.append(' ')
            self.cGameLogic.append(rowX)

        for row in range(self.numRows):
            rowXc = []
            for col in range(self.numColums):
                rowXc.append(' ')
            self.pGameLogic.append(rowXc)

    def update_pgame_logic(self, coordGrid, shipList):
        for i, rowX in enumerate(coordGrid):
            for j, colX in enumerate(rowX):
                if self.pGameLogic[i][j] == 'T' or self.pGameLogic[i][j] == 'X':
                    continue
                else:
                    self.pGameLogic[i][j] = ' '
                    for ship in shipList:
                        if pygame.rect.Rect(colX[0], colX[1], self.cellSize, self.cellSize).colliderect(ship.rect):
                            self.pGameLogic[i][j] = 'O'

    def update_cgame_logic(self, coordGrid, shipList):
        for i, rowX in enumerate(coordGrid):
            for j, colX in enumerate(rowX):
                if self.cGameLogic[i][j] == 'T' or self.cGameLogic[i][j] == 'X':
                    continue
                else:
                    self.cGameLogic[i][j] = ' '
                    for ship in shipList:
                        if pygame.rect.Rect(colX[0], colX[1], self.cellSize, self.cellSize).colliderect(ship.rect):
                            self.cGameLogic[i][j] = 'O'

    def show_grid_onscreen(self, window):
        gamegrid = [self.pGameGrid, self.cGameGrid]
        for grid in gamegrid:
            for row in grid:
                for col in row:
                    pygame.draw.rect(window, (255, 255, 255), (col[0], col[1], self.cellSize, self.cellSize), 1)

    def show_ship_onscreen(self, window, fleet, gamegrid):
        for ship in fleet:
            ship.draw(window)
            ship.snap_to_grid_edge(gamegrid)
            ship.snap_to_grid(gamegrid, self.cellSize)

    def show_button_onscreen(self, window, button):
        for buttonx in button:
            buttonx.draw(window, self.deployment)

    def create_fleet(self):
        FLEET = {
            'battleship': ['battleship', 'assets/images/ships/battleship/battleship.png',
                           (SCREENWIDTH // 2, self.cellSize1),
                           (30, self.cellSize * 4 - 5),
                           4, 'assets/images/ships/battleship/battleshipgun.png', (0.4, 0.125),
                           [-0.525, -0.34, 0.67, 0.49]],
            'cruiser': ['cruiser', 'assets/images/ships/cruiser/cruiser.png',
                        (SCREENWIDTH // 2 - self.cellSize1, self.cellSize1),
                        (30, self.cellSize * 5 - 5),
                        2, 'assets/images/ships/cruiser/cruisergun.png', (0.4, 0.125), [-0.36, 0.64]],
            'destroyer': ['destroyer', 'assets/images/ships/destroyer/destroyer.png',
                          (SCREENWIDTH // 2 - self.cellSize1 * 2, self.cellSize1), (30, self.cellSize * 3 - 5),
                          2, 'assets/images/ships/destroyer/destroyergun.png', (0.5, 0.15), [-0.52, 0.71]],
            'patrol boat': ['patrol boat', 'assets/images/ships/patrol boat/patrol boat.png',
                            (SCREENWIDTH // 2 - self.cellSize1 * 3, self.cellSize1), (25, self.cellSize * 2 - 5),
                            0, '', None, None],
            'submarine': ['submarine', 'assets/images/ships/submarine/submarine.png',
                          (SCREENWIDTH // 2 + self.cellSize1 * 2, self.cellSize1), (30, 145),
                          1, 'assets/images/ships/submarine/submarinegun.png', (0.25, 0.125), [-0.45]],
            'carrier': ['carrier', 'assets/images/ships/carrier/carrier.png',
                        (SCREENWIDTH // 2 + self.cellSize1, self.cellSize1),
                        (30, self.cellSize * 4),
                        0, '', None, None],
            'rescue ship': ['rescue ship', 'assets/images/ships/rescue ship/rescue ship.png',
                            (SCREENWIDTH // 2 + self.cellSize1 * 3, self.cellSize1), (25, self.cellSize * 2 - 5),
                            0, '', None, None]
        }
        for name in FLEET.keys():
            temp = Ship(name, FLEET[name][1],
                        FLEET[name][2],
                        FLEET[name][3],
                        FLEET[name][4],
                        FLEET[name][5],
                        FLEET[name][6],
                        FLEET[name][7])
            self.cFleet.append(temp)

        for name in FLEET.keys():
            temp = Ship(name, FLEET[name][1],
                        FLEET[name][2],
                        FLEET[name][3],
                        FLEET[name][4],
                        FLEET[name][5],
                        FLEET[name][6],
                        FLEET[name][7])
            self.pFleet.append(temp)

    def sort_fleet(self, ship, shipList):
        shipList.remove(ship)
        shipList.append(ship)

    def create_button(self):
        BUTTONIMAGE = load_image(r'assets\images\buttons\button.png', (150, 50))
        BUTTONIMAGE1 = load_image(r'assets\images\buttons\button.png', (250, 100))
        self.button = [
            Button(BUTTONIMAGE, (150, 50), (25, SCREENHEIGHT - self.cellSize1), 'Randomize'),
            Button(BUTTONIMAGE, (150, 50), (200, SCREENHEIGHT - self.cellSize1), 'Reset'),
            Button(BUTTONIMAGE, (150, 50), (375, SCREENHEIGHT - self.cellSize1), 'Deploy'),
            Button(BUTTONIMAGE1, (250, 100), (900, SCREENHEIGHT // 2 - 150), 'Easy Computer'),
            Button(BUTTONIMAGE1, (250, 100), (900, SCREENHEIGHT // 2 + 150), 'Hard Computer')
        ]

    def create_sound_image(self):
        MAINMENUIMAGE = load_image('assets/images/background/Battleship.jpg', (SCREENWIDTH // 3 * 2, SCREENHEIGHT))
        ENDSCREENIMAGE = load_image('assets/images/background/Carrier.jpg', (SCREENWIDTH, SCREENHEIGHT))
        BACKGROUND = load_image('assets/images/background/gamebg.png', (SCREENWIDTH, SCREENHEIGHT))
        PGAMEGRIDIMG = load_image('assets/images/grids/player_grid.png',
                                  ((self.numRows + 1) * self.cellSize, (self.numColums + 1) * self.cellSize))
        CGAMEGRIDIMG = load_image('assets/images/grids/comp_grid.png',
                                  ((self.numRows + 1) * self.cellSize, (self.numColums + 1) * self.cellSize))
        REDTOKEN = load_image('assets/images/tokens/redtoken.png', (self.cellSize1, self.cellSize1))
        GREENTOKEN = load_image('assets/images/tokens/greentoken.png', (self.cellSize1, self.cellSize1))
        BLUETOKEN = load_image('assets/images/tokens/bluetoken.png', (self.cellSize1, self.cellSize1))
        FIRETOKENIMAGELIST = load_animation_images('assets/images/tokens/fireloop/fire1_ ', 13,
                                                   (self.cellSize1, self.cellSize1))
        EXPLOSIONSPRITESHEET = pygame.image.load('assets/images/tokens/explosion/explosion.png').convert_alpha()
        EXPLOSIONIMAGELIST = []
        for row in range(8):
            for col in range(8):
                EXPLOSIONIMAGELIST.append(
                    load_sprite_sheet_images(EXPLOSIONSPRITESHEET, col, row, (self.cellSize, self.cellSize),
                                             (128, 128)))
        RADARGRIDIMAGES = load_animation_images('assets/images/radar_base/radar_anim', 360,
                                                (self.numRows * self.cellSize, self.numColums * self.cellSize))
        RADARBLIPIMAGES = load_animation_images('assets/images/radar_blip/Blip_', 11, (50, 50))
        RADARGRID = load_image('assets/images/grids/grid_faint.png',
                               ((self.numRows) * self.cellSize, (self.numColums) * self.cellSize))
        HITSOUND = pygame.mixer.Sound('assets/sounds/explosion.wav')
        HITSOUND.set_volume(0.05)
        SHOTSOUND = pygame.mixer.Sound('assets/sounds/gunshot.wav')
        SHOTSOUND.set_volume(0.05)
        MISSSOUND = pygame.mixer.Sound('assets/sounds/splash.wav')
        MISSSOUND.set_volume(0.05)

    def pick_random_ship_location(self, gameLogic):
        validChoice = False
        while not validChoice:
            posX = random.randint(0, 9)
            posY = random.randint(0, 9)
            if gameLogic[posX][posY] == 'O':
                validChoice = True

        return (posX, posY)

    def display_radar_scanner(self, imagelist, indnum, scanner):
        if scanner == True and indnum <= 359:
            image = increase_animation_image(imagelist, indnum)
            return image
        else:
            return False

    def randomize_ship_positions(self, shipList, gameGrid):
        placedShips = []
        for i, ship in enumerate(shipList):
            validPosition = False
            while not validPosition:
                ship.return_to_default_position()
                rotateShip = random.randint(0, 1)
                if rotateShip:
                    yAxis = random.randint(0, 9)
                    xAxis = random.randint(0, 9 - (ship.hImage.get_width() // self.cellSize))
                    ship.rotate_ship(True)
                    ship.rect.topleft = gameGrid[yAxis][xAxis]
                else:
                    yAxis = random.randint(0, 9 - (ship.vImage.get_height() // self.cellSize))
                    xAxis = random.randint(0, 9)
                    ship.rect.topleft = gameGrid[yAxis][xAxis]
                if len(placedShips) > 0:
                    for item in placedShips:
                        if ship.rect.colliderect(item.rect):
                            validPosition = False
                            break
                        else:
                            validPosition = True
                else:
                    validPosition = True
            placedShips.append(ship)

    def pick_random_ship_location(self, gameLogic):
        validChoice = False
        posX = None
        posY = None
        while not validChoice:
            posX = random.randint(0, 9)
            posY = random.randint(0, 9)
            if gameLogic[posX][posY] == 'O':
                validChoice = True

        return posX, posY

    def deployment_phase(self, deployment):
        flag = True
        if deployment:
            flag = False
        return flag


