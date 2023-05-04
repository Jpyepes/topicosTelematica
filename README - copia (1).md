# Info de la materia: ST0623 <Tópicos Especiales En Telemática>
# Estudiante(s):
## Andrés Felipe Téllez Rodríguez, aftellezr@eafit.edu.co
## Juan Pablo Yepes Garcia, jpyepesg
##
# Profesor: Edwin Nelson Montoya Munera, emontoya

## 1. Breve descripción de la actividad

El reto consiste en desplegar una aplicación tipo sistema de gestión del conocimiento, allí se indica que para este caso la plataforma seleccionada será Moodle. 
Durante el desarrollo se logró cumplir con todos los requerimientos propuestos en el texto del reto #4. 
## 2. Pasos a seguir
En esta sección se mostrará paso por paso el desarrollo del reto, cabe aclarar que primero se desarrollo una versión parcialmente monolítica del reto para así entender y afianzar los conocimientos y conceptos vistos en clase, además para tener un mejor entendimiento del problema a solucionar. 
 ### Versión monolítica
 * Crear una instancia en GCP con imagen ubuntu 22.04 LTS  
 * Abrir el cliente SSH de la instancia creada y correr los siguientes comandos en terminal:   
```bash
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y

sudo systemctl enable docker
sudo systemctl start docker
```
Estos comandos sirven para instalar y empezar docker y docker-compose  
* Como paso siguiente se debe correr el comando:  
```bash
sudo nano docker-compose.yml
``` 
El cual nos permitirá crear un archivo llamado docker-compose.  
* Como paso siguiente se debe remitir a las referencias de esta documentación y entrar a `Docker-compose Moodle` allí se baja un poco y se busca el link de `docker-compose.yml` lo cual abrirá un archivo en Git Hub el cual se debe copiar y pegar en el archivo creado en nuestra instancia.

El archivo de docker-compose que sera el monolítico se ve asi:
![docker_compose_or](https://user-images.githubusercontent.com/85372114/235812079-64ea86a5-a8fa-4379-a7e6-c7a2de0fbe9d.jpeg)
#### *Imagen 1*  

* Ahora se corre el siguiente comando para correr el archivo docker-compose:
```bash
sudo docker-compose up
``` 
* Después de correr el comando anterior se debe esperar aproximadamente unos 5 minutos y se podrá ver la aplicación desplegada buscando la ip publica de la instancia en un browser.



Corremos en nuestra instancia el ultimo comando de la primera imagen que nos permitirá desplegar la página.

La pagina y lo que terminara siendo nuestra meta se ve asi:
![PagCor](https://user-images.githubusercontent.com/85372114/235812286-73c724f1-bb50-4291-857f-7e70cd0f3232.JPEG)
#### *Imagen 2*

### Versión final
* Para la versión final empezamos creando la base de datos, para ello utilizaremos el servicio SQL de GCP, se crea una instancia y adentro de esa instancia se crea una base de datos.

![base_de_datos](https://user-images.githubusercontent.com/85372114/235812369-7bc641e4-acfd-415f-a367-105fdab620d6.jpeg)
#### *Imagen 3*

* Después de tener la base de datos creada se debe crear una instancia de VM similar a la instancia creada en la versión monolitica, sin embargo se debe cambiar el archivo docker-compose.yml. Allí se agrega la información que es requerida que fue provista por la base de datos que creamos con la instancia SQL y colocamos el puerto 443, además de asegurarse que el comando restart este en always para que cada vez que iniciamos la instancia el archivo vuelva a correr automaticamente y agregar la linea `- /mnt/moodle:/var/www/html` para avisar que habrá una carpeta de archivos compartidos en esta ruta.

El resultado es:

![docker_compose](https://user-images.githubusercontent.com/85372114/235812431-e301f519-a725-4e2d-af70-5cb66088e6a4.JPEG)
#### *Imagen 4*

* Ahora se corre el siguiente comando para correr el archivo docker-compose y así aplicar los cambios :
```bash
sudo docker-compose up
``` 

Una vez con eso creado se guarda y se pasa a la creación del NFS Server. Se busca en el GCP de Google Filestore y se crea una instancia

Proceso de creacion:
![Config_NFS_Server](https://user-images.githubusercontent.com/85372114/235818018-67d8c438-8f42-45f0-9c15-ff94a847f8c8.jpeg)
#### *Imagen 6*

Lo primero que se hizo es correr los siguientes comandos en la instancia de la VM:

![NFS_Comand](https://user-images.githubusercontent.com/85372114/235818163-4cb2a0e4-32d4-4a25-b1c5-498a86235808.jpeg)
#### *Imagen 7*

Estos comandos permitirán instalar el nfs-common en el cliente (instancia Moodle) y crear una carpeta llamada /mnt/moodle para posteriormente aplicar el mount y poder enlazar esa carpeta con el nfs-server. El ultimo comando permitirá verificar que el mount se haya hecho ya que aparecerá la ip de la instancia del nfs-server.ando.


![Mount_NFS](https://user-images.githubusercontent.com/85372114/235818828-85309981-f508-4859-a384-420dfabd5310.jpeg)
#### *Imagen 8*


Para objetivos de escalabilidad, se automatizó el mount. Para realizar esto ejecutamos el siguiente comando:

![Auto_NFS](https://user-images.githubusercontent.com/85372114/235818444-7b245717-ecc8-426e-9c44-434c4196a59e.jpeg)
#### *Imagen 9*

Esto abrirá el archivo fstab en el cual se le colocara el texto debajo del comando quedando asi:

![fstab](https://user-images.githubusercontent.com/85372114/235819289-d0dc5a3f-715e-472c-ba15-7207e5be42e6.jpeg)
#### *Imagen 10*

Ya teniendo el Nfs server y la base de datos por separado utilizando los servicios de GCP lo siguiente es hacer escalable la instancia de Moodle. Para esto se debe crear una imagen de la instancia anteriormente creada para posteriormente crear una plantilla de instancia utilizando como imagen la creada anteriormente.
Después de esto se hace click en los 3 puntos de la plantilla de instancia para crear un grupo de instancias el cual se hará auto escalable poniendo como mínimo 2 instancias y como máximo las que se deseen.

![autoscaling_group](https://user-images.githubusercontent.com/85372114/235819560-303e6bf0-0ac3-4a84-b352-0f41c3f01022.jpeg)
#### *Imagen 11*

Asi se debe de ver activado:

![autoscaling_group_on](https://user-images.githubusercontent.com/85372114/235819716-e8f02649-d2ce-437c-baac-ad063989503e.JPEG)
#### *Imagen 12*


Finalmente se genera el balanceador de cargas, buscando en GCP Load Balancing, se crea uno por https.
![balanceador_carga_1](https://user-images.githubusercontent.com/85372114/235819768-66d3a4b2-b174-4221-9b65-1dd768bf3f70.JPEG)
#### *Imagen 13*

Se selecciona el balanceador de cargas adecuado

![balanceador_carga_2](https://user-images.githubusercontent.com/85372114/235819891-e778c1b3-42f4-49c7-a6ee-5a960aea06c1.JPEG)
#### *Imagen 14*

Se llena la información y se empieza la creación del certificado SSL, donde definimos cual sera el dominio que usaremos

![balanceador_carga_3](https://user-images.githubusercontent.com/85372114/235819897-b4f494cb-6e69-4b7b-8923-ab1968aa8c78.JPEG)
#### *Imagen 15*

Para la configuración del backend, como no tenemos una previamente creada se crea una nueva

![balanceador_carga_4](https://user-images.githubusercontent.com/85372114/235819902-1552fbf3-32d6-4ea4-94c7-a319b903d72f.JPEG)
#### *Imagen 16*

Se llena la informacion requerida para el backend configurando el puerto que vamos a usar, en este caso el 443

![balanceador_carga_5](https://user-images.githubusercontent.com/85372114/235819911-7e2be3fb-103c-471d-9f00-627d5924e15d.JPEG)
#### *Imagen 17*

Una vez creado la configuración del backend se selecciona esta como la que vamos a usar, despues terminamos la creación del certificado SSL, y se espera a que sea aceptada, y se termina la configuración del balanceador quedando así:

![balanceador_carga_6](https://user-images.githubusercontent.com/85372114/235819919-df1a6c63-1e15-4bca-8cf1-15b144dc8423.JPEG)
#### *Imagen 18*


La pagina web ya debe de estar disponible usando el enlace que se le dio al balanceador.

![PagCor](https://user-images.githubusercontent.com/85372114/235812286-73c724f1-bb50-4291-857f-7e70cd0f3232.JPEG)
#### *Imagen 19*

## Referencias:
* [FileStore](https://cloud.google.com/filestore/docs/create-instance-console) 
* [Nfs Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-22-04)
* [Load Balancing](https://cloud.google.com/load-balancing?hl=es-419) 
* [Git Hub Curso](https://github.com/st0263eafit/st0263-231) 
* [Docker-compose Moodle](https://hub.docker.com/r/bitnami/moodle) 
#### versión README.md -> 1.0 (2023-Mayo)