from collections import Counter

def contar_frecuencias(texto):
    letras = [c for c in texto.upper() if c.isalpha()]
    total = len(letras)
    contador = Counter(letras)

    print("\nFrecuencias del texto:\n")

    for letra, cantidad in contador.most_common():
        porcentaje = 100 * cantidad / total
        print(f"{letra}: {cantidad:4} ({porcentaje:5.2f} %)")

def descifrar(texto, sustituciones):
    resultado = ""

    for c in texto:
        mayuscula = c.upper()

        if mayuscula in sustituciones:
            nueva = sustituciones[mayuscula]

            if c.islower():
                nueva = nueva.lower()

            resultado += nueva
        else:
            resultado += c

    return resultado

def mostrar_sustituciones(sustituciones):
    if not sustituciones:
        print("\nNo hay sustituciones definidas.")
        return

    print("\nSustituciones actuales:")

    for cifrada, clara in sorted(sustituciones.items()):
        print(f"{cifrada} -> {clara}")

def main():
    print("Ataque interactivo a cifrado por sustitución simple")
    print("Introduce el texto cifrado.")
    print("Termina introduciendo una línea vacía.\n")

    lineas = []

    while True:
        linea = input()

        if linea == "":
            break

        lineas.append(linea)

    mensaje = "\n".join(lineas)

    sustituciones = {}

    contar_frecuencias(mensaje)

    while True:
        print("\n" + "=" * 60)
        print(descifrar(mensaje, sustituciones))
        print("=" * 60)

        print("\nOpciones:")
        print("1 - Añadir o cambiar sustitución")
        print("2 - Eliminar sustitución")
        print("3 - Ver frecuencias")
        print("4 - Ver sustituciones")
        print("5 - Salir")

        opcion = input("\nOpción: ")

        if opcion == "1":
            cifrada = input("Letra cifrada: ").upper()
            clara = input("Letra original: ").upper()

            if len(cifrada) == 1 and len(clara) == 1:
                sustituciones[cifrada] = clara
            else:
                print("Debes introducir una sola letra.")

        elif opcion == "2":
            cifrada = input("Letra cifrada a eliminar: ").upper()

            if cifrada in sustituciones:
                del sustituciones[cifrada]
            else:
                print("Esa sustitución no existe.")

        elif opcion == "3":
            contar_frecuencias(mensaje)

        elif opcion == "4":
            mostrar_sustituciones(sustituciones)

        elif opcion == "5":
            print("\nTexto resultante:\n")
            print(descifrar(mensaje, sustituciones))
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()