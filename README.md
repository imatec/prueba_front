prueba_front
============

Descripción
-----------

Pequeña aplicación en Flask para probar habilidades de desarrollador front

El objetivo es construir una interfaz de usuario consistente en 2 pantallas:

* Login: 
    * Se debe ingresar un rut con guión y dígito verificador (por ej. 6-K). 
    * Si las credenciales son correctas la API devuelve un token y se debe mostrar la pantalla de Tickets.

* Tickets:
    * Utilizando el token se debe poder consultar el listado de tickets o cualquier recurso disponible por la API
    * El nombre de los tickets debe aparecer en el elemento select.
    * Utilizando el elemento checkbox, se debe poder filtrar aquellos tickets que están asignados al usuario de la sesión actual.
    * Al seleccionar una opción se debe mostrar la descripción del ticket en el elemento de texto. 

![Alt](/wireframes.jpg "")

Implementación
--------------
La API expone los siguientes métodos:

GET /api/token
Utiliza HTTP Basic Auth, por lo que se deben enviar credenciales en header *Authorization* con valores *Basic user:pass*
Como respuesta la aplicación entregará JSON con token y tiempo de duración en segundos.

GET /api/current
La aplicación expone JSON con información del usuario en sesión (asociado al token) actual.

GET /api/tickets
La aplicación lista todos los tickets del sistema en formato JSON.

Para programar la lógica de cliente se estableció el archivo *template/index.html* en la ruta raiz de la aplicación (línea 174 de prueba_front.py), pero puede agregar cuantas rutas desee. 
Este archivo utiliza un lenguaje de template (Jinja2) y se muestran algunos ejemplos de como incluir archivos con rutas relativas al directorio *static* para incluir CSS, JavaScript, etc. 

Cada *Usuario* tiene un campo "id", el cual se utiliza como llave foranea para cada *Ticket* mediante su campo *user_id*


Problemas a resolver
--------------------
En base a los objetivos y la implemntación debe demostrar capacidad para resolver los siguientes objetivos:

* El postulante tiene libertad de modificar el archivo *template/index.html* como desee, así como de generar mas rutas.
* Deberá implementar los elementos de cada pantalla (Login y Tickets), en HTML5, según el framework o librería de su elección.
* Debe implementar las 2 pantallas mencionadas (Login y Tickets).
* Para realizar consultas a API tiene 2 opciones:
    * la opción de enviar en cada consulta el usuario y contraseña (menos puntos).
    * la opción de enviar la credencial solo las veces que se necesiten, utilizando el resto de las consultas el token. Es decir, enviando las credenciales 1 vez al inicio y luego por cada vez que caduque el tiempo de vida del token (mas puntos).
* Los tickets se obtienen todos juntos en un JSON como resultado de una misma consulta (*/api/tickets* no implementa filtros ni parametrización), por lo que para poder mostrar los tickets asociados a un usuario específico, debe implementar alguna forma de filtrado en el cliente. 
* Para resolver cualquiera de los puntos puede almacenar información temporalmente, por ejemplo localStorage, o según las alternativas del framework o librería que utilice 


Envío de resultados
-------------------

El postulante deberá subir esta aplicación a un repositorio GIT (Github, GitLab, Bitbucket, etc.) y es responsable de adjuntar todas sus modificaciones a la línea principal, ya sea archivos nuevos de template, archivos estáticos, etc. como modificaciones a rutas en prueba_front.py.
También podrá adjuntar un texto explicativo si lo desea.
No es necesario dejar la aplicación funcionando en alguna plataforma, pero si lo estima conveniente para demostrar su solución, también lo podrá hacer.

Instalación
-----------

#### 1. Instalar python (probado con versión 2.7) y pip
* En linux y otros utilizando el gestor de paquetes.
* En windows el instalador  https://www.python.org/downloads/windows/ en la instalación seleccionar pip como parte de la instalación.
    * Agregar scripts al PATH o ejecutar desde powershell (referencia: http://docs.python-guide.org/en/latest/starting/install/win/):
    ```
    PS > [Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")
    ```
Verificar ejecutando *python -V*.

#### 2. Instalar virtualenv
Instalar virtualenv que permitirá manejar un ambiente para la aplicación, con sus dependencias específicas y sin modificar la del sistema.
    ```
    pip install virtualenv
    ```

#### 3. Clonar repo y crear ambiente virtual *venv*
Clonar con git y en el directorio del repo crear el ambiente virtual (es importante que se llame *venv* para que no se suban los archivos al repo ya que esta ruta está agregada al .gitignore).
    ```
    git clone https://<ruta del repo>.git
    cd prueba_front
    virtualenv venv
    ```

#### 4. Activar ambiente virtual 
(referencia: https://virtualenv.pypa.io/en/stable/userguide/#activate-script)
En linux (o sistema Posix):
    ```
    $ source venv/bin/activate
    ```
En windows, se debe primero cambiar las políticas de ejecución de scripts. Desde powershell:
    ```
    PS > Set-ExecutionPolicy RemoteSigned
    ```
y luego ejecutar:
    ```
    PS > .\venv\Scripts\activate
    ```

#### 5. Instalación de dependencias
La shell habrá cambiado a (venv) para notar que se está trabajando sobre el ambiente virtual. Ejecutar:
    ```
    (venv) PS > pip install -r .\requirements.txt
    ```

#### 6. Creación de Base de Datos
Siempre manteniendose dentro de *venv*, para generar una BD SQLite (db.sqlite) para desarrollo, ejecutar:
    ```
    (venv) PS > python .\prueba_front.py create_data
    ```

#### 7. Ejecutar la aplicación
Para ejecutar la aplicación web, en localhost y puerto 5000:
    ```
    (venv) PS > python .\prueba_front.py runserver --host 127.0.0.1 --port 5000 --debug --reload
    ```
Para detener la aplicación presionar CTRL-C. Para salir del ambiente virtual ejecutar deactivate:
    ```
    (venv) PS > deactivate
    PS >
    ```

REST-auth
=========

Companion application to my [RESTful Authentication with Flask](http://blog.miguelgrinberg.com/post/restful-authentication-with-flask) article.

Installation
------------

After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

If you are on Windows, then use the following commands instead:

    $ virtualenv venv
    $ venv\Scripts\activate
    (venv) $ pip install -r requirements.txt

Running
-------

To run the server use the following command:

    (venv) $ python api.py
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

Then from a different terminal window you can send requests.

API Documentation
-----------------

- POST **/api/users**

    Register a new user.<br>
    The body must contain a JSON object that defines `username` and `password` fields.<br>
    On success a status code 201 is returned. The body of the response contains a JSON object with the newly added user. A `Location` header contains the URI of the new user.<br>
    On failure status code 400 (bad request) is returned.<br>
    Notes:
    - The password is hashed before it is stored in the database. Once hashed, the original password is discarded.
    - In a production deployment secure HTTP must be used to protect the password in transit.

- GET **/api/users/&lt;int:id&gt;**

    Return a user.<br>
    On success a status code 200 is returned. The body of the response contains a JSON object with the requested user.<br>
    On failure status code 400 (bad request) is returned.

- GET **/api/token**

    Return an authentication token.<br>
    This request must be authenticated using a HTTP Basic Authentication header.<br>
    On success a JSON object is returned with a field `token` set to the authentication token for the user and a field `duration` set to the (approximate) number of seconds the token is valid.<br>
    On failure status code 401 (unauthorized) is returned.

- GET **/api/resource**

    Return a protected resource.<br>
    This request must be authenticated using a HTTP Basic Authentication header. Instead of username and password, the client can provide a valid authentication token in the username field. If using an authentication token the password field is not used and can be set to any value.<br>
    On success a JSON object with data for the authenticated user is returned.<br>
    On failure status code 401 (unauthorized) is returned.

Example
-------

The following `curl` command registers a new user with username `miguel` and password `python`:

    $ curl -i -X POST -H "Content-Type: application/json" -d '{"username":"miguel","password":"python"}' http://127.0.0.1:5000/api/users
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 27
    Location: http://127.0.0.1:5000/api/users/1
    Server: Werkzeug/0.9.4 Python/2.7.3
    Date: Thu, 28 Nov 2013 19:56:39 GMT
    
    {
      "username": "miguel"
    }

These credentials can now be used to access protected resources:

    $ curl -u miguel:python -i -X GET http://127.0.0.1:5000/api/resource
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 30
    Server: Werkzeug/0.9.4 Python/2.7.3
    Date: Thu, 28 Nov 2013 20:02:25 GMT
    
    {
      "data": "Hello, miguel!"
    }

Using the wrong credentials the request is refused:

    $ curl -u miguel:ruby -i -X GET http://127.0.0.1:5000/api/resource
    HTTP/1.0 401 UNAUTHORIZED
    Content-Type: text/html; charset=utf-8
    Content-Length: 19
    WWW-Authenticate: Basic realm="Authentication Required"
    Server: Werkzeug/0.9.4 Python/2.7.3
    Date: Thu, 28 Nov 2013 20:03:18 GMT
    
    Unauthorized Access

Finally, to avoid sending username and password with every request an authentication token can be requested:

    $ curl -u miguel:python -i -X GET http://127.0.0.1:5000/api/token
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 139
    Server: Werkzeug/0.9.4 Python/2.7.3
    Date: Thu, 28 Nov 2013 20:04:15 GMT
    
    {
      "duration": 600,
      "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc"
    }

And now during the token validity period there is no need to send username and password to authenticate anymore:

    $ curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc:x -i -X GET http://127.0.0.1:5000/api/resource
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 30
    Server: Werkzeug/0.9.4 Python/2.7.3
    Date: Thu, 28 Nov 2013 20:05:08 GMT
    
    {
      "data": "Hello, miguel!"
    }

Once the token expires it cannot be used anymore and the client needs to request a new one. Note that in this last example the password is arbitrarily set to `x`, since the password isn't used for token authentication.

An interesting side effect of this implementation is that it is possible to use an unexpired token as authentication to request a new token that extends the expiration time. This effectively allows the client to change from one token to the next and never need to send username and password after the initial token was obtained.

Change Log
----------

**v0.3** - Return token duration.

**v0.2** - Return a 201 status code and Location header from */api/users* endpoint.

**v0.1** - Initial release.

