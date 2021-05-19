def init_user(nickname: str, conn, c):
    """
    initialize new user

    :param nickname: user's nickname
    """
    with conn:
        c.execute(
            "INSERT INTO users VALUES (:nickname, :password, :points, :lvl)",
            {"nickname": nickname, "password": None, "points": None, "lvl": 1})


# def update_nickname(nickname: str, nickname: int) -> None:
#     """
#     update student's mail address
#
#     :param nickname:
#     :param nickname: id of the user
#     """
#     from main import conn, c
#     with conn:
#         c.execute("UPDATE users SET nickname = :nickname WHERE nickname = :nickname",
#                   {"nickname": nickname, "nickname": nickname})


def update_password(password: str, nickname: str, conn, c) -> None:
    """
    update student's mail password

    :param password: mail password
    :param nickname: id of the user
    """
    with conn:
        c.execute("UPDATE users SET password = :password WHERE nickname = :nickname",
                  {"password": password, "nickname": nickname})


def update_lvl(lvl: int, nickname: str, conn, c) -> None:
    """
    update student.letovo.ru password

    :param lvl: letovo analytics password
    :param nickname: id of the user
    """
    with conn:
        c.execute("UPDATE users SET lvl = :lvl WHERE nickname = :nickname",
                  {"lvl": lvl, "nickname": nickname})


def update_points(points: int, nickname: str, conn, c) -> None:
    """
    update student.letovo.ru login

    :param points: letovo analytics login
    :param nickname: id of the user
    """
    with conn:
        c.execute("UPDATE users SET points = :points WHERE nickname = :nickname",
                  {"points": points, "nickname": nickname})


def delete_user(nickname: str, conn, c) -> None:
    """
    delete user from DB

    :param nickname:
    :param conn:
    :param c:
    """
    with conn:
        c.execute("delete from users where nickname=:nickname", {"nickname": nickname})


def get_user(nickname: str, conn, c) -> tuple:
    """
    get user data

    :param nickname: user's nickname
    :return: user data
    """
    with conn:
        c.execute("SELECT * FROM users WHERE nickname=:nickname", {"nickname": nickname})
        return c.fetchone()
