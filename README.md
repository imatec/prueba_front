prueba_front
============

Descripción
-----------

Pequeña aplicación en Flask para demostrar habilidades de desarrollador front

El objetivo es construir una interfaz de usuario consistente en 2 pantallas:

* Login: 
    * Se debe ingresar un rut con guión y dígito verificador (por ej. 6-K). 
    * Si las credenciales son correctas la API devuelve un token y se debe mostrar la pantalla de Tickets.

* Tickets:
    * Utilizando el token se debe poder consultar el listado de tickets o cualquier recurso disponible por la API
    * El nombre de los tickets debe aparecer en el elemento select.
    * Utilizando el elemento checkbox, se debe poder filtrar aquellos tickets que están asignados al usuario de la sesión actual.
    * Al seleccionar una opción se debe mostrar la descripción del ticket en el elemento de texto. 

Pantallas Login y Tickets
-------------------------
![Alt](/wireframes.png "Wireframes")

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
    (venv) > pip install -r requirements.txt
    ```

#### 6. Creación de Base de Datos
Siempre manteniendose dentro de *venv*, para generar una BD SQLite (db.sqlite) para desarrollo, ejecutar:
    ```
    (venv) > python prueba_front.py create_data
    ```

#### 7. Ejecutar la aplicación
Para ejecutar la aplicación web, en localhost y puerto 5000:
    ```
    (venv) > python prueba_front.py runserver --host 127.0.0.1 --port 5000 --debug --reload
    ```
Para detener la aplicación presionar CTRL-C. Para salir del ambiente virtual ejecutar deactivate:
    ```
    (venv) > deactivate
    PS >
    ```

Esta prueba está basada en el ejemplo: https://github.com/miguelgrinberg/REST-auth de Miguel Grinberg publicado bajo licencia MIT
