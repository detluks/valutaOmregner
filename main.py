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
                    if data[i]=="rate":
                        for row in reader:
                            dicdic[codes[k]][data[i]] = float(",".join(row))
                            k+=1
                    else:
                        for row in reader:
                            dicdic[codes[k]][data[i]] = ",".join(row)
                            k+=1
        dicdic["DKK"]={'desc':"Danske kroner", 'rate': 100}
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
    def __init__(self, parent, dicdic:dict):
        super().__init__(parent)
        self.controller = None
        self.dicdic = dicdic
        self.valutaer = list(self.dicdic.keys())
        self.APIFunktion()
        



    def set_controller(self, controller):
        self.controller = controller

    def konverter(self):
        try:
            beløb = float(self.left_amount_var.get())
        except ValueError:
            self.right_amount_var.set("")
            return

        fra = self.left_currency_var.get()
        til = self.right_currency_var.get()

        # Omregning: først til DKK, så til målvaluta
        resultat = (beløb * self.dicdic[fra]["rate"])/(self.dicdic[til]["rate"]) 
        

        self.right_amount_var.set(f"{resultat:.2f}")

    def APIFunktion(self):
        # ---- Top overskrift ----
        title = tk.Label(self, text="ValutaKurser", font=("Arial", 24, "bold"), padx=20, pady=10, bg="white")
        title.pack(pady=20)

        # ---- Øverste beløbssektion ----
        frame_top = tk.Frame(self, bg="white")
        frame_top.pack(pady=20)

        # Beløb venstre
        self.left_amount_var = tk.StringVar()
        left_entry = tk.Entry(frame_top, textvariable=self.left_amount_var, font=("Arial", 20), width=10,
                            relief="solid", justify="center", bg="white")
        left_entry.grid(row=0, column=0, padx=10)

        # Dropdown venstre
        self.left_currency_var = tk.StringVar(value="USD")
        left_currency_menu = tk.OptionMenu(frame_top, self.left_currency_var, *self.valutaer)
        left_currency_menu.config(font=("Arial", 16), bg="white")
        left_currency_menu.grid(row=0, column=1, padx=10)

        # Skillelinje
        tk.Label(frame_top, text="→", font=("Arial", 26, "bold"), bg="white").grid(row=0, column=2, padx=20)

        # Dropdown højre
        self.right_currency_var = tk.StringVar(value="DKK")
        right_currency_menu = tk.OptionMenu(frame_top, self.right_currency_var, *self.valutaer)
        right_currency_menu.config(font=("Arial", 16), bg="white")
        right_currency_menu.grid(row=0, column=3, padx=10)

        # Beløb højre
        self.right_amount_var = tk.StringVar()
        right_entry = tk.Entry(frame_top, textvariable=self.right_amount_var, font=("Arial", 20), width=10,
                            relief="solid", justify="center", bg="white")
        right_entry.grid(row=0, column=4, padx=10)

        # Når der skrives i venstre felt → konverter
        left_entry.bind("<KeyRelease>", lambda e: self.konverter())
        left_currency_menu.bind("<Configure>", lambda e: self.konverter())
        right_currency_menu.bind("<Configure>", lambda e: self.konverter())

        # ---- Valutakurser sektion ----
        frame_rates = tk.Frame(self, bg="white")
        frame_rates.pack(pady=30)

        # Funktion til at lave en række
        def make_row(parent, valuta, kode, kurs):
            row = tk.Frame(parent, bg="white")
            row.pack(pady=5, fill="x", padx=50)

            widthBoks = 10

            tk.Label(row, text=valuta, font=("Arial", 16), relief="solid", width=18, bg="white").pack(side="left")
            tk.Label(row, text=kode, font=("Arial", 16), relief="solid", width=widthBoks, bg="white").pack(side="left")
            tk.Label(row, text=kurs, font=("Arial", 16), relief="solid", width=widthBoks, bg="white").pack(side="right")

        # Første række: Euro
        make_row(frame_rates, "Euro", "EUR", self.dicdic["EUR"]["rate"])

        # Anden række: SEK
        make_row(frame_rates, "Svenske Kroner", "SEK", self.dicdic["SEK"]["rate"])

        # Tredje række: GBP
        make_row(frame_rates, "Britiske Pund", "GBP", self.dicdic["GBP"]["rate"])

        # Fjerde række: USD
        make_row(frame_rates, "Amerikanske Dollar", "USD", self.dicdic["USD"]["rate"])

        # Femte række: CHF
        make_row(frame_rates, "Schweiziske Franc", "CHF", self.dicdic["CHF"]["rate"])









# main
if __name__ == "__main__":
    root = tk.Tk()
    root.title("ValutaKurser")
    root.geometry("900x500")
    root.configure(bg="white")

    model = Model("https://www.nationalbanken.dk/api/currencyratesxml?lang=da")
    model.getValutas()
    datoer=model.getDatoer()
    dicdic = model.dataFraDato(datoer[len(datoer)-1])
    view = View(root,dicdic)
    view.pack(fill="both", expand=True)
    controller = Controller(model, view)
    view.set_controller(controller)

    

    root.mainloop()
