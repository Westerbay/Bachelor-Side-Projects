from interface import Interface
from tkinter import messagebox
from saisi import Saisie

if __name__ == "__main__":

    try:
        Interface().run()
    except:
        if Saisie.name is None and Interface.running:
            messagebox.showinfo("Erreur", "Il semblerait que vous n'ayez pas internet en ce moment.")
        elif Interface.running:
            messagebox.showinfo("Erreur", f"Il semblerait que le pokémon {Saisie.name} pose problème, Signalez le bug!")
