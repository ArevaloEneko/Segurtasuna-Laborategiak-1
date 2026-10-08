#!/usr/bin/env python3

def garbitu_zenbakia(mezua: str) -> int:
    while True:
        try:
            return int(input(mezua).strip())
        except ValueError:
            print("Sartu baliozko zenbaki bat.")

def deszifratu_zesar(testua: str, gakoa: int) -> str:
    emaitza = ""
    for karakterea in testua:
        if karakterea.isalpha() and karakterea.isascii():
            oinarria = ord("a") if karakterea.islower() else ord("A")
            emaitza += chr((ord(karakterea) - oinarria - gakoa) % 26 + oinarria)
        else:
            emaitza += karakterea
    return emaitza

def erakutsi_konbinazioak(testua: str) -> None:
    print("\n" + "=" * 72)
    print("ZESARREN INDAR BRUTUKO DESZIFRATZEA")
    print("=" * 72)
    for gakoa in range(26):
        emaitza = deszifratu_zesar(testua, gakoa)
        print(f"{gakoa:2d} → {emaitza}")
    print("=" * 72)

def main() -> None:
    print("=" * 72)
    print("ZESARREN ZIFRATUA")
    print("=" * 72)
    testua = input("Sartu deszifratu nahi duzun testua: ").strip()

    if not testua:
        print("Testua ezin da hutsik egon.")
        return

    erakutsi_konbinazioak(testua)

if __name__ == "__main__":
    main()
