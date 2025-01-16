# Biblioteca Tkinter: UI
import customtkinter
import CTkMessagebox             # MessageBox
from tkinter import ttk          # treeview
from tkinter import filedialog   # filedialog boxes
from PIL import ImageTk,Image    # Imagens .jpg ou .png

# IDENTIFICAÇÃO DO ESTUDANTE    
# Numero :40240120
# Ñome:Dinis Miranda


# ESCREVER AQUI AS FUNÇÕES SOLICITADAS NO ENUNCIADO
#-----------------------------------------------------












#----------------------------------------------------
# GUI  INTERFACE GRAFICA -----------------------------------------------
#----------------------------------------------------
def renderWindow(appWidth, appHeight, appTitle):
    """
    Renderiza a window da app, com as dimensões e título dos argumentos
    """
    app.title(appTitle)
    # Obter as dimensões do meu screen (em pixeis)
    screenWidth = app.winfo_screenwidth()
    screenHeight = app.winfo_screenheight()
    # App centrada no screen, em função das suas dimensões# encontrar o 
    x = (screenWidth/2) - (appWidth/2)
    y= (screenHeight/2) - (appHeight/2)
    app.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')
    app.resizable(False, False) 


#-----Arranque da aplicação -------------------------------- 
app=customtkinter.CTk()                  # invoca classe Ctk , cria a "main window"
renderWindow(1000, 500, "Trails App")


# 2.1  CheckBox - definir atributos / variáveis para as CheckBox.  A segunda deve estar ativa, por defeito


ck1 = customtkinter.CTkCheckBox(app, text = "Trail Curto")
ck2 = customtkinter.CTkCheckBox(app, text = "Ultra Trail ")
ck1.place(x=50, y=20)
ck2.place(x=150, y=20)


# 2.2 btnSearch - deve invoca a função viewTrails 
btnImage1 = customtkinter.CTkImage(Image.open("/Users/dinismiranda/Downloads/TESTE/imagens/pesquisar.png"), size=(35, 35))
btnSearch = customtkinter.CTkButton(app, width=35, height=35, image = btnImage1, text = "", fg_color="transparent",  
                                    command = "")
btnSearch.place(x=300, y=12)


# 2.3 btnAsc - Deve invocar a função ordAsc
btnImage2 = customtkinter.CTkImage(Image.open("/Users/dinismiranda/Downloads/TESTE/imagens/asc.png"), size=(35, 35))
btnAsc = customtkinter.CTkButton(app, width=35, height=35, image = btnImage2 , text = "", fg_color="transparent",
                                 command = "")
btnAsc.place(x=400, y=12)


# 2.4 btnDesc - Deve invocar a função ordDesc 
btnImage3 = customtkinter.CTkImage(Image.open("/Users/dinismiranda/Downloads/TESTE/imagens/desc.png"), size=(35, 35))
btnDesc = customtkinter.CTkButton(app, width=35, height=35, image = btnImage3,  text = "", fg_color="transparent", 
                                command = "")
btnDesc.place(x=500, y=12)


# 2.5 btnNotificações  - Deve invocar a função notificacoes
btnImage4 = customtkinter.CTkImage(Image.open("/Users/dinismiranda/Downloads/TESTE/imagens/notificacao.png"), size=(40, 40))
btnNotificacoes = customtkinter.CTkButton(app, width=48, height=48, image = btnImage4 , text = "", fg_color="transparent", 
                                command = "")
btnNotificacoes.place(x=600, y=12)



lblCircuitos = customtkinter.CTkLabel(app, text = "Os meus circuitos", font = ("Helvetica", 14), text_color= "red")
lblCircuitos.place(x=200, y=50)
# Tree onde são renderizados os trails e / opu UltraTrails
tree = ttk.Treeview(app, columns = ("Prova", "Data", "Local", "Km"), show = "headings", height = 12, selectmode = "browse")
tree.column("Prova", width = 220, anchor = "w")
tree.column("Data", width = 100, anchor = "c")
tree.column("Local", width = 200, anchor = "c")
tree.column("Km", width = 120, anchor = "c")

tree.heading("Prova", text = "Prova")
tree.heading("Data", text = "Data")
tree.heading("Local", text = "Local")
tree.heading("Km", text = "Km")
tree.place(x=20, y=100)



lblNumProvas = customtkinter.CTkLabel(app, text = "Nº de provas", font = ("Helvetica", 13))
lblNumProvas.place(x=50, y=320)

# 2.6 Nº DE PROVAS renderizadas na TREE deve aparecer nesta Entry

txtNumProvas = customtkinter.CTkEntry(app, width=50)
txtNumProvas.place(x=150, y=320)



# 2.7 btnSelecionarImg - Invoca  função selecionarImagem, que deve permitir ao utilizador selecionar uma imagem da pasta Imagens
#  e configurá-la no btnImagem  

btnSelecionarImg = customtkinter.CTkButton(app, width=45, height = 45, text = "Selecionar Imagem", fg_color="black", text_color="cyan", 
                        command = "")
btnSelecionarImg.place(x=180, y=430)

img = customtkinter.CTkImage(Image.open("/Users/dinismiranda/Downloads/TESTE/imagens/img1.png"), size=(180, 180))
btnImagem = customtkinter.CTkButton(app, width=180, height=180, image = img , text = "", fg_color="transparent", 
                                    command = "")
btnImagem.place(x=330, y=300)


# 2.8 Deve invocar a função addFavoritos
btnAddFav = customtkinter.CTkButton(app, text = "Adicionar >>\n Favoritos", height=45, fg_color="black", text_color="cyan", 
                                command = "")
btnAddFav.place(x=550, y=150)



frame1 = customtkinter.CTkFrame(app, width = 300, height = 500)
frame1.place(x=700, y=1)

lblFav= customtkinter.CTkLabel(frame1, text = "Favoritos", font = ("Helvetica", 14) )
lblFav.place(x=100, y=30)

lboxFav = customtkinter.CTkTextbox(frame1, width=250, height=250, fg_color="gray", text_color="white")
lboxFav.place(x=20, y=60)

# 2.9 Deve invocar a função filefavoritos 
btnGuardarFav = customtkinter.CTkButton(frame1, text = "Guardar Favoritos", height=90, width=250, fg_color="black", text_color="cyan",
                                        command = "")
btnGuardarFav.place(x=20, y=320)





app.mainloop()   # event listening loop by calling the mainloop()