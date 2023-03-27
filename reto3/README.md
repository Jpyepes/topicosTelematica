# Materia: ST0263
# Estudiante: Juan Pablo Yepes García, jpyepesg@eafit.edu.co
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.brightspace.com
## Descripción
En este proyecto se implementaron una serie de instancias en GCP para crear un entorno de un WordPress escalable. Durante el proceso se crearon 5 instancias tipo E2 con sistema operativo Ubuntu 20.04. La idea del proyecto era crear una instancia en donde se instalaría WordPress y se conectaría a otra instancia en donde estaría instalada la base de datos MySql. Posteriormente se crearía una instancia espejo del WordPress para luego desde una instancia nueva crear un balanceador de cargas y permitir la disponibilidad del servicio (página web). Por último se crearía una instancia implementando un NFS el cual permite montar directorios remotos y administrar el espacio de almacenamiento.
Todo lo anterior se cumplió durante el desarrollo del proyecto. 

Para el desarrollo de este proyecto se necesita una cuenta en GCP.  
1. **NFS (Network file system)**:  
El NFS en sí necesita dos instancias para configurar, sin embargo, este paso será para configurar la parte del host.
Primero se deben ejecutar estos comandos en la terminal:
```bash
sudo apt update
sudo apt install nfs-kernel-server
```
Después se deben ejecutar los siguientes comandos para crear los directorios compartidos en el host:
```bash
sudo mkdir /var/nfs/general -p
ls -dl /var/nfs/general
```
Esto deberá generar una salida en terminal que se vea de esta manera: 
```bash
drwxr-xr-x 2 root root 4096 Apr 17 23:51 /var/nfs/general
```
Después se debe ejecutar el siguiente comando para asignar las credenciales al grupo `nonegroup`:
```bash
sudo chown nobody:nogroup /var/nfs/general
```
Ahora bien, se debe abrir el archivo `exports` ejecutando el siguiente comando:
```bash
sudo nano /etc/exports
```
El comando anterior abrirá el archivo
`exports`, allí se deben agregar las siguientes lineas:
```bash
/var/nfs/general    client_ip(rw,sync,no_root_squash,no_subtree_check)
/home               client_ip(rw,sync,no_root_squash,no_subtree_check)
```
Y en donde dice `client_ip` se debe poner la Ip privada que englobe las dos instancias, en mi caso se pondría `10.128.0.0/16`
Por último reiniciamos el servidor con NFS con el siguiente comando:
```bash
sudo systemctl restart nfs-kernel-server
``` 
2. **Base de datos (MySql)**  
Para la configuración de la base de datos primero se deben poner estos comandos en la terminal:
```bash
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y

sudo systemctl enable docker
sudo systemctl start docker
``` 
Posteriormente se crea un archivo llamado `confbd.yml` en donde se le añade lo siguiente (copiar y pegar):
```bash
version: '3.1'
services:
  db:
    image: mysql:5.7
    restart: always
    ports:
      - 3306:3306 
    environment:
      MYSQL_DATABASE: exampledb
      MYSQL_USER: exampleuser
      MYSQL_PASSWORD: examplepass
      MYSQL_RANDOM_ROOT_PASSWORD: '1'
    volumes:
      - db:/var/lib/mysql
volumes:
  db:
``` 
Por último se debe correr este comando en terminal:
```bash
sudo docker-compose -f confdb.yml up
```
**IMPORTANTE:** no cerrar el cliente SSH de ninguna instancia para poder hacer pruebas después de finalizar las configuraciones necesarias.    

3. **WordPress**  
Para la configuración del WordPress se deben correr primero estos comandos en la terminal de la instancia de WordPress:
```bash
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y

sudo systemctl enable docker
sudo systemctl start docker
``` 
Lo siguiente será crear un archivo llamado `confwordpress.yml` en donde se añade lo siguiente (copiar y pegar):
```bash
version: '3.1'
services:
  wordpress:
    container_name: wordpress
    image: wordpress
    ports:
      - 80:80      
    restart: always
    environment:
      WORDPRESS_DB_HOST: <ip-privada>
      WORDPRESS_DB_USER: exampleuser
      WORDPRESS_DB_PASSWORD: examplepass
      WORDPRESS_DB_NAME: exampledb
    volumes:
      - /mnt/wordpress:/var/www/html
```
**NOTA:** reemplazar `<ip-privada>` por la ip privada de la instancia del WordPress.  

Por último se debe correr este comando en terminal:
```bash
sudo docker-compose -f confwordpress.yml up
```
**IMPORTANTE:** no cerrar el cliente SSH de ninguna instancia para poder hacer pruebas después de finalizar las configuraciones necesarias.  

Para terminar de configurar WordPress se debe acceder a un browser y poner la IP pública de la instancia, esto abrirá un panel de WordPress en donde se podrán hacer las configuraciones correspondientes.

4. **WordPress Espejo**  
Como se explicó anteriormente en este proyecto se tendrán dos instancias WordPress para mejorar la disponibilidad del servicio por lo que en este paso se deberá crear una instancia y se debe repetir el paso 3 en su totalidad.  

5. **Balanceador de cargas (nginx)**  
**NOTA:** esta instancia debe tener una IP estática.  
**IMPORTANTE:** crear dominio web. 
  
Para configurar el balanceador de cargas se deben ejecutar primeramente estos comandos en terminal:
```bash
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y

sudo systemctl enable docker
sudo systemctl start docker
``` 
Lo siguiente es configurar el certificado SSL con certbot ejecutando los siguientes comandos:
```bash
sudo add-apt-repository ppa:certbot/certbot
sudo apt install letsencrypt -y
sudo apt install nginx -y
``` 
Lo siguiente es crear un archivo llamado `nginx.conf` y añadir lo siguiente (copiar y pegar):
```bash
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
  worker_connections  1024;  ## Default: 1024
}
http {  

 upstream backend{  
       server <ip_privada_1>  
       server <ip_privada_2>
}

server {
  listen 80;
  listen [::]:80;

  server_name _;
  rewrite ^ https://$host$request_uri permanent;
}

server {
  listen 443 ssl http2 default_server;
  listen [::]:443 ssl http2 default_server;

  server_name _;

  # enable subfolder method reverse proxy confs
  #include /config/nginx/proxy-confs/*.subfolder.conf;

  # all ssl related config moved to ssl.conf
  include /etc/nginx/ssl.conf;

  client_max_body_size 0;

  location / {
    proxy_pass http://backend;
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Server $host;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
}
``` 
**NOTA:** cambiar `<ip_privada_1>` e `<ip_privada_2>` por las IP's privadas de las instancias de los WordPress.  

Ejecutar los siguientes comandos:
```bash
sudo mkdir -p /var/www/letsencrypt
sudo nginx -t

sudo service nginx reload
``` 
El siguiente paso es pedir el certificado SSL con los siguientes comandos:
```bash
sudo letsencrypt certonly -a webroot --webroot-path=/var/www/letsencrypt -m <correo> --agree-tos -d <dominio.ext>
``` 
**NOTA:** cambiar campos `<correo>` y `<dominio.ext>` por los respectivos. El correo es el mismo que esta registrado en GCP.

Después correr estos comandos en la terminal:
```bash
mkdir /home/gcp-username/wordpress
mkdir /home/gcp-username/wordpress/ssl
sudo su
```
Y seguir con los siguientes comandos: 
```bash
cp /etc/letsencrypt/live/<dominio.ext>/* /home/<gcp-username>/wordpress/ssl/
exit
```
**NOTA:** cambiar campos `<gcp-username>` y `<dominio.ext>` por los respectivos. El correo es el mismo que esta registrado en GCP. El `<gcp-username>` es el usuario que aparece en la terminal SSH.  
Seguir con el siguiente comando:
```bash
sudo usermod -a -G docker <gcp-username>
```
Lo siguiente es crear un archivo llamado `docker-compose.yml` y añadir lo siguiente (copiar y pegar):
```bash
version: '3.1'
services:
  nginx:
    container_name: nginx
    image: nginx
    volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - ./ssl:/etc/nginx/ssl
    - ./ssl.conf:/etc/nginx/ssl.conf
    ports:
    - 80:80      
    - 443:443
``` 
Y también crear un archivo llamado `ssl.conf` y añadir lo siguiente (copiar y pegar):
```bash
## Version 2018/05/31 - Changelog: https://github.com/linuxserver/docker-letsencrypt/commits/master/root/defaults/ssl.conf

# session settings
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# Diffie-Hellman parameter for DHE cipher suites
# ssl_dhparam /etc/nginx/ssl/ssl-dhparams.pem;

# ssl certs
ssl_certificate /etc/nginx/ssl/fullchain.pem;
ssl_certificate_key /etc/nginx/ssl/privkey.pem;

# protocols
ssl_protocols TLSv1.1 TLSv1.2;
ssl_prefer_server_ciphers on;
ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';

# HSTS, remove # from the line below to enable HSTS
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;

# Optional additional headers
#add_header Content-Security-Policy "upgrade-insecure-requests";
#add_header X-Frame-Options "SAMEORIGIN" always;
#add_header X-XSS-Protection "1; mode=block" always;
#add_header X-Content-Type-Options "nosniff" always;
#add_header X-UA-Compatible "IE=Edge" always;
#add_header Cache-Control "no-transform" always;
#add_header Referrer-Policy "same-origin" always;
``` 
ahora bien, se deben correr los siguientes comandos en la terminal:  
```bash
sudo cp docker-compose.yml /home/<gcp-username>/wordpress/docker-compose.yml

sudo cp nginx.conf /home/<gcp-username>/wordpress
sudo cp ssl.conf /home/<gcp-username>/wordpress
```
Lo siguiente es correr estos comandos para asegurarse de que nginx no esta corriendo:
```bash
ps ax | grep nginx

sudo systemctl disable nginx
sudo systemctl stop nginx
```
Y por último se corren los siguientes comandos:
 ```bash
cd /home/<gcp-username>/wordpress
docker-compose up --build -d
```
Ahora bien, se puede buscar el nombre del dominio desde un browser y aparecerá la página creada en WordPress.  

6. **Configuración NFS cliente**  
**NOTA:** hacer cada instrucción mostrada en este paso para las dos instancias de WordPress. 
 
Correr el siguiente comando para instalar nfs-common:
 ```bash
sudo apt install nfs-common
```
lo siguiente será correr estos comandos en la terminal:
 ```bash
sudo mkdir -p /nfs/general
sudo mkdir -p /nfs/home

sudo mount <host_ip>:/var/nfs/general /nfs/general
sudo mount <host_ip>:/home /nfs/home
```
**NOTA:** cambiar `<host_ip>` por la dirección IP privada de la instancia del host del NFS.
Por último correr el comando:
```bash
df -h
```
Con lo cual saldrás esto en la terminal:
```bash
Filesystem                   Size  Used Avail Use% Mounted on
tmpfs                        198M  972K  197M   1% /run
/dev/vda1                     50G  3.5G   47G   7% /
tmpfs                        989M     0  989M   0% /dev/shm
tmpfs                        5.0M     0  5.0M   0% /run/lock
/dev/vda15                   105M  5.3M  100M   5% /boot/efi
tmpfs                        198M  4.0K  198M   1% /run/user/1000
<host_ip>:/var/nfs/general   25G  5.9G   19G  24% /nfs/general
<host_ip>:/home              25G  5.9G   19G  24% /nfs/home
```
Si se logra observar las dos ultimas líneas es porque ya esta lista la configuración. 
## Bibliografía

[Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-22-04)  
[GitHub Repo](https://github.com/st0263eafit/st0263-231/tree/main/docker-nginx-wordpress-ssl-letsencrypt)
