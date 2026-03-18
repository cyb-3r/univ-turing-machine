from pprint import pprint
from copy import deepcopy
from turingparser import parse_machine_file, parse_transition
from turingtypes import Move, Transition

BLANK: int = ord("_")
START: str = "I"
STOP: str = "F"


class Configuration:
    """Représente l'état de la machine à un temps donné

    c = (u, v, q) où :
    - u est la bande avant la tête;
    - v est la bande après la tête inclus;
    - q est l'état actuel.

    u et v sont des piles contenant les symboles de la bande.
    """

    nb_ruban: int
    rubans: list[tuple[list[int], list[int]]]
    q: str

    def __init__(self, w: str, ruban: int = 1):
        self.nb_ruban = ruban
        v = list(reversed([ord(c) for c in w]))
        self.rubans = [([], v)]
        for _ in range(1, ruban):
            self.rubans.append(([], []))
        self.q = START

    def __str__(self):
        rubans_txt = ", ".join(
            f"({u}, {v})" for u, v in zip(self.u_str(), self.v_str())
        )
        return f"({rubans_txt}, {self.q})"

    def __repr__(self):
        return self.__str__()

    @property
    def u(self) -> list[list[int]]:
        return list(map(lambda x: x[0], self.rubans))

    @property
    def v(self) -> list[list[int]]:
        return list(map(lambda x: x[1], self.rubans))

    def u_str(self):
        return tuple(
            "".join([chr(c) for c in u]) if len(u) > 0 else "_" for u in self.u
        )

    def v_str(self):
        return tuple(
            "".join([chr(c) for c in reversed(v)]) if len(v) > 0 else "_"
            for v in self.v
        )

    def lire(self):
        symbols = []
        for i in range(self.nb_ruban):
            _, v = self.rubans[i]
            if len(v) == 0:
                v.append(BLANK)
            symbols.append(v.pop())
        return tuple(symbols)

    def ecrire(self, c: tuple[int, ...]):
        for i in range(self.nb_ruban):
            _, v = self.rubans[i]
            v.append(c[i])

    def deplacer(self, move: tuple[Move, ...]):
        for i in range(self.nb_ruban):
            u, v = self.rubans[i]
            match move[i]:
                case Move.LEFT:
                    v.append(u.pop() if u else BLANK)
                case Move.RIGHT:
                    u.append(v.pop() if v else BLANK)
                case Move.STAY:
                    pass


class TuringMachine:
    """Implémentation d'une machine de turing
    dont l'état est géré par la `Configuration`
    """

    nom: str
    transitions: dict[
        tuple[str, tuple[int, ...]], tuple[str, tuple[int, ...], tuple[Move, ...]]
    ]
    ruban: int

    def __init__(self, nom: str = "", ruban: int = 1):
        self.nom = nom
        self.ruban = ruban
        self.transitions = {}

    @classmethod
    def from_file(cls, path: str) -> "TuringMachine":
        nom, ruban, transitions = parse_machine_file(path)
        machine = cls(nom, ruban)
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
            sym_str = ",".join(chr(s) for s in sym)
            raise ValueError(f"Transition non définie pour ({config.q}, {sym_str})")
        p_state, w_symbol, move = action
        config.ecrire(w_symbol)
        config.deplacer(move)
        config.q = p_state
        return config

    def run_configs(self, mot: str) -> list[Configuration]:
        chemin: list[Configuration] = []
        config = Configuration(mot, self.ruban)
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
        config = Configuration(mot, self.ruban)
        while config.q != STOP:
            try:
                config = self.step(config)
            except ValueError:
                return "_"
        return " | ".join(
            [f"{u}{v}".strip("_") for u, v in zip(config.u_str(), config.v_str())]
        )

    def run_and_log(self, mot: str) -> bool:
        config = Configuration(mot, self.ruban)
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
    m = TuringMachine.from_file("./less.txt")
    pprint(m.run_configs("0001#0101"))
