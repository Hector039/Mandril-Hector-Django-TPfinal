# Mi primer proyecto con Django.

Este proyecto está desarrollado hasta el momento, íntegramente con Django y se compone de cinco aplicaciones: users, products, carts, chats y about. El objetivo principal del mismo es el desarrollo de una plataforma de Ecommerce donde los usuarios puedan registrarse, vender y/o comprar sus productos, enviar mensajes privados y demás.


## Detalle del progreso.

En este punto del desarrollo, un usuario puede:
> - Registrarse con su Nombre, Apellido, Email, Edad y Password.
> - Loguearse utilizando su Email y Password.
> - Navegar por los productos pudiendo buscarlos con filtros como el nombre, categoría y precio.
> - Ver el detalle con informacíon de un producto en particular, incluyendo su creador.
> - Agregar y eliminar productos de su carrito de compras y pudiendo ver su detalle.
> - Siendo creador del producto, puede actualizarlo, eliminarlo o actualizar su estatus entre disponible o no disponible.
> - Actualizar sus datos de usuario, tales como su nombre, apellido, email, edad, imagen de perfil o avatar y cambiar su contraseña.
> - Al ingresar al detalle de un producto que no le pertenece, el usuario puede enviar un mensaje privado al creador y establecer un canal de chat con él.
> - Ver y enviar sus mensajes privados en link My Messages de la barra de navegación.
> - Ingresar a la sección About donde verá información del desarrollador del proyecto.

## Funcionamiento.

Estas apps, **users**, **products**, **carts**, **chats** y **about**, con sus respectivos modelos excepto esta última que es una página estática sin más, usan los formularios customizados de Django para interactuar con la base de datos y sus métodos de clase nativos para autenticar usuarios con uso de sesiones por cookies, crear/actualizar productos, etc.
Particularmente para la aplicación **users**, al usar un formulario nativo de de Django, se creó un backend customizado para la necesidad de este proyecto.
Se crearon Constraints en la base de datos para proteger la integridad de la misma, como por ejemplo evitando que un usuario pueda agregar un producto propio a su carrito, o que lo agregue más de una vez, o el checkeo de mayoría de edad en le momento del registro, etc.


## Arquitectura.

Los **templates** se encuentran en el directorio raíz, si es un template base como main.html y en cada aplicación si son específicos de la misma. 
Los archivos estáticos se sirven en la carpeta **static** en la ruta raíz, tales como los scripts de JS, los estilos de CSS y los assets.
Los archivos de avatares subidos por el usuario se guardan con un nombre específico en la carpeta **media**.
En algunas apps como la de usuario por ejemplo, se utilizaron vistas basadas en clases de Django, tanto las genéricas como las nativas para el CRUD de datos y se usaron métodos customizados para ciertos puntos específicos, como enviar datos extra por contexto o una acción extra con información de un formulario.
Se usó el lenguage de plantillas de Django para condicionar ciertos comportamientos en el renderizado, como los colores de productos que no están disponibles, botones para usuarios logueados y contenido dinámico, entre otras funcinoalidades.


## Django Admin.

En la ruta [Admin](http://127.0.0.1:8000/admin), los usuarios **SuperUsuarios** podrán loguearse para administrar las tablas de las 4 aplicaciones, pudiendo así tener control de las altas, bajas y actualización de los estatus, roles, etc

## FrontEnd.

Hasta el momento, se utiliza Bootstrap y un template de estilos de la página [Free Bootstrap themes and templates](https://startbootstrap.com/) para uso demostrativo y testeo de la plataforma, no se pretende que este sea el estilo final de la plataforma.

# Próximos pasos.
Para futuro, y para que la experiencia de un ecommerce sea completa, se deberá desarrollar la pasarela de pagos, en conjunto con el control de stock de los productos, las imágenes de los mismos, un sistema de jeraquías de usuario (user y premium por ejemplo), mecanismos de puntuación y valoración de productos, y otras funcionalidades.

# Instalación para testing.
> - python -m venv .venv
> - . .venv/Scripts/activate
> - pip install -r requirements.txt
> - py manage.py makemigrations
> - py manage.py migrate
> - py manage.py createsuperuser (email, first name, age, password)
> - py manage.py runserver

# Muchas gracias!