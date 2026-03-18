from enum import Enum


class Move(Enum):
    """
    Types de déplacement de la tête de lecture :
    - (<) LEFT  : déplace la tête de lecture vers la gauche;
    - (>) RIGHT : déplace la tête de lecture vers la droite;
    - (-) STAY  : ne déplace pas la tête de lecture.
    """

    LEFT = 2  # 0b10
    STAY = 0  # 0b00
    RIGHT = 1  # 0b01

    def __repr__(self):
        return "L" if self == Move.LEFT else "R" if self == Move.RIGHT else "S"

    def __str__(self):
        return self.__repr__()


class Transition(object):
    q_state: str
    r_symbol: int
    p_state: str
    w_symbol: int
    move: Move

    def __init__(self, q: str, a: str, p: str, b: str, d: Move) -> None:
        self.q_state = q
        self.p_state = p
        self.r_symbol = ord(a[0])
        self.w_symbol = ord(b[0])
        self.move = d

    def __str__(self):
        return (
            f"δ({self.q_state}, {self.r_symbol}) = "
            f"({self.p_state}, {self.w_symbol}, {self.move})"
        )
