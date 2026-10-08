#!/usr/bin/env python3

from collections import Counter

MAIZTASUNAK_EUSKARAZ = [
    "a", "i", "r", "e", "t", "o", "u", "n", "k",
    "l", "z", "s", "d", "g", "b", "m", "p",
    "h", "x", "f", "j", "c", "y", "v", "w", "q"
]

def kalkulatu_maiztasunak(testua: str) -> Counter:
    return Counter(
        karakterea.lower()
        for karakterea in testua
        if karakterea.isalpha() and karakterea.isascii()
    )

def sortu_ordezkapena(testua: str) -> dict[str, str]:
    maiztasunak = kalkulatu_maiztasunak(testua)
    letra_ordenatuak = sorted(
        maiztasunak,
        key=lambda letra: (-maiztasunak[letra], letra)
    )

    return {
        letra_zifratua: letra_garbia
        for letra_zifratua, letra_garbia in zip(
            letra_ordenatuak,
            MAIZTASUNAK_EUSKARAZ
        )
    }

def deszifratu(testua: str, ordezkapena: dict[str, str]) -> str:
    emaitza = ""

    for karakterea in testua:
        letra = karakterea.lower()

        if letra in ordezkapena:
            letra_berria = ordezkapena[letra]

            if karakterea.isupper():
                emaitza += letra_berria.upper()
            else:
                emaitza += letra_berria
        else:
            emaitza += karakterea

    return emaitza

def erakutsi_maiztasunak(testua: str) -> None:
    maiztasunak = kalkulatu_maiztasunak(testua)

    print("\nKriptogramaren maiztasunak:")
    print("-" * 30)

    for letra in sorted(
        maiztasunak,
        key=lambda letra: (-maiztasunak[letra], letra)
    ):
        print(f"{letra.upper()}: {maiztasunak[letra]}")

def zuzendu_ordezkapena(ordezkapena: dict[str, str]) -> None:
    while True:
        sarrera = input(
            "\nAldaketa (adibidez P=A, ENTER amaitzeko): "
        ).strip().lower()

        if not sarrera:
            break

        if "=" not in sarrera or sarrera.count("=") != 1:
            print("Formatua: P=A")
            continue

        zifratua, garbia = sarrera.split("=")

        if (
            len(zifratua) != 1
            or len(garbia) != 1
            or not zifratua.isalpha()
            or not garbia.isalpha()
        ):
            print("Letra bana idatzi behar dituzu.")
            continue

        ordezkapena[zifratua] = garbia

        print(f"{zifratua.upper()} → {garbia.upper()} aldatu da.")

def main() -> None:
    print("=" * 60)
    print("EUSKARAZKO ORDEZKAPEN-ZIFRATUAREN DESZIFRATZAILEA")
    print("=" * 60)

    testua = input("\nSartu deszifratu nahi duzun mezua:\n")

    if not testua.strip():
        print("Mezua ezin da hutsik egon.")
        return

    ordezkapena = sortu_ordezkapena(testua)

    print("\nMaiztasun-analisian oinarritutako deszifratzea:")
    print("-" * 60)
    print(deszifratu(testua, ordezkapena))

    print("\nOrain eskuz zuzendu dezakezu.")
    print("Aldatu zifratutako letra bat letra garbi batekin.")
    print("Adibidez: P=A")

    while True:
        zuzendu_ordezkapena(ordezkapena)

        print("\nDeszifratutako mezua:")
        print("-" * 60)
        print(deszifratu(testua, ordezkapena))

        berriro = input(
            "\nBeste hizkiren bat aldatu nahi duzu? [b/e]: "
        ).strip().lower()

        if berriro != "b":
            break

    print("\nAzken mezua:")
    print("-" * 60)
    print(deszifratu(testua, ordezkapena))

if __name__ == "__main__":
    main()
