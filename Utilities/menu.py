import pygame_menu
from Utilities.service import SCREENWIDTH, SCREENHEIGHT, get_font, BUTTONSOUND


class Option:
    def __init__(self, screen):
        self.screen = screen
        self.menuTheme = pygame_menu.Theme(
            background_color=pygame_menu.baseimage.BaseImage(r'assets\images\background\backroundplay.jpg'),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            title=False,
            widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(arrow_size=(50, 50)).set_background_color(
                (0, 10, 51))
        )
        self.menu = pygame_menu.Menu(
            height=SCREENHEIGHT,
            theme=self.menuTheme,
            title='',
            width=SCREENWIDTH,
            center_content=False,
            mouse_motion_selection=True

        )
        self.menu.add.label("OPTION",
                            font_name=get_font(100),
                            font_color=(0, 0, 0)
                            ).translate(0, 50)

        self.menu.add.toggle_switch('Music', True,
                                    width=150,
                                    font_name=get_font(50),
                                    font_color=(255, 255, 255),
                                    padding=0,
                                    selection_effect=pygame_menu.widgets.NoneSelection(),
                                    align=pygame_menu.locals.ALIGN_CENTER,
                                    state_text=('OFF', 'ON'),
                                    slider_color=(48, 94, 140),
                                    state_color=((255, 255, 255), (8, 14, 58)),
                                    switch_margin=(50, 0),
                                    state_text_font_color=((8, 14, 58), (255, 255, 255)),
                                    switch_height=0.8,
                                    switch_border_width=1,
                                    cursor=pygame_menu.locals.CURSOR_HAND,
                                    ).translate(0, 50)
        self.menu.add.button('QUIT', action=self.quit,
                             font_color=(255, 255, 255),
                             font_name=get_font(40),
                             align=pygame_menu.locals.ALIGN_CENTER,
                             border_width=1,
                             cursor=pygame_menu.locals.CURSOR_HAND,
                             font_size=24,
                             padding=(5, 45),
                             border_color=(0, 0, 0),
                             background_color=(60, 60, 60)
                             ).translate(0, 225)

    def run(self):
        self.menu.mainloop(self.screen)

    def quit(self):
        BUTTONSOUND.play()
        self.menu.disable()
        pygame_menu.events.EXIT
    def loop(self):
        self.menu.mainloop(self.screen)

