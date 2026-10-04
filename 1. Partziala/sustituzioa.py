#!/usr/bin/env python3
"""
INTENCION GLOBAL DEL SCRIPT
============================
Descifra (o lo intenta) un criptograma de sustitucion monoalfabetica en
euskera, combinando dos tecnicas:

 1) Analisis de frecuencias: se empareja la letra mas usada en el
    criptograma con la letra mas usada en euskera, la segunda con la
    segunda, etc. (tabla de Maiztasunak.png, ya corregida).

 2) "Crib words" (palabras adivinadas): en textos cortos, el orden de
    frecuencias puro casi nunca acierta al 100%, asi que se buscan
    palabras cifradas repetidas que encajen con palabras muy comunes
    en euskera ("eta"=y, "da"=es, "ez"=no...) y se fijan esas letras
    a mano antes de completar el resto.

 3) Prueba automatica de combinaciones: cuando dos o mas letras tienen
    una frecuencia igual o muy parecida en el criptograma, no se sabe
    con certeza cual va con cual en la tabla de euskera. El script
    genera TODAS las combinaciones posibles entre esas letras "empatadas"
    y muestra el texto resultante de cada una, para que el usuario elija
    a ojo cual tiene mas sentido en euskera.
"""

from collections import Counter
import itertools

mensaje = """JIYQ WQIEtYLP YtXLLW OPLP! CWXYM SPMQPLtP YEYQWtP CPOX PLZP SBPJPQX bPBQXWYtPQX bPtYPM. JYLYM bPW, XLPWM HYMCY PEQX PtYLPtJYM CP HPWJQWbYB WQIEtYLP; tRPBXPQ YtP tRPBXPQ, YtP «PISP, HPWJQWbYB!» XWFIPQ WJPM CWLP MPOIEW WbWBbWCY XEXPM. QPBY MPOIEWP YLY HPCP YJ CP BYFYM bYJPWM OPtPJQPtEIP, bPWMP, XLPWMCWQ YLY, JYMbPWt YZPQIZY OPJtYQ SPEPYLPM bWJQPLLP YZPM CWXtY HPWJQWbYBW, SPLtY FPLtJYP bPWZYMtJYM CWYM QXMSPWMWP bPQPLLPLW."""

# --- 1. Tabla de frecuencias del euskera, YA CORREGIDA a partir de
# Maiztasunak.png (columna por columna, de mayor a menor).
# OJO: en la imagen "k" aparece repetida (8476) en dos posiciones;
# aqui se deja una sola vez. Ademas se corrige el orden real de la
# 2a columna: g(6927) > d(5225) > s(5206), que en versiones previas
# del script estaba mal ordenado.
tabla_frecuencias_euskera = [
    'a', 'i', 'r', 'e', 't', 'o', 'u', 'n', 'k',
    'l', 'z', 'g', 'd', 's', 'b', 'm', 'p',
    'h', 'x', 'f', 'j', 'c', 'y', 'v', 'w', 'q',
]

# --- 2. Frecuencia de letras en el criptograma ---
frecuencias_cripto = Counter(c.upper() for c in mensaje if c.isalpha())
letras_ordenadas = sorted(
    frecuencias_cripto, key=lambda l: (-frecuencias_cripto[l], l)
)

print("Frecuencias del criptograma (de mayor a menor):")
for l in letras_ordenadas:
    print(f"  {l}: {frecuencias_cripto[l]}")

# Sustitucion base, solo por frecuencia (punto de partida)
sustitucion_base = {
    c: p.upper() for c, p in zip(letras_ordenadas, tabla_frecuencias_euskera)
}


def descifrar(msg, sust):
    """Aplica un diccionario de sustitucion {letra_cifrada: letra_clara}."""
    out = ""
    for c in msg:
        if c.upper() in sust:
            n = sust[c.upper()]
            out += n.lower() if c.islower() else n
        else:
            out += c  # letra sin asignar todavia: se deja tal cual
    return out


# --- 3. Pistas ("crib words") deducidas de palabras cortas repetidas ---
# "YTP" se repite 2 veces -> muy probablemente "eta" (= "y", conjuncion)
# "CP"  se repite 2 veces -> muy probablemente "da" (= "es")
# "YJ"  aparece 1 vez     -> encaja con "ez" (negacion)
# "PISP, ...!" con exclamacion -> encaja con el patron de grito "AUPA, ...!"
sustitucion_con_pistas = dict(sustitucion_base)
sustitucion_con_pistas.update({
    'P': 'A',
    'Y': 'E',
    'T': 'T',
    'C': 'D',
    'J': 'Z',
    'I': 'U',
    'S': 'P',
    'W': 'R',
})

print("\n--- Descifrado aplicando las pistas (crib words) ---")
print(descifrar(mensaje, sustitucion_con_pistas))

# --- 4. Grupos de letras con frecuencia IGUAL o muy cercana en el
# criptograma: aqui es donde el orden puro de frecuencias es dudoso,
# y conviene probar todas las combinaciones posibles.
grupos_empatados = [
    ['M', 'Q'],   # ambas con frecuencia 23
    ['J', 'X'],   # ambas con frecuencia 16 (OJO: J ya fijada arriba por pista "ez")
    ['E', 'I'],   # ambas con frecuencia 9  (OJO: I ya fijada arriba por pista "AUPA")
    ['O', 'S'],   # ambas con frecuencia 6  (OJO: S ya fijada arriba por pista "AUPA")
    ['H', 'Z'],   # ambas con frecuencia 5
]

# Solo probamos combinaciones sobre las letras que AUN no se han fijado
# a mano con una pista, para no deshacer lo ya deducido.
grupos_libres = [
    [letra for letra in grupo if letra not in sustitucion_con_pistas or letra in ('M', 'Q', 'H', 'Z')]
    for grupo in grupos_empatados
]
grupos_libres = [g for g in grupos_libres if len(g) > 1]

print("\n" + "=" * 70)
print("Probando todas las combinaciones entre letras de frecuencia empatada:")
print("(grupos:", grupos_libres, ")\n")

# Para cada grupo empatado, generamos las permutaciones de a qué letra
# clara (segun la tabla de frecuencias) va cada letra cifrada del grupo,
# manteniendo fijas las posiciones que ocupaban en la tabla original.
posiciones_por_letra = {c: i for i, c in enumerate(letras_ordenadas)}

combinaciones = []
for grupo in grupos_libres:
    posiciones = [posiciones_por_letra[c] for c in grupo]
    letras_claras_grupo = [tabla_frecuencias_euskera[p].upper() for p in posiciones]
    combinaciones.append(list(itertools.permutations(letras_claras_grupo)))

# Producto cartesiano de todas las combinaciones de todos los grupos
contador = 0
for combo in itertools.product(*combinaciones):
    contador += 1
    sust_prueba = dict(sustitucion_con_pistas)
    for grupo, asignacion in zip(grupos_libres, combo):
        for letra_cifrada, letra_clara in zip(grupo, asignacion):
            sust_prueba[letra_cifrada] = letra_clara

    texto = descifrar(mensaje, sust_prueba)
    print(f"[Combinacion {contador}] {dict(zip([l for g in grupos_libres for l in g], [a for c in [combo] for grp in c for a in grp]))}")
    print(texto[:160], "...\n")

print("=" * 70)
print(f"Total de combinaciones probadas: {contador}")
print("Revisa cual de ellas parece euskera real y usa esa asignacion")
print("como base en la correccion manual interactiva.")

# --- 5. Correccion manual interactiva (igual que antes) ---
sustituciones = dict(sustitucion_con_pistas)

print("\n" + "=" * 60)
print("Correccion manual: formato X=A (letra cifrada = letra clara).")
print("ENTER vacio para terminar.\n")

while True:
    entrada = input("Correccion (o ENTER para terminar): ").strip().upper()
    if not entrada:
        break
    if "=" not in entrada or len(entrada.split("=")) != 2:
        print("Formato incorrecto. Usa X=A")
        continue
    origen, destino = entrada.split("=")
    if len(origen) != 1 or len(destino) != 1:
        print("Cada lado debe contener una sola letra.")
        continue
    sustituciones[origen] = destino
    print("\nTexto descifrado actualizado:\n")
    print(descifrar(mensaje, sustituciones))
