from service import increase_animation_image


class BattleShips:
    pGameGrid = []
    pGameLogic = []
    cGameGrid = []
    cGameLogic = []

    def __init__(self, numrows, numcolums, cellsize, pos):
        self.numRows = numrows
        self.numColums = numcolums
        self.cellSize = cellsize
        self.pos = pos

        self.pGameGrid = []
        self.pGameLogic = []
        self.cGameGrid = []
        self.cGameLogic = []

    def create_grid(self):
        pass

    def create_logic(self):
        pass

    def show_grid_onscreen(self, window):
        pass

    def update_pgame_logic(self, coordGrid, shipList):
        pass

    def update_cgame_logic(self, coordGrid, shipList):
        pass

    def print_game_logic(self):
        print('Player Grid'.center(50, '#'))
        for _ in self.pGameLogic:
            print(_)

        print('Computer Grid'.center(50, '#'))
        for _ in self.cGameLogic:
            print(_)

    def sort_fleet(self, ship, shipList):
        pass

    def randomize_ship_positions(self, shiplist, gamegrid):
        pass

    def delployment_phase(self, deployment):
        pass

    def pick_random_ship_location(self, gameLogic):
        pass

    @staticmethod
    def display_radar_scanner(imagelist, indnum, SCANNER):
        if SCANNER and indnum <= 359:
            image = increase_animation_image(imagelist, indnum)
            return image
        else:
            return False

    def display_radar_blip(self, num, position):
        pass

