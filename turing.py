from copy import deepcopy

import turingparser as tp
import utils

BLANK: int = ord("_")
START: str = "I"
STOP: str = "F"


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

    def deplacer(self, move: utils.Move):
        match move:
            case utils.Move.LEFT:
                self.v.append(self.u.pop())
            case utils.Move.RIGHT:
                self.u.append(self.v.pop())
            case utils.Move.STAY:
                pass


class TuringMachine(object):
    nom: str
    # Transitions[q, a] -> [p, a', D]
    transitions: dict[tuple[str, int], tuple[str, int, utils.Move]]
    state: int

    def __init__(self, path: str):
        with open(path) as data:
            txt = list(
                filter(lambda x: len(x) > 0, [s.strip() for s in data.readlines()])
            )
            print(txt)
            self.nom = tp.read_header_line(txt.pop(0))

            self.transitions = {}

            for code in txt:
                self.add_transition(tp.parse_transition(code))

    def avec_transitions(self, *transitions: utils.Transition):
        self.transitions = {
            (t.q_state, t.r_symbol): (t.p_state, t.w_symbol, t.move)
            for t in transitions
        }
        return self

    def with_transitions(self, *code: str):
        self.transitions = {
            (t.q_state, t.r_symbol): (t.p_state, t.w_symbol, t.move)
            for t in map(lambda s: tp.parse_transition(s), code)
        }
        return self

    def add_transition(self, transition: utils.Transition):
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
            raise ValueError(f"utils.Transition non définie pour ({config.q}, {sym})")
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
    # m = TuringMachine("Test").with_transitions(
    #     "I,a;q1,c,>", "q1,b;q2,b,>", "q2,c;q3,a,>", "q3,_;F,_,-"
    # )
    m = TuringMachine("./test_machine.txt")
    display_chemin(m.run_configs("abc"))
    print(m.run("abc"))
