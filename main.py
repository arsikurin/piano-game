import sys
import pygame
import logging as log
import sqlite3
from colourlib import *
from piano_api import *

DEBUG = True

if DEBUG:
    log.basicConfig(format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset} %(message)s{Style.Reset}", level=log.DEBUG)
else:
    log.basicConfig(format=f"{Fg.Green}{Style.Bold}%(asctime)s{Fg.Reset} %(message)s{Style.Reset}")


def draw():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (1, 1, 100, 100), 0)


with sqlite3.connect("users.sqlite") as conn:
    c = conn.cursor()
    nickname = input(f"{Style.Bold}Enter nickname1 ->{Style.Reset}")

    if not get_user(nickname, conn, c):
        init_user(nickname, conn, c)
        log.debug("initializing user")
        if (password := input(f"{Style.Bold}Enter your password ->{Style.Reset}")) != input(
                f"{Style.Bold}Enter your password again ->{Style.Reset}"):
            delete_user(nickname, conn, c)
            print(f"{Fg.Red}Passwords do not match!")
            print(Style.Bold + "Restart the game" + Style.Reset)
            sys.exit()
        else:
            log.debug("password set")
            update_password(password, nickname, conn, c)

    else:
        log.debug("user found")
        if input(f"{Style.Bold}Enter your password ->{Style.Reset}") != get_user(nickname, conn, c)[1]:
            print(f"{Fg.Red}Passwords do not match!")
            print(f"{Style.Bold}Restart the game" + Style.Reset)
            sys.exit()
    log.debug("user in")

    pygame.init()
    screen = pygame.display.set_mode((1200, 800))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            draw()
            pygame.display.flip()
