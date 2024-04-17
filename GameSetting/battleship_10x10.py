from service import SCREENHEIGHT, SCREENWIDTH, load_animation_images, load_sprite_sheet_images, load_image
import pygame

row = 10
col = 10

cellSizeY = (SCREENHEIGHT // 2) // row
cellSizeX = (SCREENWIDTH // 2) // col

cellNum = 50

pgamegriding = load_image('assets/images/grids/player_grid.png',
                          ((row + 1) * cellSizeY, (col + 1) * cellSizeY))
cgamegriding = load_image('assets/images/grids/comp_grid.png',
                          ((row + 1) * cellSizeY, (col + 1) * cellSizeY))
redtoken = load_image('assets/images/tokens/redtoken.png', (cellSizeY, cellSizeY))
greentoken = load_image('assets/images/tokens/greentoken.png', (cellSizeY, cellSizeY))
bluetoken = load_image('assets/images/tokens/bluetoken.png', (cellSizeY, cellSizeY))
firetokenimagelist = load_animation_images('assets/images/tokens/fireloop/fire1_ ', 13,
                                           (cellSizeY, cellSizeY))
explosionspritesheet = pygame.image.load(
    'assets/images/tokens/explosion/explosion.png').convert_alpha()
explosionimagelist = []
for row in range(8):
    for col in range(8):
        explosionimagelist.append(
            load_sprite_sheet_images(explosionspritesheet, row, col, (cellSizeY, cellSizeY),
                                     (128, 128)))
radargridimages = load_animation_images('assets/images/radar_base/radar_anim', 360,
                                        ((row + 3) * cellSizeY, (col + 3) * cellSizeY))
radarblipimages = load_animation_images('assets/images/radar_blip/Blip_', 11, (cellSizeY, cellSizeY))
radargrid = load_image('assets/images/grids/grid_faint.png', ((row + 3) * cellSizeY, (col + 3) * cellSizeY))

FLEET = {
    """Giữa"""
    'battleship': ['battleship', 'assets/images/ships/battleship/battleship.png',
                   (SCREENWIDTH // 2, cellSizeX),
                   (30, cellSizeY * 4 - 5),
                   4, 'assets/images/ships/battleship/battleshipgun.png', (0.4, 0.125),
                   [-0.525, -0.34, 0.67, 0.49]],
    """Giữa bên trái 1 đơn vị"""
    'cruiser': ['cruiser', 'assets/images/ships/cruiser/cruiser.png',
                (SCREENWIDTH // 2 - cellSizeX, cellSizeX),
                (30, cellSizeY * 5 - 5),
                2, 'assets/images/ships/cruiser/cruisergun.png', (0.4, 0.125), [-0.36, 0.64]],
    """Giữa bên trái 2 đơn vị"""
    'destroyer': ['destroyer', 'assets/images/ships/destroyer/destroyer.png',
                  (SCREENWIDTH // 2 - cellSizeX * 2, cellSizeX), (30, cellSizeY * 3 - 5),
                  2, 'assets/images/ships/destroyer/destroyergun.png', (0.5, 0.15), [-0.52, 0.71]],
    """Giữa bên trái 3 đơn vị"""
    'patrol boat': ['patrol boat', 'assets/images/ships/patrol boat/patrol boat.png',
                    (SCREENWIDTH // 2 - cellSizeX * 3, cellSizeX), (25, cellSizeY * 2 - 5),
                    0, '', None, None],
    """Giữa bên phải 1 đơn vị"""
    'carrier': ['carrier', 'assets/images/ships/carrier/carrier.png',
                (SCREENWIDTH // 2 + cellSizeX, cellSizeX),
                (30, cellSizeY * 4),
                0, '', None, None],
    """Giữa bên phải 2 đơn vị"""
    'submarine': ['submarine', 'assets/images/ships/submarine/submarine.png',
                  (SCREENWIDTH // 2 + cellSizeX * 2, cellSizeX), (30, 145),
                  1, 'assets/images/ships/submarine/submarinegun.png', (0.25, 0.125), [-0.45]],
    """Giữa bên phải 3 đơn vị"""
    'rescue ship': ['rescue ship', 'assets/images/ships/rescue ship/rescue ship.png',
                    (SCREENWIDTH // 2 + cellSizeX * 3, cellSizeX), (25, cellSizeY * 2 - 5),
                    0, '', None, None]
}
