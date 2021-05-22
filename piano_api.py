import logging as log
import sqlite3
import pygame
import threading
import sys
import numpy as np
import random
import time


def main(user_nickname) -> None:
    with sqlite3.connect("users.sqlite") as conn:
        log.debug("connected to db")
        c = conn.cursor()
        if not get_user((user_nickname := user_nickname.get_value()), conn, c):
            init_user(user_nickname, conn, c)
            log.debug("initializing user")
        else:
            log.debug("user found")

        class Piano:
            pygame.display.set_caption("Piano - game")
            clock = pygame.time.Clock()
            key_height = 120
            window_width, window_height = 600, 1000
            times = np.linspace(0.5, 0.6)
            surface = pygame.display.set_mode((window_width, window_height))
            keys_amount = 0
            score = 0
            rects = []
            jump = 1

            surface.fill((255, 255, 255))
            pygame.draw.line(surface, (128, 128, 128), [200, 0], [200, 1000], 5)
            pygame.draw.line(surface, (128, 128, 128), [400, 0], [400, 1000], 5)
            pygame.draw.line(surface, (128, 128, 128), [0, 52], [600, 52], 5)
            pygame.draw.line(surface, (255, 0, 0), [0, 800], [600, 800], 5)
            pygame.display.update()

            @classmethod
            def handle_events(cls) -> None:
                """
                handles events
                """
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        if highest_score < Piano.score:
                            update_points(Piano.score, user_nickname, conn, c)
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.KEYDOWN and event.key == 49:
                        for rect in cls.rects:
                            mid, bottom = rect.midbottom
                            if mid < 100 and bottom >= 800 >= bottom - cls.key_height:
                                pygame.draw.rect(cls.surface, (255, 255, 255), rect)
                                cls.rects.remove(rect)
                                cls.keys_amount -= 1
                                cls.score += 1
                                log.debug("LEFT")
                            # else:
                            #     log.debug("MISS")

                    elif event.type == pygame.KEYDOWN and event.key == 50:
                        for rect in cls.rects:
                            mid, bottom = rect.midbottom
                            if 400 > mid > 100 and bottom >= 800 >= bottom - cls.key_height:
                                pygame.draw.rect(cls.surface, (255, 255, 255), rect)
                                cls.rects.remove(rect)
                                cls.keys_amount -= 1
                                cls.score += 1
                                log.debug("MID")
                            # else:
                            #     log.debug("MISS")

                    elif event.type == pygame.KEYDOWN and event.key == 51:
                        for rect in cls.rects:
                            mid, bottom = rect.midbottom
                            if mid > 500 and bottom >= 800 >= bottom - cls.key_height:
                                pygame.draw.rect(cls.surface, (255, 255, 255), rect)
                                cls.rects.remove(rect)
                                cls.keys_amount -= 1
                                cls.score += 1
                                log.debug("RIGHT")
                            # else:
                            #     log.debug("MISS")

            @classmethod
            def draw_left_key(cls) -> None:
                """
                creates left key
                """
                rect = pygame.rect.Rect((0, 50, 198, cls.key_height))
                pygame.draw.rect(cls.surface, (0, 0, 0), rect)
                cls.rects.append(rect)
                cls.keys_amount += 1

            @classmethod
            def draw_middle_key(cls) -> None:
                """
                creates middle key
                """
                rect = pygame.rect.Rect((203, 50, 195, cls.key_height))
                pygame.draw.rect(cls.surface, (0, 0, 0), rect)
                cls.rects.append(rect)
                cls.keys_amount += 1

            @classmethod
            def draw_right_key(cls) -> None:
                """
                creates right key
                """
                rect = pygame.rect.Rect((403, 50, 200, cls.key_height))
                pygame.draw.rect(cls.surface, (0, 0, 0), rect)
                cls.rects.append(rect)
                cls.keys_amount += 1

            @classmethod
            def move_keys(cls) -> None:
                """
                moves keys
                """
                for rect in cls.rects:
                    pygame.draw.rect(cls.surface, (255, 255, 255), rect)
                    rect.move_ip(0, cls.jump)
                    pygame.draw.rect(cls.surface, (0, 0, 0), rect)
                    pygame.draw.line(cls.surface, (255, 0, 0), [0, 800], [600, 800], 5)
                    pygame.draw.line(cls.surface, (128, 128, 128), [0, 52], [600, 52], 5)
                    if rect.midbottom[1] > 1150:
                        pygame.draw.rect(cls.surface, (255, 255, 255), rect)
                        cls.keys_amount -= 1
                        log.debug("missed a key")
                        cls.rects.remove(rect)
                        if cls.score:
                            cls.score -= 1

            @classmethod
            def clear_rects(cls) -> None:
                """
                clears excess keys
                """
                if cls.keys_amount > 20:
                    pygame.draw.rect(cls.surface, (255, 255, 255), cls.rects[0])
                    del cls.rects[0]
                    cls.keys_amount -= 1

            @classmethod
            def set_music(cls, file: str) -> None:
                pygame.mixer.music.load(file)
                pygame.mixer.music.play(-1)

            @classmethod
            def generate_keys(cls) -> None:
                """
                generates new keys
                """
                log.debug("keys generator thread started")
                while True:
                    time.sleep(float(random.choice(cls.times)))
                    choose = random.randint(0, 2)
                    if choose == 0:
                        Piano.draw_left_key()
                    elif choose == 1:
                        Piano.draw_middle_key()
                    else:
                        Piano.draw_right_key()

            @classmethod
            def render_score(cls) -> None:
                pygame.draw.rect(Piano.surface, (255, 255, 255), (0, 0, 600, 50))
                score_text = segoeui_font.render(f"{highest_score} {Piano.score}", True, (255, 0, 0))
                Piano.surface.blit(score_text, (2, 0))

            @classmethod
            def set_speed(cls) -> None:
                """
                sets keys speed
                """
                # if Piano.score < 10:
                #     clock.tick(240)
                # cls.times = np.linspace(0.6, 0.9)
                # elif Piano.score < 30:
                Piano.clock.tick(360)
                cls.times = np.linspace(0.5, 0.6)
                # elif Piano.score < 80:
                #     Piano.jump = 2
                #     clock.tick(260)
                #     cls.times = np.linspace(0.25, 0.3)
                # elif Piano.score < 120:
                #     Piano.jump = 4
                #     clock.tick(240)
                # elif Piano.score < 300:
                #     Piano.jump = 4
                #     clock.tick(360)

        keys_generator_thread = threading.Thread(target=Piano.generate_keys, daemon=True)
        keys_generator_thread.start()
        segoeui_font = pygame.font.Font("/usr/share/fonts/WindowsFonts/segoeui.ttf", 36)
        highest_score = get_user(user_nickname, conn, c)[1]
        Piano.set_music("stal-c418.wav")

        log.debug("game thread started")
        try:
            while True:
                Piano.render_score()
                Piano.set_speed()
                Piano.move_keys()
                Piano.handle_events()
                Piano.clear_rects()
                pygame.display.update()
        except KeyboardInterrupt:
            if highest_score < Piano.score:
                update_points(Piano.score, user_nickname, conn, c)
            pygame.quit()
            sys.exit()


def init_user(
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> None:
    """
    initialize new user

    :param c: cursor
    :param conn: connection to db
    :param nickname: user's nickname
    """
    with conn:
        c.execute(
            "INSERT INTO users VALUES (:nickname, :highest_points, :lvl)",
            {"nickname": nickname, "highest_points": None, "lvl": 1})


def get_user(
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> tuple:
    """
    get user data

    :param c: cursor
    :param conn: connection to db
    :param nickname: user's nickname
    :return: user data
    """
    with conn:
        c.execute("select * from users where nickname=:nickname", {"nickname": nickname})
        return c.fetchone()


def delete_user(
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> None:
    """
    delete user from db

    :param nickname: user's nickname
    :param conn: connection to db
    :param c: cursor
    """
    with conn:
        c.execute("delete from users where nickname=:nickname", {"nickname": nickname})


def update_lvl(
        lvl: int,
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> None:
    """
    update user's level

    :param c: cursor
    :param conn: connection to db
    :param lvl: user's level
    :param nickname: user's nickname
    """
    with conn:
        c.execute("update users set lvl = :lvl where nickname = :nickname",
                  {"lvl": lvl, "nickname": nickname})


def update_points(
        highest_points: int,
        nickname: str,
        conn: sqlite3.Connection,
        c: sqlite3.Cursor
) -> None:
    """
    update user's highest_points

    :param c: cursor
    :param conn: connection to db
    :param highest_points: user's highest_points
    :param nickname: user's nickname
    """
    with conn:
        c.execute("update users set highest_points = :highest_points where nickname = :nickname",
                  {"highest_points": highest_points, "nickname": nickname})
