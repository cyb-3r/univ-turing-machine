import sys
from pprint import pprint

from turing import Configuration, TuringMachine
from turingparser import code_to_binary, machine_to_code


def main():
    if len(sys.argv) < 2:
        print("Usage: python tasks.py <qX>")
        return

    q = sys.argv[1]
    verbose = True if len(sys.argv) > 2 else False

    if q == "q1":
        print("Structure de TuringMachine et Configuration:")
        print("\nclass TuringMachine:")
        print("\tAttributs: nom, transitions, ruban")
        print(
            "\tMéthodes: from_file(path), add_transition(transition), step(config), run(mot), run_and_log(mot)"
        )
        pprint(TuringMachine.__dict__)

        print("\nclass Configuration:")
        print("\tAttributs: nb_ruban, rubans, q")
        print(
            "\tMéthodes: __init__(w, ruban), lire(), ecrire(c), deplacer(move), u_str(), v_str()"
        )
        print("\tPropriétés: u, v")
        pprint(Configuration.__dict__)

    elif q == "q2":
        path = "machines/less-2.txt"
        tm = TuringMachine.from_file(path)
        print(f"Machine: {tm.nom}")
        print(f"Rubans: {tm.ruban}")
        conf = Configuration("01#10", tm.ruban)
        print(f"Configuration initiale: {conf}")

    elif q == "q3":
        path = "machines/op-not.txt"
        tm = TuringMachine.from_file(path)
        conf = Configuration("01", tm.ruban)
        print(f"Machine: {tm.nom}")
        print(f"Configuration initiale: {conf}")
        tm.step(conf)
        print(f"après une étape: {conf}")

    elif q == "q4":
        path = "machines/op-not.txt"
        ipt = "110"
        tm = TuringMachine.from_file(path)
        result = tm.run(ipt)
        print(f"Machine: {tm.nom}")
        print(f"Entrée: {ipt}")
        print(f"Résultat: {result}")

    elif q == "q5":
        path = "machines/op-not.txt"
        tm = TuringMachine.from_file(path)
        print(f"Machine: {tm.nom}")
        print("Configurations:")
        tm.run_and_log("101")

    elif q == "q6":
        machines = [
            ("machines/less-2.txt", "01#10"),
            ("machines/search.txt", "10#00#11#10#01"),
            ("machines/unary-mult.txt", "11#111"),
        ]
        for path, word in machines:
            tm = TuringMachine.from_file(path)
            result = tm.run(word)
            print(f"Résultats (rubans): {result}\n")

    elif q == "q7":
        path = "machines/op-not.txt"
        nom = TuringMachine.from_file(path).nom
        code = machine_to_code(path)
        print(f"Code de la machine '{nom}':\n{code}")

    elif q == "q8":
        machines = [
            "machines/less-2.txt",
            "machines/search.txt",
            "machines/unary-mult.txt",
        ]
        for path in machines:
            nom = TuringMachine.from_file(path).nom
            binary = code_to_binary(path)
            print(f"\n--- Code binaire de la machine '{nom}' ---")
            print((binary[:100] + "...") if not verbose else binary)
            print(f"\n--- Entier représentant la machine '{nom}' ---")
            print("1" + ((binary[:99] + "...") if not verbose else binary))

    elif q == "q9":
        path = "machines/utm.txt"
        tm = TuringMachine.from_file(path)
        machine = "0|_|_|-|1|0|0|1|>|0|0|1|0|>|0"
        entree = "110011"
        print(f"Machine: {tm.nom}")
        print(f"<M>: {machine}")
        print(f"Entrée: {entree}")
        print("Configurations:")
        tm.run_and_log("#".join([machine, entree]))

    elif q == "q10":
        path = "machines/utm-cpt.txt"
        tm = TuringMachine.from_file(path)
        machine = "0|_|_|-|1|0|0|1|>|0|0|1|0|>|0"
        entree = "110011"
        pas = "11111"
        print(f"Machine: {tm.nom}")
        print(f"<M>: {machine}")
        print(f"Entrée: {entree}")
        print(f"Nombre de pas de calcul: {pas}")
        print("Configurations:")
        tm.run_and_log("#".join([machine, entree, pas]))

    else:
        print(f"Saisie invalide: {q}")


if __name__ == "__main__":
    main()
