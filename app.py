#!/usr/bin/env python
import csv
import archivocsv
from datetime import datetime, date, time, timedelta
import calendar
from flask import Flask, render_template, redirect, url_for, flash, session, send_file
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from forms import LoginForm, ProductoForm, ClienteForm, RegistrarForm, PasswordForm

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

nombre_de_archivo = 'farmacia.csv'
archivocsv.errores(nombre_de_archivo)
registros = archivocsv.listado(nombre_de_archivo)

app.config['SECRET_KEY'] = 'un string que funcione como llave'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

#-----Errores-----#

@app.errorhandler(404)
def no_encontrado(e):
    if 'username' in session:
        return render_template('404.html'), 404
    else:
        flash('Recurso no encontrado')
        return redirect(url_for('ingresar'))

@app.errorhandler(500)
def error_interno(e):
    if 'username' in session:
        return render_template('500.html'), 500
    else:
        flash('Error en el Servidor')
        return redirect(url_for('ingresar'))
#-----Index-----#
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/farmasoft')
def index2():
    if 'username' in session:
        return render_template('index2.html')
    else:
        flash('Para Acceder debe loguearse, ingrese sus credenciales por favor.')
        return redirect(url_for('ingresar'))

#-----Logueo-----#
@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido '+ formulario.usuario.data)
                    session['username'] = formulario.usuario.data
                    return redirect(url_for('ultimas'))
                registro = next(archivo_csv, None)
            else:
                flash('Error de usuario y/o contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)

#-----Registro de usuarios-----#

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', formulario=formulario)

#-----Cambio de contraseña-----#

@app.route('/cambiar_contra', methods=['GET','POST'])
def cambiar_pass():
    if 'username' in session:
        nombre_usuario=session['username']
        formulario = PasswordForm()
        if formulario.validate_on_submit():
            if formulario.password_new.data == formulario.password_check.data:
                datos=[nombre_usuario,formulario.password_new.data]
                with open('usuarios') as archivo:
                    filereader=csv.reader(archivo.readlines())
                with open('usuarios','r+') as archivo:
                    filewriter=csv.writer(archivo)
                    for fila in filereader:
                        if fila[0]==datos[0]:
                            filewriter.writerow(datos)
                        else:
                            filewriter.writerow(fila)
                flash('La contraseña fue cambiada con éxito')
                return redirect(url_for('ingresar'))
            else:
                flash('Las passwords no matchean')
        return render_template('cambiar_contra.html', formulario=formulario)

#-----Deslogueo-----#

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))

##----------------------------------------------Consultas-------------------------------------------------##

#-----Ultimas Ventas Realizadas-----#

@app.route('/ultimas', methods=['GET', 'POST'])
def ultimas():
    if 'username' in session:   
        ultimos = 10
        ul_ventas = []
        ul_ventas = archivocsv.listar_ventas(registros, ultimos)
        return render_template('ultimas.html',ul_ventas=ul_ventas)
    else:
        flash('Para Acceder debe loguearse, ingrese sus credenciales por favor.')
        return redirect(url_for('ingresar'))

#-----Busqueda de productos por cliente-----#

@app.route('/prod_clientes', methods=['GET', 'POST'])
def prod_clientes():
    if 'username' in session:
        formulario = ClienteForm()
        if formulario.validate_on_submit():
            cliente = formulario.cliente.data.upper()
            if len(cliente) < 3:
                flash('Debe Ingresar por lo menos tres caracteres a buscar')
                return render_template('prod_clientes.html', form = formulario)
            else:
                val = archivocsv.encontrar_clientes(registros,cliente)
                if len(val) == 0:
                    flash('No hemos encontrado resultados para su busqueda')
                elif len(val) == 1:
                    listar = archivocsv.productos_por_cliente(registros=registros,cliente=cliente)
                    return render_template('prod_clientes.html', form = formulario, listar = listar, cliente= formulario.cliente.data.upper())
                else:
                    flash('Hemos encontrado varios clientes. Por favor seleccione el que desee:')
                    return render_template('prod_clientes.html', form = formulario, clientes = val)                    
        return render_template('prod_clientes.html', form = formulario)
    else:
        flash('Para Acceder debe loguearse, ingrese sus credenciales por favor.')
        return redirect(url_for('ingresar'))


#-----Clientes múltiples-----#

@app.route('/prod_clientes/<clientes>', methods=['GET', 'POST'])
def prod_clientes2(clientes):
    if 'username' in session:
        formulario = ClienteForm()
        if formulario.validate_on_submit():
            cliente = formulario.cliente.data.upper()
            if len(cliente) < 3:
                flash('Debe Ingresar por lo menos tres caracteres a buscar')
                return redirect(url_for('prod_clientes'))
            else:
                val = archivocsv.encontrar_clientes(registros,cliente)
                if len(val) == 0:
                    flash('No hemos encontrado resultados para su busqueda')
                    return redirect(url_for('prod_clientes'))                   
                elif len(val) == 1:
                    listar = archivocsv.productos_por_cliente(registros,cliente)
                    return render_template('prod_clientes.html', form = formulario, listar = listar, cliente= formulario.cliente.data.upper())
                else:
                    flash('Hemos encontrado varios clientes. Por favor seleccione el que desee:')
                    return render_template('prod_clientes.html', form = formulario, clientes = val)
        else:
            cliente = clientes
            val = archivocsv.encontrar_clientes(registros,cliente)
            listar = archivocsv.productos_por_cliente(registros,cliente)
            return render_template('prod_clientes.html', form = formulario, listar = listar, cliente=cliente)
    else:
        flash('Para Acceder debe loguearse, ingrese sus credenciales por favor.')
        return redirect(url_for('ingresar'))

#-----Busqueda de clientes por producto-----#

@app.route('/clientes_prod', methods=['GET', 'POST'])
def clientes_prod():
    if 'username' in session:
        formulario = ProductoForm()
        if formulario.validate_on_submit():
            producto = formulario.producto.data.upper()
            if len(producto) < 3:
                flash('Debe Ingresar por lo menos tres caracteres a buscar')
                return render_template('clientes_prod.html', form=formulario)
            else:
                val = archivocsv.encontrar_productos(registros, producto)
                if len(val) == 0:
                    flash('No hemos encontrado resultados para su busqueda')
                elif len(val) == 1:
                    listar = archivocsv.clientes_por_producto(registros,producto)
                    return render_template('clientes_prod.html', form = formulario, listar = listar, producto= formulario.producto.data.upper())
                else:
                    flash('Hemos encontrado varios clientes. Por favor seleccione el que desee:')
                    return render_template('clientes_prod.html', form = formulario, productos = val)
        return render_template('clientes_prod.html', form=formulario)
    else:
        flash('Para Acceder debe loguearse, ingrese sus credenciales por favor.')
        return redirect(url_for('ingresar'))

#-----Productos múltiples-----#

@app.route('/clientes_prod/<productos>', methods=['GET', 'POST'])
def cliente_prod2(productos):
    if 'username' in session:
        formulario = ProductoForm()
        if formulario.validate_on_submit():
            producto = formulario.producto.data.upper()
            if len(producto) < 3:
                flash('Debe Ingresar por lo menos tres caracteres a buscar')
                return redirect(url_for('clientes_prod'))
            else:
                val = archivocsv.encontrar_productos(registros,producto)
                if len(val) == 0:
                    flash('No hemos encontrado resultados para su busqueda')
                    return redirect(url_for('clientes_prod'))                   
                elif len(val) == 1:
                    listar = archivocsv.clientes_por_producto(registros,producto)
                    return render_template('clientes_prod.html', form = formulario, listar = listar, producto= formulario.producto.data.upper())
                else:
                    flash('Hemos encontrado varios clientes. Por favor seleccione el que desee:')
                    return render_template('clientes_prod.html', form = formulario, productos = val)
        else:
            producto = productos
            val = archivocsv.encontrar_productos(registros,producto)
            listar = archivocsv.clientes_por_producto(registros,producto)
            return render_template('clientes_prod.html', form = formulario, listar = listar, producto = producto)
    else:
        flash('Para Acceder debe loguearse, ingrese sus credenciales por favor.')
        return redirect(url_for('ingresar'))

#-----Productos más Vendidos-----#

@app.route('/prod_vendidos', methods=['GET', 'POST'])
def productos_mas_vendidos():
    if 'username' in session:
        produc = []
        cantidad = 5
        produc = archivocsv.productos_mas_vendidos(registros = registros, cantidad=cantidad)
        return render_template('prod_vendidos.html', produc = produc)
    else:
        flash('Para Acceder debe loguearse, ingrese sus credenciales por favor.')
        return redirect(url_for('ingresar'))


#-----Clientes que más dinero gastaron-----#

@app.route('/mej_clientes', methods=['GET', 'POST'])
def mejores_clientes():
    if 'username' in session:
        produc = []
        cantidad = 5
        produc = archivocsv.clientes_mas_gastaron(registros = registros, cantidad=cantidad)
        return render_template('mej_clientes.html', produc = produc)
    else:
        flash('Para Acceder debe loguearse, ingrese sus credenciales por favor.')
        return redirect(url_for('ingresar'))

#-----Descarga de consultas realizadas-----#

@app.route('/descargas/')
def descarga():
    if 'username' in session:
        ahora = datetime.now()
        nombre_descarga = "Resultados_"+str(ahora.year)+str(ahora.month)+str(ahora.day)+"_"+str(ahora.hour)+str(ahora.minute)+str(ahora.second)+".csv"
        return send_file('informe.csv',as_attachment=True,attachment_filename=nombre_descarga, cache_timeout=6)
    else:
        flash('Para Acceder debe loguearse, ingrese sus credenciales por favor.')
        return redirect(url_for('ingresar'))


if __name__ == "__main__":
    app.run(debug=True)
    #-----manager.run()-----#
