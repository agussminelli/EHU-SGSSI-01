def xor_bytes(datos, clave):
    if len(datos) != len(clave):
        raise ValueError("El mensaje y la clave deben tener la misma longitud")

    return bytes(a ^ b for a, b in zip(datos, clave))


mensaje = b"ATAQUE AL AMANECER"
clave = b"ClaveConDistintosCaracteresDaError" 

print("Mensaje original:", mensaje)
print("Mensaje hexadecimal:", mensaje.hex())
print("Clave hexadecimal:", clave.hex())

criptograma = xor_bytes(mensaje, clave)

print("Criptograma hexadecimal:", criptograma.hex())

descifrado = xor_bytes(criptograma, clave)

print("Mensaje descifrado:", descifrado)

if descifrado == mensaje:
    print("Descifrado correcto")
else:
    print("Error en el descifrado")