from enum import Enum


class UserState(Enum):
    setName = 1
    setWant = 2
    setNotWant = 3
    waiting = 4
    inGame = 5
