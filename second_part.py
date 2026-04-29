# TODO: renommer le fichier "codage.py"


def question_7(path: str) -> str:
    """Renvoie le code d'une machine a partir d'un fichier"""

    with open(path) as data:
        lines = [line for line in map(str.strip, data) if line]

    code = []
    t = len(lines)
    i = 0
    c = 2
    etats_c: dict = {}
    while i < t:
        if lines[i][0:4] == "init":
            etats_c[lines[i].split(":")[1].strip()] = 0
            i += 1
        elif lines[i][0:6] == "accept":
            etats_c[lines[i].split()[1].strip()] = 1
            i += 1
        elif (
            lines[i][0:2] == "//"
            or lines[i][0:4] == "name"
            or lines[i].isspace()
            or lines[i][0] == "\n"
        ):
            i += 1
            continue
        else:
            current = lines[i].split(",")
            next_state = lines[i + 1].split(",")
            if current[0] not in etats_c.keys():
                etats_c[current[0]] = c
                c += 1

            q = format(etats_c[current[0]], "b")
            a = current[1]

            if next_state[0] not in etats_c.keys():
                etats_c[next_state[0]] = c
                c += 1
            p = format(etats_c[next_state[0]], "b")
            b = next_state[1]
            d = next_state[2]

            code.append(f"{q}|{a}|{b}|{d}|{p}")
            i += 2

    return "|".join(code)


def question_8_1(path: str) -> str:
    code = question_7(path).split("|")
    t = len(code)
    i = 1
    while i < t:
        code[i] = str(format(ord(code[i]), "b"))
        code[i + 1] = str(format(ord(code[i + 1]), "b"))
        match code[i + 2]:
            case "<":
                code[i + 2] = "10"
            case "-":
                code[i + 2] = "00"
            case ">":
                code[i + 2] = "01"
        i += 5
    return question_8_2("|".join(code))


def question_8_2(code: str) -> str:
    c = []
    for i in code:
        match i:
            case "0":
                c.append("00")
            case "1":
                c.append("01")
            case "|":
                c.append("10")

    return "".join(c)


print(question_7("./less.txt"))
# print(question_7("./test3.txt"))
# print(question_7("./test4.txt"))
# print(question_7("./test5.txt"))
# print(question_8_1("./test5.txt"))
