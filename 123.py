import customtkinter as ctk
from tkinter import Listbox, Toplevel, messagebox

# Caminho para o ficheiro onde os jogos serão armazenados
GAMES_FILE = "games.txt"

# Configurar o tema e a aparência
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


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
    clear_game_info()

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
    clear_game_info()
    selected_index = listbox_games.curselection()
    if selected_index:
        selected_game = games[selected_index[0]]
        info_label.configure(text=f"Informações do Jogo: {selected_game['info']}")
        btn_edit_game.pack(pady=10)
        btn_remove_game.pack(pady=10)

# Função para limpar informações de jogos
def clear_game_info():
    info_label.configure(text="Informações do Jogo: Selecione um jogo para ver os detalhes.")
    btn_edit_game.pack_forget()
    btn_remove_game.pack_forget()

# Função para editar um jogo
def edit_game():
    selected_index = listbox_games.curselection()
    if selected_index:
        edit_window = Toplevel(app)
        edit_window.title("Editar Jogo")
        edit_window.geometry("400x300")

        selected_game = games[selected_index[0]]

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
        
        save_button = ctk.CTkButton(edit_window, text="Salvar", command=save_edit)
        save_button.pack(pady=20)

# Função para remover um jogo
def remove_game():
    selected_index = listbox_games.curselection()
    if selected_index:
        games.pop(selected_index[0])
        save_games(games)
        listbox_games.delete(selected_index[0])
        listbox_games_add.delete(selected_index[0])
        clear_game_info()

# Função para abrir o popup de pesquisa
def open_search_popup():
    search_window = Toplevel(app)
    search_window.title("Pesquisar Jogos")
    search_window.geometry("400x300")

    search_label = ctk.CTkLabel(search_window, text="Digite o nome do jogo:")
    search_label.pack(pady=10)

    search_entry = ctk.CTkEntry(search_window)
    search_entry.pack(pady=10)

    def search_games():
        search_query = search_entry.get().lower()
        listbox_games.delete(0, ctk.END)  # Limpar a lista principal
        found_games = [game for game in games if search_query in game["name"].lower()]
        
        if found_games:
            for game in found_games:
                listbox_games.insert(ctk.END, game["name"])
        else:
            messagebox.showinfo("Pesquisa", "Nenhum jogo encontrado com esse nome.")
            # Repopular a lista com todos os jogos, caso não haja resultados
            for game in games:
                listbox_games.insert(ctk.END, game["name"])
        
        search_window.destroy()

    search_button = ctk.CTkButton(search_window, text="Pesquisar", command=search_games)
    search_button.pack(pady=10)

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

# Configurar o grid principal para permitir redimensionamento
app.grid_rowconfigure(1, weight=1)  # Linha 1: Frames principais
app.grid_columnconfigure(0, weight=1)  # Coluna 0: Frames principais

# Lista para armazenar os jogos
games = load_games()

# Barra de menu
menu_bar = ctk.CTkFrame(app, height=50, corner_radius=0)
menu_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

btn_main = ctk.CTkButton(menu_bar, text="Main", width=100, command=show_main_frame)
btn_main.pack(side="left", padx=10, pady=10)

btn_add_game = ctk.CTkButton(menu_bar, text="Add Game", width=100, command=show_add_game_frame)
btn_add_game.pack(side="left", padx=10, pady=10)

btn_search_game = ctk.CTkButton(menu_bar, text="Search", width=100, command=open_search_popup)
btn_search_game.pack(side="right", padx=10, pady=10)

# Frame principal
main_frame = ctk.CTkFrame(app)
main_frame.grid(row=1, column=0, sticky="nsew")

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=3)

main_list_frame = ctk.CTkFrame(main_frame, width=300)
main_list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

listbox_games = Listbox(main_list_frame)
listbox_games.pack(fill="both", expand=True)
listbox_games.bind('<<ListboxSelect>>', show_game_info)

main_info_frame = ctk.CTkFrame(main_frame)
main_info_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

info_label = ctk.CTkLabel(main_info_frame, text="Informações do Jogo: Selecione um jogo para ver os detalhes.", font=("Arial", 18))
info_label.pack(pady=10, padx=20)

btn_edit_game = ctk.CTkButton(main_info_frame, text="Editar Jogo", command=edit_game)
btn_remove_game = ctk.CTkButton(main_info_frame, text="Remover Jogo", command=remove_game)

# Frame para adicionar jogos
add_game_frame = ctk.CTkFrame(app)
add_game_frame.grid(row=1, column=0, sticky="nsew")

add_game_frame.grid_rowconfigure(0, weight=1)
add_game_frame.grid_columnconfigure(0, weight=1)

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

# Mostrar o frame principal por padrão
show_main_frame()

# Preencher listboxes com jogos
for game in games:
    listbox_games.insert(ctk.END, game["name"])
    listbox_games_add.insert(ctk.END, game["name"])

app.mainloop()
