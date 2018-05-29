# Sofi - Sistema Gestión de Eventos

es una aplicación web para la gestión y organización de eventos, posee interfaz de administración
para gestionar la información de (eventos, presentaciones, ponentes, suscripciones...) y es ideal
como portal web de publicación de eventos tipo blog.

# Pasos para crear el entorno de desarrollo

Cuando somos un usuario normal del sistema, en el terminal se mostrará el siguiente símbolo: ~$

Cuando accedemos al usuario root del sistema, en el terminal se mostrará el siguiente símbolo: ~#

Crear las siguientes carpetas

    ~$ mkdir Programación

Desde el terminal, moverse a la carpeta Programación y ejecutar

    ~$ mkdir Pyhton

Entrar a la carpeta Python y hacer lo siguiente

    ~$ mkdir EntornosVirtuales ProyectosDjango

Probado en Debian y Ubuntu. Instalar curl git graphviz graphviz-dev phppgadmin postgresql python y virtualenv

    ~# apt install curl git graphviz graphviz-dev postgresql phppgadmin python3-dev virtualenv

Para instalar npm hacer lo siguiente

    ~# curl -sL https://deb.nodesource.com/setup_10.x | bash -

    ~# apt install -y nodejs

Desde el terminal, moverse a la carpeta EntornosVirtuales y ejecutar

    ~$ virtualenv -p python3 sofi

Para activar el entorno

    ~$ source sofi/bin/activate

Nos movemos a la Carpeta ProyectosDjango para descargar el sistema con el siguiente comando

    (sofi) ~$ git clone https://gestion.cenditel.gob.ve/scm/git/sofi.git

Tendremos las carpetas estructuradas de la siguiente manera

    // Entorno virtual
    Programación/Python/EntornosVirtuales/sofi

    // Servidor de desarrollo
    Programación/Python/ProyectosDjango/sofi

Instalar las dependencias de css y js: moverse a la carpeta static y ejecutar

    // Usa el archivo package.json para instalar lo que ya se configuro allí
    (sofi) ~$ npm install

    // Terminado el proceso volver a la carpeta raíz del proyecto

Crear la base de datos para __sofi__ usando PostgresSQL

    // Acceso al usuario postgres
    ~# su postgres

    // Acceso a la interfaz de comandos de PostgreSQL
    postgres@xxx:$ psql

    // Creación del usuario de a base de datos
    postgres=# CREATE USER admin WITH LOGIN ENCRYPTED PASSWORD '123' CREATEDB;
    postgres=# \q

    // Desautenticar el usuario PostgreSQL y regresar al usuario root
    postgres@xxx:$ exit

    // Salir del usuario root
    ~# exit

Puedes crear la base de datos usando la interfaz gráfica phppgadmin

    // Desde algún navegador ir al siguiente sitio y entrar con el usuario que se acaba de crear
    localhost/phppgadmin

    // Nombre de la base de datos: sofi

Crear la base de datos para __sofi__ usando MariaDB

    // Acesso al usuario root del sistema
    # mysql

    // Crea el usuario
    CREATE USER 'admin'@'localhost' IDENTIFIED BY '123';

    // Se Otorgan todos los permisos
    GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';

    FLUSH PRIVILEGES;

Puedes crear la base de datos usando la interfaz gráfica phpmyadmin

    // Desde algún navegador ir al siguiente sitio y entrar con el usuario que se acaba de crear
    localhost/phpmyadmin

    // Nombre de la base de datos: sofi

Instalamos los requemientos que el sistema necesita en el entorno virtual

    (sofi) ~$ pip install -r requirements.txt

Hacer las migraciones

    (sofi) ~$ python manage.py makemigrations base usuario

    (sofi) ~$ python manage.py migrate

Crear usuario administrador

    (sofi) ~$ python manage.py createsuperuser

Correr el servidor de django

    (sofi) ~$ python manage.py runserver

Poner en el navegador la url que sale en el terminal para entrar el sistema

Llegado hasta aquí el sistema ya debe estar funcionando

Para salir del entorno virtual se puede ejecutar desde cualquier lugar del terminal: deactivate

