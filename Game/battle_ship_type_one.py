import random

from Game.battle_ships import BattleShips
from Utilities.ship import Ship
from Utilities.service import SCREENWIDTH, SCREENHEIGHT, load_image, increase_animation_image, get_font, BUTTONSOUND, \
    PLAYERLOSESOUND, PLAYERWINSOUND, PLAYINGSOUND, PLAYINGSOUND1, PLAYINGSOUND2
from Utilities.button import Button
import pygame
from Game.player import Player
from Machine.easy_computer import EasyComputer
from Machine.hard_computer import HardComputer
from GameSetting import battleship_10x10, battleship_20x20


class BattleShips_TypeOne(BattleShips):
    def __init__(self, numrows, numcolumns, graphic, numfleet, music):
        super().__init__(numrows, numcolumns, graphic, numfleet, music)
        if numrows == 10:
            self.size = battleship_10x10
        elif numrows == 20:
            self.size = battleship_20x20
        self.pos = (self.size.cellSizeX, self.size.cellSizeX)
        self.deployment = True
        self.scanner = False
        self.indnum = 0
        self.blipposition = None
        self.cFleet = []
        self.pFleet = []
        self.button = []
        self.tokens = []
        self.status = True
        self.pgamegriding = self.size.pgamegriding
        self.cgamegriding = self.size.cgamegriding
        self.redtoken = self.size.redtoken
        self.greentoken = self.size.greentoken
        self.bluetoken = self.size.bluetoken
        self.firetokenimagelist = self.size.firetokenimagelist
        self.explosionspritesheet = self.size.explosionspritesheet
        self.explosionimagelist = self.size.explosionimagelist
        self.radargridimages = self.size.radargridimages
        self.radarblipimages = self.size.radarblipimages
        self.radargrid = self.size.radargrid
        self.playerchoice = None
        self.player = Player()
        self.computer = None

    def create_grid(self):
        startx = self.pos[0]
        starty = self.pos[1]

        for row in range(self.numRows):
            rowx = []
            for col in range(self.numColums):
                rowx.append((startx, starty))
                startx += self.size.cellSizeY
            self.pGameGrid.append(rowx)
            startx = self.pos[0]
            starty += self.size.cellSizeY

        startx = SCREENWIDTH - (self.numRows * self.size.cellSizeY) - self.pos[0]
        starty = self.pos[1]
        for row in range(self.numRows):
            rowxc = []
            for col in range(self.numColums):
                rowxc.append((startx, starty))
                startx += self.size.cellSizeY
            self.cGameGrid.append(rowxc)
            startx = SCREENWIDTH - (self.numRows * self.size.cellSizeY) - self.pos[0]
            starty += self.size.cellSizeY

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
                        if pygame.rect.Rect(colX[0], colX[1], self.size.cellSizeY, self.size.cellSizeY).colliderect(
                                ship.rect):
                            self.pGameLogic[i][j] = 'O'

    def update_cgame_logic(self, coordGrid, shipList):
        for i, rowX in enumerate(coordGrid):
            for j, colX in enumerate(rowX):
                if self.cGameLogic[i][j] == 'T' or self.cGameLogic[i][j] == 'X':
                    continue
                else:
                    self.cGameLogic[i][j] = ' '
                    for ship in shipList:
                        if pygame.rect.Rect(colX[0], colX[1], self.size.cellSizeY, self.size.cellSizeY).colliderect(
                                ship.rect):
                            self.cGameLogic[i][j] = 'O'

    def show_grid_onscreen(self, window):
        gamegrid = [self.pGameGrid, self.cGameGrid]
        for grid in gamegrid:
            for row in grid:
                for col in row:
                    pygame.draw.rect(window, (255, 255, 255),
                                     (col[0], col[1], self.size.cellSizeY, self.size.cellSizeY), 1)

    def show_ship_onscreen(self, window, fleet, gamegrid, visible=False):
        for ship in fleet:
            if visible:
                ship.draw(window)
            ship.snap_to_grid_edge(gamegrid, self.size.cellNum)
            ship.snap_to_grid(gamegrid, self.size.cellSizeY)

    def show_button_onscreen(self, window, button):
        for buttonx in button:
            if buttonx.name in ['Randomize', 'Reset', 'Deploy', 'Back', 'Radar Scan', 'Redeploy']:
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
        FLEET = None
        if self.numfleet == 0:
            FLEET = self.size.FLEET
        elif self.numfleet == 1:
            FLEET = self.size.FLEET1
        elif self.numfleet == 2:
            FLEET = self.size.FLEET2
        elif self.numfleet == 3:
            FLEET = self.size.FLEET3
        elif self.numfleet == 4:
            FLEET = self.size.FLEET4
        elif self.numfleet == 5:
            FLEET = self.size.FLEET5
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

    def num_ship_available(self, fleet):
        num = 0
        for i in fleet:
            num += 1
        return num

    def num_ship_deployed(self, fleet):
        num = 0
        for i in fleet:
            if i.check_available():
                num += 1
        return num

    def create_button(self):
        BUTTONIMAGE = load_image(r'assets/images/buttons/button.png', (150, 50))
        BUTTONIMAGE1 = load_image(r'assets/images/buttons/button.png', (250, 100))
        self.button = [
            Button(BUTTONIMAGE, (150, 50), (25, SCREENHEIGHT - self.size.cellSizeX), 'Randomize'),
            Button(BUTTONIMAGE, (150, 50), (200, SCREENHEIGHT - self.size.cellSizeX), 'Reset'),
            Button(BUTTONIMAGE, (150, 50), (375, SCREENHEIGHT - self.size.cellSizeX), 'Deploy'),
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
                    yAxis = random.randint(0, self.numColums - 1)
                    xAxis = random.randint(0, self.numRows - 1 - (ship.hImage.get_width() // self.size.cellSizeY))
                    ship.rotate_ship(True)
                    ship.rect.topleft = gameGrid[yAxis][xAxis]
                else:
                    yAxis = random.randint(0, self.numColums - 1 - (ship.vImage.get_height() // self.size.cellSizeY))
                    xAxis = random.randint(0, self.numRows - 1)
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

    def take_turns(self, p1, p2, turntimer):
        if p1.turn:
            p2.turn = False
        else:
            p2.turn = True
            if not p2.makeAttack(self.pGameLogic, self, turntimer, self.numRows):
                p1.turn = True

    def check_for_winners(self, grid):
        validGame = True
        for row in grid:
            if 'O' in row:
                validGame = False
        return validGame

    def start_game(self, window, level):
        playmusic = None
        if self.music == 0:
            playmusic = PLAYINGSOUND
        elif self.music == 1:
            playmusic = PLAYINGSOUND1
        elif self.music == 2:
            playmusic = PLAYINGSOUND2
        playmusic.play(-1)
        if self.status:
            self.create_grid()
            self.create_fleet()
            self.create_logic()
            self.create_button()
            self.randomize_ship_positions(self.cFleet, self.cGameGrid)
        else:
            self.status = True

        if level == 1:
            self.computer = EasyComputer()
        elif level == 2:
            self.computer = HardComputer()

        flag = True
        turntimer = 0
        while flag:
            if (not self.status or self.check_for_winners(self.cGameLogic) or self.check_for_winners(
                    self.pGameLogic)) and not self.deployment:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.deployment:
                            for ship in self.pFleet:
                                if ship.rect.collidepoint(pygame.mouse.get_pos()):
                                    ship.active = True
                                    ship.select_ship_and_move(self.pFleet, self, window)
                                    self.sort_fleet(ship, self.pFleet)

                        else:
                            if self.player.turn:
                                turntimer = pygame.time.get_ticks()
                                self.player.makeAttack(self.cGameGrid, self.cGameLogic, self)

                        for button in self.button:
                            if button.rect.collidepoint(pygame.mouse.get_pos()):
                                if button.name == 'Deploy' and button.active and self.num_ship_deployed(
                                        self.pFleet) == self.num_ship_available(self.pFleet):
                                    self.deployment = False
                                    BUTTONSOUND.play()
                                elif button.name == 'Redeploy' and button.active:
                                    self.deployment = True
                                    BUTTONSOUND.play()
                                elif button.name == 'Back':
                                    self.playerchoice = 0
                                    BUTTONSOUND.play()
                                    playmusic.stop()
                                    flag = False
                                elif button.name == 'Radar Scan' and button.active:
                                    self.scanner = True
                                    self.indnum = 0
                                    self.blipposition = self.pick_random_ship_location(self.cGameLogic)
                                    BUTTONSOUND.play()
                                elif button.name == 'Randomize' and button.active:
                                    BUTTONSOUND.play()
                                elif button.name == 'Reset' and button.active:
                                    BUTTONSOUND.play()
                                button.action_on_press(self)

                    elif event.button == 2:
                        self.print_game_logic()

                    elif event.button == 3:
                        if self.deployment:
                            for ship in self.pFleet:
                                if ship.rect.collidepoint(
                                        pygame.mouse.get_pos()) and not ship.check_for_rotate_collisions(self.pFleet):
                                    ship.rotate_ship(True)

            if self.scanner:
                self.indnum += 1
            self.update_game_screen(window, 1)
            self.take_turns(self.player, self.computer, turntimer)

        if self.status and not self.playerchoice == 0 and not self.playerchoice == 1:
            self.end_screen(window)

    def update_game_screen(self, window, scene):
        if scene == 1:
            self.deployment_screen(window)
        elif scene == 2:
            self.end_screen(window)

        pygame.display.update()

    def deployment_screen(self, window):
        textstatus = ""
        if self.deployment:
            textstatus = "  DEPLOYING (" + str(self.num_ship_deployed(self.pFleet)) + "/" + str(
                self.num_ship_available(self.pFleet)) + ")   "
        else:
            textstatus = " PLAYING "

        if not self.graphic:
            bggame = load_image(r'assets/images/background/Black.png', (SCREENWIDTH, SCREENHEIGHT))
            window.blit(bggame, (0, 0))
            self.show_grid_onscreen(window)
            textstatus = get_font(39).render(textstatus, True, "White")

        elif self.graphic:
            bggame = load_image(r'assets/images/background/gamebg.png', (SCREENWIDTH, SCREENHEIGHT))
            window.blit(bggame, (0, 0))
            window.blit(self.pgamegriding, (self.size.cellSizeX // 2, self.size.cellSizeX // 2))
            window.blit(self.cgamegriding,
                        (self.cGameGrid[0][0][0] - self.size.cellSizeY, self.cGameGrid[0][0][1] - self.size.cellSizeY))
            textstatus = get_font(39).render(textstatus, True, "Black")

        testrect = textstatus.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 + 100))

        sign = pygame.image.load(r'assets\images\buttons\sign.png')
        sign_center = (testrect.centerx, testrect.centery)
        sign_top_left = (sign_center[0] - sign.get_width() // 4 + 25, sign_center[1] - sign.get_height() // 2 + 25)
        resized_sign = pygame.transform.scale(sign, (385, 200))

        window.blit(resized_sign, sign_top_left)
        window.blit(textstatus, testrect)

        #  Draws the player and computer grids to the screen
        #  Draw ships to screen
        self.show_ship_onscreen(window, self.pFleet, self.pGameGrid, True)
        self.show_ship_onscreen(window, self.cFleet, self.cGameGrid, True)
        self.show_button_onscreen(window, self.button)
        self.computer.draw(window, self)
        self.show_radar_scanner_onscreen(window)
        self.show_radar_blip_onscreen(window)
        self.show_token_onscreen(window, self.tokens)
        self.update_pgame_logic(self.pGameGrid, self.pFleet)
        self.update_cgame_logic(self.cGameGrid, self.cFleet)

    def end_screen(self, window):
        flag = True
        if not self.check_for_winners(self.cGameLogic):
            PLAYERLOSESOUND.play()
        else:
            PLAYERWINSOUND.play()
        while flag:
            bgendscreen = pygame.image.load(r'assets/images/background/Carrier.jpg')
            bgendscreen = pygame.transform.scale(bgendscreen, (SCREENWIDTH, SCREENHEIGHT))
            window.blit(bgendscreen, (0, 0))

            ""

            """Player win"""
            if self.check_for_winners(self.cGameLogic):
                result = " PLAYER WIN "
            else:
                result = " COMPUTER WIN"

            textcomputer = get_font(100).render(result, True, "Black")
            testrect = textcomputer.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 6))
            window.blit(textcomputer, testrect)

            BUTTONIMAGE = load_image(r'assets/images/buttons/button.png', (300, 100))

            self.show_grid_onscreen(window)
            #  Draw ships to screen
            self.show_ship_onscreen(window, self.pFleet, self.pGameGrid, True)
            self.show_ship_onscreen(window, self.cFleet, self.cGameGrid, True)
            self.show_token_onscreen(window, self.tokens)
            button = [
                Button(BUTTONIMAGE, (300, 100), ((SCREENWIDTH - 300) // 2, (SCREENHEIGHT - 100) // 2 - 150),
                       'Play Again'),
                Button(BUTTONIMAGE, (300, 100), ((SCREENWIDTH - 300) // 2, (SCREENHEIGHT - 100) // 2),
                       'Quit'),
            ]

            for buttonx in button:
                if buttonx.name in ['Play Again', 'Quit']:
                    buttonx.active = True
                    buttonx.draw(window, self.deployment)
                else:
                    buttonx.active = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for buttonx in button:
                            if buttonx.rect.collidepoint(pygame.mouse.get_pos()):
                                if buttonx.name == 'Play Again' and buttonx.active:
                                    BUTTONSOUND.play()
                                    self.playerchoice = 1
                                    PLAYERWINSOUND.stop()
                                    flag = False
                                elif buttonx.name == 'Quit' and buttonx.active:
                                    BUTTONSOUND.play()
                                    self.playerchoice = 0
                                    PLAYERWINSOUND.stop()
                                    flag = False
            pygame.display.update()
