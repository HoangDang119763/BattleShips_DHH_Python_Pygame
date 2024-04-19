import pygame
import pygame_menu
import pygame.mixer

import Utilities.service
from Utilities.service import SCREENWIDTH, SCREENHEIGHT, get_font, BUTTONSOUND, set_volume
from Game.battle_ship_type_one import BattleShips_TypeOne


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.music1 = True
        self.graphic = True
        self.selectorSize = None
        self.selectorLevel = None
        self.selectorFleet = None
        self.selectorMusic = None
        self.menuTheme = pygame_menu.Theme(
            background_color=pygame_menu.baseimage.BaseImage(r'assets\images\background\backroundplay.jpg'),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            title=False,
            widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(arrow_size=(80, 80)).set_background_color(
                pygame_menu.baseimage.BaseImage(r'assets\images\buttons\buttonselect.png'))
        )

        self.menu_playTheme = pygame_menu.Theme(
            background_color=pygame_menu.baseimage.BaseImage(r'assets\images\background\Carrier.jpg'),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            title=False,
            widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(arrow_size=(80, 80)).set_background_color(
                pygame_menu.baseimage.BaseImage(r'assets\images\buttons\buttonselect.png'))
        )

        self.menu_customTheme = pygame_menu.Theme(
            background_color=pygame_menu.baseimage.BaseImage(r'assets\images\background\cruiser.jpg'),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            title=False,
            widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(arrow_size=(80, 80)).set_background_color(
                pygame_menu.baseimage.BaseImage(r'assets\images\buttons\buttonselect.png'))
        )

        self.menu_optionTheme = pygame_menu.Theme(
            background_color=pygame_menu.baseimage.BaseImage(r'assets\images\background\Destroyer.jpg'),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            title=False,
            widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(arrow_size=(80, 80)).set_background_color(
                pygame_menu.baseimage.BaseImage(r'assets\images\buttons\buttonselect.png'))
        )

        """Menu List"""
        self.menu = pygame_menu.Menu(
            height=SCREENHEIGHT,
            theme=self.menuTheme,
            title='',
            width=SCREENWIDTH,
            center_content=False,
            mouse_motion_selection=True

        )

        self.menu_play = pygame_menu.Menu(
            height=SCREENHEIGHT,
            theme=self.menu_playTheme,
            title='',
            width=SCREENWIDTH,
            center_content=False,
            mouse_motion_selection=True

        )

        self.menu_custom = pygame_menu.Menu(
            height=SCREENHEIGHT,
            theme=self.menu_customTheme,
            title='',
            width=SCREENWIDTH,
            center_content=False,
            mouse_motion_selection=True

        )

        self.menu_option = pygame_menu.Menu(
            height=SCREENHEIGHT,
            theme=self.menu_optionTheme,
            title='',
            width=SCREENWIDTH,
            center_content=False,
            mouse_motion_selection=True

        )

        """Main menu"""
        self.menu.add.label("MENU",
                            font_name=get_font(100),
                            font_color=(0, 0, 0),
                            padding=(30, 60),
                            ).translate(0, 50).set_background_color(pygame_menu.baseimage.BaseImage(r'assets\images\buttons\sign.png'))

        self.menu.add.button('PLAY', self.play,
                             font_color=(255, 255, 255),
                             font_name=get_font(70),
                             align=pygame_menu.locals.ALIGN_CENTER,
                             cursor=pygame_menu.locals.CURSOR_HAND,
                             padding=(5, 60),
                             background_color=pygame_menu.baseimage.BaseImage(r'assets\images\buttons\button.png'),
                             ).translate(0, 80).set_max_width(280)

        self.menu.add.button('CUSTOM', action=self.custom,
                             font_color=(255, 255, 255),
                             font_name=get_font(70),
                             align=pygame_menu.locals.ALIGN_CENTER,
                             cursor=pygame_menu.locals.CURSOR_HAND,
                             padding=(5, 60),
                             background_color=pygame_menu.baseimage.BaseImage(r'assets\images\buttons\button.png')
                             ).translate(0, 110).set_max_width(280)

        self.menu.add.button('OPTION', action=self.option,
                             font_color=(255, 255, 255),
                             font_name=get_font(70),
                             align=pygame_menu.locals.ALIGN_CENTER,
                             cursor=pygame_menu.locals.CURSOR_HAND,
                             padding=(5, 60),
                             background_color=pygame_menu.baseimage.BaseImage(r'assets\images\buttons\button.png')
                             ).translate(0, 140).set_max_width(280)

        self.menu.add.button('QUIT', action=self.quit,
                             font_color=(255, 255, 255),
                             font_name=get_font(70),
                             align=pygame_menu.locals.ALIGN_CENTER,
                             cursor=pygame_menu.locals.CURSOR_HAND,
                             padding=(5, 60),
                             background_color=pygame_menu.baseimage.BaseImage(r'assets\images\buttons\button.png')
                             ).translate(0, 170).set_max_width(280)

        """PLay menu"""
        self.menu_play.add.label("PLAY",
                                 font_name=get_font(100),
                                 font_color=(0, 0, 0),
                                 padding=(30, 60)
                                 ).translate(0, 50).set_background_color(pygame_menu.baseimage.BaseImage(r'assets\images\buttons\sign.png'))

        self.menu_play.add.button('GAME 10x10 - EASY', self.start_game_typeone10x10_easy,
                                  font_color=(255, 255, 255),
                                  font_name=get_font(50),
                                  align=pygame_menu.locals.ALIGN_CENTER,
                                  cursor=pygame_menu.locals.CURSOR_HAND,
                                  padding=(5, 60),
                                  background_color=pygame_menu.baseimage.BaseImage(r'assets\images\buttons\button.png')
                                  ).translate(0, 80).set_max_width(600)

        self.menu_play.add.button('GAME 10x10 - HARD', self.start_game_typeone10x10_hard,
                                  font_color=(255, 255, 255),
                                  font_name=get_font(50),
                                  align=pygame_menu.locals.ALIGN_CENTER,
                                  cursor=pygame_menu.locals.CURSOR_HAND,
                                  padding=(5, 60),
                                  background_color=pygame_menu.baseimage.BaseImage(r'assets\images\buttons\button.png')
                                  ).translate(0, 110).set_max_width(600)

        self.menu_play.add.button('GAME 20x20 - EASY', self.start_game_typeone20x20_easy,
                                  font_color=(255, 255, 255),
                                  font_name=get_font(50),
                                  align=pygame_menu.locals.ALIGN_CENTER,
                                  cursor=pygame_menu.locals.CURSOR_HAND,
                                  padding=(5, 60),
                                  background_color=pygame_menu.baseimage.BaseImage(r'assets\images\buttons\button.png')
                                  ).translate(0, 140).set_max_width(600)

        self.menu_play.add.button('GAME 20x20 - HARD', self.start_game_typeone20x20_hard,
                                  font_color=(255, 255, 255),
                                  font_name=get_font(50),
                                  align=pygame_menu.locals.ALIGN_CENTER,
                                  cursor=pygame_menu.locals.CURSOR_HAND,
                                  padding=(5, 60),
                                  background_color=pygame_menu.baseimage.BaseImage(r'assets\images\buttons\button.png')
                                  ).translate(0, 170).set_max_width(600)

        self.menu_play.add.button('QUIT', self.back,
                                  font_color=(255, 255, 255),
                                  font_name=get_font(60),
                                  align=pygame_menu.locals.ALIGN_CENTER,
                                  cursor=pygame_menu.locals.CURSOR_HAND,
                                  padding=(5, 60),
                                  background_color=pygame_menu.baseimage.BaseImage(r'assets\images\buttons\button.png')
                                  ).translate(0, 200).set_max_width(300)

        """Custom menu"""
        self.menu_custom.add.label("CUSTOM",
                                   font_name=get_font(100),
                                   font_color=(0, 0, 0),
                                   padding=(30, 60),
                                   ).translate(0, 50).set_background_color(pygame_menu.baseimage.BaseImage(r'assets\images\buttons\sign.png'))

        items = [('10 x 10', 10, 10),
                 ('20 x 20', 20, 20)]
        self.selectorSize = self.menu_custom.add.selector(
            title='Size:',
            padding=(20, 150),
            items=items,
            align=pygame_menu.locals.ALIGN_CENTER,
            selection_effect=pygame_menu.widgets.HighlightSelection(),
            cursor=pygame_menu.locals.CURSOR_HAND,
            font_color=(0, 0, 0),
            font_name=get_font(40),
            style=pygame_menu.widgets.SELECTOR_STYLE_FANCY,
            style_fancy_bgcolor=pygame_menu.themes.TRANSPARENT_COLOR,
            style_fancy_bordercolor=pygame_menu.themes.TRANSPARENT_COLOR,
            style_fancy_arrow_color=(0, 0, 0),
            style_fancy_arrow_margin=(10, 10, 0),
            background_color=(pygame_menu.baseimage.BaseImage(r'assets\images\buttons\setting.png'))
        ).translate(50, 80).set_max_width(600)

        levels = [('EASY', 1),
                  ('HARD', 2)]
        self.selectorLevel = self.menu_custom.add.selector(
            title='Level:',
            padding=(20, 150),
            items=levels,
            align=pygame_menu.locals.ALIGN_CENTER,
            selection_effect=pygame_menu.widgets.HighlightSelection(),
            cursor=pygame_menu.locals.CURSOR_HAND,
            font_color=(0, 0, 0),
            font_name=get_font(40),
            style=pygame_menu.widgets.SELECTOR_STYLE_FANCY,
            style_fancy_bgcolor=pygame_menu.themes.TRANSPARENT_COLOR,
            style_fancy_bordercolor=pygame_menu.themes.TRANSPARENT_COLOR,
            style_fancy_arrow_color=(0, 0, 0),
            style_fancy_arrow_margin=(10, 10, 0),
            background_color=(pygame_menu.baseimage.BaseImage(r'assets\images\buttons\setting.png'))
        ).translate(50, 110).set_max_width(600)

        fleets = [('0', 0),
                  ('1', 1),
                  ('2', 2),
                  ('3', 3),
                  ('4', 4),
                  ('5', 5)]
        self.selectorFleet = self.menu_custom.add.selector(
            title='Fleet:',
            padding=(20, 150),
            items=fleets,
            align=pygame_menu.locals.ALIGN_CENTER,
            selection_effect=pygame_menu.widgets.HighlightSelection(),
            cursor=pygame_menu.locals.CURSOR_HAND,
            font_color=(0, 0, 0),
            font_name=get_font(40),
            style=pygame_menu.widgets.SELECTOR_STYLE_FANCY,
            style_fancy_bgcolor=pygame_menu.themes.TRANSPARENT_COLOR,
            style_fancy_bordercolor=pygame_menu.themes.TRANSPARENT_COLOR,
            style_fancy_arrow_color=(0, 0, 0),
            style_fancy_arrow_margin=(10, 10, 0),
            background_color=(pygame_menu.baseimage.BaseImage(r'assets\images\buttons\setting.png'))
        ).translate(50, 140).set_max_width(600)

        self.menu_custom.add.button('GAME CUSTOM', self.start_game_custom,
                                    font_color=(255, 255, 255),
                                    font_name=get_font(40),
                                    align=pygame_menu.locals.ALIGN_CENTER,
                                    cursor=pygame_menu.locals.CURSOR_HAND,
                                    padding=(5, 60),
                                    background_color=pygame_menu.baseimage.BaseImage(
                                        r'assets\images\buttons\button.png')
                                    ).translate(0, 170).set_max_width(300)

        self.menu_custom.add.button('QUIT', self.back,
                                    font_color=(255, 255, 255),
                                    font_name=get_font(40),
                                    align=pygame_menu.locals.ALIGN_CENTER,
                                    cursor=pygame_menu.locals.CURSOR_HAND,
                                    padding=(5, 60),
                                    background_color=pygame_menu.baseimage.BaseImage(
                                        r'assets\images\buttons\button.png')
                                    ).translate(0, 200).set_max_width(300)

        """Option menu"""
        self.menu_option.add.label("OPTION",
                                   font_name=get_font(100),
                                   font_color=(0, 0, 0),
                                   padding=(30, 60)
                                   ).translate(0, 50).set_background_color(pygame_menu.baseimage.BaseImage(r'assets\images\buttons\sign.png'))

        self.menu_option.add.toggle_switch('Music:', self.music1,
                                           width=390,
                                           font_name=get_font(40),
                                           font_color=(0, 0, 0),
                                           padding=(20, 150),
                                           selection_effect=pygame_menu.widgets.HighlightSelection(),
                                           align=pygame_menu.locals.ALIGN_CENTER,
                                           state_text=('OFF', 'ON'),
                                           slider_color=(64, 64, 64),
                                           state_color=((255, 0, 0), (0, 255, 33)),
                                           switch_margin=(40, 0),
                                           state_text_font_color=((0, 0, 0), (255, 255, 255)),
                                           switch_height=0.7,
                                           switch_border_width=1,
                                           cursor=pygame_menu.locals.CURSOR_HAND,
                                           background_color=(
                                               pygame_menu.baseimage.BaseImage(r'assets\images\buttons\setting.png'))
                                           ).translate(50, 80).set_onchange(self.toggle_music)

        self.menu_option.add.toggle_switch('Graphic:', self.graphic,
                                           width=340,
                                           font_name=get_font(40),
                                           font_color=(0, 0, 0),
                                           padding=(20, 150),
                                           selection_effect=pygame_menu.widgets.HighlightSelection(),
                                           align=pygame_menu.locals.ALIGN_CENTER,
                                           state_text=('OFF', 'ON'),
                                           slider_color=(64, 64, 64),
                                           state_color=((255, 0, 00), (0, 255, 33)),
                                           switch_margin=(40, 0),
                                           state_text_font_color=((0, 0, 0), (255, 255, 255)),
                                           switch_height=0.7,
                                           switch_border_width=1,
                                           cursor=pygame_menu.locals.CURSOR_HAND,
                                           background_color=(pygame_menu.baseimage.BaseImage(r'assets\images\buttons\setting.png')),
                                           ).translate(50, 110).set_onchange(self.toggle_graphic)

        fleets = [('0', 0),
                  ('1', 1),
                  ('2', 2)]
        self.selectorMusic = self.menu_option.add.selector(
            title='List Music:',
            padding=(20, 150),
            items=fleets,
            align=pygame_menu.locals.ALIGN_CENTER,
            selection_effect=pygame_menu.widgets.HighlightSelection(),
            cursor=pygame_menu.locals.CURSOR_HAND,
            font_color=(0, 0, 0),
            font_name=get_font(50),
            style=pygame_menu.widgets.SELECTOR_STYLE_FANCY,
            style_fancy_bgcolor=pygame_menu.themes.TRANSPARENT_COLOR,
            style_fancy_bordercolor=pygame_menu.themes.TRANSPARENT_COLOR,
            style_fancy_arrow_color=(0, 0, 0),
            style_fancy_arrow_margin=(10, 10, 0),
            background_color=(pygame_menu.baseimage.BaseImage(r'assets\images\buttons\setting.png')),
            background_width=600
        ).translate(50, 140)

        self.menu_option.add.button('QUIT', self.back,
                                    font_color=(255, 255, 255),
                                    font_name=get_font(80),
                                    align=pygame_menu.locals.ALIGN_CENTER,
                                    cursor=pygame_menu.locals.CURSOR_HAND,
                                    padding=(5, 60),
                                    background_color=pygame_menu.baseimage.BaseImage(
                                        r'assets\images\buttons\button.png')
                                    ).translate(0, 200).set_max_width(300)

    def run(self):
        self.menu.mainloop(self.screen)

    def quit(self):
        BUTTONSOUND.play()
        self.menu.disable()
        pygame.quit()

    def play(self):
        BUTTONSOUND.play()
        self.menu_play.mainloop(self.screen)

    def custom(self):
        BUTTONSOUND.play()
        self.menu_custom.mainloop(self.screen)

    def option(self):
        BUTTONSOUND.play()
        self.menu_option.mainloop(self.screen)

    def back(self):
        BUTTONSOUND.play()
        self.menu.mainloop(self.screen)

    def loop(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()
            self.menu.mainloop(self.screen, events)

    def toggle_music(self, value):
        self.music1 = value
        set_volume(self.music1)

    def toggle_graphic(self, value):
        self.graphic = value

    def start_game_typeone10x10_easy(self):
        BUTTONSOUND.play()
        music = self.selectorMusic.get_value()[0][1]
        print("Play game Game 10x10 easy")
        game = BattleShips_TypeOne(10, 10, self.graphic, 0, music)
        game.start_game(self.screen, 1)
        if game.playerchoice == 1:
            self.start_game_typeone10x10_easy()

    def start_game_typeone10x10_hard(self):
        BUTTONSOUND.play()
        music = self.selectorMusic.get_value()[0][1]
        print("Play game Game 10x10 hard")
        game = BattleShips_TypeOne(10, 10, self.graphic, 0, music)
        game.start_game(self.screen, 2)
        if game.playerchoice == 1:
            self.start_game_typeone10x10_hard()

    def start_game_typeone20x20_easy(self):
        BUTTONSOUND.play()
        music = self.selectorMusic.get_value()[0][1]
        print("Play game Game 20x20 easy")
        game = BattleShips_TypeOne(20, 20, self.graphic, 0, music)
        game.start_game(self.screen, 1)
        if game.playerchoice == 1:
            self.start_game_typeone20x20_easy()

    def start_game_typeone20x20_hard(self):
        BUTTONSOUND.play()
        music = self.selectorMusic.get_value()[0][1]
        print("Play game Game 20x20 hard")
        game = BattleShips_TypeOne(20, 20, self.graphic, 0, music)
        game.start_game(self.screen, 2)
        if game.playerchoice == 1:
            self.start_game_typeone20x20_easy()

    def start_game_custom(self):
        BUTTONSOUND.play()
        music = self.selectorMusic.get_value()[0][1]
        print("Play game Game 20x20 hard")
        row = self.selectorSize.get_value()[0][1]
        col = self.selectorSize.get_value()[0][2]
        level = self.selectorLevel.get_value()[0][1]
        fleet = self.selectorFleet.get_value()[0][1]
        game = BattleShips_TypeOne(row, col, self.graphic, fleet, music)
        game.start_game(self.screen, level)
        if game.playerchoice == 1:
            self.start_game_custom()
