import customtkinter as ctk
from tkinter import Listbox, Toplevel, messagebox
import os

# Configurar o tema e a aparência
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

# Diretório onde os ficheiros dos utilizadores serão armazenados
USER_FILES_DIR = "user_files"
os.makedirs(USER_FILES_DIR, exist_ok=True)

# Variável global para armazenar o utilizador atual
current_user = None

def get_user_file():
    """Retorna o caminho do ficheiro do utilizador atual."""
    if current_user:
        return os.path.join(USER_FILES_DIR, f"{current_user}_games.txt")
    return None

def load_games():
    """Carrega os jogos do ficheiro do utilizador atual."""
    games = []
    user_file = get_user_file()
    if user_file and os.path.exists(user_file):
        with open(user_file, "r") as file:
            for line in file:
                name, info, category = line.strip().split("|")
                games.append({"name": name, "info": info, "category": category})
    return games

def save_games(games):
    """Guarda os jogos no ficheiro do utilizador atual."""
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

def add_game():
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
        combobox_game_info.set("")  # Limpar a seleção da categoria

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

    # Obter categorias únicas
    categories = sorted(set(game["category"] for game in games))

    # Criar checkboxes dinamicamente
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
app.grid_rowconfigure(1, weight=1)  # Linha 1: Frames principais
app.grid_columnconfigure(0, weight=1)  # Coluna 0: Frames principais

# Lista para armazenar os jogos
games = []

# Frame de Login
login_frame = ctk.CTkFrame(app)
login_frame.grid(row=1, column=0, sticky="nsew")

label_login_user = ctk.CTkLabel(login_frame, text="Nome de Usuário:")
label_login_user.pack(pady=10)
entry_login_user = ctk.CTkEntry(login_frame)
entry_login_user.pack(pady=10)

label_login_pass = ctk.CTkLabel(login_frame, text="Senha:")
label_login_pass.pack(pady=10)
entry_login_pass = ctk.CTkEntry(login_frame, show="*")
entry_login_pass.pack(pady=10)

btn_login = ctk.CTkButton(login_frame, text="Login", command=login)
btn_login.pack(pady=10)

btn_to_register = ctk.CTkButton(login_frame, text="Register", command=show_register_frame)
btn_to_register.pack(pady=10)

# Frame de Registo
register_frame = ctk.CTkFrame(app)
register_frame.grid(row=1, column=0, sticky="nsew")

label_register_user = ctk.CTkLabel(register_frame, text="Nome de Usuário:")
label_register_user.pack(pady=10)
entry_register_user = ctk.CTkEntry(register_frame)
entry_register_user.pack(pady=10)

label_register_pass = ctk.CTkLabel(register_frame, text="Senha:")
label_register_pass.pack(pady=10)
entry_register_pass = ctk.CTkEntry(register_frame, show="*")
entry_register_pass.pack(pady=10)

label_register_confirm = ctk.CTkLabel(register_frame, text="Confirmar Senha:")
label_register_confirm.pack(pady=10)
entry_register_confirm = ctk.CTkEntry(register_frame, show="*")
entry_register_confirm.pack(pady=10)

btn_register = ctk.CTkButton(register_frame, text="Registrar", command=register)
btn_register.pack(pady=10)

btn_to_login = ctk.CTkButton(register_frame, text="Voltar", command=show_login_frame)
btn_to_login.pack(pady=10)

# Frame principal
main_frame = ctk.CTkFrame(app)
main_frame.grid(row=1, column=0, sticky="nsew")

# Barra de menu
menu_bar = ctk.CTkFrame(main_frame, corner_radius=0)
menu_bar.pack(side="top", anchor="nw", fill="x")

btn_main = ctk.CTkButton(menu_bar, text="Main", width=100, command=show_main_frame)
btn_main.pack(side="left", padx=10, pady=10)

btn_add_game = ctk.CTkButton(menu_bar, text="Add Game", width=100, command=show_add_game_frame)
btn_add_game.pack(side="left", padx=10, pady=10)

main_list_frame = ctk.CTkFrame(main_frame, height= 300, width=300)
main_list_frame.pack(side="left", anchor="nw", fill="y", padx=20)

listbox_games = Listbox(main_list_frame)
listbox_games.pack(fill="both", expand=True)
listbox_games.bind('<<ListboxSelect>>', show_game_info)

search_frame = ctk.CTkFrame(main_list_frame)
search_frame.pack(fill="x", pady=5)

search_label = ctk.CTkLabel(search_frame, text="Pesquisar:")
search_label.pack(side="left", padx=5)

search_entry = ctk.CTkEntry(search_frame)
search_entry.pack(side="left", fill="x", expand=True, padx=5)

search_button = ctk.CTkButton(search_frame, text="Procurar", command=search_games)
search_button.pack(side="left", padx=5)

main_info_frame = ctk.CTkFrame(main_frame)
# main_info_frame.grid(column=1, sticky="nsew", padx=10, pady=10)
main_info_frame.pack(fill="both", expand=True)

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

label_game_category = ctk.CTkLabel(entry_frame, text="Categoria do Jogo:")
label_game_category.grid(row=2, column=0, padx=10, pady=10)

# Combobox com categorias de jogos
game_categories = ["Ação", "Aventura", "RPG", "Estratégia", "Simulação",
                    "Desporto", "Puzzle", "Battle Royale", "Indie", "Moba",
                      "Corrida", "Plataforma", "Sandbox", "Survival", "Horror",
                        "FPS", "MMORPG", "Rogue-like", "Metroidvania", "Stealth",
                          "Terror", "Open World"]
combobox_game_info = ctk.CTkComboBox(entry_frame, values=game_categories)
combobox_game_info.grid(row=2, column=1, padx=10, pady=10)

btn_save_game = ctk.CTkButton(add_game_frame, text="Adicionar Jogo", command=add_game)
btn_save_game.pack(pady=10)

btn_back_to_main = ctk.CTkButton(add_game_frame, text="Voltar", command=show_main_frame)
btn_back_to_main.pack(pady=10)

# Create the filter button
btn_filter = ctk.CTkButton(search_frame, text="≡", width=30, command=apply_filters)
btn_filter.pack(side="left", padx=10, pady=10)

# Adjust the filter button position
btn_filter.pack(side="left", padx=5)

# Inicializar o primeiro frame
show_login_frame()

# Iniciar o loop principal
app.mainloop()
