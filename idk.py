# Biblioteca Tkinter: UI
import customtkinter
import CTkMessagebox             # MessageBox
from tkinter import ttk          # Treeview
from tkinter import filedialog   # Filedialog boxes
from PIL import ImageTk, Image    # Imagens .jpg ou .png
import os
from datetime import datetime

# Função para carregar dados no TreeView
def viewTrails():
    # Limpar TreeView
    for item in tree.get_children():
        tree.delete(item)
    
    trails = []

    # Verificar CheckBox e carregar dados dos ficheiros
    if ck1_var.get() == 1:  # Trail Curto selecionado
        if os.path.exists("trails.txt"):
            with open("trails.txt", "r") as file:
                trails.extend(file.readlines())
        else:
            CTkMessagebox.CTkMessagebox(title="Erro", message="O ficheiro trails.txt não foi encontrado.")
    
    if ck2_var.get() == 1:  # Ultra Trail selecionado
        if os.path.exists("ultratrails.txt"):
            with open("ultratrails.txt", "r") as file:
                trails.extend(file.readlines())
        else:
            CTkMessagebox.CTkMessagebox(title="Erro", message="O ficheiro ultratrails.txt não foi encontrado.")

    # Adicionar dados à TreeView
    for trail in trails:
        columns = trail.strip().split(";")
        if len(columns) == len(tree["columns"]):  # Certifique-se de que os dados têm o formato correto
            tree.insert("", "end", values=columns)
        else:
            print(f"Erro ao processar linha: {trail}")  # Para depuração

    # Atualizar número de provas renderizadas
    txtNumProvas.configure(state="normal")
    txtNumProvas.delete(0, "end")
    txtNumProvas.insert(0, len(tree.get_children()))
    txtNumProvas.configure(state="disabled")

# Função para ordenar TreeView em ordem ascendente
def ordAsc():
    rows = [(tree.set(item, "Prova"), item) for item in tree.get_children("")]
    rows.sort()
    for index, (val, item) in enumerate(rows):
        tree.move(item, "", index)

# Função para ordenar TreeView em ordem descendente
def ordDesc():
    rows = [(tree.set(item, "Prova"), item) for item in tree.get_children("")]
    rows.sort(reverse=True)
    for index, (val, item) in enumerate(rows):
        tree.move(item, "", index)

# Função para exibir notificação da prova mais próxima
def notificacoes():
    now = datetime.now()
    closest_date = None
    closest_name = ""

    for item in tree.get_children():
        prova = tree.item(item, "values")
        date_str = prova[1]  # Supondo que a data esteja na segunda coluna
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # Ajustar formato se necessário

        if closest_date is None or (date_obj >= now and date_obj < closest_date):
            closest_date = date_obj
            closest_name = prova[0]

    if closest_date:
        CTkMessagebox.CTkMessagebox(title="Próxima Prova", 
                                    message=f"A próxima prova é '{closest_name}' em {closest_date.strftime('%d-%m-%Y')}.")
    else:
        CTkMessagebox.CTkMessagebox(title="Próxima Prova", message="Não há provas futuras na lista.")

# Função para selecionar imagem
def selecionarImagem():
    file_path = filedialog.askopenfilename(initialdir="Imagens", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
    if file_path:
        img = customtkinter.CTkImage(Image.open(file_path), size=(180, 180))
        btnImagem.configure(image=img)

# GUI Interface Gráfica -----------------------------------------------
def renderWindow(appWidth, appHeight, appTitle):
    """
    Renderiza a window da app, com as dimensões e título dos argumentos
    """
    app.title(appTitle)
    # Obter as dimensões do meu screen (em pixeis)
    screenWidth = app.winfo_screenwidth()
    screenHeight = app.winfo_screenheight()
    # App centrada no screen, em função das suas dimensões
    x = (screenWidth/2) - (appWidth/2)
    y = (screenHeight/2) - (appHeight/2)
    app.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')
    app.resizable(False, False)

# ----- Arranque da aplicação -------------------------------- 
app = customtkinter.CTk()  # Invoca classe Ctk, cria a "main window"
renderWindow(1000, 500, "Trails App")

# 2.1 CheckBox - definir atributos / variáveis para as CheckBox.
ck1_var = customtkinter.IntVar()
ck2_var = customtkinter.IntVar()

ck1 = customtkinter.CTkCheckBox(app, text="Trail Curto", variable=ck1_var, onvalue=1, offvalue=0)
ck2 = customtkinter.CTkCheckBox(app, text="Ultra Trail", variable=ck2_var, onvalue=1, offvalue=0)

ck1.place(x=50, y=20)
ck2.place(x=150, y=20)

# 2.2 btnSearch - deve invocar a função viewTrails 
#btnImage1 = customtkinter.CTkImage(Image.open("/pesquisar.png"), size=(35, 35))
btnSearch = customtkinter.CTkButton(app, width=35, height=35, text="", fg_color="transparent",  
                                    command=viewTrails)
btnSearch.place(x=300, y=12)

# 2.3 btnAsc - Deve invocar a função ordAsc
#btnImage2 = customtkinter.CTkImage(Image.open("/asc.png"), size=(35, 35))
btnAsc = customtkinter.CTkButton(app, width=35, height=35 text="kwbkfw", fg_color="transparent",
                                 command=ordAsc)
btnAsc.place(x=400, y=12)

# 2.4 btnDesc - Deve invocar a função ordDesc 
#btnImage3 = customtkinter.CTkImage(Image.open("/desc.png"), size=(35, 35))
btnDesc = customtkinter.CTkButton(app, width=35, height=35, text="", fg_color="transparent", 
                                command=ordDesc)
btnDesc.place(x=500, y=12)

# 2.5 btnNotificações - Deve invocar a função notificacoes
#btnImage4 = customtkinter.CTkImage(Image.open("/notificacao.png"), size=(40, 40))
btnNotificacoes = customtkinter.CTkButton(app, width=48, height=48, text="", fg_color="transparent", 
                                command=notificacoes)
btnNotificacoes.place(x=600, y=12)

# Tree onde são renderizados os trails e/ou UltraTrails
lblCircuitos = customtkinter.CTkLabel(app, text="Os meus circuitos", font=("Helvetica", 14), text_color="red")
lblCircuitos.place(x=200, y=50)
tree = ttk.Treeview(app, columns=("Prova", "Data", "Local", "Km"), show="headings", height=12, selectmode="browse")
tree.column("Prova", width=220, anchor="w")
tree.column("Data", width=100, anchor="c")
tree.column("Local", width=200, anchor="c")
tree.column("Km", width=120, anchor="c")
tree.heading("Prova", text="Prova")
tree.heading("Data", text="Data")
tree.heading("Local", text="Local")
tree.heading("Km", text="Km")
tree.place(x=20, y=100)

# 2.6 Nº de provas renderizadas na TREE deve aparecer nesta Entry
lblNumProvas = customtkinter.CTkLabel(app, text="Nº de provas", font=("Helvetica", 13))
lblNumProvas.place(x=50, y=320)
txtNumProvas = customtkinter.CTkEntry(app, width=50, state="disabled")
txtNumProvas.place(x=150, y=320)

# 2.7 btnSelecionarImg - Invoca função selecionarImagem
btnSelecionarImg = customtkinter.CTkButton(app, width=45, height=45, text="Selecionar Imagem", fg_color="black", 
                                           text_color="cyan", command=selecionarImagem)
btnSelecionarImg.place(x=180, y=430)

#img = customtkinter.CTkImage(Image.open("/img1.png"), size=(180, 180))
btnImagem = customtkinter.CTkButton(app, width=180, height=180, text="", fg_color="transparent")
btnImagem.place(x=330, y=300)

app.mainloop()
