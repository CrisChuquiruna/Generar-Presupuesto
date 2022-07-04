
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import *
from tkinter import ttk
from fpdf import FPDF
from datetime import datetime
import webbrowser
import os

absolutepath = os.path.abspath(__file__)

fileDirectory = r"{}".format(os.path.dirname(absolutepath))

raiz=Tk()
raiz.config(bg="#60ABFD")
raiz.title("Presupuesto Bureau")
raiz.geometry("1200x600")

#---------------------------Variables--------------------------------------

#Info de tramites
tramites = {}
listaEntryTramites =[]
listaEntryMontos =[]
listaTramites =[]


#---------------------------Titulo--------------------------------------


def borrarTXT(enlace):
    with open (enlace,'w') as archivo:
        archivo.write("")
def escribirTexto(nombreTramite,monto,enlace):
    with open (enlace,'a') as archivo:
        archivo.write("\n{}\n{}".format(nombreTramite,monto))
        archivo.close()
def almacenarBD():
    with open (fileDirectory + r'\BDTramites.txt') as archivo:
        save = archivo.readlines()        
        for i in range(1,len(save),2):            
            tramites[save[i].strip("\n")]=save[i+1].strip("\n")
   
almacenarBD()

#---------------------------Crear Pdf--------------------------------------
class PDF(FPDF):
    def logo (self, name, x, y, w, h):
        self.image(name, x, y, w, h)

    def texts(self,name):
        with open(name,'rb') as xy:
            txt=xy.read().decode('latin-1')
        self.set_xy(10.0,30.0)
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10,txt)
    
    def titles(self, title):
        self.set_xy(50.50,10.00)
        self.set_font('Arial', '', 12)
        self.set_text_color(0, 0 , 0)
        self.cell(w=210.0, h=40.0, align= 'C', txt=title, border=0)
    
    def subtitle(self,subtitle,first):
        self.set_font('Arial', '', 12)
        self.set_text_color(0, 0 , 0)
        if (first == True):
            self.set_xy(10.0,40.0)
            self.cell(w=50.0, h=40.0, txt=subtitle)
        else:
            self.set_xy(100.0,40.0)
            self.cell(w=100.0, h=40.0, txt=subtitle)
        
        
    
def creadorDePDF(nombre,apellido,tipoDeTramite,tramitesElegidos,textoCom):

    contTotal= 0        
    # Borro el TXT en que uso para crear el pdf 
    urlTXT =fileDirectory + r'\TramitesImprimir.txt'    
    borrarTXT(urlTXT)
    #Escribo El inicio
    now = datetime.now()
    try:
        archivo = open (urlTXT, 'a')
        archivo.write(f"\t\t\t {now.day}/{now.month}/{now.year}".rjust(140))                                                                                                             
        archivo.write("\nTrámite: {}".format(tipoDeTramite))
        archivo.write("\nPresupuesto para: {} {}\n\n".format(nombre, apellido))
    finally:
        archivo.close()
    
    def escribirTex(nombreTramite,monto):
        with open (urlTXT,"a") as archivo:
            archivo.write("{}:        \t${}\n".format(nombreTramite,monto))
    for i in tramitesElegidos:
        escribirTex(i,tramites[i])
        contTotal += int(tramites[i])
    escribirTex("\n\n\nPrecio Total: ",contTotal)
    
    def escribirNotas():
        with open (fileDirectory + r'\TramitesImprimir.txt',"a") as archivo:
            archivo.write("\nNotas:{}".format(textoCom))
    escribirNotas()
    
    # Creo el PDF
    pdf= PDF()
    pdf.add_page()
    pdf.logo(fileDirectory + r'\Bureau Argentina rectangulo.png', 20, 10, 55, 20)
    pdf.texts(fileDirectory + r'\TramitesImprimir.txt')      
    pdf.set_author('Alicia')   
    pdf.output(fileDirectory + r'\PDFs\ {} {}.pdf'.format(nombre,apellido),'F')
    
    # Abro el PDF
    webbrowser.open_new(fileDirectory + r'\PDFs\ {} {}.pdf'.format(nombre,apellido))
    raiz.destroy()

    
#---------------------------Editar Tramites--------------------------------------
frameEdit=Frame(raiz,bg="#60ABFD")       
def editarTramites():    
    frameInicio.pack_forget() 
    # Crear un frame principal (se necesitan dos)
    
    frameEdit.pack(fill=BOTH,expand=True)

    # Crear un Canvas
    mi_canvas = Canvas(frameEdit, bg="#60ABFD")
    mi_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Agregar Scrollbar al Canvas
    mi_scrollbar = ttk.Scrollbar(frameEdit, orient=VERTICAL, command=mi_canvas.yview)
    mi_scrollbar.pack(side=RIGHT, fill=Y)

    # Configurar el Canvas
    mi_canvas.configure(yscrollcommand=mi_scrollbar.set)
    mi_canvas.bind('<Configure>', lambda e: mi_canvas.configure(scrollregion= mi_canvas.bbox("all")))

    # Crear un segundo Frame dentro del Canvas
    segundoFrame = Frame(mi_canvas,bg ="#60ABFD")
    # Agregar una nueva ventana al Canvas
    mi_canvas.create_window((0,0), window=segundoFrame, anchor="nw")
    #Arreglar el buf del ScrollBar
    for i in range(100):
        labelDebug = Label(segundoFrame,bg="#60ABFD")
        labelDebug.grid(column=6,row= i)

    #Entrys
    def generarEntrys(): #Genera los Entrys de los que estan en la lista tramites
        contadorImporante=0
        cont=0
        for i in tramites:
                
            #Agrego Entry con un tramite a la lista
            listaEntryTramites.append(Entry(segundoFrame))
            listaEntryTramites[cont].grid(row=cont+1, column=1, pady= 5, padx= 5 ,ipady = 7 , ipadx = 20 )
            listaEntryTramites[cont].config(justify="center", font=("Roboto Cn",13))
            listaEntryTramites[cont].insert(0,i)
            
            listaEntryMontos.append(Entry(segundoFrame))
            listaEntryMontos[cont].grid(row=cont+1, column=2, pady= 5, padx= 5,ipady = 7 , ipadx = 20)
            listaEntryMontos[cont].config(justify="center", font=("Roboto Cn",13))
            listaEntryMontos[cont].insert(0,tramites[i])
            
            cont += 1
                  
    generarEntrys()
     
    #Botones    
    def guardarValores(): #Guarda los Entrys en el diccionario tramites
        borrarTXT(fileDirectory + r'\BDTramites.txt')        
        listaTramitesABorrar=[]
        for i in tramites:
            if i not in listaEntryTramites:
                listaTramitesABorrar.append(i)
        for i in listaTramitesABorrar:
            tramites.pop(i)
        for i in range(len(listaEntryTramites)):
            
            if listaEntryTramites[i].get() != "":
                tramites[listaEntryTramites[i].get()]=listaEntryMontos[i].get()
                escribirTexto(listaEntryTramites[i].get(),listaEntryMontos[i].get(),fileDirectory + r'\BDTramites.txt')
                           
            else:
              
                listaEntryMontos[i].destroy()
                listaEntryTramites[i].destroy()                     
                  
        
        almacenarBD()
        listaEntryTramites.clear()
        listaEntryMontos.clear()
        frameEdit.pack_forget()    
        mi_canvas.pack_forget()
        mi_scrollbar.pack_forget()             
        interfazPrincipal()
   
    B_Guardar=Button(segundoFrame, text="Guardar", width=20,command=guardarValores, cursor="hand2")
    B_Guardar.grid(row=len(listaEntryTramites)+2,column=2,pady=5, padx=5)
    B_Guardar.configure(font=("Roboto Cn",13))
    
    def nuevoTramite():
        listaEntryTramites.append(Entry(segundoFrame))
        listaEntryTramites[len(listaEntryTramites)-1].grid(row=len(listaEntryTramites), column=1, pady= 5, padx= 5,ipady = 7 , ipadx = 20)
        listaEntryTramites[len(listaEntryTramites)-1].config(justify="center", font=("Roboto Cn",13))

        listaEntryMontos.append(Entry(segundoFrame))
        listaEntryMontos[len(listaEntryMontos)-1].grid(row=len(listaEntryMontos), column=2, pady= 5, padx= 5,ipady = 7 , ipadx = 20)
        listaEntryMontos[len(listaEntryMontos)-1].config(justify="center", font=("Roboto Cn",13))
        B_NuevoTramite.grid(row=len(listaEntryTramites)+1,column=0,pady=5, padx=5)
        B_Guardar.grid(row=len(listaEntryTramites)+2,column=2,pady=5, padx=5)

    B_NuevoTramite=Button(segundoFrame, text="+", width=4,command=nuevoTramite, cursor="hand2")
    B_NuevoTramite.grid(row=len(listaEntryTramites)+1,column=0,pady=5, padx=5)
    B_NuevoTramite.configure(font=("Roboto Cn",13))

    #Labels
    L_tramites=Label(segundoFrame,text="Tramites ",font=("Verdana",20),bg="#60ABFD" )
    L_tramites.grid(row=0, column=1, pady= 5, padx= 5)

    L_monto=Label(segundoFrame,text="Monto ",font=("Verdana",20),bg="#60ABFD")
    L_monto.grid(row=0,column=2, pady= 5, padx= 5)

 
#---------------------------Tramites eleccion--------------------------------------
listaMenus = []
def tramitesSeleccion(nombre,apellido,tipoDeTramite):
    miFrame.pack_forget()
    #Creo el Frame
    main_Frame2= Frame(raiz,bg="#60ABFD")
    main_Frame2.pack(side=BOTTOM,fill=BOTH, expand=1)

    # Crear un Canvas
    mi_canvas = Canvas(main_Frame2,bg="#60ABFD")
    mi_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    # Agregar Scrollbar al Canvas
    mi_scrollbar = ttk.Scrollbar(main_Frame2, orient=VERTICAL, command=mi_canvas.yview)
    mi_scrollbar.pack(side=RIGHT, fill=Y)
    # Configurar el Canvas
    mi_canvas.configure(yscrollcommand=mi_scrollbar.set)
    mi_canvas.bind('<Configure>', lambda e: mi_canvas.configure(scrollregion= mi_canvas.bbox("all")))
    #Creo segundo Frame
    frameSeleccion = Frame(mi_canvas,bg="#60ABFD")   

    # Agregar una nueva ventana al Canvas
    mi_canvas.create_window((0,0), window=frameSeleccion, anchor="nw")

    # Para arreglar el bug del scroll
    for i in range(100):
        labelDebug = Label(frameSeleccion,bg="#60ABFD")
        labelDebug.grid(column=6,row= i)

    # Entrys
    def tenerListaConLosNombresDeLosTramites():
        lista =[]
        for i in tramites:
            lista.append(i)
        return lista

    listaDeTramitesParaAutoFill = tenerListaConLosNombresDeLosTramites()    
    listaAutoFillEntrys = []  
    l_monto = []  

    listaAutoFillEntrys.append(AutocompleteCombobox( frameSeleccion,completevalues=listaDeTramitesParaAutoFill))
    listaAutoFillEntrys[0].grid(row=1,column=1,pady=5, padx=5,ipady = 7 , ipadx = 20)
    listaAutoFillEntrys[0].configure( font=("Roboto Cn",13))

    l_monto.append(Label( frameSeleccion,text="{}".format(listaAutoFillEntrys[0].get())))
    print(listaAutoFillEntrys[0].get())
    l_monto[0].grid(row=1,column=2,pady=5, padx=5)
    l_monto[0].configure( font=("Roboto Cn",13),bg="#60ABFD")
    #Crear Boton De Agregar Tramite
 
    def nuevoTramite():        
        listaAutoFillEntrys.append(AutocompleteCombobox(frameSeleccion,completevalues=listaDeTramitesParaAutoFill)) 
        listaAutoFillEntrys[len(listaAutoFillEntrys)-1].grid(row=len(listaAutoFillEntrys),column=1,pady=5, padx=5,ipady = 7 , ipadx = 20)        
        listaAutoFillEntrys[len(listaAutoFillEntrys)-1].configure(font=("Roboto Cn",13))

        l_monto.append(Label( frameSeleccion))
        l_monto[len(listaAutoFillEntrys)-1].grid(row=len(listaAutoFillEntrys),column=2,pady=5, padx=5)
        l_monto[len(listaAutoFillEntrys)-1].configure(font=("Roboto Cn",13),bg="#60ABFD")

        agregarTramite.grid(row=len(listaAutoFillEntrys)+1,column=2,pady=5, padx=5) 
        B_abrirPDF.grid(row=len(listaAutoFillEntrys)+3,column=1,pady=5, padx=5)  
        b_sacarTramite.grid(row=len(listaAutoFillEntrys)+1,column=3,pady=5, padx=5) 

        textoComentario.grid(row=len(listaAutoFillEntrys)+2, column=1, pady=5, padx=5) 
        scroll.grid(row=len(listaAutoFillEntrys)+2, column=2, sticky= "nsew") 

        for i in range(len(l_monto)-1):
            l_monto[i].configure(text="   ${}".format(tramites[listaAutoFillEntrys[i].get()]))
        

    agregarTramite=Button(frameSeleccion, text="+", width=4,command=lambda: nuevoTramite(), cursor="hand2")
    agregarTramite.grid(row=len(listaAutoFillEntrys)+1,column=2,pady=5, padx=5)
    agregarTramite.configure(font=("Roboto Cn",13))

    # Boton borrar Tramite
    def sacarTramite():        
        listaAutoFillEntrys[len(listaAutoFillEntrys)-1].grid_forget()        
        del listaAutoFillEntrys[len(listaAutoFillEntrys)-1]

        l_monto[len(listaAutoFillEntrys)].grid_forget()
        del l_monto[len(listaAutoFillEntrys)]
        agregarTramite.grid(row=len(listaAutoFillEntrys)+1,column=2,pady=5, padx=5) 
        B_abrirPDF.grid(row=len(listaAutoFillEntrys)+3,column=1,pady=5, padx=5) 
        b_sacarTramite.grid(row=len(listaAutoFillEntrys)+1,column=3,pady=5, padx=5)  

        textoComentario.grid(row=len(listaAutoFillEntrys)+2, column=1, pady=5, padx=5) 
        scroll.grid(row=len(listaAutoFillEntrys)+2, column=2, sticky= "nsew")
        
    #Text
    textoComentario=Text(frameSeleccion, width=30, height=10)
    textoComentario.grid(row=len(listaAutoFillEntrys)+2, column=1, pady=5)
    #Scroll para el Text
    scroll=Scrollbar(frameSeleccion, command=textoComentario.yview)
    scroll.grid(row=len(listaAutoFillEntrys)+2, column=2, sticky= "nsew")
    #Para que el scroll tenga el posicionador funcionando correctamente
    textoComentario.config(yscrollcommand=scroll.set)

    b_sacarTramite=Button(frameSeleccion, text="-", width=4,command=lambda: sacarTramite(), cursor="hand2")
    b_sacarTramite.grid(row=len(listaAutoFillEntrys)+1,column=3,pady=5, padx=5)
    b_sacarTramite.configure(font=("Roboto Cn",13))
    # Boton para crear el pdf
    def guardarEleccion():
        listaDeElegidos= []
        for i in range(len(listaAutoFillEntrys)):
            listaDeElegidos.append(listaAutoFillEntrys[i].get())
    
        creadorDePDF(nombre,apellido,tipoDeTramite,listaDeElegidos,textoComentario.get("1.0", "end-1c"))
    B_abrirPDF=Button(frameSeleccion, text="Abrir PDF", width=10,command=guardarEleccion, cursor="hand2")
    B_abrirPDF.grid(row=len(listaAutoFillEntrys)+3,column=1,pady=5, padx=5)
    B_abrirPDF.configure(font=("Roboto Cn",13))

#---------------------------Ingreso de cliente--------------------------------------
miFrame=Frame(bg="#60ABFD")
def interfazIngresoCliente():
    frameInicio.destroy()
    
    miFrame.pack(side=LEFT,expand=True)
    #Info basica
    nombre=StringVar() 
    apellido=StringVar()
    tipoDeTramite=StringVar()
    #Labels
    L_nombre=Label(miFrame,text="Nombre: ",font=("Verdana",15),bg="#60ABFD")
    L_nombre.grid(row=1, column=0, pady= 5, padx= 5)

    L_apellido=Label(miFrame,text="Apellido: ",font=("Verdana",15),bg="#60ABFD")
    L_apellido.grid(row=2,column=0, pady= 5, padx= 5)

    L_tipoDeTramite=Label(miFrame,text="Trámite: ",font=("Verdana",15),bg="#60ABFD")
    L_tipoDeTramite.grid(row=3,column=0, pady= 5, padx= 5)

    #Entrys
    E_nombre= Entry(miFrame, textvariable=nombre)
    E_nombre.grid(row=1, column=1, pady= 5, padx= 5,ipady = 5 , ipadx = 20)
    E_nombre.config(justify="center", font=("Roboto Cn",13))

    E_apellido= Entry(miFrame, textvariable=apellido)
    E_apellido.grid(row=2, column=1, pady= 5, padx= 5,ipady = 5 , ipadx = 20)
    E_apellido.config(justify="center", font=("Roboto Cn",13))

    E_tipoDeTramite= Entry(miFrame, textvariable=tipoDeTramite)
    E_tipoDeTramite.grid(row=3, column=1, pady= 5, padx= 5,ipady = 5 , ipadx = 20)
    E_tipoDeTramite.config(justify="center", font=("Roboto Cn",13))

    #Boton para guardar
    def guardarUsuario():
        nombre = E_nombre.get()
        apellido = E_apellido.get()
        tipoDeTramite = E_tipoDeTramite.get()
       
        if(nombre=="" or apellido==""):
            errorCamposVacios=Label(miFrame,text="Hay campos vacios ",font=("Verdana",9),bg="#60ABFD",fg="red")
            errorCamposVacios.grid(row=4, column=1)
        else:
            miFrame.destroy()
            tramitesSeleccion(nombre,apellido,tipoDeTramite)
    B_guardarUsuario=Button(miFrame, text="Siguiente", width=15,command=guardarUsuario, cursor="hand2")
    B_guardarUsuario.grid(row=4,column=3,pady=5, padx=5)
    B_guardarUsuario.configure(font=("Roboto Cn",13))

#---------------------------Inicio--------------------------------------
frameInicio=Frame(bg="#60ABFD")

def interfazPrincipal():    
    frameInicio.pack(expand=True)
    L_titulo=Label(frameInicio, text= "Presupuestos Bureau",bg="#60ABFD", fg="black", font=("Verdana",25))
    L_titulo.grid(row=0,column=0,columnspan=4)

    B_CrearPDF=Button(frameInicio, text="CrearPdf", width=15,command=interfazIngresoCliente, cursor="hand2")
    B_CrearPDF.grid(row=1,column=1,pady=5, padx=5)
    B_CrearPDF.configure(font=("Roboto Cn",13))

    B_EditarTramites=Button(frameInicio, text="Editar Tramites", width=15,command=editarTramites, cursor="hand2")
    B_EditarTramites.grid(row=1,column=2,pady=5, padx=5)
    B_EditarTramites.configure(font=("Roboto Cn",13))
interfazPrincipal()


raiz.mainloop()