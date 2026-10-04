mensaje = "Uunejvxb dw vdwmx wdnex jzdr, nw wdnbcaxb lxajixwnb"

def descifrar_cesar(texto, clave):
    resultado = ""

    for caracter in texto:
        if caracter.isalpha():
            base = ord('a') if caracter.islower() else ord('A')
            resultado += chr((ord(caracter) - base - clave) % 26 + base)
        else:
            resultado += caracter

    return resultado

print("Ataque por fuerza bruta contra César\n")

for clave in range(26):
    resultado = descifrar_cesar(mensaje, clave)
    print(f"Clave {clave:2}: {resultado}")