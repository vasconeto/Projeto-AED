import customtkinter as ctk
from tkinter import Listbox, Toplevel, messagebox
import os

# Configurar o tema e a aparência
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

is_admin = False  # Variável global para verificar se o utilizador é administrador

# Diretório onde os ficheiros dos utilizadores serão armazenados
USER_FILES_DIR = "user_files"
os.makedirs(USER_FILES_DIR, exist_ok=True)

# Função para retornar o formato do caminho do SO
def path_format():
    if os.name == "nt":
        return "\\"
    else:
        return "/"

pathFormat = path_format()
new_user_file = f".{pathFormat}user_files{pathFormat}users.txt"
admin_file = f".{pathFormat}user_files{pathFormat}admin_data.txt"

# Variável global para armazenar o utilizador atual
current_user = None

def get_user_file():
    if current_user:
        return os.path.join(USER_FILES_DIR, f"{current_user}_games.txt")
    return None

def load_games():
    games = []
    user_file = get_user_file()
    if user_file and os.path.exists(user_file):
        with open(user_file, "r") as file:
            for line in file:
                name, info, category = line.strip().split("|")
                games.append({"name": name, "info": info, "category": category})
    return games

def save_games(games):
    user_file = get_user_file()
    if user_file:
        with open(user_file, "w") as file:
            for game in games:
                file.write(f"{game['name']}|{game['info']}|{game['category']}\n")

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

# Função para adicionar jogos
def add_game():
    if not is_admin:
        messagebox.showerror("Permissão Negada", "Apenas administradores podem adicionar jogos.")
        return

    game_name = entry_game_name.get()
    game_info = entry_game_info.get()
    game_category = combobox_game_info.get()
    
    if game_name and game_info and game_category:
        new_game = {"name": game_name, "info": game_info, "category": game_category}
        games.append(new_game)
        listbox_games.insert(ctk.END, game_name)
        save_games(games)
        entry_game_name.delete(0, ctk.END)
        entry_game_info.delete(0, ctk.END)
        combobox_game_info.set("")

def show_game_info(event):
    clear_game_info()
    selected_index = listbox_games.curselection()
    if selected_index:
        selected_game = games[selected_index[0]]
        info_label.configure(text=f"Informações do Jogo: {selected_game['info']}")
        btn_edit_game.pack(pady=10)
        btn_remove_game.pack(pady=10)

def clear_game_info():
    info_label.configure(text="Informações do Jogo: Selecione um jogo para ver os detalhes.")
    btn_edit_game.pack_forget()
    btn_remove_game.pack_forget()

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

def search_games():
    query = search_entry.get().lower()
    listbox_games.delete(0, ctk.END)
    for game in games:
        if query in game["name"].lower():
            listbox_games.insert(ctk.END, game["name"])
    if not listbox_games.size():
        listbox_games.insert(ctk.END, "Nenhum jogo encontrado.")

def apply_filters():
    filter_window = Toplevel(app)
    filter_window.title("Filtrar Jogos")
    filter_window.geometry("300x400")

    categories = sorted(set(game["category"] for game in games))
    check_vars = {category: ctk.BooleanVar() for category in categories}

    for category, var in check_vars.items():
        ctk.CTkCheckBox(filter_window, text=category, variable=var).pack(anchor="w", padx=10, pady=5)

    def confirm_filters():
        selected_filters = [cat for cat, var in check_vars.items() if var.get()]
        listbox_games.delete(0, ctk.END)

        for game in games:
            if game["category"] in selected_filters:
                listbox_games.insert(ctk.END, game["name"])

        filter_window.destroy()

    ctk.CTkButton(filter_window, text="Aplicar", command=confirm_filters).pack(pady=10)

def check_user(username):
    with open(new_user_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        if line.split("|")[0] == username:
            return True
    return False

def verify_admin(username):
    with open(admin_file, "r", encoding="utf-8") as file:
        return username in [line.strip() for line in file]

def login():
    global current_user, games, is_admin
    username = entry_login_user.get()
    password = entry_login_pass.get()

    if os.path.exists(new_user_file):
        with open(new_user_file, "r") as file:
            lines = file.readlines()
        for line in lines:
            stored_username, stored_password = line.strip().split("|")
            if username == stored_username and password == stored_password:
                current_user = username
                is_admin = verify_admin(username)
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
    if username == "" or password == "" or confirm_password == "":
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return
    if password != confirm_password:
        messagebox.showerror("Erro de Registo", "As senhas não coincidem.")
        return
    if check_user(username):
        messagebox.showerror("Erro de Registo", "Usuário já existe.")
        return
    with open(new_user_file, "a") as file:
        file.write(f"{username}|{password}\n")
    open(os.path.join(USER_FILES_DIR, f"{username}_games.txt"), "w").close()
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

# Frames e widgets aqui...
# Inicializar o primeiro frame
show_login_frame()

# Iniciar o loop principal
app.mainloop()
