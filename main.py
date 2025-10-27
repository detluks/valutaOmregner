import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import csv


# model
class Model:
    def __init__(self, url=""):
        self.url = url
    
    def get_valutas(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text)



# controller
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view



# view
class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        self.create_widgets()

    def create_widgets(self):
        self.grid(padx=20, pady=20)


    def set_controller(self, controller):
        self.controller = controller




# main
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Valuta omregner")
    root.geometry("400x150")

    model = Model("https://valutaomregneren.dk/")
    view = View(root)
    controller = Controller(model, view)
    view.set_controller(controller)

    root.mainloop()
