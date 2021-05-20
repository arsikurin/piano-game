import sqlite3
import pygame_menu
from colourlib import *
from piano_api import *
from pygame_menu.examples import create_example_window

DEBUG = True
if DEBUG:
    log.basicConfig(format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset} %(message)s{Style.Reset}", level=log.DEBUG)
else:
    log.basicConfig(format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset} %(message)s{Style.Reset}")

with sqlite3.connect("users.sqlite") as conn:
    log.debug("connected to db")
    # c = conn.cursor()
    # nickname = input(f"{Style.Bold}Enter nickname1 ->{Style.Reset}")
    #
    # if not get_user(nickname, conn, c):
    #     init_user(nickname, conn, c)
    #     log.debug("initializing user")
    #     if (password := input(f"{Style.Bold}Enter your password ->{Style.Reset}")) != input(
    #             f"{Style.Bold}Enter your password again ->{Style.Reset}"):
    #         delete_user(nickname, conn, c)
    #         print(f"{Fg.Red}Passwords do not match!")
    #         print(Style.Bold + "Restart the game" + Style.Reset)
    #         sys.exit()
    #     else:
    #         log.debug("password set")
    #         update_password(password, nickname, conn, c)
    #
    # else:
    #     log.debug("user found")
    #     if input(f"{Style.Bold}Enter your password ->{Style.Reset}") != get_user(nickname, conn, c)[1]:
    #         print(f"{Fg.Red}Passwords do not match!")
    #         print(f"{Style.Bold}Restart the game" + Style.Reset)
    #         sys.exit()
    # log.debug("user in")

    pygame.init()
    menu_surface = create_example_window("Piano - menu", (600, 400))

    menu = pygame_menu.Menu(
        height=400,
        theme=pygame_menu.themes.THEME_SOLARIZED_DARK,
        title="Piano",
        width=600
    )

    user_name = menu.add.text_input("Nickname: ", default="3p1c Cl1ck3r", maxchar=24)
    # menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button("Play", main)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    log.debug("menu set")
    menu.mainloop(menu_surface)
