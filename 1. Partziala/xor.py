#!/usr/bin/env python3

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def hex_irakurgarria(datuak: bytes) -> str:
    return " ".join(f"{byte:02X}" for byte in datuak)

def ascii_irakurgarria(datuak: bytes) -> str:
    emaitza = ""
    for byte in datuak:
        if 32 <= byte <= 126:
            emaitza += chr(byte)
        else:
            emaitza += f"\\x{byte:02X}"
    return emaitza

def egiaztatu_sarrerak(mezu_bytes: bytes, gakoa_bytes: bytes) -> None:
    if not mezu_bytes:
        raise ValueError("Mezua ezin da hutsik egon.")
    if not gakoa_bytes:
        raise ValueError("Gakoa ezin da hutsik egon.")
    if len(mezu_bytes) != len(gakoa_bytes):
        raise ValueError(
            f"Mezuak eta gakoak byte kopuru bera izan behar dute "
            f"(mezua: {len(mezu_bytes)}, gakoa: {len(gakoa_bytes)})."
        )

def erakutsi_emaitza(mezu_bytes: bytes, gakoa_bytes: bytes, kriptograma: bytes, deszifratua: bytes) -> None:
    print("\n" + "=" * 72)
    print("XOR ZIFRATZEA")
    print("=" * 72)

    print("\nJatorrizko mezua:")
    print(mezu_bytes.decode("utf-8"))

    print("\nGakoa:")
    print(gakoa_bytes.decode("utf-8"))

    print("\nKRIPTOGRAMA - ASCII:")
    print(ascii_irakurgarria(kriptograma))

    print("\nKRIPTOGRAMA - HEX:")
    print(hex_irakurgarria(kriptograma))

    print("\nDESZIFRATUTAKO MEZUA - ASCII:")
    print(deszifratua.decode("utf-8"))

    print("\nDESZIFRATUTAKO MEZUA - HEX:")
    print(hex_irakurgarria(deszifratua))

    print("\nEgiaztapena:")
    print("Bai" if deszifratua == mezu_bytes else "Ez")

def zifratu_eta_deszifratu(testua: str, gakoa: str) -> tuple[bytes, bytes, bytes, bytes]:
    mezu_bytes = testua.encode("utf-8")
    gakoa_bytes = gakoa.encode("utf-8")
    egiaztatu_sarrerak(mezu_bytes, gakoa_bytes)
    kriptograma = xor_bytes(mezu_bytes, gakoa_bytes)
    deszifratua = xor_bytes(kriptograma, gakoa_bytes)
    return mezu_bytes, gakoa_bytes, kriptograma, deszifratua

def main() -> None:
    print("=" * 72)
    print("XOR ZIFRATZAILEA")
    print("=" * 72)

    testua = input("Sartu zifratu nahi duzun testua: ")
    gakoa = input("Sartu gakoa, testuaren byte luzera bera izan behar duena: ")

    try:
        mezu_bytes, gakoa_bytes, kriptograma, deszifratua = zifratu_eta_deszifratu(testua, gakoa)
        erakutsi_emaitza(mezu_bytes, gakoa_bytes, kriptograma, deszifratua)
    except ValueError as errorea:
        print(f"\nErrorea: {errorea}")

if __name__ == "__main__":
    main()
