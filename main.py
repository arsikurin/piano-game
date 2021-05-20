# import pygame
# import logging as log
import threading
import sqlite3
from colourlib import *
from piano_api import *

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
    clock = pygame.time.Clock()
    times = np.linspace(0.35, 0.6)
    key_generator_thread = threading.Thread(target=keys_generator, daemon=True)
    key_generator_thread.start()

    while True:
        segoeui_font = pygame.font.Font("/usr/share/fonts/WindowsFonts/segoeui.ttf", 36)
        pygame.draw.rect(Piano.surface, (255, 255, 255), (0, 0, 600, 50))
        score_text = segoeui_font.render(f"Score: {Piano.score}", True, (255, 0, 0))
        Piano.surface.blit(score_text, (2, 0))
        pygame.display.update()

        speed_setter()
        Piano.mover()
        Piano.handle_events()
        pygame.display.update()
        Piano.clear_rects()
