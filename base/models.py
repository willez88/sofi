from django.db import models


class Country(models.Model):
    """!
    Clase que contiene los paises

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre del pais
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        """

        return self.name


class State(models.Model):
    """!
    Clase que contiene los estados que se encuentran en un país

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre del Estado
    name = models.CharField(max_length=50, unique=True)

    # Pais en donde esta ubicado el Estado
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        """

        return self.name


class Municipality(models.Model):
    """!
    Clase que contiene los municipios que se encuentran en un estado

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre del Municipio
    name = models.CharField(max_length=50, unique=True)

    # Estado en donde se encuentra el Municipio
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        """

        return self.name


class City(models.Model):
    """!
    Clase que contiene las ciudades que se encuentran en un estado

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre de la Ciudad
    name = models.CharField(max_length=50, unique=True)

    # Estado en donde se encuentra ubicada la Ciudad
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        """

        return self.name


class Parish(models.Model):
    """!
    Clase que contiene las parroquias que se encuentran un municipio

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre de la Parroquia
    name = models.CharField(max_length=50, unique=True)

    # Municipio en el que se encuentra ubicada la Parroquia
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        """

        return self.name


class Location(models.Model):
    """!
    Clase que contiene los datos de una ubicación geográfica

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Establece la dirección exacta
    address = models.CharField(max_length=500)

    # Establece la relación entre la parroquia y la ubicación
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        """

        return self.address
