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
    return tt.Transition(
        current[0], current[1][0], next_state[0], next_state[1][0], str_to_move(next_state[2])
    )


def parse_machine_file(path: str) -> tuple[str, list[tt.Transition]]:
    with open(path) as data:
        lines = [line for line in map(str.strip, data) if line]

    name = read_header_line(lines[0])
    transitions = [parse_transition(code) for code in lines[1:]]

    return name, transitions
