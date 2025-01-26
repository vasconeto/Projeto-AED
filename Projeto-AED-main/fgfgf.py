import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import Listbox, Toplevel, messagebox, filedialog
import os

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")  # Define o modo como escuro
ctk.set_default_color_theme("blue")  # Define o tema em tons azulados

# Variáveis globais
is_admin = False
current_user = None
games = []  # Inicializa a variável games
entry_game_name = None
entry_game_info = None
entry_review = None
entry_rating = None
combobox_game_info = None
btn_save_game = None

# Diretório onde os ficheiros dos utilizadores serão armazenados
USER_FILES_DIR = "user_files"
os.makedirs(USER_FILES_DIR, exist_ok=True)

def path_format():
    """Retorna o formato de declarar caminhos, dependendo do Sistema Operativo"""
    return "\\" if os.name == "nt" else "/"

pathFormat = path_format()

new_user_file = f".{pathFormat}user_files{pathFormat}users.txt"
admin_file = f".{pathFormat}user_files{pathFormat}admin_data.txt"

def get_user_file():
    """Retorna o caminho do ficheiro do utilizador atual."""
    if current_user:
        return os.path.join(USER_FILES_DIR, f"{current_user}_games.txt")
    return None

def load_games():
    """Carrega os jogos do ficheiro do utilizador atual."""
    global games  # Certifique-se de que está usando a variável global
    games = []  # Reinicializa a lista de jogos
    user_file = get_user_file()
    if user_file and os.path.exists(user_file):
        with open(user_file, "r") as file:
            for line in file:
                # Ignora linhas vazias
                if line.strip():
                    parts = line.strip().split("|")
                    # Verifica se a linha contém o número correto de partes
                    if len(parts) == 6:  # Espera 6 partes: name, info, category, review, rating, image_path
                        name, info, category, review, rating, image_path = parts
                        games.append({"name": name, "info": info, "category": category, "review": review, "rating": rating, "image_path": image_path})
                    else:
                        print(f"Formato inválido na linha: {line.strip()}")  # Para depuração

def update_listbox():
    """Atualiza a Listbox com os jogos carregados."""
    listbox_games.delete(0, ctk.END)  # Limpa a Listbox
    for game in games:
        listbox_games.insert(ctk.END, game["name"])  # Adiciona os nomes dos jogos à Listbox

def save_games():
    """Guarda os jogos no ficheiro do utilizador atual."""
    user_file = get_user_file()
    if user_file:
        with open(user_file, "w") as file:
            for game in games:
                file.write(f"{game['name']}|{game['info']}|{game['category']}|{game['review']}|{game['rating']}|{game['image_path']}\n")

def show_main_frame():
    main_frame.tkraise()
    clear_game_info()

def show_add_game_window():
    add_game_window = Toplevel(app)
    add_game_window.title("Adicionar Jogo")
    add_game_window.geometry("1280x720")

    # Carregar a imagem de fundo
    background_image = Image.open("transferir.png")
    background_photo = ctk.CTkImage(background_image, size=(1280, 720))

    # Função para redimensionar o fundo
    def resize_background(event):
        resized_image = background_image.resize((event.width, event.height))
        background_photo_resized = ctk.CTkImage(resized_image, size=(event.width, event.height))
        background_label.configure(image=background_photo_resized)
        background_label.image = background_photo_resized

    background_label = ctk.CTkLabel(add_game_window, image=background_photo)
    background_label.place(relwidth=1, relheight=1)
    add_game_window.bind("<Configure>", resize_background)

    # Frame para os campos de entrada
    add_game_frame = ctk.CTkFrame(add_game_window, corner_radius=10, fg_color=("#003DA5", "#003DA5"), width=500, height=600)
    add_game_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = ctk.CTkLabel(add_game_frame, text="Adicionar Jogo", font=("Arial", 30, "bold"), text_color="#c7d5e0")
    title_label.pack(pady=(20, 20))

    # Campo para o título do jogo
    title_entry = ctk.CTkEntry(add_game_frame, placeholder_text="Título do Jogo", font=("Arial", 16),
                                fg_color="#3c596e", border_color="#66c0f4", text_color="#c7d5e0")
    title_entry.pack(pady=(10, 20), padx=20, fill="x")

    # Combobox para categorias de jogos
    game_categories = ["Ação", "Aventura", "RPG", "Estratégia", "Simulação",
                      "Desporto", "Puzzle", "Battle Royale", "Indie", "Moba",
                      "Corrida", "Plataforma", "Sandbox", "Survival", "Horror",
                      "FPS", "MMORPG", "Rogue-like", "Metroidvania", "Stealth",
                      "Terror", "Open World"]
    category_combobox = ctk.CTkComboBox(add_game_frame, values=game_categories)
    category_combobox.pack(pady=(10, 20), padx=20, fill="x")

    # Campo para resumo do jogo
    summary_entry = ctk.CTkEntry(add_game_frame, placeholder_text="Resumo do Jogo", font=("Arial", 16),
                                  fg_color="#3c596e", border_color="#66c0f4", text_color="#c7d5e0")
    summary_entry.pack(pady=(10, 20), padx=20, fill="x")

    # Variável para armazenar o caminho da imagem
    image_path = ""

    # Função para inserir imagem
    def upload_image():
        nonlocal image_path  # Permite modificar a variável image_path
        file_path = filedialog.askopenfilename(title="Selecionar Imagem", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            image_path = file_path  # Armazena o caminho da imagem
            messagebox.showinfo("Imagem", "Imagem selecionada com sucesso.")

    upload_button = ctk.CTkButton(add_game_frame, text="Inserir Imagem", command=upload_image)
    upload_button.pack(pady=(10, 20), padx=20)

    # Botão para salvar o jogo
    def save_new_game():
        game_name = title_entry.get()
        game_category = category_combobox.get()
        game_summary = summary_entry.get()

        if game_name and game_category and game_summary:
            new_game = {"name": game_name, "info": game_summary, "category": game_category, "review": "", "rating": "", "image_path": image_path}
            games.append(new_game)
            save_games()
            messagebox.showinfo("Sucesso", "Jogo adicionado com sucesso!")
            add_game_window.destroy()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    save_button = ctk.CTkButton(add_game_frame, text="Salvar Jogo", command=save_new_game)
    save_button.pack(pady=(10, 20), padx=20)

    # Botão para fechar a janela
    close_button = ctk.CTkButton(add_game_frame, text="Fechar", command=add_game_window.destroy)
    close_button.pack(pady=(10, 20), padx=20)

def add_game():
    game_name = entry_game_name.get()
    game_info = entry_game_info.get()
    game_category = combobox_game_info.get()
    if game_name and game_info and game_category:
        new_game = {"name": game_name, "info": game_info, "category": game_category, "review": "", "rating": ""}
        games.append(new_game)
        update_listbox()  # Atualiza a Listbox após adicionar um novo jogo
        save_games()
        entry_game_name.delete(0, ctk.END)
        entry_game_info.delete(0, ctk.END)
        combobox_game_info.set("")  # Limpar a seleção da categoria
        show_main_frame()
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def show_game_info(event):
    clear_game_info()
    selected_index = listbox_games.curselection()
    if selected_index:
        selected_game = games[selected_index[0]]
        info_label.configure(text=f"Informações do Jogo: {selected_game['info']}")

        # Carregar e exibir a imagem do jogo
        if selected_game["image_path"]:
            try:
                img = Image.open(selected_game["image_path"])
                img = img.resize((200, 200), Image.LANCZOS)  # Redimensiona a imagem
                img_tk = ImageTk.PhotoImage(img)
                image_label.configure(image=img_tk)
                image_label.image = img_tk  # Mantém uma referência da imagem
            except Exception as e:
                print(f"Erro ao carregar a imagem: {e}")
                image_label.configure(image='')  # Limpa a imagem se houver erro

        btn_edit_game.pack(pady=10)
        btn_remove_game.pack(pady=10)

def clear_game_info():
    info_label.configure(text="Informações do Jogo: Selecione um jogo para ver os detalhes.")
    image_label.configure(image='')  # Limpa a imagem
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
                games[selected_index[0]]["name"] = new_name
                games[selected_index[0]]["info"] = new_info
                save_games()
                update_listbox()  # Atualiza a Listbox após editar um jogo
                edit_window.destroy()
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

        save_button = ctk.CTkButton(edit_window, text="Salvar", command=save_edit)
        save_button.pack(pady=20)

def rate_game():
    selected_index = listbox_games.curselection()
    if selected_index:
        rate_window = Toplevel(app)
        rate_window.title("Avaliar Jogo")
        rate_window.geometry("400x300")

        selected_game = games[selected_index[0]]

        label_review = ctk.CTkLabel(rate_window, text="Review:",text_color="black")
        label_review.pack(pady=10)
        entry_review = ctk.CTkEntry(rate_window)
        entry_review.insert(0, selected_game["review"])
        entry_review.pack(pady=10)

        label_rating = ctk.CTkLabel(rate_window, text="Nota do Jogo:",text_color="black")
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
                save_games()
                rate_window.destroy()
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

        save_button = ctk.CTkButton(rate_window, text="Salvar", command=save_review)
        save_button.pack(pady=20)

def remove_game():
    selected_index = listbox_games.curselection()
    if selected_index:
        games.pop(selected_index[0])
        save_games()
        update_listbox()  # Atualiza a Listbox após remover um jogo
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
        checkbox = ctk.CTkCheckBox(filter_window, text=category, variable=var, text_color="black")
        checkbox.pack(anchor="w", padx=10, pady=5)

    def confirm_filters():
        selected_filters = [cat for cat, var in check_vars.items() if var.get()]
        listbox_games.delete(0, ctk.END)

        for game in games:
            if game["category"] in selected_filters:
                listbox_games.insert(ctk.END, game["name"])

        filter_window.destroy()

    ctk.CTkButton(filter_window, text="Aplicar", command=confirm_filters, text_color="black").pack(pady=10)

def open_register_window():
    register_window = ctk.CTkToplevel(app)
    register_window.title("Register")
    register_window.geometry("1280x720")

    background_image = Image.open("transferir.png")
    background_photo = ctk.CTkImage(background_image, size=(1280, 720))

    def resize_background(event):
        resized_image = background_image.resize((event.width, event.height))
        background_photo_resized = ctk.CTkImage(resized_image, size=(event.width, event.height))
        background_label.configure(image=background_photo_resized)
        background_label.image = background_photo_resized

    background_label = ctk.CTkLabel(register_window, image=background_photo)
    background_label.place(relwidth=1, relheight=1)
    register_window.bind("<Configure>", resize_background)

    register_frame = ctk.CTkFrame(register_window, corner_radius=10, fg_color=("#003DA5", "#003DA5"), width=500, height=600)
    register_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = ctk.CTkLabel(register_frame, text="Register", font=("Arial", 30, "bold"), text_color="#c7d5e0")
    title_label.pack(pady=(20, 20))

    username_entry = ctk.CTkEntry(register_frame, placeholder_text="Username", font=("Arial", 16),
                                  fg_color="#3c596e", border_color="#66c0f4", text_color="#c7d5e0")
    username_entry.pack(pady=(10, 20), padx=20, fill="x")

    password_entry = ctk.CTkEntry(register_frame, placeholder_text="Password", show="*", font=("Arial", 16),
                                  fg_color="#3c596e", border_color="#66c0f4", text_color="#c7d5e0")
    password_entry.pack(pady=(10, 20), padx=20, fill="x")

    confirm_password_entry = ctk.CTkEntry(register_frame, placeholder_text="Confirm Password", show="*", font=("Arial", 16),
                                          fg_color="#3c596e", border_color="#66c0f4", text_color="#c7d5e0")
    confirm_password_entry.pack(pady=(10, 30), padx=20, fill="x")

    def register():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        user_file = "user_files/users.txt"
        if not os.path.exists(user_file):
            os.makedirs("user_files")
            with open(user_file, "w"): pass

        with open(user_file, "r") as file:
            users = file.readlines()
            for user in users:
                stored_user, _ = user.strip().split("|")
                if username == stored_user:
                    messagebox.showerror("Erro", "Nome de usuário já existe.")
                    return

        with open(user_file, "a") as file:
            file.write(f"{username}|{password}\n")

        messagebox.showinfo("Sucesso", "Cadastro bem-sucedido!")
        register_window.destroy()

    register_button = ctk.CTkButton(register_frame, text="Register", font=("Arial", 18),
                                    fg_color="#66c0f4", text_color="#1b2838", hover_color="#5a9bcc", command=register)
    register_button.pack(pady=20, padx=20, fill="x")

    back_to_login_label = ctk.CTkLabel(register_frame, text="Back to Login", font=("Arial", 14),
                                       text_color="#66c0f4", cursor="hand2")
    back_to_login_label.pack(pady=(0, 20))
    back_to_login_label.bind("<Button-1>", lambda e: register_window.destroy())

def login():
    global current_user, is_admin
    username = username_entry.get()
    password = password_entry.get()

    user_file = "user_files/users.txt"
    if not os.path.exists(user_file):
        os.makedirs("user_files")
        with open(user_file, "w"): pass

    with open(user_file, "r") as file:
        users = file.readlines()

    for user in users:
        stored_user, stored_pass = user.strip().split("|")
        if username == stored_user and password == stored_pass:
            current_user = username
            is_admin = (username == "admin")
            messagebox.showinfo("Login", "Login bem-sucedido!")
            load_games()  # Carrega os jogos do usuário atual
            main_frame.tkraise()  # Exibe a tela principal após o login bem-sucedido
            return

    messagebox.showerror("Erro", "Nome de usuário ou senha inválidos.")

# Janela principal (Login)
app = ctk.CTk()
app.title("Steam Style Login")
app.geometry("1280x720")  # Dimensões da janela principal

# Carregar a imagem de fundo usando Pillow
background_image = Image.open("transferir.png")
background_photo = ctk.CTkImage(background_image, size=(1280, 720))

# Função para ajustar o fundo quando a janela é redimensionada
def resize_background(event):
    resized_image = background_image.resize((event.width, event.height))
    background_photo_resized = ctk.CTkImage(resized_image, size=(event.width, event.height))
    background_label.configure(image=background_photo_resized)
    background_label.image = background_photo_resized

# Fundo personalizado (fundo será ajustado para o tamanho da janela)
background_label = ctk.CTkLabel(app, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Vincula o redimensionamento da janela à função resize_background
app.bind("<Configure>", resize_background)

# Frame principal para organizar os elementos
login_frame = ctk.CTkFrame(app, corner_radius=10, fg_color=("#003DA5", "#003DA5"), width=500, height=600)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

# Título "Sign In"
title_label = ctk.CTkLabel(login_frame, text="Sign In", font=("Arial", 30, "bold"), text_color="#c7d5e0")
title_label.pack(pady=(20, 20))

# Campo de nome de usuário
username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", font=("Arial", 16),
                              fg_color="#3c596e", border_color="#66c0f4", text_color="#c7d5e0")
username_entry.pack(pady=(10, 20), padx=20, fill="x")

# Campo de senha
password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", font=("Arial", 16), 
                               fg_color="#3c596e", border_color="#66c0f4", text_color="#c7d5e0")
password_entry.pack(pady=(10, 30), padx=20, fill="x")

# Botão de login
login_button = ctk.CTkButton(login_frame, text="Sign In", font=("Arial", 18),
                             fg_color="#66c0f4", text_color="#1b2838", hover_color="#5a9bcc", command=login)
login_button.pack(pady=20, padx=20, fill="x")

# Link "Create account"
link_label = ctk.CTkLabel(login_frame, text="Create account", font=("Arial", 14),
                          text_color="#66c0f4", cursor="hand2")
link_label.pack(pady=(0, 20))
link_label.bind("<Button-1>", lambda e: open_register_window())  # Abre a janela de registro

# Frame principal do catálogo (após login)
main_frame = ctk.CTkFrame(app, fg_color=("#003DA5", "#003DA5"))  # Definindo a cor de fundo do main_frame
main_frame.place(relwidth=1, relheight=1)  # Configura o frame principal para ocupar toda a janela
main_frame.lower()  # Inicialmente, mantém o frame principal oculto

# Barra de menu
menu_bar = ctk.CTkFrame(main_frame, corner_radius=0, fg_color=("#003DA5", "#003DA5"))  # Definindo a cor de fundo do menu
menu_bar.pack(side="top", anchor="nw", fill="x")

btn_main = ctk.CTkButton(menu_bar, text="Main", width=100, command=show_main_frame)
btn_main.pack(side="left", padx=10, pady=10)

btn_add_game = ctk.CTkButton(menu_bar, text="Add Game", width=100, command=show_add_game_window)
btn_add_game.pack(side="left", padx=10, pady=10)

main_list_frame = ctk.CTkFrame(main_frame, height=300, width=300)
main_list_frame.pack(side="left", anchor="nw", fill="y", padx=20)

listbox_games = Listbox(main_list_frame, bg="gray", fg="white", font=("Arial", 16))
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

# Create the filter button
btn_filter = ctk.CTkButton(search_frame, text="≡", width=30, command=apply_filters, fg_color="black")
btn_filter.pack(side="left", padx=10, pady=10)

main_info_frame = ctk.CTkFrame(main_frame)
main_info_frame.pack(fill="both", expand=True)

info_label = ctk.CTkLabel(main_info_frame, text="Informações do Jogo: Selecione um jogo para ver os detalhes.", font=("Arial", 18))
info_label.pack(pady=10, padx=20)

# Label para exibir a imagem do jogo
image_label = ctk.CTkLabel(main_info_frame)
image_label.pack(pady=10)

btn_edit_game = ctk.CTkButton(main_info_frame, text="Editar Jogo", command=edit_game)
btn_remove_game = ctk.CTkButton(main_info_frame, text="Remover Jogo", command=remove_game)

btn_rate_game = ctk.CTkButton(main_info_frame, text="Rate Jogo", command=rate_game,text_color="black")
btn_rate_game.pack(pady=30, padx=20)

# Iniciar o loop principal
app.mainloop()