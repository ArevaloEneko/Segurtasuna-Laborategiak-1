def xor_bytes(a: bytes, b: bytes) -> bytes:
    """Aplica XOR byte a byte entre dos secuencias de la misma longitud.

    Al ser XOR una operación simétrica, esta misma función sirve tanto
    para cifrar como para descifrar: cifrar(m, k) = c, cifrar(c, k) = m.
    """
    return bytes(x ^ y for x, y in zip(a, b))


def hex_legible(datos: bytes) -> str:
    """Devuelve el hexadecimal separado por espacios cada byte, para
    que sea más fácil de leer que un bloque continuo de caracteres."""
    return " ".join(f"{byte:02x}" for byte in datos)


def cifrar_flujo(mensaje_texto: str, gakoa_texto: str) -> tuple[bytes, bytes, bytes, bytes]:
    """Cifra y descifra un mensaje mediante XOR con una clave de la misma longitud.

    Devuelve (mensaje_bytes, gakoa_bytes, kriptograma, deszifratua).
    """
    mensaje_bytes = mensaje_texto.encode("utf-8")
    gakoa_bytes = gakoa_texto.encode("utf-8")

    # Importante: la longitud se comprueba sobre los BYTES ya codificados,
    # no sobre el número de caracteres. Con letras como ñ, ü o acentos,
    # un carácter puede ocupar más de un byte en UTF-8, así que comparar
    # len(mensaje_texto) con len(gakoa_texto) podría dar un resultado
    # engañoso.
    if len(mensaje_bytes) != len(gakoa_bytes):
        raise ValueError(
            f"Mezuak eta gakoak luzera bera izan behar dute "
            f"(mezua: {len(mensaje_bytes)} byte, gakoa: {len(gakoa_bytes)} byte)"
        )

    kriptograma = xor_bytes(mensaje_bytes, gakoa_bytes)
    deszifratua = xor_bytes(kriptograma, gakoa_bytes)

    return mensaje_bytes, gakoa_bytes, kriptograma, deszifratua


def mostrar_resultado(mensaje_texto: str, mensaje_bytes: bytes, gakoa_bytes: bytes,
                       kriptograma: bytes, deszifratua: bytes) -> None:
    print("Jatorrizko mezua (testua):")
    print(f"  {mensaje_texto}")
    print("Jatorrizko mezua (hex):")
    print(f"  {hex_legible(mensaje_bytes)}")

    print("\nGakoa (hex):")
    print(f"  {hex_legible(gakoa_bytes)}")

    print("\nKriptograma (hex):")
    print(f"  {hex_legible(kriptograma)}")

    print("\nDeszifratutako mezua (hex):")
    print(f"  {hex_legible(deszifratua)}")
    print("Deszifratutako mezua (testua):")
    print(f"  {deszifratua.decode('utf-8')}")

    print("\nEgiaztapena (deszifratua == jatorrizko mezua):")
    print(f"  {deszifratua == mensaje_bytes}")


def main() -> None:
    # Datos de prueba del enunciado
    mensaje_texto = "GURE MEZUA HAU DA"
    gakoa_texto = "GAKO1234567890"

    opcion = input(
        "Pulsa ENTER para usar el mensaje/clave de prueba, "
        "o escribe 's' para introducir los tuyos: "
    ).strip().lower()

    if opcion == "s":
        mensaje_texto = input("Mezua: ")
        gakoa_texto = input(
            f"Gakoa ({len(mensaje_texto.encode('utf-8'))} byte behar ditu): "
        )

    try:
        mensaje_bytes, gakoa_bytes, kriptograma, deszifratua = cifrar_flujo(
            mensaje_texto, gakoa_texto
        )
    except ValueError as error:
        print(f"\nErrorea: {error}")
        return

    mostrar_resultado(mensaje_texto, mensaje_bytes, gakoa_bytes, kriptograma, deszifratua)


if __name__ == "__main__":
    main()
