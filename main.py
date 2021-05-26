from piano_api import *
from pygame_menu.examples import create_example_window

DEBUG = True
if DEBUG:
    log.basicConfig(format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset} %(message)s{Style.Reset}", level=log.DEBUG)
else:
    log.basicConfig(format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset} %(message)s{Style.Reset}")


def start() -> None:
    """
    calls main function
    """
    main(user_nickname, game_mode)


def set_game_mode(a: tuple[tuple[str, int], int], b: int) -> None:
    """
    sets game mode

    :param a: a tuple consisting of callback data and a tuple with name and position
    :param b: callback data
    """
    global game_mode
    game_mode = a


game_mode = (("Endless", 1), 0)
pygame.init()
pygame.font.init()
pygame.mixer.init()
menu_surface = create_example_window("Piano - menu", (600, 400))

try:
    menu = pygame_menu.Menu(
        height=400,
        theme=pygame_menu.themes.THEME_SOLARIZED_DARK,
        title="Piano",
        width=600
    )
except AttributeError:
    log.debug("THEME_SOLARIZED_DARK not found. Switching to THEME_DARK")
    menu = pygame_menu.Menu(
        height=400,
        theme=pygame_menu.themes.THEME_DARK,
        title="Piano",
        width=600
    )
user_nickname = menu.add.text_input("Nickname: ", default="3p1c Cl1ck3r", maxchar=24)
menu.add.selector("Game mode: ", [("Endless", 1), ("Normal", 2), ("Hardcore", 3)], onchange=set_game_mode)
menu.add.button("Play", start)
menu.add.button("Quit", pygame_menu.events.EXIT)
log.debug("menu set")
menu.mainloop(menu_surface)
