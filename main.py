import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import csv
import os
data = ["code", "rate", "desc"]


# model
class Model:
    def __init__(self, url=""):
        self.url = url
    
    def getValutas(self):
      response = requests.get(self.url)
      soup = BeautifulSoup(response.text, "xml") 
      dato = soup.dailyrates["id"]
      os.makedirs(f"saves/{dato}", exist_ok=True)

      for i in range(len(data)):
        csv_path = f"saves/{dato}/{data[i]}"
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for cur in soup.find_all("currency"):
                linje = []
                if data[i] == "rate":
                    rate = cur["rate"].replace(",", ".")
                    linje.append(float(rate))
                else:
                    spekData = cur[data[i]]
                    linje.append(spekData)
                writer.writerow(linje)
    
    def dataFraDato(self, dato):
        dicdic = {}
        codes = []
        for i in range(3):
            filePath = f"saves/{dato}/{data[i]}"
            with open(filePath, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                if i == 0:
                    for row in reader:
                        dicdic[",".join(row)] = {'desc':'','rate':''}
                        codes.append(",".join(row))
                else:
                    k = 0
                    for row in reader:
                        dicdic[codes[k]][data[i]] = ",".join(row)
                        k+=1
        return dicdic

    def getDatoer(self):
        savesPath = "saves"
        datoer = [
            dato for dato in os.listdir(savesPath)
            if os.path.isdir(os.path.join(savesPath, dato))
        ]
        return datoer



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

    model = Model("https://www.nationalbanken.dk/api/currencyratesxml?lang=da")
    view = View(root)
    controller = Controller(model, view)
    view.set_controller(controller)
    model.get_valutas()

    root.mainloop()
