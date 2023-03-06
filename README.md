# ST0263 - Tópicos especiales en telemática
# Juan Pablo Yepes García, jpyepesg@eafit.edu.co
# Edwin Nelson Montoya Munera, emontoya@eafit.edu.co

## Reto #2
1. En el reto #2 se realizo el diseño y la implementación de los sistemas de comunicación MOM y gRPC con python y aws. El esquema consiste en un api gateway en el que se implementa un balanceador de cargas tipo round robin para intercalar el uso de los sistemas de comunicación anteriormente mencionados.

1.1  Se cumplieron los requerimientos funcionales propuestos en el reto. Se cumplió con implementar la comunicación gRCP, la comunicación MOM, los microservicios, el balanceador de cargas y el api gateway.

2. El diseño de la arquitectura es cliente/servidor y se trato de dejar todo con bajo acoplamiento separando los archivos de las comunicaciones.
3. Se utilizó el ambiente de desarrollo Visual Studio acompañado de git para comunicarse con la maquina virtual en AWS, todo el proyecto se desarrollo en el lenguaje de programación python en la versión 3.9.6, se utilizaron librerías básicas como `sys` , `os` y aparte se añadieron todas las librerías necesarias para la comunicación gRPC y para la comunicación MOM.
4. Para ejecutarlo se debe iniciar la instancia creada con el nombre 'reto2' en AWS abrir dos terminales y  en una correr los comandos: 
```console
sudo chmod 777 mom.sh
sudo chmod 777 grpc.sh
./mom.sh
```
Luego se debe abrir la otra terminal y correr el comando:
```console
./grpc.sh
```
Luego buscar en las propiedades de la instancia la ip pública, después se debe abrir un navegador. Para listar archivos en la url se debe poner: `ippública:8000/listarArchivos` y esto devolverá un json con la lista de archivos de la carpeta pre definida, para buscar archivos se debe poner en la url: `ippública:8000/buscarArchivos/nombreArchivoABuscar`
esto devolverá un json con una respuesta de si está o no esta el archivo dentro de los elementos listados de la carpeta predefinida.
Los puertos habilitados en la instancia de AWS son: `8000, 5672, 15672`.

## Referencias

* [FastAPI](https://fastapi.tiangolo.com/es/)

* [gRPC](https://grpc.io/docs/languages/python/basics/)
