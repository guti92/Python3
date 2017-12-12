#Revision de errores
import csv
def errores(nombre_documento):
    class LongitudRegistroIncorrectaError(Exception):
        pass

    class MiError(Exception):
        pass
    CANTIDAD_CAMPOS = 5
    try:
        with open(nombre_documento, 'r', encoding='latin-1') as mi_archivo:
            archivo_csv=csv.reader(mi_archivo)
            item = 1
            columna = 1
            for linea in archivo_csv:
                if len (linea) != CANTIDAD_CAMPOS:
                    raise LongitudRegistroIncorrectaError()
                else:
                    v=0
                    for v in range(CANTIDAD_CAMPOS):
                        columna = v + 1
                        if linea[v] == '':
                            error= 'El campo {} esta VACÍO en el Registro {}'.format(columna, item)
                            raise MiError(error)
                        else:
                            pass
                        if item == 1:
                            detec_colum = linea[v].strip(' ')
                            detec_colum = detec_colum.upper()
                            if detec_colum == 'PRECIO':
                                colum_precio = v
                            elif detec_colum =='CANTIDAD':
                                colum_cantidad = v
                            else:
                                pass                 
                        else:
                            if v == colum_cantidad:
                                val_columa=int(float(linea[v]))
                            elif v == colum_precio:
                                detec_colum = linea[v].strip(' ')
                                if detec_colum.isdigit() == True:
                                    raise ValueError()
                                else:
                                    f=float(linea[v])                            
                            else:
                                pass
                                       
                item = item + 1
            print('Mediante la siguiente url, puede acceder al sitio web:')                 
    except FileNotFoundError:
        print('No se encuentra el archivo indicado')
    except PermissionError:
        print('No posee permisos sobre el documento')
    except LongitudRegistroIncorrectaError:
        mensaje='La {} no tiene la cantidad de campos correctos'.format(linea)
        print(mensaje)
        with open('Error.log','w') as error_file:
            error_file.write(mensaje)
    except ValueError:
        if v == colum_cantidad:
            print('El Registro {} tiene un Valor Incorrecto en el campo "CANTIDAD", recuerde que debe contener un valor entero'.format(registro))
        else:
            print('El Registro {} tiene un Valor Incorrecto en el campo "PRECIO"'.format(item, v))

#Funciones de consultas al archivo csv
def listado(nombre_documento):
    class Registro:
        def __init__ (self, cliente, codigo, producto, cantidad, precio):
            self.cliente = cliente
            self.codigo = codigo
            self.producto = producto
            self.cantidad = cantidad
            self.precio = precio
        def __str__ (self):
            return '{}, {}, {}, {}, {}'.format(self.cliente, self.codigo, self.producto, self.cantidad, self.precio)
        def __repr__ (self):
            return '{}, {}, {}, {}, {}'.format(self.cliente, self.codigo, self.producto, self.cantidad, self.precio)
        def __gt__ (self, otro):
            return self.cantidad > otro.cantidad
        def compra (self):
            return self.cantidad * self.precio

    col_cliente = 0
    col_codigo = 0
    col_producto = 0
    col_cantidad = 0
    col_precio = 0
    col_detec_campo = 0
    registros = []

    with open(nombre_documento, 'r', encoding = 'latin-1') as mi_archivo:
        archivo_csv = csv.reader(mi_archivo)
        x = 0
        for linea in archivo_csv:
            if x == 0:
                y = 0
                for y in range(5):
                    detec_campo = linea[y].strip(' ')
                    detec_campo = detec_campo.upper()
                    if detec_campo == 'CLIENTE':
                        col_cliente = y
                    elif detec_campo == 'CODIGO':
                        col_codigo = y
                    elif detec_campo == 'PRODUCTO':
                        col_producto = y
                    elif detec_campo == 'CANTIDAD':
                        col_cantidad = y
                    else:
                        col_precio = y
                    y = y + 1
                x = x + 1
            else:
                registros.append(Registro(cliente = linea[col_cliente].strip(' ').upper(), codigo = linea[col_codigo].strip(' '), producto = linea[col_producto].strip(' ').upper(), cantidad = float(linea[col_cantidad].strip(' ')), precio = float(linea[col_precio].strip(' '))))
    return (registros)

#--Funcion que provee las ultimas ventas--#
def listar_ventas(registros, ultimos):
    ventas = []
    registros_reverse = registros.reverse()
    while ultimos > len(registros):
        ultimos -= 1
    for x in range(ultimos):
        ventas.append(registros[x])
    return ventas

#--Encuentra a los clientes que coincidan con los caracteres ingresados por el usuario--#

def encontrar_clientes(registros, nombre_cliente):
    cliente = []
    for x in range(len(registros)):
        if nombre_cliente in registros[x].cliente:
            if registros[x].cliente in cliente:
                pass
            else:
                cliente.append(registros[x].cliente)
        else:
            pass
    return cliente

#--Lista de productos que compro determinado cliente--#

def productos_por_cliente(registros, cliente):

    nombre_cliente = cliente.upper()
    productos = []

    for x in range(len(registros)):
        if nombre_cliente in registros[x].cliente:
            productos.append(registros[x])
    return productos

#--Encuentra a los productos que coincidan con los caracteres ingresados por el usuario--#

def encontrar_productos(registros, nombre_producto):
    producto = []
    for x in range(len(registros)):
        if nombre_producto in registros[x].producto:
            if registros[x].producto in producto:
                pass
            else:
                producto.append(registros[x].producto)
        else:
            pass
    return producto

#--Lista de productos que compro determinado cliente--#

def clientes_por_producto(registros, producto):

    nombre_producto = producto.upper()
    cliente = []

    for x in range(len(registros)):
        if nombre_producto in registros[x].producto:
            cliente.append(registros[x])
    return cliente

#--Listado de productos más vendidos--#

def productos_mas_vendidos(registros, cantidad):
    producto = []
    cant_producto = []
    colunna=0

    for x in range(len(registros)):
        if x == 0:
            producto.append(registros[x].producto)
            cant_producto.append([])
            cant_producto[colunna]= [0, registros[x]]
        else:
            if registros[x].producto in producto:
                pass
            else:
                colunna = colunna + 1
                producto.append(registros[x].producto)
                cant_producto.append([])
                cant_producto[colunna]= [0, registros[x]]

    for x in range(len(producto)):
        for y in range(len(registros)):
            if producto[x] in registros[y].producto:
                cant_producto[x][0]= cant_producto[x][0] + registros[y].cantidad
            else:
                pass

    cant_producto.sort(reverse=True)

    while cantidad > len(producto):
        cantidad -= 1
    list_cant = []
    for x in range(cantidad):
        list_cant.append([0]*2)
        list_cant[x][0] = cant_producto[x][0]
        list_cant[x][1] = cant_producto[x][1]
    return list_cant

#--Mejores clientes--#
def clientes_mas_gastaron(registros, cantidad):
    clientes = []
    cant_cliente = []
    colunna=0

    for x in range(len(registros)):
        if x == 0:
            clientes.append(registros[x].cliente)
            cant_cliente.append([])
            cant_cliente[colunna]=[0, registros[x]]
        else:
            if registros[x].cliente in clientes:
                pass
            else:
                clientes.append(registros[x].cliente)
                colunna = colunna + 1
                cant_cliente.append([])
                cant_cliente[colunna]=[0, registros[x]]


    for x in range(len(clientes)):
        for y in range(len(registros)):
            if clientes[x] in registros[y].cliente:
                cant_cliente[x][0]= cant_cliente[x][0] + (registros[y].cantidad * registros[y].precio)
            else:
                pass

    cant_cliente.sort(reverse=True)

    while cantidad > len(clientes):
        cantidad -= 1
    list_cant = []
    for x in range(cantidad):
        list_cant.append([0]*2)
        list_cant[x][0] = cant_cliente[x][0]
        list_cant[x][1] = cant_cliente[x][1]
    return list_cant





