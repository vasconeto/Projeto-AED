import customtkinter
import CTkMessagebox  # Corrigir a importação

app = customtkinter.CTk()
app.title("Log in page")

# Dimensões da janela
appwidth = 400
appheight = 600

screenWidth = app.winfo_screenwidth()
screenHeight = app.winfo_screenheight()

# Resolução
x = (screenWidth / 2) - (appwidth / 2)
y = (screenHeight / 2) - (appheight / 2)
app.geometry(f"{appwidth}x{appheight}+{int(x)}+{int(y)}")
app.resizable(False, False)
app.configure(fg_color="black")


def register():
    username = entryUser.get()
    password = entryPass.get()
    passwordVerification = passVerification.get()

    if not username or not password or not passwordVerification:
        CTkMessagebox(title="Error", message="Please fill all fields", icon="error")
    elif password != passwordVerification:
        CTkMessagebox(title="Error", message="Passwords do not match", icon="error")
    else:
        CTkMessagebox(title="Success", message="Account created successfully", icon="info")
        entryUser.delete(0, 'end')
        entryPass.delete(0, 'end')
        passVerification.delete(0, 'end')


frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=20, padx=20, fill='both', expand=True)

entryUser = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entryUser.pack(pady=12, padx=10)

entryPass = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entryPass.pack(pady=12, padx=10)

passVerification = customtkinter.CTkEntry(master=frame, placeholder_text="Repeat Password", show="*")
passVerification.pack(pady=12, padx=10)

buttonRegister = customtkinter.CTkButton(master=frame, text='Register', command=register)
buttonRegister.pack(pady=12, padx=10)

checkboxRemember = customtkinter.CTkCheckBox(master=frame, text='Remember Me')
checkboxRemember.pack(pady=12, padx=10)

app.mainloop()
