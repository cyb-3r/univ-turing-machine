from copy import deepcopy

from turingparser import parse_machine_file, parse_transition
from turingtypes import Move, Transition

BLANK: int = ord("_")
START: str = "I"
STOP: str = "F"


class Configuration:
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
    q: str

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
        if len(self.v) == 0:
            self.v.append(BLANK)
        return self.v.pop()

    def ecrire(self, c: int):
        self.v.append(c)

    def deplacer(self, move: Move):
        match move:
            case Move.LEFT:
                self.v.append(self.u.pop() if self.u else BLANK)
            case Move.RIGHT:
                self.u.append(self.v.pop() if self.v else BLANK)
            case Move.STAY:
                pass


class TuringMachine:
    nom: str
    transitions: dict[tuple[str, int], tuple[str, int, Move]]

    def __init__(self, nom: str = ""):
        self.nom = nom
        self.transitions = {}

    @classmethod
    def from_file(cls, path: str) -> "TuringMachine":
        nom, transitions = parse_machine_file(path)
        machine = cls(nom)
        for t in transitions:
            machine.add_transition(t)
        return machine

    def with_transitions(self, *code: str):
        for c in code:
            self.add_transition(parse_transition(c))
        return self

    def add_transition(self, transition: Transition):
        self.transitions[(transition.q_state, transition.r_symbol)] = (
            transition.p_state,
            transition.w_symbol,
            transition.move,
        )
        return self

    def step(self, config: Configuration) -> Configuration:
        sym = config.lire()
        action = self.transitions.get((config.q, sym))
        if action is None:
            raise ValueError(f"Transition non définie pour ({config.q}, {chr(sym)})")
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

    def run(self, mot: str) -> str:
        config = Configuration(mot)
        while config.q != STOP:
            try:
                config = self.step(config)
            except ValueError:
                return "_"
        return "".join([config.u_str(), config.v_str()])

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


def display_chemin(configs: list[Configuration]):
    print(" -> ".join(map(str, configs)))


# Testing
if __name__ == "__main__":
    m = TuringMachine.from_file("./test_machine.txt")
    display_chemin(m.run_configs("abc"))
    print(m.run("abc"))
