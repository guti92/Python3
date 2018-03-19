Parcial - Estructura de Datos y Paradigmas de Programación

• A grandes rasgos, ¿cómo será el flujo del programa? Al loguearse el usuario en la aplicación, tiene la posibilidad de acceder a todo el contenido almacenado en el archivo .csv, al igual que poder cambiar su contraseña. En primera instancia puede visualizar las ultimas ventas realizadas y además hay diferentes secciones para realizar busquedas específicas.
Por otro lado, si el usuario no posee credenciales, tiene la posibilidad de registrase en el sitio web.

• ¿Qué estructura se utilizará para representar la información del archivo? La base de datos de la farmacia esta en un archivo .csv. Se maneja el mismo mediante codigo python y se plasma en la pagina web desde el archivo "app.py", el cual contiene las vinculaciones tanto desde el archivo con dichos codigos, al igual que los templates en html5, los cuales nos dan interfaz grafica para el usuario.

• ¿Cómo se usa el programa? Al acceder al sitio web, debe presionar el boton "Ingresar", situado en la parte superior del sitio. Una vez allì,se solicitará el usuario y contraseña con el fin de validar credenciales y poder acceder al contenido de la documentacion que maneja la farmacia. En el caso de no poseer dichas credenciales, pueden registrarse desde el boton correspondiente, el cual se ubica tambien en la parte superior, junto al de ingreso. Una vez logueados, pueden realizar las siguientes consultas: - Productos por cliente: se selecciona un cliente de la lista y se devuelven todas los productos comprados por el mismo. - Clientes por producto: se selecciona un producto de la lista y se devuelven todas los clientes que compraron dicho producto. - Productos mas vendidos: se muestra una lista con los 5 productos mas vendidos. - Mejores clientes: se muestra una lista con los 5 clientes que mas compraron. Por ultimo, cuando finalizan sus tareas, se recomienda realizar un deslogueo, desde el boton "Salir".

• ¿Qué clases se diseñaron?¿Por qué? Se diseñaron 5 clases de formularios ya que tenian distintos campos y funciones.

    LoginForm --> Utilizada para el logueo del usuario.
    RegistrarForm --> Empleada para el registro de un nuevo usuario.
    ProductoForm --> Destinada para el uso de busqueda por producto.
    ClienteForm --> Destinada para el uso de busqueda por cliente.
    PasswordForm --> Creada para el cambio de contraseña.

