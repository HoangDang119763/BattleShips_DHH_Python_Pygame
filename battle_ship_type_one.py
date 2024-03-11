import random

from battle_ships import BattleShips
from ship import Ship
from service import SCREENWIDTH, SCREENHEIGHT, load_image, load_animation_images, load_sprite_sheet_images, \
    increase_animation_image, TURNTIMER
from button import Button
import pygame


def deployment_phase(deployment):
    flag = True
    if deployment:
        flag = False
    return flag


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

            self.pgamegriding = load_image('assets/images/grids/player_grid.png',
                                           ((self.numRows + 1) * self.cellSize, (self.numColums + 1) * self.cellSize))
            self.cgamegriding = load_image('assets/images/grids/comp_grid.png',
                                           ((self.numRows + 1) * self.cellSize, (self.numColums + 1) * self.cellSize))
            self.redtoken = load_image('assets/images/tokens/redtoken.png', (self.cellSize1, self.cellSize1))
            self.greentoken = load_image('assets/images/tokens/greentoken.png', (self.cellSize1, self.cellSize1))
            self.bluetoken = load_image('assets/images/tokens/bluetoken.png', (self.cellSize1, self.cellSize1))
            self.firetokenimagelist = load_animation_images('assets/images/tokens/fireloop/fire1_ ', 13,
                                                            (self.cellSize1, self.cellSize1))
            self.explosionspritesheet = pygame.image.load(
                'assets/images/tokens/explosion/explosion.png').convert_alpha()
            self.explosionimagelist = []
            for row in range(8):
                for col in range(8):
                    self.explosionimagelist.append(
                        load_sprite_sheet_images(self.explosionspritesheet, col, row, (self.cellSize, self.cellSize),
                                                 (128, 128)))
            self.radargridimages = load_animation_images('assets/images/radar_base/radar_anim', 360,
                                                         (self.numRows * self.cellSize, self.numColums * self.cellSize))
            self.radarblipimages = load_animation_images('assets/images/radar_blip/Blip_', 11, (50, 50))
            self.radargrid = load_image('assets/images/grids/grid_faint.png',
                                        (self.numRows * self.cellSize, self.numColums * self.cellSize))
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

            self.pgamegriding = load_image('assets/images/grids/player_grid.png',
                                           ((self.numRows + 1) * self.cellSize, (self.numColums + 1) * self.cellSize))
            self.cgamegriding = load_image('assets/images/grids/comp_grid.png',
                                           ((self.numRows + 1) * self.cellSize, (self.numColums + 1) * self.cellSize))
            self.redtoken = load_image('assets/images/tokens/redtoken.png', (self.cellSize, self.cellSize))
            self.greentoken = load_image('assets/images/tokens/greentoken.png', (self.cellSize, self.cellSize))
            self.bluetoken = load_image('assets/images/tokens/bluetoken.png', (self.cellSize, self.cellSize))
            self.firetokenimagelist = load_animation_images('assets/images/tokens/fireloop/fire1_ ', 13,
                                                            (self.cellSize, self.cellSize))
            self.explosionspritesheet = pygame.image.load(
                'assets/images/tokens/explosion/explosion.png').convert_alpha()
            self.explosionimagelist = []
            for row in range(8):
                for col in range(8):
                    self.explosionimagelist.append(
                        load_sprite_sheet_images(self.explosionspritesheet, col, row, (self.cellSize, self.cellSize),
                                                 (128, 128)))
            self.radargridimages = load_animation_images('assets/images/radar_base/radar_anim', 360,
                                                         (self.numRows * self.cellSize, self.numColums * self.cellSize))
            self.radarblipimages = load_animation_images('assets/images/radar_blip/Blip_', 11, (50, 50))
            self.radargrid = load_image('assets/images/grids/grid_faint.png',
                                        (self.numRows * self.cellSize, self.numColums * self.cellSize))

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
        if self.cGameLogic:
            self.cGameLogic = []
        if self.pGameLogic:
            self.pGameLogic = []
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

    def show_ship_onscreen(self, window, fleet, gamegrid, visible=False):
        for ship in fleet:
            if visible:
                ship.draw(window)
            ship.snap_to_grid_edge(gamegrid)
            ship.snap_to_grid(gamegrid, self.cellSize)

    def show_button_onscreen(self, window, button):
        for buttonx in button:
            if buttonx.name in ['Randomize', 'Reset', 'Deploy', 'Quit', 'Radar Scan', 'Redeploy']:
                buttonx.active = True
                buttonx.draw(window, self.deployment)
            else:
                buttonx.active = False

    def show_token_onscreen(self, window, token):
        for tokens in token:
            tokens.draw(window)

    def show_radar_scanner_onscreen(self, window):
        radarScan = self.display_radar_scanner(self.radargridimages, self.indnum, self.scanner)
        if not radarScan:
            pass
        else:
            window.blit(radarScan, (self.cGameGrid[0][0][0], self.cGameGrid[0][-1][1]))
            window.blit(self.radargrid, (self.cGameGrid[0][0][0], self.cGameGrid[0][-1][1]))

    def show_radar_blip_onscreen(self, window):
        radarBlip = self.display_radar_blip(self.indnum, self.blipposition, self.scanner)
        if radarBlip:
            window.blit(radarBlip, (self.cGameGrid[self.blipposition[0]][self.blipposition[1]][0],
                                    self.cGameGrid[self.blipposition[0]][self.blipposition[1]][1]))

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

    def pick_random_ship_location(self, gameLogic):
        validChoice = False

        posX = -1
        posY = -1
        while not validChoice:
            posX = random.randint(0, 100 % 10)
            posY = random.randint(0, 100 % 10)
            if gameLogic[posX][posY] == 'O':
                validChoice = True

        return posX, posY

    def display_radar_scanner(self, imagelist, indnum, scanner):
        if scanner and indnum <= 359:
            image = increase_animation_image(imagelist, indnum)
            return image
        else:
            return False

    def display_radar_blip(self, num, position, scanner):
        if scanner:
            image = None
            if position[0] >= 5 and position[1] >= 5:
                if 0 <= num <= 90:
                    image = increase_animation_image(self.radarblipimages, num // 10)
            elif position[0] < 5 <= position[1]:
                if 270 < num <= 360:
                    image = increase_animation_image(self.radarblipimages, (num // 4) // 10)
            elif position[0] < 5 and position[1] < 5:
                if 180 < num <= 270:
                    image = increase_animation_image(self.radarblipimages, (num // 3) // 10)
            elif position[0] >= 5 > position[1]:
                if 90 < num <= 180:
                    image = increase_animation_image(self.radarblipimages, (num // 2) // 10)
            return image

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

    def take_turns(self, p1, p2):
        if p1.turn:
            p2.turn = False
        else:
            p2.turn = True
            if not p2.makeAttack(self.pGameLogic, self, TURNTIMER):
                p1.turn = True

    def check_for_winners(self, grid):
        validGame = True
        for row in grid:
            if 'O' in row:
                validGame = False
        return validGame