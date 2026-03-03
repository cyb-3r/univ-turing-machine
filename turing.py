from dataclasses import dataclass
from enum import Enum
from copy import deepcopy

BLANK: int = ord("_")
START: str = "I"
STOP: str = "F"
# ASCII
GAMMA: list[int] = [c for c in range(256)]
SIGMA: list[int] = [c for c in GAMMA if c != BLANK]


class Move(Enum):
    """
    Types de déplacement de la tête de lecture :
    - (L) LEFT  : déplace la tête de lecture vers la gauche;
    - (R) RIGHT : déplace la tête de lecture vers la droite;
    - (S) STAY  : ne déplace pas la tête de lecture.
    """

    LEFT = -1
    STAY = 0
    RIGHT = 1

    def __repr__(self):
        return "L" if self == Move.LEFT else "R" if self == Move.RIGHT else "S"

    def __str__(self):
        return self.__repr__()


@dataclass
class Transition(object):
    q_state: int
    r_symbol: str
    w_symbol: str
    move: Move
    p_state: int

    def __str__(self):
        return (
            f"δ({self.q_state}, {self.r_symbol}) = "
            f"({self.p_state}, {self.w_symbol}, {self.move})"
        )


class Configuration(object):
    """
    La configuration représente l'état de la machine à un temps donné.
    c = (u, v, q) où :
    - u est la bande avant la tête;
    - v est la bande après la tête inclus;
    - q est l'état actuel.

    u et v sont des piles contenant les symboles de la bande.
    """

    u: list[int]
    v: list[int]
    q: int

    def __init__(self, w: str):
        self.u = []
        self.v = list(reversed([ord(c) for c in w]))
        self.q = START

    def u_str(self):
        return "".join([chr(c) for c in self.u]) if len(self.u) > 0 else "_"

    def v_str(self):
        return "".join([chr(c) for c in reversed(self.v)]) if len(self.v) > 0 else "_"

    def __str__(self):
        return f"({self.u_str()}, {self.v_str()}, {self.q})"

    def __repr__(self):
        return self.__str__()

    def lire(self):
        if not self.v:
            self.v.append(BLANK)
        return self.v.pop()

    def ecrire(self, c: int):
        self.v.append(c)

    def deplacer(self, move: Move):
        match move:
            case Move.LEFT:
                self.v.append(self.u.pop())
            case Move.RIGHT:
                self.u.append(self.v.pop())
            case Move.STAY:
                pass


class TuringMachine(object):
    nom: str
    start: str
    transitions: dict[tuple[int, str], tuple[int, str, Move]]
    state: int

    def __init__(self, nom: str):
        self.nom = nom
        self.start = START
        self.transitions = {}

    def get_states(self) -> set[str]:
        return (
            {q for _, q in self.transitions.keys()}
            | {p for _, p, _ in self.transitions.values()}
            | {START, STOP}
        )

    def avec_transitions(self, *transitions: Transition):
        self.transitions = {
            (t.q_state, t.r_symbol): (t.p_state, t.w_symbol, t.move)
            for t in transitions
        }
        return self

    def add_transition(self, transition: Transition):
        self.transitions[(transition.q_state, transition.r_symbol)] = (
            transition.p_state,
            transition.w_symbol,
            transition.move,
        )
        return self

    def show_transition(self, q_state: int, r_symbol: str) -> str:
        p_state, w_symbol, move = self.transitions[(q_state, r_symbol)]
        return (
            f"δ({self.states[q_state]}, {r_symbol}) -> "
            f"({self.states[p_state]}, {w_symbol}, {move})"
        )

    def step(self, config: Configuration) -> Configuration:
        sym = config.lire()
        action = self.transitions.get((config.q, sym))
        if action is None:
            raise ValueError(f"Transition non définie pour ({config.q}, {sym})")
        p_state, w_symbol, move = action
        config.ecrire(w_symbol)
        config.deplacer(move)
        config.q = p_state
        return config

    def run_configs(self, mot: str) -> list[Configuration]:
        chemin: list[Configuration] = []
        config = Configuration(mot)
        while config.q != STOP:
            try:
                chemin.append(deepcopy(config))
                config = self.step(config)
            except ValueError as e:
                print(e)
                break
        chemin.append(deepcopy(config))
        return chemin

    def run(self, mot: str) -> bool:
        config = Configuration(mot)
        while config.q != STOP:
            try:
                config = self.step(config)
            except ValueError:
                return False
        return True

    def run_and_log(self, mot: str) -> bool:
        config = Configuration(mot)
        while config.q != STOP:
            try:
                print(config)
                config = self.step(config)
            except ValueError as e:
                print(e)
                return False
        print(config)
        return True

    def run_display(self, mot: str):
        print(" -> ".join(map(str, self.run_configs(mot))))


# Testing
if __name__ == "__main__":
    m = TuringMachine("Reader").avec_transitions(
        Transition(START, ord("a"), ord("a"), Move.RIGHT, "q1"),
        Transition("q1", ord("b"), ord("b"), Move.RIGHT, "q2"),
        Transition("q2", ord("c"), ord("c"), Move.RIGHT, "q3"),
        Transition("q3", BLANK, BLANK, Move.STAY, STOP),
    )
    print(m.transitions.keys(), m.transitions.values())
    print(m.get_states())
    m.run_display("abc")
    m.run_and_log("abc")
    print(f'"abc" est {"accepté" if m.run("abc") else "refusé"}')
