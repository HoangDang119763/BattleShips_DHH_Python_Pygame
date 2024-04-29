import pygame

SCREENWIDTH = 1530
SCREENHEIGHT = 775
NUMROWS = 10
NUMCOLS = 10
cellSizeY = (SCREENHEIGHT // 2) // (NUMROWS)
cellSizeX = (SCREENWIDTH // 2) // (NUMCOLS)
CELLSIZE = cellSizeY
STAGE = ['Main Menu', 'Deployment', 'Game Over']
GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Battle Ships')
icon = pygame.image.load(r'assets\images\background\icon.png')
pygame.display.set_icon(icon)

bg = None


def load_image(path, size, rotate=False):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    if rotate:
        img = pygame.transform.rotate(img, -90)
    return img


def load_animation_images(path, aniNum, size):
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


def get_font(size):
    return pygame.font.Font(r'assets/images/font/font.ttf', size)


pygame.mixer.init()

HITSOUND = pygame.mixer.Sound(r'assets/sounds/sounds/explosion.wav')
SHOTSOUND = pygame.mixer.Sound(r'assets/sounds/sounds/gunshot.wav')
MISSSOUND = pygame.mixer.Sound(r'assets/sounds/sounds/splash.wav')
BUTTONSOUND = pygame.mixer.Sound(r'assets/sounds/sounds/buttonsound.mp3')
PLAYERLOSESOUND = pygame.mixer.Sound(r'assets/sounds/sounds/playerlose.mp3')
PLAYERWINSOUND = pygame.mixer.Sound(r'assets/sounds/sounds/playerwin.mp3')
PLAYINGSOUND = pygame.mixer.Sound(r'assets/sounds/sounds/playing.mp3')
PLAYINGSOUND1= pygame.mixer.Sound(r'assets/sounds/sounds/playing1.mp3')
PLAYINGSOUND2 = pygame.mixer.Sound(r'assets/sounds/sounds/playing2.mp3')
HITSOUND.set_volume(0.05)
SHOTSOUND.set_volume(0.05)
MISSSOUND.set_volume(0.05)
MISSSOUND.set_volume(0.05)
BUTTONSOUND.set_volume(10)
PLAYERLOSESOUND.set_volume(0.9)
PLAYERWINSOUND.set_volume(0.15)
PLAYINGSOUND.set_volume(0.05)
PLAYINGSOUND1.set_volume(0.05)
PLAYINGSOUND2.set_volume(0.05)


def set_volume(status):
    if status:
        HITSOUND.set_volume(0.05)
        SHOTSOUND.set_volume(0.05)
        MISSSOUND.set_volume(0.05)
        MISSSOUND.set_volume(0.05)
        BUTTONSOUND.set_volume(10)
        PLAYERLOSESOUND.set_volume(0.9)
        PLAYERWINSOUND.set_volume(0.15)
        PLAYINGSOUND.set_volume(0.05)
        PLAYINGSOUND1.set_volume(0.05)
        PLAYINGSOUND2.set_volume(0.05)
    else:
        HITSOUND.set_volume(0)
        SHOTSOUND.set_volume(0)
        MISSSOUND.set_volume(0)
        MISSSOUND.set_volume(0)
        BUTTONSOUND.set_volume(0)
        PLAYERLOSESOUND.set_volume(0)
        PLAYERWINSOUND.set_volume(0)
        PLAYINGSOUND.set_volume(0)
        HITSOUND.stop()
        SHOTSOUND.stop()
        MISSSOUND.stop()
        MISSSOUND.stop()
        BUTTONSOUND.stop()
        PLAYERLOSESOUND.stop()
        PLAYERWINSOUND.stop()
        PLAYINGSOUND.stop()
        PLAYINGSOUND1.stop()
        PLAYINGSOUND2.stop()

