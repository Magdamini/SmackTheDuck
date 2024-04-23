from enum import Enum, auto

class GameStates(Enum):
    MAP = auto()
    START = auto()
    SELECT_PLAYER = auto()
    SELECT_ANIMAL = auto()
    END = auto()
    BATTLE = auto()
