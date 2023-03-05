import os

def buscarArchivos(nombre):
    mensaje = ""
    contenido = os.listdir('/home/ubuntu/reto2/')
    if(nombre in contenido):
      mensaje = f"El archivo {nombre} si está en el directorio"
    else:
      mensaje = f"El archivo {nombre} no está en el directorio"
    return mensaje
