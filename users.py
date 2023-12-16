import sqlite3
from user import User


class UsersList:

    _usersList: list[User] = []

    def __init__(self):
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        try:
            cur.execute("CREATE TABLE users(id, first_name, second_name, state, real_name, want, not_want, gift_user_id)")
        except Exception as ex:
            print(ex)
            pass

        result = list(cur.execute("SELECT * FROM users;").fetchall())

        for i in result:
            user = User(int(i[0]), i[1], i[2], i[3])
            user.from_db(i[4], i[5], i[6], int(i[7]))
            self._usersList.append(user)

        con.close()

    def addUser(self, new_user: User):
        self._usersList.append(new_user)
        con = sqlite3.connect("users.db")
        cur = con.cursor()

        cur.execute(f"""INSERT INTO users VALUES('{new_user.getId()}', '{new_user.getFirstName()}', '{new_user.getSecondName()}', 
                        '{new_user.getState()}', '{new_user.getRealName()}', '{new_user.getWant()}', '{new_user.getNotWant()}', '{new_user.getGiftUserId()}')""")
        con.commit()
        con.close()

    def getUserById(self, id: int) -> User | None:
        for i in self._usersList:
            if i.getId() == id:
                return i
        return None

    def getUsers(self) -> list[User]:
        return self._usersList

    def __str__(self):
        usersStr = ""
        for i in self._usersList:
            fullFlag = True
            if i.getRealName() == "-1":
                fullFlag = False
            if i.getWant() == "-1":
                fullFlag = False
            if i.getNotWant() == "-1":
                fullFlag = False
            profile = " Профиль не заполнен"
            square = "🟥"
            if fullFlag:
                square = "🟩"
                profile = " Профиль заполнен"

            usersStr += f"{square} {i.getUserLink()}: {profile}\n"
        return usersStr
