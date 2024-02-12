#modelo
from tkinter import messagebox
import re
from peewee import *

"""Modelo: componentes que llevan la tarea de hacer funcionar la app (ejemplo “agregar empleados”, “hacer la suma del sueldo”, etc)"""

#Creacion de la db y tabla

database = SqliteDatabase("mybs.db")

class BaseModel(Model):
    class Meta:
        database = database

class Empleados(BaseModel):
    nombre = CharField(unique=True)
    edad = FloatField()
    area = CharField()
    horas_diarias = FloatField()
    pago_por_hora = FloatField()
    dias_trabajados = FloatField()
    sueldo_mensual = CharField()

database.connect()
database.create_tables([Empleados])

#funciones

class OperacionL():
    def limpiar(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados):
        nombre.set("")
        edad.set("")
        area.set("")
        horas_diarias.set("")
        pago_por_hora.set("")
        dias_trabajados.set("")
    
class Operaciones():
    
    def alta(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados, sueldo_men, planilla):
        regx = nombre.get()
        patron = "^[A-Za-záéíóú]*$" 
        if(re.match(patron, regx)):

            EmpleadoExistente = Empleados.select().where(Empleados.nombre == nombre.get()).first()

            if EmpleadoExistente:
                messagebox.showerror("Error", "Ya existe un empleado con ese nombre en la base de datos.")
                return
        
            if horas_diarias.get() and pago_por_hora.get() and dias_trabajados.get():
                sueldo_men = (horas_diarias.get() * pago_por_hora.get()) * (dias_trabajados.get())
                empleado = Empleados()
                empleado.nombre = nombre.get()
                empleado.edad = edad.get()
                empleado.area = area.get()
                empleado.horas_diarias = horas_diarias.get()
                empleado.pago_por_hora = pago_por_hora.get()
                empleado.dias_trabajados = dias_trabajados.get()
                empleado.sueldo_mensual = sueldo_men
                empleado.save()

                ActualizarTreeview(planilla)
                messagebox.showinfo("Exito", "Empleado agregado.")
                OperacionL.limpiar(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados)

            else: 
                messagebox.showerror("Error", "Horas diarias, pago por hora, y dias trabajados deben ser valores enteros.")

    def baja(self, planilla):
        valor = planilla.selection()
        print(valor)
        item = planilla.item(valor)
        print(item)    
        print(item['text'])

        Borrar = Empleados.get(Empleados.id == item["text"])
        Borrar.delete_instance()

        planilla.delete(valor)

        messagebox.showinfo("Éxito", "Empleado dado de baja.")

    def modificar(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados, planilla):
        valor = planilla.selection()
        print(valor)
        item = planilla.item(valor)
        print(item)    
        print(item['text'])    

        horas_diarias_nuevo = horas_diarias.get()
        pago_por_hora_nuevo = pago_por_hora.get()
        dias_trabajados_nuevo = dias_trabajados.get()

        sueldo_men = (horas_diarias_nuevo * pago_por_hora_nuevo) * dias_trabajados_nuevo

        ActualizarDatos = Empleados.update(nombre=nombre.get(), 
                                           edad=edad.get(), area=area.get(), 
                                           horas_diarias=horas_diarias_nuevo, pago_por_hora=pago_por_hora_nuevo, 
                                           dias_trabajados=dias_trabajados_nuevo, sueldo_mensual=sueldo_men).where(Empleados.id == item["text"])
        ActualizarDatos.execute()

        messagebox.showinfo("Éxito", "Empleado actualizado con éxito")
        ActualizarTreeview(planilla)
        OperacionL.limpiar(self, nombre, edad, area, horas_diarias, pago_por_hora, dias_trabajados)

def ActualizarTreeview(mytreeview):
    records = mytreeview.get_children()
    for element in records:
        mytreeview.delete(element)   

    for fila in Empleados.select():
        mytreeview.insert("", 0, text=fila.id, values=(fila.nombre, fila.edad, fila.area, fila.horas_diarias, fila.pago_por_hora, fila.dias_trabajados))