import utils


def _read_header_line(line: str) -> str:
    return line.split(":")[-1].strip()


def _str_to_move(symbol: str) -> utils.Move:
    match symbol:
        case "<":
            return utils.Move.LEFT
        case "-":
            return utils.Move.STAY
        case ">":
            return utils.Move.RIGHT
        case _:
            return utils.Move.STAY


def process_transition(code: str):
    """
    Une transition s'écrit sous la forme q,a;p,a,D où:
        - q est l'état de départ;
        - a est une lettre dans l'alphabet;
        - p est l'état d'arrivée;
        - D est un élément parmis {<, -, >} <=> {L, S, R}
    """

    temp = code.split(";")
    current, next = temp[0].split(","), temp[1].split(",")
    print(f"d({current[0]}, {current[1]}) = ({next[0]}, {next[1]}, {next[2]})")
    return utils.Transition(
        current[0], current[1][0], next[0], next[1][0], _str_to_move(next[2])
    )


def parsefile(path: str):
    with open(path) as data:
        txt = list(filter(lambda x: len(x) > 0, [s.strip() for s in data.readlines()]))
        print(txt)
        name = _read_header_line(txt.pop(0))
        start = _read_header_line(txt.pop(0))
        halt = _read_header_line(txt.pop(0))
        print(name, start, halt)

        for code in txt:
            process_transition(code)


if __name__ == "__main__":
    parsefile("./test_machine.txt")
