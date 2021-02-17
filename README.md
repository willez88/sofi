# Sofi - Sistema Gestión de Eventos

es una aplicación web para la gestión y organización de eventos, posee interfaz de administración
para gestionar la información de (eventos, presentaciones, ponentes, suscripciones...) y es ideal
como portal web de publicación de eventos tipo blog.

# Pasos para crear el entorno de desarrollo

Cuando somos un usuario normal del sistema, en el terminal se mostrará el siguiente símbolo: ~$

Cuando accedemos al usuario root del sistema, en el terminal se mostrará el siguiente símbolo: ~#

Probado en Debian y Ubuntu. Instalar los siguientes programas

    ~# apt install curl git graphviz graphviz-dev libfreetype6-dev libjpeg-dev libz-dev postgresql phppgadmin python3-dev python3-setuptools virtualenv

Para instalar npm hacer lo siguiente

    // Ubuntu
    ~$ curl -sL https://deb.nodesource.com/setup_lts.x | sudo -E bash -

    // Debian
    ~# curl -sL https://deb.nodesource.com/setup_lts.x | bash -

    ~# apt install -y nodejs

Crear las siguientes carpetas

    ~$ mkdir Programación

Desde el terminal, moverse a la carpeta Programación y ejecutar

    ~$ cd Programación/

    ~$ mkdir python

Entrar a la carpeta python y hacer lo siguiente

    ~$ cd python/

    ~$ mkdir entornos_virtuales proyectos_django

Entrar a Entornos Virtuales

    ~$ cd entornos_virtuales/

    ~$ mkdir django

Desde el terminal, moverse a la carpeta django y ejecutar

    ~$ cd django/

    ~$ virtualenv -p python3 sofi

Para activar el entorno

    ~$ source sofi/bin/activate

Nos movemos a la carpeta proyectos_django, descargamos el sistema y entramos a la carpeta con los siguientes comandos

    (sofi) ~$ cd ../../proyectos_django/

    # Si se hace el clone en CENDITEL
    (sofi) ~$ export GIT_SSL_NO_VERIFY=1

    # Desde el repositorio de CENDITEL
    (sofi) ~$ git clone https://gestion.cenditel.gob.ve/scm/git/sofi.git

    # Desde github
    (sofi) ~$ git clone https://github.com/willez88/sofi.git

    (sofi) ~$ cd sofi/

    (sofi) ~$ cp sofi/settings.default.py sofi/settings.py

Tendremos las carpetas estructuradas de la siguiente manera

    // Entorno virtual
    Programación/python/entornos_virtuales/django/sofi

    // Servidor de desarrollo
    Programación/python/proyectos_django/sofi

Instalar las dependencias de css y js: moverse a la carpeta static y ejecutar

    (sofi) ~$ cd static/

    // Usa el archivo package.json para instalar lo que ya se configuro allí
    (sofi) ~$ npm install

    // Terminado el proceso volver a la carpeta raíz del proyecto
    (sofi) ~$ cd ../

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

Instalamos los requemientos que el sistema necesita en el entorno virtual

    (sofi) ~$ pip install -r requirements/dev.txt

Hacer las migraciones y cargar los datos iniciales

    (sofi) ~$ python manage.py makemigrations base user event

    (sofi) ~$ python manage.py migrate

    (sofi) ~$ python manage.py loaddata 1_country.json 2_state.json 3_municipality.json 4_city.json 5_parish.json

Crear usuario administrador

    (sofi) ~$ python manage.py createsuperuser

Correr el servidor de django

    (sofi) ~$ python manage.py runserver

Poner en el navegador la url que sale en el terminal para entrar el sistema

Llegado hasta aquí el sistema ya debe estar funcionando

Para salir del entorno virtual se puede ejecutar desde cualquier lugar del terminal: deactivate

Generar modelo de datos relacional del __sofi__ completo. Crea la imagen en la raíz del proyecto

    (sofi) ~$ python manage.py graph_models -a -g -o sofi.svg

Generar modelo de datos relacional de las aplicaciones del proyecto

    (sofi) ~$ python manage.py graph_models base -g -o base.svg

    (sofi) ~$ python manage.py graph_models user -g -o user.svg

    (sofi) ~$ python manage.py graph_models event -g -o event.svg
