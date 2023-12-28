import hashlib

"""
Alumnos: Almanza Torres José Luis 
        Jimenez Reyes Abraham
        Martínez Pardo Esaú

Practica para calcular el checksum

@since 15 deseptiembre de 2023
"""

# Función para calcular el checksum con SHA-256
def calcular_checksum_sha256(datos):
    checksum = hashlib.sha256(datos.encode()).hexdigest()
    return checksum

# Función para calcular el checksum con MD5
def calcular_checksum_md5(datos):
    checksum = hashlib.md5(datos.encode()).hexdigest()
    return checksum

#Funcion para calcular el checksum con sha512
def calcular_checksum_sha512(datos):
    checksum = hashlib.sha512(datos.encode()).hexdigest()
    return checksum    

# Función para convertir un checksum a otro algoritmo
def convertir_checksum(checksum, nuevo_algoritmo):
    if nuevo_algoritmo == "SHA512":
        if len(checksum) % 2 != 0:
            checksum = "0" + checksum
        datos = bytes.fromhex(checksum)
        nuevo_checksum = hashlib.sha512(datos).hexdigest()
        return nuevo_checksum
    else:
        raise ValueError("Conversión no compatible")        

# Función del emisor
def emisor(datos):
    checksum_sha256 = calcular_checksum_sha256(datos)
    print(f"Emisor - Datos: {datos}, Checksum SHA-256 calculado: {checksum_sha256}")
    return datos, checksum_sha256

# Función del receptor
def receptor(datos):
    checksum_sha256= calcular_checksum_sha256(datos)
    print(f"Receptor - Datos recibidos: {datos}, Checksum 256 calculado: {checksum_sha256}")
    return datos, checksum_sha256

# Leer datos desde un archivo de texto
try:
    with open("cuento.txt", "r") as archivo:
        datos_a_transmitir = archivo.read()
except FileNotFoundError:
    print("El archivo 'cuento.txt' no se encontró.")
    exit(1)

# Calcular el checksum SHA-256 de los datos
checksum_recibido = calcular_checksum_sha256(datos_a_transmitir)
print(f"Checksum SHA-256 calculado: {checksum_recibido}")

# Calcular el checksum MD5 de los datos
checksum_otro = calcular_checksum_sha256(datos_a_transmitir)
print(f"Checksum SHA-256 calculado: {checksum_otro}")

# Convertir el checksum SHA-256 al nuevo algoritmo (SHA-512)
nuevo_checksum_sha512 = convertir_checksum(checksum_recibido, "SHA512")
print(f"Checksum SHA-256 convertido a SHA-512: {nuevo_checksum_sha512}")

# Convertir el checksum MD5 al nuevo algoritmo (SHA-512)
nuevo_checksum_md5_sha512 = convertir_checksum(checksum_otro, "SHA512")
print(f"Checksum SHA-256 convertido a SHA-512: {nuevo_checksum_md5_sha512}")


# Comparar los dos nuevos checksums SHA-1
if nuevo_checksum_sha512 == nuevo_checksum_md5_sha512:
    print("Las conversiones y las comparaciones con SHA-1 fueron exitosas. Los checksums coinciden.")
else:
    print("Error en las conversiones o las comparaciones. Los checksums SHA-1 no coinciden.")
