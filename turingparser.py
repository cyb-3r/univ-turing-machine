"""Contient les fonctions pour construire une machine de turing à partir de
fichiers

# Syntaxe du langage de machine de turing:

Un fichier est composé d'un en-tête suivi d'une liste de transitions.
Les lignes vides sont ignorées.
Les commentaires commencent par '#' et prennent la ligne entière.
Ne surtout pas mélanger des commentaires avec du code !

**Format** :

```none
<fichier>        ::= <en-tete> <transitions>

<en-tete>        ::= "name:" <string> "\n" "rubans:" <entier> "\n"

<transitions>    ::= <transition> | <transition> "\n" <transitions>

<transition>     ::= <etat_depart> "," <symboles_lus> ";" <etat_arrivee> "," <symboles_ecrits> "," <deplacements>

<etat_depart>    ::= <string>
<etat_arrivee>   ::= <string>

<symboles_lus>   ::= <symbole> | <symbole> <symboles_lus>
<symboles_ecrits>::= <symbole> | <symbole> <symboles_ecrits>
<symbole>        ::= <char> | "_"

<deplacements>   ::= <direction> | <direction> <deplacements>
<direction>      ::= "<" | "L" | "-" | "S" | ">" | "R"
```

- `<string>` est une chaîne de caractères ordinaire.
- `<char>` est un caractère de la table ASCII.

"""

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
    Créer une instance de `Transition` à partir d'une chaîne donnée

    Une transition s'écrit sous la forme q,a...;p,b...,D... où:
        - q est l'état de départ;
        - a... est une chaîne de lettres lues dans l'alphabet;
        - p est l'état d'arrivée;
        - b... est une chaîne de lettres écrites dans l'alphabet;
        - D... est une chaîne de déplacements parmis {<, -, >} <=> {L, S, R}
    """

    temp = code.split(";")
    
    current = temp[0].split(",")
    q = current[0].strip()
    a = tuple("".join(current[1:]).replace(" ", ""))

    next_state = temp[1].split(",")
    p = next_state[0].strip()
    
    rest = "".join(next_state[1:]).replace(" ", "")
    k = len(a)
    b = tuple(rest[:k])
    d = tuple(str_to_move(s) for s in rest[k:])

    return tt.Transition(q, a, p, b, d)


def parse_machine_file(path: str) -> tuple[str, int, list[tt.Transition]]:
    """Renvoie les éléments nécessaires à la construction d'une machine"""
    with open(path) as data:
        lines = [line for line in map(str.strip, data) if line and not line.startswith("#")]

    name = read_header_line(lines[0])
    rubans = int(read_header_line(lines[1]))
    transitions = [parse_transition(code) for code in lines[2:]]

    return (name, rubans, transitions)
