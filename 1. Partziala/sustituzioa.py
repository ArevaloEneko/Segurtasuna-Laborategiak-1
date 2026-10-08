#!/usr/bin/env python3

from collections import Counter

MAIZTASUNAK_EUSKARAZ = [
    "A", "I", "R", "E", "T", "O", "U", "N", "K",
    "L", "Z", "S", "D", "G", "B", "M", "P",
    "H", "X", "F", "J", "C", "Y", "V", "W", "Q"
]


def kalkulatu_maiztasunak(testua: str) -> Counter:
    # Maiuskulak eta minuskulak sinbolo desberdinak dira
    return Counter(k for k in testua if k.isalpha() and k.isascii())


def sortu_ordezkapena(testua: str) -> dict[str, str]:
    maiztasunak = kalkulatu_maiztasunak(testua)
    ordenatuak = sorted(maiztasunak, key=lambda l: (-maiztasunak[l], l))
    return dict(zip(ordenatuak, MAIZTASUNAK_EUSKARAZ))


def deszifratu(testua: str, ordezkapena: dict[str, str]) -> str:
    return "".join(ordezkapena.get(k, k) for k in testua)


def aplikatu_aldaketa(
    ordezkapena: dict[str, str], oraingoa: str, nahi_dena: str
) -> None:
    """Pantailan 'oraingoa' ageri den tokian 'nahi_dena' jarri (trukea)."""
    for zifratua, garbia in list(ordezkapena.items()):
        if garbia == oraingoa:
            ordezkapena[zifratua] = nahi_dena
        elif garbia == nahi_dena:
            ordezkapena[zifratua] = oraingoa


def erakutsi_ordezkapena(ordezkapena: dict[str, str]) -> None:
    print("\nOraingo ordezkapena (zifratua → garbia):")
    print(", ".join(f"{z}→{g}" for z, g in sorted(ordezkapena.items())))


def main() -> None:
    print("=" * 60)
    print("EUSKARAZKO ORDEZKAPEN-ZIFRATUAREN DESZIFRATZAILEA")
    print("=" * 60)

    testua = input("\nSartu deszifratu nahi duzun mezua:\n")
    if not testua.strip():
        print("Mezua ezin da hutsik egon.")
        return

    ordezkapena = sortu_ordezkapena(testua)
    historia: list[dict[str, str]] = []

    print("\nMaiztasun-analisian oinarritutako deszifratzea:")
    print("-" * 60)
    print(deszifratu(testua, ordezkapena))

    print("\nOrain eskuz zuzendu dezakezu.")
    print("Idatzi: ikusten duzun letra = nahi duzun letra (adib. I=E).")
    print("Komandoak: '?' ordezkapena ikusi, '<' azken aldaketa desegin,")
    print("ENTER amaitzeko.")

    while True:
        sarrera = input("\nAldaketa: ").strip().upper()

        if not sarrera:
            break

        if sarrera == "?":
            erakutsi_ordezkapena(ordezkapena)
            continue

        if sarrera == "<":
            if historia:
                ordezkapena = historia.pop()
                print("Azken aldaketa desegin da.")
                print("-" * 60)
                print(deszifratu(testua, ordezkapena))
            else:
                print("Ez dago desegiteko ezer.")
            continue

        partes = [p.strip() for p in sarrera.split("=")]
        if len(partes) != 2 or any(len(p) != 1 or not p.isalpha() for p in partes):
            print("Formatua: I=E (letra bana alde bakoitzean).")
            continue

        oraingoa, nahi_dena = partes
        historia.append(dict(ordezkapena))
        aplikatu_aldaketa(ordezkapena, oraingoa, nahi_dena)

        print(f"\n{oraingoa} → {nahi_dena} aldatu da (biak trukatu dira).")
        print("\nMezua eguneratuta:")
        print("-" * 60)
        print(deszifratu(testua, ordezkapena))

    print("\nAzken mezua:")
    print("-" * 60)
    print(deszifratu(testua, ordezkapena))


if __name__ == "__main__":
    main()