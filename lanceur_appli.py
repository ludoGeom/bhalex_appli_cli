import tkinter as tk
from app_insert_personne import create_app as app1
from app_modif_personne import create_app as app2
from app_adhesion import create_app as app3

class Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Lanceur d'Applications")
        self.root.geometry("300x500")
        self.root.configure(bg="#96c0eb")  # Bleu clair, ou "blue" pour un bleu standard

        frame = tk.Frame(self.root, bg="#96c0eb")
        frame.pack(expand=True, fill=tk.BOTH)

        btn_app1 = tk.Button(frame, text="Application Insérer", command=lambda: app1(self.root), bg="#3b5998", fg="white")

        btn_app1.pack(pady=10, fill=tk.X)

        btn_app2 = tk.Button(frame, text="Application Modifier", command=lambda: app2(self.root), bg="#3b5998", fg="white")
        btn_app2.pack(pady=10, fill=tk.X)

        btn_app3 = tk.Button(frame, text="Application Adhérer", command=lambda: app3(self.root), bg="#3b5998", fg="white")
        btn_app3.pack(pady=10, fill=tk.X)

        btn_quit = tk.Button(frame, text="Quitter", command=self.root.destroy,  bg="#ff0000", fg="white", activebackground="#ff0000")
        btn_quit.pack(pady=20, fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()
