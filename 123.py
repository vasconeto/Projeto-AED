import customtkinter as ctk
import os

# Initialize the app
app = ctk.CTk()
app.title("Game Managing App")

# Set the window size and position
appwidth = 1280
appheight = 720
screenWidth = app.winfo_screenwidth()
screenHeight = app.winfo_screenheight()
x = (screenWidth // 2) - (appwidth // 2)
y = (screenHeight // 2) - (appheight // 2)
app.geometry(f"{appwidth}x{appheight}+{int(x)}+{int(y)}")
app.resizable(True, True)
app.configure(fg_color="white")

# Create a menu bar
menu_bar = customtkinter.CTkMenu(app)
app.config(menu=menu_bar)

# Add file menu
file_menu = customtkinter.CTkMenu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Game")
file_menu.add_command(label="Open Game")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)

# Add help menu
help_menu = customtkinter.CTkMenu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About")

# Create a sidebar for navigation
sidebar = customtkinter.CTkFrame(app, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

# Add buttons to the sidebar
btn_dashboard = customtkinter.CTkButton(sidebar, text="Dashboard")
btn_dashboard.pack(pady=10, padx=10)

btn_games = customtkinter.CTkButton(sidebar, text="Games")
btn_games.pack(pady=10, padx=10)

btn_settings = customtkinter.CTkButton(sidebar, text="Settings")
btn_settings.pack(pady=10, padx=10)

# Create a main content area
main_content = customtkinter.CTkFrame(app, corner_radius=0)
main_content.pack(side="right", fill="both", expand=True)

# Add a label to the main content area
label = customtkinter.CTkLabel(main_content, text="Welcome to the Game Managing App!", font=("Arial", 24))
label.pack(pady=20)

# Start the main event loop
app.mainloop()