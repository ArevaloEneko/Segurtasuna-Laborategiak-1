#!/usr/bin/env python3

from collections import Counter

MAIZTASUNAK_EUSKARAZ = [
    "a", "i", "r", "e", "t", "o", "u", "n", "k",
    "l", "z", "g", "d", "s", "b", "m", "p",
    "h", "x", "f", "j", "c", "y", "v", "w", "q"
]

def kalkulatu_maiztasunak(testua: str) -> Counter:
    return Counter(
        karakterea.lower()
        for karakterea in testua
        if karakterea.isalpha() and karakterea.isascii()
    )

def ordenatu_maiztasunak(maiztasunak: Counter) -> list[str]:
    return sorted(maiztasunak, key=lambda letra: (-maiztasunak[letra], letra))

def sortu_maiztasun_ordezkapena(maiztasunak: Counter) -> dict[str, str]:
    letra_ordenatuak = ordenatu_maiztasunak(maiztasunak)
    return dict(zip(letra_ordenatuak, MAIZTASUNAK_EUSKARAZ))

def deszifratu(testua: str, ordezkapena: dict[str, str]) -> str:
    emaitza = ""
    for karakterea in testua:
        letra = karakterea.lower()
        if letra in ordezkapena:
            letra_berria = ordezkapena[letra]
            emaitza += letra_berria.upper() if karakterea.isupper() else letra_berria
        else:
            emaitza += karakterea
    return emaitza

def erakutsi_maiztasunak(maiztasunak: Counter) -> None:
    guztira = sum(maiztasunak.values())
    print("\n" + "=" * 72)
    print("KRIPTOGRAMAREN LETRA-MAIZTASUNAK")
    print("=" * 72)
    for letra in ordenatu_maiztasunak(maiztasunak):
        kopurua = maiztasunak[letra]
        ehunekoa = kopurua * 100 / guztira
        barra = "█" * max(1, round(ehunekoa / 2))
        print(f"{letra.upper():<8}{kopurua:<10}{ehunekoa:>6.2f}%   {barra}")

def erakutsi_maiztasun_taula() -> None:
    print("\n" + "=" * 72)
    print("EUSKARAREN MAIZTASUN-TAULA")
    print("=" * 72)
    for posizioa in range(0, len(MAIZTASUNAK_EUSKARAZ), 9):
        zatia = MAIZTASUNAK_EUSKARAZ[posizioa:posizioa + 9]
        print("   ".join(f"{posizioa + i + 1:2d}. {letra.upper()}" for i, letra in enumerate(zatia)))

def erakutsi_ordezkapena(ordezkapena: dict[str, str]) -> None:
    print("\n" + "=" * 72)
    print("PROPOSATUTAKO ORDEZKAPENA")
    print("=" * 72)
    for zifratua in sorted(ordezkapena):
        print(f"    {zifratua.upper()} → {ordezkapena[zifratua].upper()}")

def erakutsi_deszifratzea(testua: str, ordezkapena: dict[str, str]) -> None:
    print("\n" + "=" * 72)
    print("DESZIFRATUTAKO TESTUA")
    print("=" * 72)
    print(deszifratu(testua, ordezkapena))

def eskuz_aldatu_ordezkapena(ordezkapena: dict[str, str]) -> None:
    print("\n" + "=" * 72)
    print("ESKUZKO ZUZENKETA")
    print("=" * 72)
    print("Erabili X=A formatua.")
    print("X zifratutako letra da eta A letra garbia.")
    print("ENTER sakatu amaitzeko.")
    while True:
        sarrera = input("\nZuzendu: ").strip().lower()
        if not sarrera:
            break
        if "=" not in sarrera or sarrera.count("=") != 1:
            print("Formatua okerra da. Erabili X=A.")
            continue
        zifratua, garbia = sarrera.split("=")
        if len(zifratua) != 1 or len(garbia) != 1 or not zifratua.isalpha() or not garbia.isalpha():
            print("Bi aldeek letra bakarra izan behar dute.")
            continue
        ordezkapena[zifratua] = garbia
        print(f"Zuzenketa aplikatuta: {zifratua.upper()} → {garbia.upper()}")

def menu_interaktiboa(testua: str, maiztasunak: Counter, ordezkapena: dict[str, str]) -> None:
    while True:
        print("\n" + "=" * 72)
        print("MAIZTASUN BIDEZKO DESZIFRATZAILEA")
        print("=" * 72)
        print("1. Kriptogramaren maiztasunak ikusi")
        print("2. Euskararen maiztasun-taula ikusi")
        print("3. Ordezkapen-proposamena ikusi")
        print("4. Deszifratutako testua ikusi")
        print("5. Eskuzko zuzenketa egin")
        print("6. Maiztasun-proposamena berrezarri")
        print("7. Irten")
        aukera = input("\nAukeratu aukera bat [1-7]: ").strip()
        if aukera == "1":
            erakutsi_maiztasunak(maiztasunak)
        elif aukera == "2":
            erakutsi_maiztasun_taula()
        elif aukera == "3":
            erakutsi_ordezkapena(ordezkapena)
        elif aukera == "4":
            erakutsi_deszifratzea(testua, ordezkapena)
        elif aukera == "5":
            eskuz_aldatu_ordezkapena(ordezkapena)
        elif aukera == "6":
            ordezkapena.clear()
            ordezkapena.update(sortu_maiztasun_ordezkapena(maiztasunak))
            print("\nMaiztasun-proposamena berrezarri da.")
        elif aukera == "7":
            print("\nPrograma amaituta.")
            break
        else:
            print("Aukera baliogabea. Aukeratu 1 eta 7 arteko zenbaki bat.")

def main() -> None:
    print("=" * 72)
    print("ORDEZKAPEN MONOALFABETIKOAREN DESZIFRATZAILEA")
    print("=" * 72)
    print("Edozein ordezkapen-kriptogramarekin lan egiteko diseinatuta dago.")
    print("Deszifratzea euskararen letra-maiztasunetan oinarritzen da.")
    testua = input("\nSartu deszifratu nahi duzun kriptograma: ")
    if not testua.strip():
        print("Errorea: testua ezin da hutsik egon.")
        return
    maiztasunak = kalkulatu_maiztasunak(testua)
    if not maiztasunak:
        print("Errorea: ez da letrarik aurkitu.")
        return
    ordezkapena = sortu_maiztasun_ordezkapena(maiztasunak)
    print("\nHasierako maiztasun-analisia:")
    erakutsi_deszifratzea(testua, ordezkapena)
    menu_interaktiboa(testua, maiztasunak, ordezkapena)

if __name__ == "__main__":
    main()
