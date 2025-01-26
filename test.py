import customtkinter as ctk
from tkinter import Listbox, Toplevel, messagebox
import os

# Configurar o tema e a aparência
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

# Variáveis globais
is_admin = False
current_user = None
entry_game_name = None
entry_game_info = None
entry_review = None
entry_rating = None
combobox_game_info = None
btn_save_game = None

# Diretório onde os ficheiros dos utilizadores serão armazenados
USER_FILES_DIR = "user_files"
os.makedirs(USER_FILES_DIR, exist_ok=True)

# Retorna o formato de declarar caminhos, dependendo do Sistema Operativo
def path_format():
    return "\\" if os.name == "nt" else "/"

pathFormat = path_format()

new_user_file = f".{pathFormat}user_files{pathFormat}users.txt"
admin_file = f".{pathFormat}user_files{pathFormat}admin_data.txt"

# Retorna o caminho do ficheiro do utilizador atual
def get_user_file():
    if current_user:
        return os.path.join(USER_FILES_DIR, f"{current_user}_games.txt")
    return None


# Carrega os jogos do utilizador
def load_games():
    games = []
    user_file = get_user_file()
    if user_file and os.path.exists(user_file):
        with open(user_file, "r") as file:
            for line in file:
                name, info, category, review, rating = line.strip().split("|")
                games.append({"name": name, "info": info, "category": category, "review": review, "rating": rating})
    return games

# Guarda os jogos no ficheiro do utilizador atual
def save_games(games):
    user_file = get_user_file()
    if user_file:
        with open(user_file, "w") as file:
            for game in games:
                file.write(f"{game['name']}|{game['info']}|{game['category']}|{game['review']}|{game['rating']}\n")

# 
def show_main_frame():
    main_frame.tkraise()
    clear_game_info()

# Abre a janela de adicionar jogo
def show_add_game_frame():
    global entry_game_info, combobox_game_info, btn_save_game, entry_game_name
    
    # Limpar todos os widgets do entry_frame
    for widget in entry_frame.winfo_children():
        widget.destroy()
    
    # Limpar todos os botões do add_game_frame (exceto o entry_frame)
    for widget in add_game_frame.winfo_children():
        if widget != entry_frame:  # Não remover o entry_frame
            widget.destroy()
    
    # Recriar os widgets básicos
    label_game_name = ctk.CTkLabel(entry_frame, text="Nome do Jogo:")
    label_game_name.grid(row=0, column=0, padx=10, pady=10)
    entry_game_name = ctk.CTkEntry(entry_frame)
    entry_game_name.grid(row=0, column=1, padx=10, pady=10)
    
    if is_admin:
        # Criar widgets de admin
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
    
    add_game_frame.tkraise()

# Abre janela do login
def show_login_frame():
    login_frame.tkraise()

# Abre janela do registo
def show_register_frame():
    register_frame.tkraise()

# Adicionar jogo
def add_game():
    game_name = entry_game_name.get()
    game_info = entry_game_info.get()
    game_category = combobox_game_info.get()
    if game_name and game_info and game_category:
        new_game = {"name": game_name, "info": game_info, "category": game_category, "review": "", "rating": ""}
        games.append(new_game)
        listbox_games.insert(ctk.END, game_name)
        save_games(games)
        entry_game_name.delete(0, ctk.END)
        entry_game_info.delete(0, ctk.END)
        combobox_game_info.set("")  # Limpar a seleção da categoria
        show_main_frame()

def get_favorites_file():
    if current_user:
        return os.path.join(USER_FILES_DIR, f"{current_user}_favorites.txt")
    return None

def load_favorites():
    favorites = []
    favorites_file = get_favorites_file()
    if favorites_file and os.path.exists(favorites_file):
        with open(favorites_file, "r") as file:
            favorites = [line.strip() for line in file]
    return favorites

def save_favorites(favorites):
    favorites_file = get_favorites_file()
    if favorites_file:
        with open(favorites_file, "w") as file:
            for favorite in favorites:
                file.write(f"{favorite}\n")

def add_to_favorites():
    selected_index = listbox_games.curselection()
    if selected_index:
        selected_game_name = games[selected_index[0]]["name"]
        favorites = load_favorites()
        if selected_game_name not in favorites:
            favorites.append(selected_game_name)
            save_favorites(favorites)
            messagebox.showinfo("Sucesso", f"{selected_game_name} foi adicionado aos favoritos!")
        else:
            messagebox.showinfo("Informação", f"{selected_game_name} já está nos favoritos.")
    else:
        messagebox.showerror("Erro", "Selecione um jogo para adicionar aos favoritos.")
        
# Mostra as informações do jogo
def show_game_info(event):
    clear_game_info()
    selected_index = listbox_games.curselection()
    if selected_index:
        selected_game = games[selected_index[0]]
        formatted_info = break_text(selected_game['info'], 7)

        # Create a scrollable frame to act as the box
        scrollable_frame = ctk.CTkScrollableFrame(main_info_frame, width=400, height=200, corner_radius=10)
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Create a label inside the scrollable frame to display the game info
        info_label = ctk.CTkLabel(scrollable_frame, text=f"Informações do Jogo:\n{formatted_info}", anchor="w", justify="left")
        info_label.pack(pady=10, padx=10, fill="both", expand=True)

        # Add review and rating labels
        review_label = ctk.CTkLabel(scrollable_frame, text=f"Review: {selected_game['review']}", anchor="w", justify="left")
        review_label.pack(pady=10, padx=10, fill="both", expand=True)

        rating_label = ctk.CTkLabel(scrollable_frame, text=f"Nota: {selected_game['rating']}", anchor="w", justify="left")
        rating_label.pack(pady=10, padx=10, fill="both", expand=True)

        # Create a frame for the buttons
        button_frame = ctk.CTkFrame(main_info_frame)
        button_frame.pack(pady=10)

        btn_edit_game = ctk.CTkButton(button_frame, text="Editar Jogo", command=edit_game)
        btn_edit_game.grid(row=0, column=0, padx=5)

        btn_review_game = ctk.CTkButton(button_frame, text="Review", command=rate_game)
        btn_review_game.grid(row=0, column=2, padx=5)

        btn_remove_game = ctk.CTkButton(button_frame, text="Remover Jogo", command=remove_game)
        btn_remove_game.grid(row=0, column=4, padx=5)

        btn_add_to_favorites = ctk.CTkButton(button_frame, text="Adicioanr aos Favoritos", command=add_to_favorites)
        btn_add_to_favorites.grid(row=0, column=6, padx=5)

# Apaga as informações do jogo quando é removido
def clear_game_info():
    for widget in main_info_frame.winfo_children():
        widget.destroy()

# Divide a informação em várias linhas
def break_text(text, word_limit):
    words = text.split()
    broken_text = ""
    for i in range(0, len(words), word_limit):
        broken_text += ' '.join(words[i:i + word_limit]) + '\n'
    return broken_text.strip()

# Edita o jogo
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
                games[selected_index[0]]["name"] = new_name
                games[selected_index[0]]["info"] = new_info
                save_games(games)
                listbox_games.delete(selected_index[0])
                listbox_games.insert(selected_index[0], new_name)
                edit_window.destroy()
        
        save_button = ctk.CTkButton(edit_window, text="Salvar", command=save_edit)
        save_button.pack(pady=20)

# Função de avaliar e dar review ao jogo
def rate_game():
    selected_index = listbox_games.curselection()
    if selected_index:
        rate_window = Toplevel(app)
        rate_window.title("Avaliar Jogo")
        rate_window.geometry("400x300")

        selected_game = games[selected_index[0]]

        label_review = ctk.CTkLabel(rate_window, text="Review:")
        label_review.pack(pady=10)
        entry_review = ctk.CTkEntry(rate_window)
        entry_review.insert(0, selected_game["review"])
        entry_review.pack(pady=10)

        label_rating = ctk.CTkLabel(rate_window, text="Nota do Jogo:")
        label_rating.pack(pady=10)
        entry_rating = ctk.CTkEntry(rate_window)
        entry_rating.insert(0, selected_game["rating"])
        entry_rating.pack(pady=10)

        def save_review():
            new_review = entry_review.get()
            new_rating = entry_rating.get()
            if new_review and new_rating:
                games[selected_index[0]]["review"] = new_review
                games[selected_index[0]]["rating"] = new_rating
                save_games(games) 
                rate_window.destroy()
        
        save_button = ctk.CTkButton(rate_window, text="Salvar", command=save_review)
        save_button.pack(pady=20)
    

# Apaga o jogo
def remove_game():
    selected_index = listbox_games.curselection()
    if selected_index:
        games.pop(selected_index[0])
        save_games(games)
        listbox_games.delete(selected_index[0])
        clear_game_info()

# Pesquisa o jogo
def search_games():
    query = search_entry.get().lower()
    listbox_games.delete(0, ctk.END)
    for game in games:
        if query in game["name"].lower():
            listbox_games.insert(ctk.END, game["name"])
    if not listbox_games.size():
        listbox_games.insert(ctk.END, "Nenhum jogo encontrado.")

# Aplcia os filtros de pesquisa
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


def count_users():
    if os.path.exists(new_user_file):
        with open(new_user_file, "r") as file:
            lines = file.readlines()
        return len(lines)
    return 0

def show_admin_dashboard():
    admin_dashboard = ctk.CTkToplevel()
    admin_dashboard.title("Admin Dashboard")
    admin_dashboard.geometry("300x200")

    # Count the number of users
    num_users = count_users()

    # Conta os jogos
    num_games = len(games)


    # Mostra numero de jogos
    label_num_games = ctk.CTkLabel(admin_dashboard, text=f"Número de Jogos: {num_games}")
    label_num_games.pack(pady=10)

    # Display the number of users
    label_num_users = ctk.CTkLabel(admin_dashboard, text=f"Número de Utilizadores: {num_users}")
    label_num_users.pack(pady=10)

# Identifica o utilizador
def check_user(username):
    with open(new_user_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        fields = line.strip().split("|")
        if fields[0] == username:
            return True
        
    return False

# Verifica se é admin
def verify_admin(username):
    with open(admin_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        if line.strip() == username:
            return True
        
    return False

# Função do login
def login():
    global current_user, games, is_admin, btn_admin_dash

    username = entry_login_user.get()
    password = entry_login_pass.get()

    if os.path.exists(new_user_file):
        with open(new_user_file, "r") as file:
            lines = file.readlines()
        
        for line in lines:
            fields = line.strip().split("|")
            stored_username, stored_password = fields[0], fields[1]
            if username == stored_username and password == stored_password:
                current_user = username
                is_admin = verify_admin(username)
                games = load_games()
                listbox_games.delete(0, ctk.END)
                for game in games:
                    listbox_games.insert(ctk.END, game["name"])

                if is_admin:
                    print(is_admin)
                    btn_add_game.pack(side="left", padx=10, pady=10)  # Show "Add Game"
                    btn_admin_dash = ctk.CTkButton(menu_bar, text="Admin Dashboard", command=show_admin_dashboard)
                    btn_admin_dash.pack(side="left", padx=10, pady=10)
                else:
                    print(is_admin)

                show_main_frame()
                return

    messagebox.showerror("Erro de Login", "Nome de Utilizador ou Password incorretos.")

# Função do registo
def register():
    username = entry_register_user.get()
    password = entry_register_pass.get()
    confirm_password = entry_register_confirm.get()

    if username == "" or password == "" or confirm_password == "":
        messagebox.showerror("Erro", "Preencha todos o campos!")
        return

    if password != confirm_password:
        messagebox.showerror("Erro de Registo", "As Passwords não coincidem.")
        return
    
    is_user = check_user(username)

    if is_user:
        messagebox.showerror("Erro de Registo", "Utilizador já existe.")
        return

    with open(new_user_file, "a") as file:
        file.write(f"{username}|{password}\n")

    open(os.path.join(USER_FILES_DIR, f"{username}_games.txt"), "w").close()  # Criar ficheiro de jogos vazio

    messagebox.showinfo("Registo", "Registo concluído com sucesso!")
    show_login_frame()

# Abre a janela do perfil
def open_profile_window():
    if current_user:
        profile_window = ctk.CTkToplevel()
        profile_window.title(f"Perfil do {current_user}")
        profile_window.geometry("300x200")

        # Conta os jogos
        num_games = len(games)

        # Conta os generos
        genre_count = {}
        for game in games:
            genre = game["category"]
            if genre in genre_count:
                genre_count[genre] += 1
            else:
                genre_count[genre] = 1

        # Genero mais usado
        if genre_count:
            most_common_genre = max(genre_count, key=genre_count.get)
            most_common_genre_count = genre_count[most_common_genre]
        else:
            most_common_genre = "N/A"
            most_common_genre_count = 0

        # Mostra numero de jogos
        label_num_games = ctk.CTkLabel(profile_window, text=f"Número de Jogos: {num_games}")
        label_num_games.pack(pady=10)

        # Mostra o genero mais usado
        label_most_common_genre = ctk.CTkLabel(profile_window, text=f"Género Mais Comum: {most_common_genre} ({most_common_genre_count} jogos)")
        label_most_common_genre.pack(pady=10)

    def logout():
        profile_window.destroy()
        show_login_frame()
        btn_admin_dash.destroy()

    logout_button = ctk.CTkButton(profile_window, text="Log Out", command=logout)
    logout_button.pack(pady=10)

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

label_login_user = ctk.CTkLabel(login_frame, text="Nome de Utilizador:")
label_login_user.pack(pady=10)
entry_login_user = ctk.CTkEntry(login_frame)
entry_login_user.pack(pady=10)

label_login_pass = ctk.CTkLabel(login_frame, text="Password:")
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

label_register_user = ctk.CTkLabel(register_frame, text="Nome de Utilizador:")
label_register_user.pack(pady=10)
entry_register_user = ctk.CTkEntry(register_frame)
entry_register_user.pack(pady=10)

label_register_pass = ctk.CTkLabel(register_frame, text="Password:")
label_register_pass.pack(pady=10)
entry_register_pass = ctk.CTkEntry(register_frame, show="*")
entry_register_pass.pack(pady=10)

label_register_confirm = ctk.CTkLabel(register_frame, text="Confirmar Password:")
label_register_confirm.pack(pady=10)
entry_register_confirm = ctk.CTkEntry(register_frame, show="*")
entry_register_confirm.pack(pady=10)

btn_register = ctk.CTkButton(register_frame, text="Registar", command=register)
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

btn_perfil = ctk.CTkButton(menu_bar, text="Perfil", width=100, command=open_profile_window)
btn_perfil.pack(side="right", padx=10, pady=10)

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
main_info_frame.pack(fill="both", expand=True)

info_label = ctk.CTkLabel(main_info_frame, text="Informações do Jogo: Selecione um jogo para ver os detalhes.", font=("Arial", 18))
info_label.pack(pady=10, padx=20)

btn_edit_game = ctk.CTkButton(main_info_frame, text="Editar Jogo", command=edit_game)
btn_remove_game = ctk.CTkButton(main_info_frame, text="Remover Jogo", command=remove_game)
btn_add_to_favorites = ctk.CTkButton(main_info_frame, text="Adicionar aos Favoritos", command=add_to_favorites)

btn_rate_game = ctk.CTkButton(main_info_frame, text="Rate Jogo", command=rate_game)
btn_rate_game.pack(pady=30, padx=20)


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

btn_save_game = ctk.CTkButton(add_game_frame, text="Adicionar Jogo", command=add_game)
btn_save_game.pack(pady=10)

# Create the filter button
btn_filter = ctk.CTkButton(search_frame, text="≡", width=30, command=apply_filters)
btn_filter.pack(side="left", padx=10, pady=10)

# Adjust the filter button position
btn_filter.pack(side="left", padx=5)

# Inicializar o primeiro frame
show_login_frame()

# Iniciar o loop principal
app.mainloop()
