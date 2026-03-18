import turingtypes as tt


def read_header_line(line: str) -> str:
    return line.split(":")[-1].strip()


def str_to_move(symbol: str) -> tt.Move:
    match symbol:
        case "<" | "L":
            return tt.Move.LEFT
        case "-" | "S":
            return tt.Move.STAY
        case ">" | "R":
            return tt.Move.RIGHT
        case _:
            return tt.Move.STAY


def parse_transition(code: str) -> tt.Transition:
    """
    Une transition s'écrit sous la forme q,a;p,a,D où:
        - q est l'état de départ;
        - a est une lettre dans l'alphabet;
        - p est l'état d'arrivée;
        - D est un élément parmis {<, -, >} <=> {L, S, R}
    """

    temp = code.split(";")
    current = temp[0].split(",")
    next_state = temp[1].split(",")

    q = current[0]
    a = tuple(current[1:])

    p = next_state[0]
    k = len(a)
    b = tuple(next_state[1 : 1 + k])
    d = tuple(str_to_move(s) for s in next_state[1 + k :])

    return tt.Transition(q, a, p, b, d)


def parse_machine_file(path: str) -> tuple[str, int, list[tt.Transition]]:
    with open(path) as data:
        lines = [line for line in map(str.strip, data) if line]

    name = read_header_line(lines[0])
    rubans = int(read_header_line(lines[1]))
    transitions = [parse_transition(code) for code in lines[2:]]

    return name, rubans, transitions
