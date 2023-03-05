import os
def listarArchivos ():
    contenido = os.listdir('/home/ubuntu/reto2/')
    contenidoStr = ", ".join(contenido)
    print(contenido)
    return contenidoStr
