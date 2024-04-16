import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import *
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import pyperclip

# Variabila globala pentru a stoca cheia
encryption_key = None

# Generarea cheii si stocarea acestia in variabila globala
def generate_key():
    global encryption_key
    encryption_key = Fernet.generate_key()

    # Conversia cheii intr-un string pentru a putea fi afisata in popup
    key_str = encryption_key.decode()

    # Aratam cheia utilizatorului printr-un messagebox
    messagebox.showinfo("Generarea cheii", f"Cheia a fost generata cu succes:\n\n{key_str}")

    # Copiem cheia automat in clipboard
    pyperclip.copy(key_str)

    # Informam utilizatorul de faptul ca a fost copiata cheia automat
    messagebox.showinfo("Generarea cheii", "Cheia a fost copiata in clipboard.")

    # Pentru Debugging
    # print("Generated key:", key_str)

# Criptarea fisierului utilizand cheia globala stocata
def encrypt_file():
    global encryption_key
    if encryption_key is None:
        messagebox.showerror("Eroare", "Va rugam sa generati o cheie inainte de a cripta un fisier!")
        return

    # Intrebam userul sa aleaga un fisier + eroare
    file_path = filedialog.askopenfilename()
    if not file_path:
        messagebox.showwarning("Atentie!", "Nu s-a selectat fisierul.")
        return
        
    # Citim continutul fisierului
    with open(file_path, 'rb') as file:
        original = file.read()

    # Criptam fisierul folosind cheia globala stocata anterior
    fernet = Fernet(encryption_key)
    encrypted = fernet.encrypt(original)

    # Scriem continutul criptat intr-un fisier nou
    encrypt_file_path = file_path + '.enc'
    with open(encrypt_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    # Mesaj pentru criptarea cu succes a fisierului
    messagebox.showinfo("Criptare", "Fisierul a fost criptat cu succes.")

    # Pentru Debugging
    # print("Encrypted file path:", encrypt_file_path)

# Decriptarea fisierului folosing o cheie inserata manual
def decrypt_file():
    try:
        # Intrebam utilizatorul de locatia fisierului ce urmeaza a fi decriptat
        encrypted_file_path = filedialog.askopenfilename()
        if not encrypted_file_path:
            messagebox.showwarning("Atentie", "Nu a fost selectat fisierul.")
            return

        # Intrebam userul care este cheia pentru decryptare + input pentru a o scrie
        key = simpledialog.askstring("Introduceti Cheia", "Introduceti cheia pentru decriptare:")
        if not key:
            messagebox.showwarning("Atentie", "Nu s-a introdus o cheie de decriptare.")
            return

        # Citim continutul fisierului criptat
        with open(encrypted_file_path, 'rb') as enc_file:
            encrypted = enc_file.read()

        # Decriptam fisierul utilizand cheia (corecta) introdusa de user
        fernet = Fernet(key.encode())
        decrypted = fernet.decrypt(encrypted)

        # Intrebam utilizatorul unde salvam noul fisier decriptat
        decrypted_file_path = filedialog.asksaveasfilename(defaultextension=".txt")

        # Scriem continutul decriptat in noul fisier
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)

        messagebox.showinfo("Decriptare", "Fisierul a fost decriptat cu succes.")

    except Exception as e:
        messagebox.showerror("Error", str(e))



# Crearea ferestrei principale
window = tk.Tk()
window.title("CryptuS by PK")
window.geometry('850x640')
window.configure(bg='#333333')
frame = tk.Frame(bg='#333333')

bg_photo = Image.open('imagine.jpg')
photo = ImageTk.PhotoImage(bg_photo)

background_label = tk.Label(window, image=photo)
background_label.place(relwidth=1, relheight=1)

# Crearea butoanelor pentru generarea cheii, criptare si decriptare fisier
generate_key_button = tk.Button(window, text="Genereaza cheia", bg='#FC8EFE', fg="#FFFFFF", command=generate_key)
generate_key_button.place(relx=0.5, rely=0.3, anchor=CENTER)
encrypt_button = tk.Button(window, text="Cripteaza fisier", bg="#F76262", fg="#FFFFFF", command=encrypt_file)
encrypt_button.place(relx=0.5, rely=0.5, anchor=CENTER)
decrypt_button = tk.Button(window, text="Decriptare fisier", bg="#86F762", fg="#FFFFFF", command=decrypt_file)
decrypt_button.place(relx=0.5, rely=0.7, anchor=CENTER)

# Pornirea aplicatie GUI
window.mainloop()