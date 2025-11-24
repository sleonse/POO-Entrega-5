import os

class Crud:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo


        # Cargar ruta absoluta
        ubicacion = os.getcwd()
        self.ruta_archivo = os.path.join(ubicacion, nombre_archivo)

        if not os.path.exists(self.ruta_archivo):
                    with open(self.ruta_archivo, 'w', encoding='utf-8') as archivo:
                        pass


    # FUncion que crea un nuevo
    def create(self, nombre, numero):

        nueva_linea = f"{nombre}!{numero}\n"
        with open(self.ruta_archivo, 'a', encoding='utf-8') as archivo:
            archivo.write(nueva_linea)
        return True


    # funcion que devuelve el numero
    def read(self, argumento):
        with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if not linea.strip(): continue               
                usuario = linea.strip().split('!')


                if len(usuario) >= 2:                
                    if argumento == usuario[0]:
                        return usuario[1]
        return None
            
    # Funcion que elimina 
    def delete(self, argumento):
        texto_nuevo = []
        with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
            eliminado = False
            for linea in archivo:
                usuario = linea.strip().split('!')
                if usuario[0] == argumento:
                    eliminado = True
                else:
                    texto_nuevo.append(linea)
        with open(self.ruta_archivo, 'w') as archivo:
            archivo.writelines(texto_nuevo)
        if eliminado:
            return True
        else:
            return False


    # Funcion que actualiza el numero
    def update(self, nombre, nuevo_numero):
        texto_actualizado = []
        actualizado = False
        with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                usuario = linea.strip().split('!')
                if usuario[0] == nombre:
                    linea = f'{usuario[0]}!{nuevo_numero}\n'
                    actualizado = True

                texto_actualizado.append(linea)
        with open(self.ruta_archivo, 'w') as archivo:
            archivo.writelines(texto_actualizado)
        
        if actualizado:
            return True
        else:
            return False
    

    # Parte de la interfaz

import tkinter as tk

class Interfaz:

    def __init__(self):
        self.ventana_principal = tk.Tk()
        self.ventana_principal.geometry('420x220')
        self.ventana_principal.resizable(False, False)

        self.frame_entradas = tk.Frame(self.ventana_principal)

        self.label_nombre = tk.Label(self.frame_entradas, text='Nombre', width=10, anchor='w')
        self.label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.entry_nombre = tk.Entry(self.frame_entradas, width=20)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.label_numero = tk.Label(self.frame_entradas, text='Número', width=10, anchor='w')
        self.label_numero.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.entry_numero = tk.Entry(self.frame_entradas, width=20)
        self.entry_numero.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        self.frame_entradas.pack(pady=10, padx=15)

        self.frame_botones = tk.Frame(self.ventana_principal)

        self.boton_crear = tk.Button(self.frame_botones, text='Crear', width=8, command = self.crear)
        self.boton_crear.pack(side=tk.LEFT, padx=5, pady=5)

        self.boton_leer = tk.Button(self.frame_botones, text='Leer', width=8, command = self.leer)
        self.boton_leer.pack(side=tk.LEFT, padx=5, pady=5)

        self.boton_actualizar = tk.Button(self.frame_botones, text='Actualizar', width=8, command = self.actualizar)
        self.boton_actualizar.pack(side=tk.LEFT, padx=5, pady=5)

        self.boton_eliminar = tk.Button(self.frame_botones, text='Eliminar', width=8, command = self.eliminar)
        self.boton_eliminar.pack(side=tk.LEFT, padx=5, pady=5)

        self.boton_limpiar = tk.Button(self.frame_botones, text='Limpiar', width=8, command = self.limpiar)
        self.boton_limpiar.pack(side=tk.LEFT, padx=5, pady=5)

        self.frame_botones.pack(pady=10, padx=15)
        
        self.label_status = tk.Label(self.ventana_principal, text="")
        self.label_status.pack(padx=15 , pady=10, fill=tk.X)

        # Crear objeto crud

        self.Archivo = Crud('friendsContact.txt')

        self.ventana_principal.mainloop()

    # Metodos
    def crear(self):
        if not self.es_numero():
            self.label_status.config(text = 'Formato de numero invalido.')
            return

        nombre = self.entry_nombre.get()
        if '!' in nombre:
            self.label_status.config(text = 'Formato de nombre invalido')
            return
               
        numero = self.entry_numero.get()
        number = self.Archivo.read(nombre)
        if nombre and numero:
            if number is None:
                self.entry_nombre.delete(0, tk.END)
                self.entry_numero.delete(0, tk.END)
                self.Archivo.create(nombre, numero)
                self.label_status.config(text = 'Contacto creado exitosamente.')
            elif number:
                self.label_status.config(text = 'Contacto ya existente.')  
        else:
            self.label_status.config(text = 'Complete todos los campos.')

    def leer(self):
        argumento = self.entry_nombre.get()
        if '!' in argumento:
            self.label_status.config(text = 'Formato de nombre invalido')
            return

        
        number = self.Archivo.read(argumento)
        if number:
            self.entry_numero.delete(0, tk.END)
            self.entry_numero.insert(0, number)
            self.label_status.config(text = 'Contacto leido correctamente.')
        elif number is None:
            self.label_status.config(text = 'Contacto no encontrado.')
    
    def eliminar(self):
        argumento = self.entry_nombre.get()
        if '!' in argumento:
            self.label_status.config(text = 'Formato de nombre invalido')
            return        
        if self.Archivo.read(argumento):
            self.Archivo.delete(argumento)
            self.entry_nombre.delete(0, tk.END)
            self.entry_numero.delete(0, tk.END)
            self.label_status.config(text = 'Contacto eliminado exitosamente.')
        elif self.Archivo.read(argumento) is None:
            self.label_status.config(text = 'Contacto no encontrado.')
    
    def actualizar(self):
        name = self.entry_nombre.get()
        if '!' in name:
            self.label_status.config(text = 'Formato de nombre invalido')
            return

        if not self.es_numero():
            self.label_status.config(text = 'Formato de numero invalido.')
            return

        if self.Archivo.read(name):
            nuevo_numero = self.entry_numero.get()
            self.Archivo.update(name, nuevo_numero)
            self.entry_nombre.delete(0, tk.END)
            self.entry_numero.delete(0, tk.END)
            self.label_status.config(text = 'Contacto actualizado exitosamente.')
        else:
            self.label_status.config(text = 'Contacto no encontrado')

    def limpiar(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_numero.delete(0, tk.END)
        self.label_status.config(text = 'Casillas limpiadas.')

    def es_numero(self):
        if self.entry_numero.get().isdigit():
            return True
        else:
            return False
        

# Ejecucion
Prueba = Interfaz()
