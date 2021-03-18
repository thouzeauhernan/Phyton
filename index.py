from sqlite3.dbapi2 import Row
from tkinter import ttk
from tkinter import *

import sqlite3


print("hola mundo")

class producto:
    db_nombre = 'baseDatos.db'
    #
    def __init__(self,window):
        self.wind=window
        self.wind.title('nueva aplicacion')
       
        #crear un frame
        frame = LabelFrame(self.wind, text = 'Registrar un nuevo producto')
        frame.grid(row=0,column=0, columnspan=3,pady=20)
        
        #label de entrada
        Label(frame, text = 'nombre:').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        #label de entrada
        Label(frame, text = 'Precio:').grid(row=2, column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        #boton de producto
        ttk.Button(frame, text='Guardar Producto', command = self.add_productos).grid(row=3, columnspan=2, sticky=W + E)

        #mensaje de Salida
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky=W+E)

        #tabla
        self.tree = ttk.Treeview(height=10,columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)
        
        #botones para eliminar y editar
        ttk.Button(text='Eliminar Producto', command = self.eliminar_producto).grid(row=5,column=0, sticky=W + E)
        ttk.Button(text='Editar Producto', command = self.editar_producto).grid(row=5, column=1,  sticky=W + E)

        #traer los datos de la db
        self.get_productos()
    #
    def run_query(self, query, parametros = ()):
        with sqlite3.connect(self.db_nombre) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parametros)
            conn.commit()
        return resultado
    
    def get_productos(self):
        #limpiando la tabla
        record = self.tree.get_children()
        for element in record:
            self.tree.delete(element)
        #consulta de datos
        query = 'SELECT * FROM productos ORDER BY Nombre DESC'
        db_filas = self.run_query(query)
        for row in db_filas:
            
            self.tree.insert('',0,text = row[1], values = row[2])
    #
    def validacion(self):
        return (len(self.name.get()) !=0 and len(self.precio.get()) !=0)
    #
    def add_productos(self):
        if self.validacion():
            query = 'INSERT INTO productos VALUES(NULL, ?, ?)'
            parametros =(self.name.get(),self.precio.get())
            self.run_query(query,parametros)
            self.mensaje['text'] = 'Producto Guardado Correctamente'
            self.name.delete(0,END)
            self.precio.delete(0,END)
        else:
            self.mensaje['text'] = 'El nombre y el Precio son requeridos'
        self.get_productos()
    
    def eliminar_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Seleccione un Producto'
            return
        self.mensaje['text'] = ''
        Nombre = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM productos WHERE Nombre = ?'
        self.run_query(query,(Nombre,))
        self.mensaje['text'] = 'El producto fue eliminado correctamente'
        self.get_productos()

    def editar_registro(self, nuevo_nombre, Nombre, nuevo_precio, Precio_viejo):
        query = 'UPDATE productos set Nombre = ?, Precio = ? WHERE Nombre = ? AND Precio = ?'
        parametros = (nuevo_nombre, nuevo_precio,Nombre,Precio_viejo)
        self.run_query(query,parametros)
        self.ventana_editar.destroy()
        self.mensaje['text'] = 'El producto fue actualizado correctamente'
        self.get_productos()
    
    def editar_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Seleccione un Producto'
            return
        Nombre = self.tree.item(self.tree.selection())['text']
        Precio_viejo = self.tree.item(self.tree.selection())['values'][0]
        self.ventana_editar = Toplevel()
        self.ventana_editar.title = 'Editar Producto'

        #nombre viejo
        Label(self.ventana_editar, text= 'Nombre Actual').grid(row=0,column=1)
        Entry(self.ventana_editar, textvariable = StringVar(self.ventana_editar, value = Nombre), state= 'readonly').grid(row=0,column=2)
        #nombre nuevo
        Label(self.ventana_editar, text= 'Nombre Nuevo').grid(row=1,column=1)
        nuevo_nombre = Entry(self.ventana_editar)
        nuevo_nombre.grid(row=1,column=2)

        #Precio viejo
        Label(self.ventana_editar, text= 'Precio Actual').grid(row=2,column=1)
        Entry(self.ventana_editar, textvariable = StringVar(self.ventana_editar, value = Precio_viejo), state= 'readonly').grid(row=2,column=2)
        #Precio nuevo
        Label(self.ventana_editar, text= 'Precio Nuevo').grid(row=3,column=1)
        nuevo_precio = Entry(self.ventana_editar)
        nuevo_precio.grid(row=3,column=2)
        Button(self.ventana_editar, text = 'Actualizar Datos', command = lambda: self.editar_registro(nuevo_nombre.get(),Nombre,nuevo_precio.get(),Precio_viejo)).grid(row=4,column=2, sticky=W)

    

if __name__=='__main__':
    window = Tk()
    aplicacion = producto(window)
    window.mainloop()