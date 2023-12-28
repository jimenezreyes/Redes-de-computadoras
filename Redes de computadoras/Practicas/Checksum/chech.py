"""
Alumnos: Almanza Torres José Luis 
        Jimenez Reyes Abraham
        Martínez Pardo Esaú

Practica para calcular el checksum

@since 15 deseptiembre de 2023
"""

#Importamos la biblioteca hashlib, esto nos ayuda con el hash SHA-256.
import hashlib

def calcular_checksum(datos):
    checksum = hashlib.sha256(datos.encode()).hexdigest()
    return checksum

def emisor(datos):
    checksum = calcular_checksum(datos)
    print(f"Emisor - Datos: {datos}, Checksum calculado: {checksum}")
    return datos, checksum

def receptor(datos, checksum_recibido):
    checksum_calculado = calcular_checksum(datos)
    if checksum_calculado == checksum_recibido:
        print(f"Receptor - Datos recibidos: {datos}, Checksum recibido: {checksum_recibido}")
        print("La transmisión fue exitosa. No se detectaron errores.")
    else:
        print(f"Receptor - Datos recibidos: {datos}, Checksum recibido: {checksum_recibido}")
        print("Error en la transmisión. Los datos están corruptos.")

# Leer datos desde un archivo de texto
try:
    with open("cuento.txt", "r") as archivo:
        datos_a_transmitir = archivo.read()
except FileNotFoundError:
    print("El archivo 'datos.txt' no se encontró.")
    exit(1)

# Ejemplo de uso
datos_transmitidos, checksum_enviado = emisor(datos_a_transmitir)
receptor(datos_transmitidos, checksum_enviado)