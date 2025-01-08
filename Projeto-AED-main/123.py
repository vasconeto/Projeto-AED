import customtkinter as ctk
from tkinter import Listbox, Toplevel, messagebox
import os

# Diretório onde os ficheiros dos utilizadores serão armazenados
USER_FILES_DIR = "user_files"
os.makedirs(USER_FILES_DIR, exist_ok=True)

# Caminho para o ficheiro onde os jogos serão armazenados
GAMES_FILE = "games.txt"

# Variável global para armazenar o utilizador atual
current_user = None

# Funções para manipular ficheiros
def get_user_file():
    """Retorna o caminho do ficheiro do utilizador atual."""
    if current_user:
        return os.path.join(USER_FILES_DIR, f"{current_user}_games.txt")
    return None

def load_games():
    """Carrega os jogos do ficheiro do utilizador atual e do GAMES_FILE."""
    games = []
    user_file = get_user_file()
    if user_file and os.path.exists(user_file):
        with open(user_file, "r") as file:
            for line in file:
                name, info = line.strip().split("|")
                games.append({"name": name, "info": info, "favorite": False})

    try:
        with open(GAMES_FILE, "r") as file:
            for line in file:
                parts = line.strip().split("|")
                name, info = parts[0], parts[1]
                favorite = len(parts) > 2 and parts[2] == "1"  # Marcação de favorito
                games.append({"name": name, "info": info, "favorite": favorite})
    except FileNotFoundError:
        pass
    return games

def save_games(games):
    """Guarda os jogos no ficheiro do utilizador atual e no GAMES_FILE."""
    user_file = get_user_file()
    if user_file:
        with open(user_file, "w") as file:
            for game in games:
                file.write(f"{game['name']}|{game['info']}\n")

    with open(GAMES_FILE, "w") as file:
        for game in games:
            favorite = "1" if game.get("favorite", False) else "0"
            file.write(f"{game['name']}|{game['info']}|{favorite}\n")

# Funções de navegação
def show_main_frame():
    main_frame.tkraise()
    clear_game_info()

def show_add_game_frame():
    add_game_frame.tkraise()

def show_login_frame():
    login_frame.tkraise()

def show_register_frame():
    register_frame.tkraise()

def show_favorites_frame():
    favorites_frame.tkraise()
    listbox_favorites.delete(0, ctk.END)
    for game in games:
        if game.get("favorite", False):
            listbox_favorites.insert(ctk.END, game["name"])

def add_game():
    game_name = entry_game_name.get()
    game_info = entry_game_info.get()
    if game_name and game_info:
        new_game = {"name": game_name, "info": game_info, "favorite": False}
        games.append(new_game)
        listbox_games.insert(ctk.END, game_name)
        save_games(games)
        entry_game_name.delete(0, ctk.END)
        entry_game_info.delete(0, ctk.END)

def show_game_info(event):
    clear_game_info()
    selected_index = listbox_games.curselection()
    if selected_index:
        selected_game = games[selected_index[0]]
        info_label.configure(text=f"Informações do Jogo: {selected_game['info']}")
        btn_edit_game.pack(pady=10)
        btn_remove_game.pack(pady=10)
        star_button.pack(pady=10)
        star_button.configure(text="★" if selected_game.get("favorite", False) else "☆")

def clear_game_info():
    info_label.configure(text="Informações do Jogo: Selecione um jogo para ver os detalhes.")
    btn_edit_game.pack_forget()
    btn_remove_game.pack_forget()
    star_button.pack_forget()

def toggle_favorite_star():
    selected_index = listbox_games.curselection()
    if selected_index:
        game = games[selected_index[0]]
        game["favorite"] = not game.get("favorite", False)  # Alterna o estado de favorito
        save_games(games)
        # Atualiza o ícone da estrela
        star_button.configure(text="★" if game["favorite"] else "☆")
        messagebox.showinfo(
            "Favoritos", 
            f"O jogo '{game['name']}' foi {'adicionado aos' if game['favorite'] else 'removido dos'} favoritos."
        )

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
                games[selected_index[0]] = {"name": new_name, "info": new_info, "favorite": selected_game.get("favorite", False)}
                save_games(games)
                listbox_games.delete(selected_index[0])
                listbox_games.insert(selected_index[0], new_name)
                edit_window.destroy()
        
        save_button = ctk.CTkButton(edit_window, text="Salvar", command=save_edit)
        save_button.pack(pady=20)

def remove_game():
    selected_index = listbox_games.curselection()
    if selected_index:
        games.pop(selected_index[0])
        save_games(games)
        listbox_games.delete(selected_index[0])
        clear_game_info()

def login():
    global current_user, games

    username = entry_login_user.get()
    password = entry_login_pass.get()

    user_file = os.path.join(USER_FILES_DIR, f"{username}_data.txt")

    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            stored_username, stored_password = file.read().strip().split("|")
            if username == stored_username and password == stored_password:
                current_user = username
                games = load_games()
                listbox_games.delete(0, ctk.END)
                for game in games:
                    listbox_games.insert(ctk.END, game["name"])
                show_main_frame()
                return

    messagebox.showerror("Erro de Login", "Nome de usuário ou senha incorretos.")

def register():
    username = entry_register_user.get()
    password = entry_register_pass.get()
    confirm_password = entry_register_confirm.get()

    if password != confirm_password:
        messagebox.showerror("Erro de Registo", "As senhas não coincidem.")
        return

    user_file = os.path.join(USER_FILES_DIR, f"{username}_data.txt")

    if os.path.exists(user_file):
        messagebox.showerror("Erro de Registo", "Usuário já existe.")
        return

    with open(user_file, "w") as file:
        file.write(f"{username}|{password}")

    open(os.path.join(USER_FILES_DIR, f"{username}_games.txt"), "w").close()  # Criar ficheiro de jogos vazio

    messagebox.showinfo("Registo", "Registo concluído com sucesso!")
    show_login_frame()

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
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)

# Lista para armazenar os jogos
games = load_games()

# Barra de menu
menu_bar = ctk.CTkFrame(app, height=50, corner_radius=0)
menu_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

btn_main = ctk.CTkButton(menu_bar, text="Main", width=100, command=show_main_frame)
btn_main.pack(side="left", padx=10, pady=10)

btn_add_game = ctk.CTkButton(menu_bar, text="Add Game", width=100, command=show_add_game_frame)
btn_add_game.pack(side="left", padx=10, pady=10)

btn_favorites = ctk.CTkButton(menu_bar, text="Favoritos", width=100, command=show_favorites_frame)
btn_favorites.pack(side="left", padx=10, pady=10)

btn_logout = ctk.CTkButton(menu_bar, text="Logout", width=100, command=show_login_frame)
btn_logout.pack(side="left", padx=10, pady=10)

# Frame principal (tela de menu)
main_frame = ctk.CTkFrame(app)
main_frame.grid(row=1, column=0, sticky="nsew")
listbox_games = Listbox(main_frame, width=60, height=15)
listbox_games.pack(padx=20, pady=10)
listbox_games.bind("<ButtonRelease-1>", show_game_info)

# Frame de adicionar jogo
add_game_frame = ctk.CTkFrame(app)
add_game_frame.grid(row=1, column=0, sticky="nsew")
entry_game_name = ctk.CTkEntry(add_game_frame, placeholder_text="Nome do Jogo")
entry_game_name.pack(pady=10)
entry_game_info = ctk.CTkEntry(add_game_frame, placeholder_text="Informações do Jogo")
entry_game_info.pack(pady=10)
btn_add_game = ctk.CTkButton(add_game_frame, text="Adicionar Jogo", command=add_game)
btn_add_game.pack(pady=10)

# Frame de login
login_frame = ctk.CTkFrame(app)
login_frame.grid(row=1, column=0, sticky="nsew")
entry_login_user = ctk.CTkEntry(login_frame, placeholder_text="Username")
entry_login_user.pack(pady=10)
entry_login_pass = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*")
entry_login_pass.pack(pady=10)
btn_login = ctk.CTkButton(login_frame, text="Login", command=login)
btn_login.pack(pady=10)
btn_register = ctk.CTkButton(login_frame, text="Registrar", command=show_register_frame)
btn_register.pack(pady=10)

# Frame de registo
register_frame = ctk.CTkFrame(app)
register_frame.grid(row=1, column=0, sticky="nsew")
entry_register_user = ctk.CTkEntry(register_frame, placeholder_text="Username")
entry_register_user.pack(pady=10)
entry_register_pass = ctk.CTkEntry(register_frame, placeholder_text="Password", show="*")
entry_register_pass.pack(pady=10)
entry_register_confirm = ctk.CTkEntry(register_frame, placeholder_text="Confirmar Password", show="*")
entry_register_confirm.pack(pady=10)
btn_register_user = ctk.CTkButton(register_frame, text="Registrar", command=register)
btn_register_user.pack(pady=10)

# Frame de favoritos
favorites_frame = ctk.CTkFrame(app)
favorites_frame.grid(row=1, column=0, sticky="nsew")
listbox_favorites = Listbox(favorites_frame, width=60, height=15)
listbox_favorites.pack(padx=20, pady=10)

# Widgets de detalhes do jogo
info_label = ctk.CTkLabel(main_frame, text="Informações do Jogo: Selecione um jogo para ver os detalhes.")
info_label.pack(pady=20)

btn_edit_game = ctk.CTkButton(main_frame, text="Editar Jogo", command=edit_game)
btn_remove_game = ctk.CTkButton(main_frame, text="Remover Jogo", command=remove_game)
star_button = ctk.CTkButton(main_frame, text="☆", command=toggle_favorite_star)

# Iniciar a aplicação
show_login_frame()
app.mainloop()