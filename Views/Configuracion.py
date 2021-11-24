from tkinter import *
from decouple import config


class VentanaConfiguracion(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("630x360")
        self.title("Ventana de Configuración")

        icon = PhotoImage(file='Resources/Cristiano.png')
        self.iconphoto(True, icon)
        self.resizable(False, False)

        self.defineInterfaz()

    def defineInterfaz(self):
        #aqui se configura el comando para llamr al asistente
        self.lbltilt = Label(self, text='Cambiar comando para llamar al asistente', font='Arial', )
        self.lbltilt.place(x=130, y=10)
        self.lbmsg = Label(self, text='Comando para llamar bicho')
        self.lbmsg.place(x=15, y=85)
        self.txtmsg = Entry(self, validate='focusin', validatecommand=self.ocultarlb)
        self.txtmsg.place(x=215, y=88)
        self.btnguardar = Button(self, text='Guardar', command=self.guardar, width=10)
        self.btnguardar.place(x=390, y=80)
        self.lbalerta = Label(self, text='Comando guardado', fg='#4EB743')

        #En esta parte se establece como se va a ingresar un nuevo programa para poder abrirlo
        self.lbltilt2 = Label(self, text='Agregar nuevo programa', font='Arial', )
        self.lbltilt2.place(x=200, y=150)
        self.lbprog = Label(self, text='Nombre del programa')
        self.lbprog.place(x=15, y=290)
        self.txtprog = Entry(self, validate='focusin', validatecommand=self.ocultarlbProg)
        self.txtprog.place(x=215, y=290)
        self.btnguardarprog = Button(self, text='Registrar', command=self.guardarProg, width=10)
        self.btnguardarprog.place(x=390, y=285)
        self.lbalertaprog = Label(self, text='Programa guardado', fg='#4EB743')
        self.lbruta = Label(self, text='Ruta')
        self.lbruta.place(x=15, y=225)
        self.txtruta = Entry(self, validate='focusin', validatecommand=self.ocultarlbRuta)
        self.txtruta.place(x=215, y=225)


    def guardar(self):
        if len(self.txtmsg.get().strip) == 0:
            return

        with open('data.txt', 'r') as file:
            filedata = file.read()
            indexcmdact = filedata.index('COMANDO_ACTIVACION')
            indexcmdviejo1 = filedata.index("'", indexcmdact)+1
            indexcmdviejo2 = filedata.index("'", indexcmdviejo1)
            cmdviejo = filedata[indexcmdviejo1:indexcmdviejo2]
        filedata = filedata.replace(cmdviejo, self.txtmsg.get().strip())
        with open('data.txt', 'w') as file:
            file.write(filedata)

        self.txtmsg.delete(0, 'end')
        self.lbalerta.place(x=485, y=80)

    def guardarProg(self):
        nombre = self.txtprog.get()
        ruta = self.txtruta.get()
        with open('data.txt', 'r') as file:
            filedata = file.read()

        with open('data.txt', 'w') as file:
            file.write(f"{filedata}\n{nombre} = '{ruta}'")

        self.txtprog.delete(0, 'end')
        self.txtruta.delete(0, 'end')
        self.lbalertaprog.place(x=485, y=290)



    def ocultarlb(self):
        self.lbalerta.place_forget()

    def ocultarlbProg(self):
        self.lbalertaprog.place_forget()

    def ocultarlbRuta(self):
        self.lbalertaprog.place_forget()

    def mostrarVista(self):
        self.mainloop()
