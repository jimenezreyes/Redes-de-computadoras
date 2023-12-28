# Ejecutar con python3 P7_Equipo5.py
# Equipo 5: Almanza Torres José Luis
#           Jimenez Reyes Abraham 
#           Martínez Pardo Esaú

# Función para obtener la dirección IP del usuario
def obtener_direccion_ip():
    ip = input("\nEscribe la dirección IP: ")
    octetos = ip.split(".")

    # Validar cada octeto de la dirección IP
    for i, octeto in enumerate(octetos):
        try:
            octetos[i] = int(octeto)
            if not (0 <= octetos[i] <= 255):
                raise ValueError
        except ValueError:
            print("\nLa dirección IP está mal escrita")
            exit()

    return octetos

# Función para obtener el prefijo de la dirección IP
def obtener_prefijo():
    try:
        prefijo = int(input("\nEscribe el tamaño del prefijo para la dirección IP: "))
        if not (8 <= prefijo <= 32):
            raise ValueError
    except ValueError:
        print("\nEl prefijo escrito no es válido.")
        exit()

    return prefijo

# Función para obtener el número de redes que el usuario necesita
def obtener_numero_de_redes():
    try:
        num_redes = int(input("\nEscribe el número de redes que necesitas: "))
    except ValueError:
        print("\nEl número de redes no es un número")
        exit()

    return num_redes

# Función para obtener información sobre las redes del usuario
def obtener_informacion_redes(num_redes):
    info_redes = []

    for i in range(num_redes):
        nombre_red = input("\nEscribe el nombre de la red: ")
        try:
            num_host = int(input(f"\nEscribe el número de host de la red {nombre_red}: "))
        except ValueError:
            print("\nEl número de host no es un número")
            exit()

        info_redes.append((nombre_red, num_host))

    return info_redes

# Función principal para calcular VLSM
def calcular_vlsm(octetos, info_redes):
    # Ordenar la información de las redes de acuerdo al número de hosts en orden descendente
    info_redes_ordenadas = sorted(info_redes, key=lambda x: x[1], reverse=True)
    resultado = []
    contador = 0

    # Calcular parámetros para cada red
    for nombre_red, num_host in info_redes_ordenadas:
        ip_red, prefijo_red, host_util, primera_ip, segunda_ip, broadcast, fail = calcular_parametros_red(octetos, num_host)
        resultado.append((nombre_red, ip_red, prefijo_red, host_util, primera_ip, segunda_ip, broadcast))

        # Verificar si hay algún fallo y mostrar mensaje en caso de ser el primero
        if fail and contador == 0:
            print("\nEl algoritmo falló debido porque el número de host no coincide con la dirección IP")
            contador += 1

    return resultado

# Función para calcular los parámetros de una red específica
def calcular_parametros_red(octetos, num_host):
    n = calcular_valor_n(num_host)
    host_util = pow(2, n) - 2
    prefijo_red = 32 - n
    numero_magico = pow(2, n)
    fail = False

    ip_red = ".".join(map(str, octetos))
    primera_ip = ".".join(map(str, octetos[:3] + [octetos[3] + 1]))
    segunda_ip = ".".join(map(str, octetos[:3] + [octetos[3] + numero_magico - 2]))
    broadcast = ".".join(map(str, octetos[:3] + [octetos[3] + numero_magico - 1]))

    octetos[3] += numero_magico
    if octetos[3] >= 255:
        octetos[2] += 1
        octetos[3] = 0
        if not fail:
            fail = True

    return ip_red, prefijo_red, host_util, primera_ip, segunda_ip, broadcast, fail

# Función para calcular el valor de n
def calcular_valor_n(num_host):
    n = 1
    while pow(2, n) < num_host:
        n += 1
    return n

# Función para verificar si el prefijo coincide con la clase de la dirección IP
def verificar_prefijo(prefijo, octetos):
    oct_1 = octetos[0]
    if oct_1 >= 0 and oct_1 < 128:
        if not (8 <= prefijo <= 32):
            print("\nEl prefijo no coincide con la clase de la dirección IP.")
            exit()
    elif oct_1 >= 128 and oct_1 < 192:
        if not (16 <= prefijo <= 32):
            print("\nEl prefijo no coincide con la clase de la dirección IP.")
            exit()
    elif oct_1 >= 192 and oct_1 < 224:
        if not (24 <= prefijo <= 32):
            print("\nEl prefijo no coincide con la clase de la dirección IP.")
            exit()
    else:
        print("\nLa IP ingresada no es válida.")

# Función para imprimir la tabla resultante
def imprimir_tabla_resultante(resultado):
    print("\n{:<7} {:<19} {:<19} {:<23} {:<23} {:<15}".format(
        "Subred", "Id de red", "Prefijo",
        "Rango útil Primera IP", "Rango útil Última IP", "Broadcast"
    ))

    for i in range(len(resultado)):
        print("{:<7} {:<19} {:<19} {:<23} {:<23} {:<15}".format(
            str(resultado[i][0]),
            str(resultado[i][1]),
            str(resultado[i][2]),
            str(resultado[i][4]),
            str(resultado[i][5]),
            str(resultado[i][6])
        ))

# Función principal
def main():
    print("*********************************************************")
    print("***************Calculadora VLSM  EQUIPO 5****************")
    print("*********************************************************")

    octetos = obtener_direccion_ip()
    prefijo = obtener_prefijo()
    verificar_prefijo(prefijo, octetos)
    num_redes = obtener_numero_de_redes()
    info_redes = obtener_informacion_redes(num_redes)
    resultado = calcular_vlsm(octetos, info_redes)
    imprimir_tabla_resultante(resultado)

if __name__ == "__main__":
    main()
