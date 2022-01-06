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
        self.lbltilt = Label(self, text='Cambiar comando para llamar al asistente', font='Arial', )
        self.lbltilt.place(x=130, y=10)
        self.lbmsg = Label(self, text='Comando para llamar bicho')
        self.lbmsg.place(x=15, y=85)
        self.txtmsg = Entry(self, validate='focusin', validatecommand=self.ocultarlb)
        self.txtmsg.place(x=215, y=88)
        self.btnguardar = Button(self, text='Guardar', command=self.guardar, width=10)
        self.btnguardar.place(x=390, y=80)
        self.lbalerta = Label(self, text='Comando guardado', fg='#4EB743')

        self.lbprog = Label(self, text='Nombre del programa')
        self.lbprog.place(x=15, y=225)
        self.txtprog = Entry(self, validate='focusin', validatecommand=self.ocultarlbProg)
        self.txtprog.place(x=215, y=228)
        self.btnguardarprog = Button(self, text='Registrar', command=self.guardarProg, width=10)
        self.btnguardarprog.place(x=390, y=220)
        self.lbalertaprog = Label(self, text='Programa guardado', fg='#4EB743')

    def guardar(self):
        if len(self.txtmsg.get().strip()) == 0:
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
        self.lbalerta.place(x=485, y=15)

    def guardarProg(self):
        self.txtprog.delete(0, 'end')
        self.lbalertaprog.place(x=485, y=65)

    def ocultarlb(self):
        self.lbalerta.place_forget()

    def ocultarlbProg(self):
        self.lbalertaprog.place_forget()

    def mostrarVista(self):
        self.mainloop()
