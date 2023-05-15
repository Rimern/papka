import subprocess
import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Создание защищенной папки")
        self.window.geometry("300x200")

        self.folder_label = tk.Label(self.window, text="Введите адрес папки:")
        self.folder_label.pack(pady=10)

        self.folder_entry = tk.Entry(self.window)
        self.folder_entry.pack(pady=10)

        self.password_label = tk.Label(self.window, text="Введите пароль:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack(pady=10)

        self.create_button = tk.Button(self.window, text="Создать папку", command=self.create_protected_folder)
        self.create_button.pack(pady=10)

    def create_protected_folder(self):
        folder_path = self.folder_entry.get()
        password = self.password_entry.get()

        try:
            subprocess.run(["mkdir", "-p", folder_path])
            subprocess.run(["chmod", "700", folder_path])
            subprocess.run(["sudo", "chmod", "root:root", folder_path])
            subprocess.run(["sudo", "chmod", "600", folder_path])

            subprocess.run(["sudo", "mount", "-t", "ecryptfs", "-o", f"key=passphrase:passwd={password},ecryptfs_cipher=aes,ecryptfs_key_bytes=16,ecryptfs_passthrough=n,no_sig_cache,ecryptfs_enable_filename_crypto=n", folder_path, folder_path])

            messagebox.showinfo("Успех", "Защищенная папка успешно создана!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Ошибка", "Произошла ошибка при создании защищенной папки.")

app = App()
app.window.mainloop()
