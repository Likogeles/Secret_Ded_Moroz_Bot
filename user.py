import sqlite3

from userState import UserState


def stateFromStr(state_text: str) -> UserState:
    match state_text:
        case "UserState.setName":
            return UserState.setName
        case "UserState.setWant":
            return UserState.setWant
        case "UserState.setNotWant":
            return UserState.setNotWant
        case "UserState.waiting":
            return UserState.waiting
        case "UserState.inGame":
            return UserState.inGame
    return UserState.inGame


class User:
    _state: UserState = UserState.setWant
    _id: int = -1
    _first_name: str = "-1"
    _second_name: str = "-1"
    _real_name: str = "-1"
    _want: str = "-1"
    _not_want: str = "-1"
    _gift_user_id: int = -1

    def __init__(self, _id: int, _first_name: str, _second_name: str, _state: str):
        self._id = _id
        self._first_name = _first_name
        self._second_name = _second_name
        self._state = stateFromStr(_state)

    def from_db(self, _real_name: str, _want: str, _not_want: str, _gift_user_id: int):
        self._real_name = _real_name
        self._want = _want
        self._not_want = _not_want
        self._gift_user_id = _gift_user_id

    def getId(self) -> int:
        return self._id

    def setState(self, state: UserState):
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute(
            f"UPDATE users SET state = '{state}' WHERE id = '{self._id}';")
        con.commit()
        con.close()
        self._state = state

    def getState(self) -> UserState:
        return self._state

    def setGiftUserId(self, user_id: int):
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute(
            f"UPDATE users SET gift_user_id = '{user_id}' WHERE id = '{self._id}';")
        con.commit()
        con.close()
        self._gift_user_id = user_id

    def getGiftUserId(self) -> int:
        return self._gift_user_id

    def setRealName(self, real_name: str):
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute(
            f"UPDATE users SET real_name = '{real_name}' WHERE id = '{self._id}';")
        con.commit()
        con.close()
        self._real_name = real_name

    def getRealName(self) -> str:
        return self._real_name

    def setWant(self, want: str):
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute(
            f"UPDATE users SET want = '{want}' WHERE id = '{self._id}';")
        con.commit()
        con.close()
        self._want = want

    def getWant(self) -> str:
        return self._want

    def setNotWant(self, not_want: str):
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute(
            f"UPDATE users SET not_want = '{not_want}' WHERE id = '{self._id}';")
        con.commit()
        con.close()
        self._not_want = not_want

    def getNotWant(self) -> str:
        return self._not_want

    def getFirstName(self) -> str:
        return self._first_name

    def getSecondName(self) -> str:
        return self._second_name

    def getUserLink(self) -> str:
        return f'<a href="tg://user?id={self._id}">{self._real_name}</a>'
