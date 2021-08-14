import firebase_admin
import yaml
import sqlite3

from firebase_admin import credentials, firestore
from typing import Optional

firebase_admin.initialize_app(
    credentials.Certificate("fbAdminConfig.json"))
db = firestore.client()


def update_data(
        chat_id: str,
        student_id: int = None,
        mail_address: str = None,
        mail_password: str = None,
        analytics_login: str = None,
        analytics_password: str = None,
        token: str = None
) -> None:
    """Fill out at least one param in every document!!! Otherwise all data in document will be erased"""
    pas = ""
    st = f'"student_id": {student_id},'
    ma = f'"mail_address": "{mail_address}",'
    mp = f'"mail_password": "{mail_password}",'
    al = f'"analytics_login": "{analytics_login}",'
    ap = f'"analytics_password": "{analytics_password}",'
    t = f'"token": "{token}",'

    request_payload: str = '''
    {
        "data": {''' + \
                           f'{st if student_id else pas}' + \
                           f'{ma if mail_address else pas}' + \
                           f'{mp if mail_password else pas}' + \
                           f'{al if analytics_login else pas}' + \
                           f'{ap if analytics_password else pas}' + \
                           f'{t if token else pas}' + \
                           '''},
                           "preferences": {
                               "lang": "en"
                           }
                       }
                       '''
    doc_ref = db.collection(u"users").document(chat_id)
    doc_ref.set(yaml.load(request_payload, Loader=yaml.FullLoader), merge=True)


def get_token(chat_id: str) -> Optional[str]:
    doc = db.collection(u"users").document(chat_id).get()
    try:
        if doc.exists:
            return doc.to_dict()["data"]["token"]
    except KeyError:
        pass
    return None


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
            "insert into users values (:nickname, :highest_points, :lvl)",
            {"nickname": nickname, "highest_points": 0, "lvl": 1})


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
