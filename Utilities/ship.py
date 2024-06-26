from Utilities.service import load_image
import pygame
from Utilities.gun import Guns
class Ship:
    def __init__(self, name, img, pos, size, numGuns=0, gunPath=None, gunsize=None, gunCoordsOffset=None):
        self.name = name
        self.pos = pos
        #  Load the Vertical image
        self.vImage = load_image(img, size)
        self.vImageWidth = self.vImage.get_width()
        self.vImageHeight = self.vImage.get_height()
        self.vImageRect = self.vImage.get_rect()
        self.vImageRect.topleft = pos
        #  Load the Horizontal image
        self.hImage = pygame.transform.rotate(self.vImage, -90)
        self.hImageWidth = self.hImage.get_width()
        self.hImageHeight = self.hImage.get_height()
        self.hImageRect = self.hImage.get_rect()
        self.hImageRect.topleft = pos
        #  Image and Rectangle
        self.image = self.vImage
        self.rect = self.vImageRect
        self.rotation = False
        #  Utilities is current selection
        self.active = False
        self.available = True
        #  Load gun Images
        self.gunslist = []
        if numGuns > 0:
            self.gunCoordsOffset = gunCoordsOffset
            for num in range(numGuns):
                self.gunslist.append(
                    Guns(gunPath,
                             self.rect.center,
                             (size[0] * gunsize[0],
                              size[1] * gunsize[1]),
                             self.gunCoordsOffset[num])
                )

    def select_ship_and_move(self, pFleet, game, window):
        """Chọn thuyền và di chuyển nó theo chuột"""
        while self.active:
            self.rect.center = pygame.mouse.get_pos()
            game.update_game_screen(window, 1)
            for eventShip in pygame.event.get():
                if eventShip.type == pygame.MOUSEBUTTONDOWN:
                    if not self.check_for_collisions(pFleet):
                        if eventShip.button == 1:
                            if self.rotation:
                                self.vImageRect.center = self.hImageRect.center = self.rect.center
                            else:
                                self.hImageRect.center = self.vImageRect.center = self.rect.center
                            self.active = False
                            self.available = self.check_available()

                    """Chuột phải để thay đổi chiều"""
                    if eventShip.button == 3:
                        self.rotate_ship()

    def rotate_ship(self, doRotation=False):
        if self.active or doRotation == True:
            if self.rotation == False:
                self.rotation = True
            else:
                self.rotation = False
            self.switch_image_and_rect()

    def switch_image_and_rect(self):
        if self.rotation:
            self.image = self.hImage
            self.rect = self.hImageRect
        else:
            self.image = self.vImage
            self.rect = self.vImageRect
        self.hImageRect.center = self.vImageRect.center = self.rect.center

    def check_for_collisions(self, shiplist):
        slist = shiplist.copy()
        slist.remove(self)
        flag = False
        for item in slist:
            if self.rect.colliderect(item.rect):
                flag = True
        return flag

    def check_for_rotate_collisions(self, shiplist):
        slist = shiplist.copy()
        slist.remove(self)
        flag = False
        for ship in slist:
            if self.rotation == True:
                if self.vImageRect.colliderect(ship.rect):
                    flag = True
            else:
                if self.hImageRect.colliderect(ship.rect):
                    flag = True
        return flag

    def return_to_default_position(self):
        if self.rotation == True:
            self.rotate_ship(True)

        self.rect.topleft = self.pos
        self.hImageRect.center = self.vImageRect.center = self.rect.center

    def check_available(self):
        flag = True
        if self.rect.topleft == self.pos:
            flag = False
        return flag

    def snap_to_grid_edge(self, gridCoords, num):
        if self.rect.topleft != self.pos:
            if self.rect.left > gridCoords[0][-1][0] + num or \
                    self.rect.right < gridCoords[0][0][0] or \
                    self.rect.top > gridCoords[-1][0][1] + num or \
                    self.rect.bottom < gridCoords[0][0][1]:
                if not self.active:
                    self.return_to_default_position()

            elif self.rect.right > gridCoords[0][-1][0] + num:
                self.rect.right = gridCoords[0][-1][0] + num
            elif self.rect.left < gridCoords[0][0][0]:
                self.rect.left = gridCoords[0][0][0]
            elif self.rect.top < gridCoords[0][0][1]:
                self.rect.top = gridCoords[0][0][1]
            elif self.rect.bottom > gridCoords[-1][0][1] + num:
                self.rect.bottom = gridCoords[-1][0][1] + num
            self.vImageRect.center = self.hImageRect.center = self.rect.center

    def snap_to_grid(self, gridCoords, cellsize):
        for rowX in gridCoords:
            for cell in rowX:
                if self.rect.left >= cell[0] and self.rect.left < cell[0] + cellsize \
                        and self.rect.top >= cell[1] and self.rect.top < cell[1] + cellsize:
                    if self.rotation == False:
                        self.rect.topleft = (cell[0] + (cellsize - self.image.get_width()) // 2, cell[1])
                    else:
                        self.rect.topleft = (cell[0], cell[1] + (cellsize - self.image.get_height()) // 2)

        self.hImageRect.center = self.vImageRect.center = self.rect.center

    def draw(self, window):
        window.blit(self.image, self.rect)
        for guns in self.gunslist:
            guns.draw(window, self)
