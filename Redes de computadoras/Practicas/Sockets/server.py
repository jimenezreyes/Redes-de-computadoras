import socket
import threading
import time
# Obtener nombre del host
hostname = socket.gethostname()
# Puerto
port = 8001
# Tamaño de bits que van a ser recibidos
buffer_size = 1024

# Mensajes de ayuda y comandos
comando_version_servidor = "[1] Para mostrar la version del servidor"
comando_terminar_conexion = "[2] Para terminar la conexion con el cliente."
comando_informacion_servidor = "[3] Para mostrar la informacion del servidor"
comando_autores = "[4] Para mostrar a los autores del codigo"
comando_tarea_especial = "[5] Para escribir algo en el servidor"
comandos_usuales = "Puede ingresar comandos conocidos para saber su función, como ls, mkdir, cd, sudo."
opciones = f"Posibles comandos a ejecutar:\n{comando_version_servidor}\n{comando_terminar_conexion}\n{comando_informacion_servidor}\n{comando_autores}\n{comando_tarea_especial}\n{comandos_usuales}\n"

# Creando el socket y las conexiones, para poder escuchar peticiones
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("** Socket creado satisfactoriamente **")
server_socket.bind((hostname, port))
server_socket.listen(1)
print("Esperando conexiones...")

# Función que ejecuta el comando y retorna el resultado
def procesar_comando(comando):
    resultado = ""
    if comando == "exit":
        resultado = comando
    elif comando == "1":
        resultado = obtener_version_servidor()
    elif comando == "2":
        resultado = terminar_conexion_con_cliente()
    elif comando == "3":
        resultado = obtener_informacion_servidor()
    elif comando == "4":
        resultado = mostrar_autores()
    elif comando == "5":
        resultado = ejecutar_tarea_especial()
    elif comando == "ls":
        resultado = "El comando ls se utiliza para listar archivos o directorios en Linux y otros sistemas operativos basados en Unix.\nPara observar un ejemplo, "
    elif comando == "mkdir":
        resultado = "comando mkdir"
    elif comando == "cd":
        resultado = "comando cd"
    elif comando == "sudo":
        resultado = "comando sudo"
    else:
        resultado = "ERROR: Comando no encontrado."

    return resultado

# Nuevas funciones para los comandos
def obtener_version_servidor():
    return "Versión del servidor: 1.0"

def terminar_conexion_con_cliente():
    # Aquí puedes cerrar la conexión con el cliente
    return "Terminando la conexión con el cliente..."

def obtener_informacion_servidor():
    # Ejemplo: obtén información del sistema o recursos del servidor
    import platform
    return f"Información del servidor: {platform.system()} {platform.release()}"

def ejecutar_tarea_especial():
    # Ejemplo: realiza una tarea especial, como crear un archivo en el servidor
    with open("archivo_especial.txt", "w") as archivo:
        archivo.write("Contenido especial")
    return "Realizando tarea especial en el servidor: Se creó un archivo especial"

def mostrar_autores():
    return "Autores: Almanza Torres José Luis, Jimenez Reyes Abraham, Martínez Pardo Esaú"   

# Función que maneja la conexión con un cliente
def manejar_cliente(connection, address):
    try:
        print(f'Conexion establecida con {address}.')
        connection.send(f"~ server ~ Bienvenido, usted ha sido conectado satisfactoriamente al servidor :D\n{opciones}*** Para cerrar la comunicación, ingrese \"exit\" ****".encode('UTF-8'))
        while True:
            data = connection.recv(buffer_size)
            if not data:
                break  # Si el cliente cierra la conexión, salimos del bucle
            peticion = data.decode('utf-8')
            print(f'Petición recibida: \"{peticion}\"')
            respuesta = procesar_comando(peticion)
            print('Respuesta enviada')
            connection.send(respuesta.encode('UTF-8'))
    except Exception as e:
        print(f'Error al manejar la conexión con {address}: {str(e)}')
    finally:
        print(f'~ Cerrando comunicación con {address}... ~')
        connection.close()
        print("** Comunicación cerrada con éxito **")

# Bucle principal para aceptar conexiones
while True:
    client_connection, client_address = server_socket.accept()
    threading.Thread(target=manejar_cliente, args=(client_connection, client_address)).start()
