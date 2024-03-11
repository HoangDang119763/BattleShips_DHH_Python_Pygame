import pygame
from player import Player
from easy_computer import EasyComputer
from hard_computer import HardComputer

from battle_ship_type_one import BattleShips_TypeOne
from service import GAMESCREEN, GAMESTATE, updateGameScreen, STAGE

pygame.init()

game = BattleShips_TypeOne()
game.create_grid()
game.create_fleet()
game.create_logic()
game.create_button()
game.randomize_ship_positions(game.cFleet, game.cGameGrid)
player1 = Player()
computer = EasyComputer()
print(game.deployment)
print(GAMESTATE)
RUNGAME = True

while RUNGAME:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNGAME = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if game.deployment:
                    for ship in game.pFleet:
                        if ship.rect.collidepoint(pygame.mouse.get_pos()):
                            ship.active = True
                            game.sort_fleet(ship, game.pFleet)
                            ship.select_ship_and_move(game.pFleet, game, GAMESCREEN, GAMESTATE)

                else:
                    if player1.turn:
                        player1.makeAttack(game.cGameGrid, game.cGameLogic, game)
                for button in game.button:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        if button.name == 'Deploy' and button.active:
                            status = button.deployment_phase(game.deployment)
                            game.deployment = status
                        elif button.name == 'Redeploy' and button.active:
                            status = button.deployment_phase(game.deployment)
                            game.deployment = status
                            print(game.deployment)
                        elif button.name == 'Quit':
                            RUNGAME = False
                        elif button.name == 'Radar Scan' and button.active:
                            game.scanner = True
                            game.indnum = 0
                            game.blipposition = game.pick_random_ship_location(game.cGameLogic)
                        elif (button.name == 'Easy Computer' or button.name == 'Hard Computer') and button.active:
                            if button.name == 'Easy Computer':
                                computer = EasyComputer()
                            elif button.name == 'Hard Computer':
                                computer = HardComputer()
                            if GAMESTATE == 'Game Over':
                                game.tokens.clear()
                                for ship in game.pFleet:
                                    ship.returnToDefaultPosition()

                                game.randomize_ship_positions(game.cFleet, game.cGameGrid)
                                game.create_logic()
                                game.update_pgame_logic(game.pGameGrid, game.pFleet)
                                game.update_cgame_logic(game.cGameGrid, game.cFleet)
                                status = game.delployment_phase(game.deployment)
                                game.deployment = status
                            GAMESTATE = 'Deployment'
                            print(GAMESTATE)
                        button.action_on_press(game)

            elif event.button == 2:
                game.print_game_logic()

            elif event.button == 3:
                if game.deployment:
                    for ship in game.pFleet:
                        if ship.rect.collidepoint(pygame.mouse.get_pos()) and not ship.check_for_rotate_collisions(
                                game.pFleet):
                            ship.rotate_ship(True)

    updateGameScreen(GAMESCREEN, GAMESTATE, game)
    if game.scanner:
        game.indnum += 1

    if GAMESTATE == 'Deployment' and game.deployment != True:
        player1Wins = game.check_for_winners(game.cGameLogic)
        computerWins = game.check_for_winners(game.pGameLogic)
        if player1Wins or computerWins:
            GAMESTATE = STAGE[2]

    game.take_turns(player1, computer)

pygame.quit()
