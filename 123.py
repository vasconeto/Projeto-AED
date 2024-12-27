import customtkinter as ctk
from tkinter import Listbox
import json

# Caminho para o ficheiro JSON onde os jogos serão armazenados
GAMES_FILE = "games.json"

# Configurar o tema e a aparência
ctk.set_appearance_mode("system")  # Pode ser "light", "dark" ou "system"
ctk.set_default_color_theme("dark-blue")  # Outras opções: "green", "dark-blue"

# Inicializar a aplicação
app = ctk.CTk()
app.title("Game Managing App")

# Configurar o tamanho e a posição da janela
appwidth = 1280
appheight = 720
screenWidth = app.winfo_screenwidth()
screenHeight = app.winfo_screenheight()
x = (screenWidth // 2) - (appwidth // 2)
y = (screenHeight // 2) - (appheight // 2)
app.geometry(f"{appwidth}x{appheight}+{int(x)}+{int(y)}")
app.resizable(True, True)

# Criar uma barra de navegação no topo (simulando um menu)
menu_bar = ctk.CTkFrame(app, height=50, corner_radius=0)
menu_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Função para mostrar o frame principal
def show_main_frame():
    main_frame.tkraise()

# Função para mostrar o frame de adicionar jogos
def show_add_game_frame():
    add_game_frame.tkraise()

# Adicionar botões à barra de menu
btn_main = ctk.CTkButton(menu_bar, text="Main", width=100, command=show_main_frame)
btn_main.pack(side="left", padx=10, pady=10)

btn_add_game = ctk.CTkButton(menu_bar, text="Add Game", width=100, command=show_add_game_frame)
btn_add_game.pack(side="left", padx=10, pady=10)

btn_profile = ctk.CTkButton(menu_bar, text="Profile", width=100, command=lambda: print("Profile clicked"))
btn_profile.pack(side="right", padx=10, pady=10)

# Lista para armazenar os jogos
games = []

# Função para carregar jogos do ficheiro JSON
def load_games():
    global games
    try:
        with open(GAMES_FILE, "r") as file:
            games = json.load(file)
            for game in games:
                listbox_games.insert(ctk.END, game["name"])
                listbox_games_add.insert(ctk.END, game["name"])
    except FileNotFoundError:
        games = []

# Função para salvar jogos no ficheiro JSON
def save_games():
    with open(GAMES_FILE, "w") as file:
        json.dump(games, file)

# Função para adicionar um jogo
def add_game():
    game_name = entry_game_name.get()
    game_info = entry_game_info.get()
    if game_name and game_info:
        new_game = {"name": game_name, "info": game_info}
        games.append(new_game)
        listbox_games.insert(ctk.END, game_name)
        listbox_games_add.insert(ctk.END, game_name)
        save_games()
        entry_game_name.delete(0, ctk.END)
        entry_game_info.delete(0, ctk.END)

# Função para exibir as informações do jogo
def show_game_info(event):
    selected_index = listbox_games.curselection()
    if selected_index:
        selected_game = games[selected_index[0]]
        info_label.configure(text=f"Informações do Jogo: {selected_game['info']}")

# Configuração de frames principais
main_frame = ctk.CTkFrame(app)
main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

add_game_frame = ctk.CTkFrame(app)
add_game_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Conteúdo do frame principal
main_list_frame = ctk.CTkFrame(main_frame, width=300)
main_list_frame.pack(side="left", fill="y", padx=10, pady=10)

listbox_games = Listbox(main_list_frame)
listbox_games.pack(fill="both", expand=True)
listbox_games.bind('<<ListboxSelect>>', show_game_info)

main_info_frame = ctk.CTkFrame(main_frame)
main_info_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

info_label = ctk.CTkLabel(main_info_frame, text="Informações do Jogo: Selecione um jogo para ver os detalhes.", font=("Arial", 18))
info_label.pack(pady=10, padx=20)

# Conteúdo do frame de adicionar jogos
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

# Lista de jogos na aba de adicionar jogos
listbox_frame_add = ctk.CTkFrame(add_game_frame)
listbox_frame_add.pack(fill="both", expand=True, padx=10, pady=10)

listbox_games_add = Listbox(listbox_frame_add)
listbox_games_add.pack(fill="both", expand=True)

# Configuração de layout responsivo
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(1, weight=1)

# Mostrar o frame principal inicialmente
show_main_frame()

# Carregar jogos ao iniciar a aplicação
load_games()

# Iniciar o loop principal da aplicação
app.mainloop()