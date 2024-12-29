import customtkinter as ctk
from tkinter import Listbox, Toplevel

# Caminho para o ficheiro onde os jogos serão armazenados
GAMES_FILE = "games.txt"

# Configurar o tema e a aparência
ctk.set_appearance_mode("system")  # Pode ser "light", "dark" ou "system"
ctk.set_default_color_theme("dark-blue")  # Outras opções: "green", "dark-blue"

# Funções para manipular ficheiros
def load_games():
    """Carrega os jogos do ficheiro para a lista."""
    games = []
    try:
        with open(GAMES_FILE, "r") as file:
            for line in file:
                name, info = line.strip().split("|")
                games.append({"name": name, "info": info})
    except FileNotFoundError:
        pass
    return games

def save_games(games):
    """Guarda os jogos no ficheiro."""
    with open(GAMES_FILE, "w") as file:
        for game in games:
            file.write(f"{game['name']}|{game['info']}\n")

# Funções de navegação
def show_main_frame():
    main_frame.tkraise()

def show_add_game_frame():
    add_game_frame.tkraise()

# Função para adicionar um jogo
def add_game():
    game_name = entry_game_name.get()
    game_info = entry_game_info.get()
    if game_name and game_info:
        new_game = {"name": game_name, "info": game_info}
        games.append(new_game)
        listbox_games.insert(ctk.END, game_name)
        listbox_games_add.insert(ctk.END, game_name)
        save_games(games)
        entry_game_name.delete(0, ctk.END)
        entry_game_info.delete(0, ctk.END)

# Função para exibir informações de um jogo selecionado
def show_game_info(event):
    selected_index = listbox_games.curselection()
    if selected_index:
        selected_game = games[selected_index[0]]
        info_label.configure(text=f"Informações do Jogo: {selected_game['info']}")

# Função para editar um jogo
def edit_game():
    selected_index = listbox_games.curselection()
    if selected_index:
        # Criar uma janela para editar o jogo
        edit_window = Toplevel(app)
        edit_window.title("Editar Jogo")
        edit_window.geometry("400x300")

        selected_game = games[selected_index[0]]

        # Campos de entrada para o nome e as informações do jogo
        label_name = ctk.CTkLabel(edit_window, text="Nome do Jogo:")
        label_name.pack(pady=10)
        entry_name = ctk.CTkEntry(edit_window)
        entry_name.insert(0, selected_game["name"])
        entry_name.pack(pady=10)

        label_info = ctk.CTkLabel(edit_window, text="Informações do Jogo:")
        label_info.pack(pady=10)
        entry_info = ctk.CTkEntry(edit_window)
        entry_info.insert(0, selected_game["info"])
        entry_info.pack(pady=10)

        # Função para salvar as alterações
        def save_edit():
            new_name = entry_name.get()
            new_info = entry_info.get()
            if new_name and new_info:
                games[selected_index[0]] = {"name": new_name, "info": new_info}
                save_games(games)
                listbox_games.delete(selected_index[0])
                listbox_games.insert(selected_index[0], new_name)
                listbox_games_add.delete(selected_index[0])
                listbox_games_add.insert(selected_index[0], new_name)
                edit_window.destroy()
        
        # Botão para salvar as alterações
        save_button = ctk.CTkButton(edit_window, text="Salvar", command=save_edit)
        save_button.pack(pady=20)

# Função para remover um jogo
def remove_game():
    selected_index = listbox_games.curselection()
    if selected_index:
        # Remover o jogo da lista e do ficheiro
        games.pop(selected_index[0])
        save_games(games)
        listbox_games.delete(selected_index[0])
        listbox_games_add.delete(selected_index[0])
        info_label.configure(text="Informações do Jogo: Selecione um jogo para ver os detalhes.")

# Inicializar a aplicação
app = ctk.CTk()
app.title("Game Managing App")

# Configurar tamanho e posição da janela
appwidth = 1280
appheight = 720
screenWidth = app.winfo_screenwidth()
screenHeight = app.winfo_screenheight()
x = (screenWidth // 2) - (appwidth // 2)
y = (screenHeight // 2) - (appheight // 2)
app.geometry(f"{appwidth}x{appheight}+{int(x)}+{int(y)}")
app.resizable(True, True)

# Lista para armazenar os jogos
games = load_games()

# Barra de menu
menu_bar = ctk.CTkFrame(app, height=50, corner_radius=0)
menu_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

btn_main = ctk.CTkButton(menu_bar, text="Main", width=100, command=show_main_frame)
btn_main.pack(side="left", padx=10, pady=10)

btn_add_game = ctk.CTkButton(menu_bar, text="Add Game", width=100, command=show_add_game_frame)
btn_add_game.pack(side="left", padx=10, pady=10)

btn_profile = ctk.CTkButton(menu_bar, text="Profile", width=100, command=lambda: print("Profile clicked"))
btn_profile.pack(side="right", padx=10, pady=10)

# Frame principal
main_frame = ctk.CTkFrame(app)
main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

main_list_frame = ctk.CTkFrame(main_frame, width=300)
main_list_frame.pack(side="left", fill="y", padx=10, pady=10)

listbox_games = Listbox(main_list_frame)
listbox_games.pack(fill="both", expand=True)
listbox_games.bind('<<ListboxSelect>>', show_game_info)

main_info_frame = ctk.CTkFrame(main_frame)
main_info_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

info_label = ctk.CTkLabel(main_info_frame, text="Informações do Jogo: Selecione um jogo para ver os detalhes.", font=("Arial", 18))
info_label.pack(pady=10, padx=20)

btn_edit_game = ctk.CTkButton(main_info_frame, text="Editar Jogo", command=edit_game)
btn_edit_game.pack(pady=10)

btn_remove_game = ctk.CTkButton(main_info_frame, text="Remover Jogo", command=remove_game)
btn_remove_game.pack(pady=10)

# Frame para adicionar jogos
add_game_frame = ctk.CTkFrame(app)
add_game_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

entry_frame = ctk.CTkFrame(add_game_frame)
entry_frame.pack(pady=20, padx=20, fill="x")

label_game_name = ctk.CTkLabel(entry_frame, text="Nome do Jogo:")
label_game_name.grid(row=0, column=0, padx=10, pady=10)
entry_game_name = ctk.CTkEntry(entry_frame)
entry_game_name.grid(row=0, column=1, padx=10, pady=10)

label_game_info = ctk.CTkLabel(entry_frame, text="Informações do Jogo:")
label_game_info.grid(row=1, column=0, padx=10, pady=10)
entry_game_info = ctk.CTkEntry(entry_frame)
entry_game_info.grid(row=1, column=1, padx=10, pady=10)

btn_add_game = ctk.CTkButton(entry_frame, text="Adicionar Jogo", command=add_game)
btn_add_game.grid(row=2, column=0, columnspan=2, pady=10)

listbox_frame_add = ctk.CTkFrame(add_game_frame)
listbox_frame_add.pack(fill="both", expand=True, padx=10, pady=10)

listbox_games_add = Listbox(listbox_frame_add)
listbox_games_add.pack(fill="both", expand=True)

# Configuração de layout responsivo
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(1, weight=1)

# Mostrar o frame principal inicialmente
show_main_frame()

# Carregar os jogos na lista
for game in games:
    listbox_games.insert(ctk.END, game["name"])
    listbox_games_add.insert(ctk.END, game["name"])

# Iniciar o loop principal
app.mainloop()
