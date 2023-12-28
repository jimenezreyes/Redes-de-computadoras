"""
Implementación del algoritmo de comprobación de redundancia cíclica (CRC).
Equipo 5:
- José Luis Almanza Torres
- Abraham Jimenez Reyes
- Esaú Martínez Pardo
"""

# Función para transformar números en superíndices
def convertir_a_superindice(numero):
    numeros_normales = "0123456789r"
    numeros_superindice = "⁰¹²³⁴⁵⁶⁷⁸⁹ʳ"
    tabla_de_conversion = numero.maketrans(numeros_normales, numeros_superindice)
    return numero.translate(tabla_de_conversion)


# Veamos que aquí hacemos la representación del polinomio, para poder verificar que el procedimeinto hecho
# en el ensayo concuerda con el del código
# Ejercicio a
trama_ejercicio_a = [1, 1, 1, 1, 0, 0, 1, 0, 1]  # Trama del ejercicio a
polinomio_generador_ejercicio_a = [1, 0, 1, 0, 1]  # Polinomio generador del ejercicio a

# Ejercicio b
trama_ejercicio_b = '110101111'  # Trama del ejercicio b
polinomio_generador_ejercicio_b = [1, 0, 0, 1, 1]  # Polinomio generador del ejercicio b



# Función que obtiene una representación legible de un polinomio
def obtener_polinomio_legible(polinomio):
    grados = [convertir_a_superindice(str(i)) for i in range(len(polinomio) - 1, -1, -1)]
    terminos = [f'{coeficiente}x{grado}' for coeficiente, grado in zip(polinomio, grados) if coeficiente != 0]
    polinomio_legible = ' + '.join(terminos)
    return polinomio_legible


# Función que convierte de un polinomio a un binario.
def polinomio_a_binario(polinomio):
    binario = ''.join(map(str, polinomio))
    return binario


# Obtener el grado del polinomio generador
def polinomio_grado(polinomio):
    return len(polinomio) - 1

# Funcion que nmos ayuda a calcular el xrmx
def obtener_xrmx(trama, polinomio):
    grado = polinomio_grado(polinomio) ## Obtener el grado del polinomio generador

    polinomio_generador_binario = polinomio_a_binario(polinomio)
    trama_binaria = polinomio_a_binario(trama)
    # Mostrar información relevante
    print(f"La trama es: {trama_binaria}\n")
    print(f"El polinomio generador es: {obtener_polinomio_legible(polinomio)} => {polinomio_generador_binario}\n")
    print(f"Se agregarán {grado} bits 0 a la cadena.\n")
    # Calcular x^r * M(x)
    x_r_mult_message = trama_binaria + '0' * grado
    # Mostrar el valor de x^r * M(x)
    print(f'El valor de x{convertir_a_superindice("r")}M(x) es: {x_r_mult_message}\n')

    return x_r_mult_message



def xor(a, b):
    """
    Realiza una operación XOR a nivel de bits entre dos cadenas binarias a y b.

    Args:
    a (str): Cadena binaria 1.
    b (str): Cadena binaria 2.

    Returns:
    str: Resultado de la operación XOR entre a y b.
    """
    if len(a) != len(b):
        raise ValueError("Las cadenas deben tener la misma longitud para realizar XOR.")
    
    result = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            result += '0'
        else:
            result += '1'
    
    return result



def crc_div(trama, gen):
    """
    Realiza la división de xrmx entre el polinomio generador binario.

    Args:
    trama (str): Cadena binaria de la trama.
    gen (str): Polinomio generador binario.

    Returns:
    str: Valor del CRC binario.
    """

    grado = polinomio_grado(gen)
    xrmx = obtener_xrmx(trama, gen)
    gen = polinomio_a_binario(gen)
    tamGen = len(gen)
    actual = xrmx[:tamGen]
    xrmx = xrmx[tamGen:]
    cont = 0

    print("===== Procedimiento de División ===== \n")
    
    while len(xrmx) > 0:
        print(f"Divisor: {gen}, dividendo: {actual}")
        actual = xor(gen, actual)
        print("XOR:", actual)

        for bit in actual:
            if bit == '0':
                cont += 1
            else:
                break

        if cont >= len(xrmx):
            break

        actual = actual[cont:] + xrmx[:cont]
        print("Var actual nueva :", actual, "\n")

        if len(xrmx) <= cont:
            xrmx = ''
        else:
            xrmx = xrmx[cont:]

        cont = 0

    if len(xrmx) > 0:
        actual += xrmx
    else:
        actual = xor(gen, actual)

    crc = actual[-grado:]
 
    print("El valor de crc es:", crc, "\n")

    return crc


# Obtenemos la T, que simplemente es la trama concatenada con el CRC
def obten_t(trama, polinomio):
    trama = polinomio_a_binario(trama)
    crc = crc_div(trama, polinomio)
    t = trama + crc
    print("El valor de T es: " + t)
    return


print("\n~~~ Programa para el cálculo de CRC ~~~\n")
print("Menú: \n")
print("Opciones disponibles:\n")
print("1. Calcular CRC del ejercicio 1")
print("2. Calcular CRC del ejercicio 2")
print("3. Ingresar trama y polinomio generador personalizados para su calculo")
print("============================================")
print("\n")

opcion = input("Por favor, ingresa una opción de un numero: ")
print("\n")

if opcion == "1":
    obten_t(trama_ejercicio_a, polinomio_generador_ejercicio_a)
    exit()

elif opcion == "2":
    obten_t(trama_ejercicio_b, polinomio_generador_ejercicio_b)
    exit()

elif opcion == "3":
    trama = input("Ingresa la trama en binario: ")
    grado = int(input("Ingresa el grado del polinomio generador: "))
    polinomio = []
    literal = 0
    auxGrado = grado
    print("Ingresa '1' si existe la literal o '0' si no existe. Comienza desde el término de mayor grado hasta el término independiente.")
    # Ingresar el polinomio generador literal a literal
    for i in range(grado + 1):
        literal = int(input("Ingresa el coeficiente del término x^" + str(auxGrado) + ": "))
        polinomio.append(literal)
        auxGrado -= 1

    obten_t(trama, polinomio)
    exit()

else:
    print("Opción no válida. Por favor, selecciona una opción válida.")
    exit()
