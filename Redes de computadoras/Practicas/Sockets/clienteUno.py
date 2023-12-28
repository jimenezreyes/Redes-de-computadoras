#Equipo 5 
#Almanza Torres José Luis
#Jimenez Reyes Abraham
#Martínez Pardo Esaú

# CLIENTE
import socket
import threading

#Obtener nombre socket
host = socket.gethostname() 
# IP del servidor (usando la dirección IP de la interfaz inalámbrica)
server_ip = "192.168.1.71"
#IP del servidor
port = 8001
#Tamaño de bits que van a ser recibidos
buffer = 1024

s = socket.socket()

#Solicitud de conexión con servidor
s.connect((host, port))

#Espera de recepción de conexión con el servidor 
data = s.recv(buffer)
#Protegemos el mensaje 
print (data.decode('utf-8'))

while True:

  # Enviando el mensaje al servidor 
  mensaje = input("Escribe un mensaje: ")
  print('Mi petición al servidor es: \"{}\"'.format(mensaje))
  s.send(mensaje.encode('utf-8'))
  respuesta = s.recv(buffer)
  entrada = respuesta.decode('utf-8')
  print("Respuesta del servidor:\n", entrada)

  #Cerrando conexión 
  if entrada == "exit":
    print("Conexión cerrada exitosamente")
    break
s.close()
