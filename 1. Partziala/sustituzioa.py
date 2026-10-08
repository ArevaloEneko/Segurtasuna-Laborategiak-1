#!/usr/bin/env python3

from collections import Counter

MAIZTASUNAK_EUSKARAZ = [
    "a", "i", "r", "e", "t", "o", "u", "n", "k",
    "l", "z", "g", "d", "s", "b", "m", "p",
    "h", "x", "f", "j", "c", "y", "v", "w", "q"
]

def kalkulatu_maiztasunak(testua: str) -> Counter:
    return Counter(karakterea.lower() for karakterea in testua if karakterea.isalpha() and karakterea.isascii())

def sortu_ordena(maiztasunak: Counter) -> list[str]:
    return sorted(maiztasunak, key=lambda letra: (-maiztasunak[letra], letra))

def sortu_ordezkapena(letra_ordenatuak: list[str]) -> dict[str, str]:
    return {
        letra: argia
        for letra, argia in zip(letra_ordenatuak, MAIZTASUNAK_EUSKARAZ)
    }

def deszifratu(testua: str, ordezkapena: dict[str, str]) -> str:
    emaitza = ""
    for karakterea in testua:
        gakoa = karakterea.lower()
        if gakoa in ordezkapena:
            berria = ordezkapena[gakoa]
            emaitza += berria.upper() if karakterea.isupper() else berria
        else:
            emaitza += karakterea
    return emaitza

def erakutsi_maiztasunak(maiztasunak: Counter, ordena: list[str]) -> None:
    guztira = sum(maiztasunak.values())
    print("\n" + "=" * 72)
    print("KRIPTOGRAMAREN MAIZTASUNAK")
    print("=" * 72)
    if guztira == 0:
        print("Ez da letrarik aurkitu.")
        return

    print(f"{'Letra':<8}{'Kopurua':<10}{'Ehunekoa':<10}")
    print("-" * 28)
    for letra in ordena:
        ehunekoa = maiztasunak[letra] * 100 / guztira
        barra = "█" * max(1, int(ehunekoa / 2))
        print(f"{letra.upper():<8}{maiztasunak[letra]:<10}{ehunekoa:>6.2f}%   {barra}")

def erakutsi_ordezkapena(ordezkapena: dict[str, str]) -> None:
    print("\n" + "=" * 72)
    print("MAIZTASUNAREN ARABERAKO ORDEZKAPENA")
    print("=" * 72)
    if not ordezkapena:
        print("Ez dago ordezkapenik.")
        return

    print("Zifratua → Garbia")
    print("-" * 28)
    for zifratua, garbia in ordezkapena.items():
        print(f"    {zifratua.upper()} → {garbia.upper()}")

def eskuz_aldatu_ordezkapena(ordezkapena: dict[str, str]) -> None:
    while True:
        print("\n" + "=" * 72)
        print("ESKUZKO ZUZENKETA")
        print("=" * 72)
        print("Idatzi formatu honetan: X=A")
        print("X zifratutako letra da eta A jatorrizko letra.")
        print("ENTER sakatu menu nagusira itzultzeko.")

        sarrera = input("\nZuzentzeko letra: ").strip().upper()

        if not sarrera:
            break

        if "=" not in sarrera or len(sarrera.split("=")) != 2:
            print("Formatua okerra da. Erabili X=A.")
            continue

        zifratua, garbia = sarrera.split("=")

        if len(zifratua) != 1 or len(garbia) != 1:
            print("Alde bakoitzean letra bakarra jarri behar da.")
            continue

        if not zifratua.isalpha() or not garbia.isalpha():
            print("Bi aldeek letrak izan behar dute.")
            continue

        ordezkapena[zifratua.lower()] = garbia.lower()
        print(f"Zuzenketa aplikatuta: {zifratua} → {garbia}")

def menu_interaktiboa(testua: str, maiztasunak: Counter, ordena: list[str], ordezkapena: dict[str, str]) -> None:
    while True:
        print("\n" + "=" * 72)
        print("MAIZTASUN BIDEZKO DESZIFRATZEA")
        print("=" * 72)
        print("1. Maiztasunak ikusi")
        print("2. Ordezkapena ikusi")
        print("3. Deszifratutako testua ikusi")
        print("4. Eskuzko zuzenketa egin")
        print("5. Irten")

        aukera = input("\nAukeratu aukera bat [1-5]: ").strip()

        if aukera == "1":
            erakutsi_maiztasunak(maiztasunak, ordena)
        elif aukera == "2":
            erakutsi_ordezkapena(ordezkapena)
        elif aukera == "3":
            print("\n" + "=" * 72)
            print("EMAITZA")
            print("=" * 72)
            print(deszifratu(testua, ordezkapena))
        elif aukera == "4":
            eskuz_aldatu_ordezkapena(ordezkapena)
        elif aukera == "5":
            print("\nPrograma amaituta.")
            break
        else:
            print("Aukera baliogabea. Aukeratu 1, 2, 3, 4 edo 5.")

def main() -> None:
    print("=" * 72)
    print("ORDEZKAPEN MONOALFABETIKOAREN DESZIFRATZAILEA")
    print("=" * 72)
    print("Programak euskararen letra-maiztasunak bakarrik erabiliko ditu.")
    print("Ez da hitz-pistarik, eskuzko zuzenketarik edo konbinaziorik erabiliko.\n")

    testua = input("Sartu deszifratu nahi duzun testua: ").strip()

    if not testua:
        print("Testua ezin da hutsik egon.")
        return

    maiztasunak = kalkulatu_maiztasunak(testua)
    ordena = sortu_ordena(maiztasunak)
    ordezkapena = sortu_ordezkapena(ordena)

    menu_interaktiboa(testua, maiztasunak, ordena, ordezkapena)

if __name__ == "__main__":
    main()
