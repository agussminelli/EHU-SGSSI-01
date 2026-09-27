from langdetect import detect, LangDetectException

mensaje = "Uunejvxb dw vdwmx wdnex jzdr, nw wdnbcaxb lxajixwnb"

def descifrar_cesar(texto, clave):
    resultado = ""

    for caracter in texto:
        if caracter.isalpha():

            if caracter.isupper():
                base = ord('A')
            else:
                base = ord('a')

            resultado += chr(
                (ord(caracter) - base - clave) % 26 + base
            )

        else:
            resultado += caracter

    return resultado


for clave in range(26):

    texto_descifrado = descifrar_cesar(mensaje, clave)

    try:
        idioma = detect(texto_descifrado)
    except LangDetectException:
        idioma = "desconocido"

    print(
        f"Clave {clave:2}: {texto_descifrado} "
        f"-> idioma: {idioma}"
    )

    if idioma == "es":
        print("\nPosible solución encontrada:")
        print("Clave:", clave)
        print("Mensaje:", texto_descifrado)
        break