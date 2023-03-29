#Importacion para pruebas

import json
import os


import datetime
from functools import partial


import tkinter as tk
from tkinter import ttk
from tkinter import *
from calendar import monthcalendar

from Funciones.Funciones import Manipulacion 

import tkcalendar


## Mea culpa: Al programa no llegue a terminarlo por no saber organizar mis tiempos con otros compromisos y proyectos.
# Espero poder terminarlo y subirlo a gitHub


class App(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent,padding=10, )
        self.window = parent

        # Atributos de las ventanas
        parent.minsize(width=700, height=600)
        parent.title("Calendario de Eventos")
        parent.fecha_botones = []
        parent.topLevel = None
        parent.header = None

        
        
        
        # Atributos de la clase
        self.año = datetime.date.today().year  #Retorna el año actual <class int>
        self.mes = datetime.date.today().month  ## Retorna el mes actual <class int>
        self.dia = datetime.date.today().day  ## Retorna el dia actual

        
        
        #print(f"Esta es la linea que queres: {self.window.func.mes_int_a_string(3)}")

        # Funciones internas

        self.config_encabezado()
        self.hacer_botones_dias()
        self.dias_config()
        self.botones_cambio_mes()
        



    def config_encabezado(self):
        """
        Creando el header del calendario que contiene el mes, el año y 2 botones para avanzar en estos atributos
        """

        header_texto = f"{Manipulacion.mes_int_a_string(self.mes)} {self.año}"
        self.header = Label(self, text=header_texto, font="Arvo 20", justify=CENTER)
        self.header.grid(row=0, column=1, columnspan=5, sticky=EW, ipady=25)

        lista_dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        for i,j in enumerate(lista_dias):
            Label(self, text=lista_dias[i], bd=1, relief=SOLID).grid(row=1, column=i, sticky=NSEW, ipady=20)

    
    
    def botones_cambio_mes(self):
        btn = Button(self, text=">", command=self.mes_up, height=2, width=7 )
        btn.grid(row=0,column=5)

        btn = Button(self, text="<", command=self.mes_down, height=2, width=7 )
        btn.grid(row=0,column=1)


    def hacer_botones_dias(self):
        """ Crear botones de dias """
        coords = [(i, j) for i in range(2, 8) for j in range(0, 7)]
        for coord in coords:
            btn = Button(
                self,bg="#5d6094",relief=SUNKEN, bd=2, height=4, width=14)
            btn.grid(row=coord[0], column=coord[1], sticky=NSEW)
            self.window.fecha_botones.append(btn)

    
    def dias_config(self):
        self.dates = Manipulacion.fecha_lista(self.año, self.mes)  # cargamos una lista 
          

        for i, j in enumerate(self.dates):  # Configure button text to show dates
            if j == 0:
                self.window.fecha_botones[i].configure(text="", state=DISABLED, bg="#5d6094")
            else:
                
                self.window.fecha_botones[i].configure(text=j, command = partial(self.select_dia,j) ,bg="white", state=NORMAL,)
                
            if j == datetime.date.today().day \
                    and self.mes == datetime.date.today().month \
                    and self.año == datetime.date.today().year:
                self.window.fecha_botones[i].configure(bg="#D9FFE3")
        

    def act_encabezado(self):
        self.header.configure(text=f"{Manipulacion.mes_int_a_string(self.mes)} {self.año}")

    

    ##################################################################################################################

    # Funciones botones

    def mes_up(self):
        "Incrementa el mes y actualiza el encabezado"
        self.mes += 1
        if self.mes == 13:
            self.mes = 1
            self.año += 1
        self.act_encabezado()
        self.dias_config()


    def mes_down(self):
        "Decrementa el mes y actualiza el encabezado"

        self.mes -= 1
        if self.mes ==0:
            self.mes = 12
            self.año -= 1
        self.act_encabezado()
        self.dias_config()

    def select_dia(self,numdia):

        top_level = tk.Toplevel(self.window)

        eventos = Eventos(top_level,numdia,self.mes,self.año).grid()

    
    
   



        



############### CLASE VENTANA DE VISUALIZACION y MANIPULACION DE EVENTOS #############################

class Eventos(ttk.Frame):
    def __init__(self,parent,dia,mes,año):
        super().__init__(parent,padding=(10),)

        # Atributos de la ventana
        
        parent.title("Gestor de eventos")
        #parent.geometry("800x500")
        
        self.grid(row=0,column=3)
        # Atributos de la clase
        self.dia = dia
        self.mes = mes
        self.año = año
        

        
        # HEADER
        header_texto = f"{Manipulacion.mes_int_a_string(self.mes) } {self.dia} {self.año}"
        self.header = Label(self, text=header_texto, font="consolas 28 bold", justify=CENTER)
        self.header.grid(row=0, column=0, columnspan=5, sticky=NSEW)

        #FRAME VISUALIZACION DE EVENTOS
        self.frame = Frame(self,width=400, height=250)
        self.frame.grid()

        self.eventos_registrados =ttk.Treeview(self.frame, columns=(f"#{n}" for n in range(0,5)))
        self.eventos_registrados.heading("#0",text="Titulo")
        self.eventos_registrados.heading("#1", text="Hora")
        self.eventos_registrados.heading("#2",text="Descripcion")
        self.eventos_registrados.heading("#3", text="Hora de aviso")
        self.eventos_registrados.heading("#4", text="Modo de Aviso")
        self.eventos_registrados.heading("#5", text="Duracion")
        self.eventos_registrados.grid()

        self.leer_datos_eventos()

        #FRAME Y BOTONES ABM
        self.frame2 = Frame(self, width=400, height=250)
        self.frame2.grid()

        self.btn_agregar = Button(self.frame2, text="Agregar" ,width=15 , height=5,
                                  command=self.abrir_ventana_datosEventos).grid(row=1,column=1)
        
        self.btn_eliminar = Button(self.frame2, text="Eliminar",
                                   width=15, height=5).grid(row=1,column=2)
        
        self.btn_editar = Button(self.frame2, text= "Modificar",
                                 width=15, height=5).grid(row=1,column=3)
        
        
        
    def abrir_ventana_datosEventos(self):
        top_level2 = tk.Toplevel()
        datos_eventos = Datos(top_level2,self.dia,self.mes,self.año).grid()

    def leer_datos_eventos(self):
            #Falta estudiar y condicionar la lectura de los datos en sus correspondientes dias
            f = open('WriteData.json','r')
            data = json.loads(f.read())

            count = 0

            for record in data[f"{self.dia}"]:
                self.eventos_registrados.insert(parent='', index="end", id=count, text="",
                                                values=(record['Titulo'],record['Descripcion'],record['Hora de Aviso'], record['Duracion de evento'], record['Modo de recordatorio']))
                count += 1
        
    
        
        

        
class Datos(ttk.Frame):
    def __init__(self,parent,dia,mes,año):
        super().__init__(parent,padding=(10),)

        # Atributos de la ventana
        
        parent.title("Datos de evento")
        #parent.geometry("800x500")
        
        self.grid()
        # Atributos de la clase
        self.dia = dia
        self.mes = mes
        self.año = año
        

        
        # HEADER
        header_texto = "Datos"
        self.header = Label(self, text=header_texto, font="consolas 28 bold", justify=CENTER)
        self.header.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        

        #FRAME TITULO Y DESCRIPCION
        self.frame = Frame(self, width=400, height=250)
        self.frame.grid()

        self.labelTitle = Label(self.frame,text="Titulo", font= "consolas 18 bold",padx=20)
        self.labelTitle.grid(row=0,column=1)

        self.titulo = Entry(self.frame,width=40)
        self.titulo.grid(row=1,column=1)

        self.labelDesc = Label(self.frame,text="Descripcion", font= "consolas 18 bold",padx=20)
        self.labelDesc.grid(row=2,column=1)

            #Caja texto descripcion
        self.descripcion = Text(self.frame, width=40, height = 20)
        self.descripcion.grid(row=3,column=1)

        

        #FRAME Horarios
        self.frame2 = Frame(self, width=400, height=250)
        self.frame2.grid(row=1,column=1)
        self.labelTitle2 = Label(self.frame2,text="Hora de aviso ",font= "consolas 18 bold",padx=20)
        self.labelTitle2.grid(row=1,column=1)

            #Selector de hora
        self.tit_hora = Label(self.frame2,text="Seleccione hora",pady=10)
        self.tit_hora.grid(row=2,column=1)

        self.hora = ttk.Combobox(self.frame2,values=[f"{h}" for h in range(0,24)])
        self.hora.grid(row=3,column=1)

            #Selector de minutos
        self.tit_min = Label(self.frame2, text="Seleccione minutos",pady=10)
        self.tit_min.grid(row=4,column=1)

        self.minutos = ttk.Combobox(self.frame2,values=[f"{m}" for m in range(0,61,5) ])
        self.minutos.grid(row=5,column=1)

            #Duracion del evento (Acotado en horas solamente en el dia seleccionado por el momento)
        
        self.tit_dur = Label(self.frame2, text="Duracion del evento en horas",pady=10)
        self.tit_dur.grid(row=6,column=1)

        self.duracion = ttk.Combobox(self.frame2,values=[f"{h}" for h in range(0,24)])
        self.duracion.grid(row=7,column=1)

            #Modo de aviso

        self.mod_aviso = Label(self.frame2, text="Modo de recordatorio",pady=10)
        self.mod_aviso.grid(row=8,column=1)

        self.mod_aviso = ttk.Combobox(self.frame2,values=["Whatsapp","Email"])
        self.mod_aviso.grid(row=9,column=1,pady=10)


        self.guardar = Button(self.frame2,text="Guardar", width=20,height=3, pady=20, command=self.accion_guardar)
        self.guardar.grid(row=10,column=1)



    ## Convendria traer los datos y creacion desde otro archivo o carpeta.
    def accion_guardar(self):


        print(self.titulo.get())
        print(self.hora.get())
        print(self.minutos.get())
        print(self.duracion.get())
        print(self.mod_aviso.get())
        print(self.descripcion.get('1.0',"end"))

        path, _ = os.path.split(os.path.abspath(__file__))


        ## Falta considerar los if de creacion de diccionarios, existencia y agregacion de datos

        data = {}   # Creo un diccionario

        data[f"{self.año}"] = f"{Manipulacion.mes_int_a_string(self.mes) }"
        
        data[f"{self.dia}"] = []

        data[f"{self.dia}"].append({
            'Titulo': self.titulo.get(),
            'Descripcion': f'{self.descripcion.get("1.0","end")}',
            'Hora de Aviso' : self.hora.get(),
            'Minuto de Aviso': self.minutos.get(),
            'Duracion de evento': self.duracion.get(),
            'Modo de recordatorio': self.mod_aviso.get()

        })

        with open(path+'/WriteData.json','w') as file:
            json.dump(data,file,indent=6)

        self.destroy()

        




root = tk.Tk()
App(root).grid()
root.mainloop()
