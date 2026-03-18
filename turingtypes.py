from enum import Enum


class Move(Enum):
    """
    Types de déplacement de la tête de lecture :
    - (<|L) LEFT  : déplace la tête de lecture vers la gauche;
    - (>|R) RIGHT : déplace la tête de lecture vers la droite;
    - (-|S) STAY  : ne déplace pas la tête de lecture.
    """

    LEFT = 2  # 0b10
    STAY = 0  # 0b00
    RIGHT = 1  # 0b01

    def __repr__(self):
        return "L" if self == Move.LEFT else "R" if self == Move.RIGHT else "S"

    def __str__(self):
        return self.__repr__()


class Transition:
    q_state: str
    r_symbol: tuple[int, ...]
    p_state: str
    w_symbol: tuple[int, ...]
    move: tuple[Move, ...]

    def __init__(
        self,
        q: str,
        a: tuple[str, ...],
        p: str,
        b: tuple[str, ...],
        d: tuple[Move, ...],
    ) -> None:
        self.q_state = q
        self.p_state = p
        self.r_symbol = tuple(ord(c[0]) for c in a)
        self.w_symbol = tuple(ord(c[0]) for c in b)
        self.move = d

    def __str__(self):
        r_str = "".join(chr(c) for c in self.r_symbol)
        w_str = "".join(chr(c) for c in self.w_symbol)
        m_str = "".join(str(m) for m in self.move)
        return f"δ({self.q_state}, {r_str}) = ({self.p_state}, {w_str}, {m_str})"
