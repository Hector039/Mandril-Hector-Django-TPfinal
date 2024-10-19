# Mi primer proyecto con Django.

Este proyecto está desarrollado hasta el momento, íntegramente con Django y se compone de tres aplicaciones: users, products y carts. La objetivo principal del mismo es el desarrollo de una plataforma de Ecommerce donde los usuarios puedan registrarse, vender y comprar sus productos entre sí.


## Detalle del progreso.

En este punto del desarrollo, un usuario puede:
> - Registrarse con su Nombre, Apellido, Email, Edad y Password.
> - Loguearse utilizando su Email y Password.
> - Navegar por los productos pudiendo buscarlos con filtros como el nombre, categoría y precio.
> - Ver el detalle con informacíon de un producto en particular, incluyendo su creador.
> - Agregar y eliminar productos de su carrito de compras y pudiendo ver su detalle.
> - Siendo creador del producto, puede actualizar dicho producto, o eliminarlo.

## Funcionamiento.

Estas apps, **users**, **products** y **carts**, con sus respectivos modelos, usan los formularios customizados de Django para interactuar con la base de datos y sus métodos de clase nativos para autenticar usuarios con uso de sesiones por cookies, crear/actualizar productos, etc.
Particularmente para la aplicación **users**, al usar un formulario nativo de de Django, se creó un backend customizado para la necesidad de este proyecto.
Se crearon Constraints en la base de datos para proteger la integridad de la misma, evitando que un usuario no pueda agregar un producto propio a su carrito, o que lo agregue más de una vez, o el checkeo de mayoría de edad en le momento del registro.


## Arquitectura.

Los templates se encuentran en el directorio raíz, si es un template base como main.html y en cada aplicación si son específicos de la misma. 
Los archivos estáticos se sirven en la carpeta static en la ruta raíz, tales como los scripts de JS, los estilos de CSS y los assets. 

## Django Admin.

En la ruta [Admin](http://127.0.0.1:8000/admin), los usuarios **SuperUsuarios** podrán loguearse para administrar las tablas de las 3 aplicaciones, pudiendo así tener control de las altas, bajas y actualización de los estatus, roles, etc

## FrontEnd.

Hasta el momento, se utiliza Bootstrap y un template de estilos de la página [Free Bootstrap themes and templates](https://startbootstrap.com/) para uso demostrativo y testeo de la plataforma, no se pretende que este sea el estilo final de la plataforma.

# Continuará....