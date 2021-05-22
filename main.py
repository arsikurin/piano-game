import pygame_menu
from colourlib import *
from piano_api import *
from pygame_menu.examples import create_example_window

DEBUG = True
if DEBUG:
    log.basicConfig(format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset} %(message)s{Style.Reset}", level=log.DEBUG)
else:
    log.basicConfig(format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset} %(message)s{Style.Reset}")


def start():
    main(user_nickname)


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
# menu.add.selector("Difficulty :", [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button("Play", start)
menu.add.button("Quit", pygame_menu.events.EXIT)
log.debug("menu set")
menu.mainloop(menu_surface)
