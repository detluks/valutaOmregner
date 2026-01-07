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

    def refresh_rates(self):
        #Hent nye kurser, opdater dato-liste og sæt view til nyeste dato.
        self.model.getValutas()
        datoer = sorted(self.model.getDatoer())
        if not datoer:
            return
        latest = datoer[-1]
        dicdic = self.model.dataFraDato(latest)
        self.view.update_data(dicdic, datoer, latest)

    def change_dato(self, dato):
        #Skift til en anden dato valgt i dropdown.
        datoer = sorted(self.model.getDatoer())
        dicdic = self.model.dataFraDato(dato)
        self.view.update_data(dicdic, datoer, dato)



# view
class View(ttk.Frame):
    def __init__(self, parent, dicdic:dict, datoer, current_dato):
        super().__init__(parent)
        self.controller = None   

        # data fra model (gives via main/controller)
        self.dicdic = dicdic
        self.valutaer = list(self.dicdic.keys())
        self.datoer = sorted(datoer)
        self.current_dato = current_dato

        # Tk-variabler
        self.left_amount_var = tk.StringVar()
        self.right_amount_var = tk.StringVar()
        self.left_currency_var = tk.StringVar(value="USD")
        self.right_currency_var = tk.StringVar(value="DKK")
        self.dato_var = tk.StringVar(value=self.current_dato)

        # widget referencer der skal opdateres
        self.dato_menu = None
        self.left_currency_menu = None
        self.right_currency_menu = None
        self.eur_label = None
        self.sek_label = None
        self.gbp_label = None
        self.usd_label = None
        self.chf_label = None

        self.APIFunktion()

    def set_controller(self, controller):
        self.controller = controller

    # ---------- UI BYGNING ----------

    def APIFunktion(self):
        # ---- Top-bar med overskrift + dato-dropdown + refresh-knap ----
        header_frame = tk.Frame(self, bg="white")
        header_frame.pack(fill="x", pady=10)

        # Titel til venstre
        title = tk.Label(
            header_frame,
            text="ValutaKurser",
            font=("Arial", 24, "bold"),
            padx=20,
            pady=10,
            bg="white"
        )
        title.pack(side="left")

        # Højre side: dato-dropdown + refresh-knap
        controls_frame = tk.Frame(header_frame, bg="white")
        controls_frame.pack(side="right", padx=20)

        tk.Label(
            controls_frame,
            text="Dato:",
            font=("Arial", 10),
            bg="white"
        ).pack(side="left", padx=(0, 5))

        self.dato_menu = tk.OptionMenu(
            controls_frame,
            self.dato_var,
            *self.datoer,
            command=self._on_dato_changed
        )
        self.dato_menu.config(font=("Arial", 10), bg="white")
        self.dato_menu.pack(side="left")

        refresh_button = tk.Button(
            controls_frame,
            text="↻",
            font=("Arial", 12),
            command=self._on_refresh_clicked,
            relief="raised",
            bg="white",
        )
        refresh_button.pack(side="left", padx=(5, 0))

        # ---- Øverste beløbssektion ----
        frame_top = tk.Frame(self, bg="white")
        frame_top.pack(pady=20)

        # Beløb venstre
        left_entry = tk.Entry(
            frame_top,
            textvariable=self.left_amount_var,
            font=("Arial", 20),
            width=10,
            relief="solid",
            justify="center",
            bg="white"
        )
        left_entry.grid(row=0, column=0, padx=10)

        # Dropdown venstre
        self.left_currency_menu = tk.OptionMenu(
            frame_top,
            self.left_currency_var,
            *self.valutaer,
            command=lambda *_: self.konverter()
        )
        self.left_currency_menu.config(font=("Arial", 16), bg="white")
        self.left_currency_menu.grid(row=0, column=1, padx=10)

        # Skillelinje
        tk.Label(
            frame_top,
            text="→",
            font=("Arial", 26, "bold"),
            bg="white"
        ).grid(row=0, column=2, padx=20)

        # Dropdown højre
        self.right_currency_menu = tk.OptionMenu(
            frame_top,
            self.right_currency_var,
            *self.valutaer,
            command=lambda *_: self.konverter()
        )
        self.right_currency_menu.config(font=("Arial", 16), bg="white")
        self.right_currency_menu.grid(row=0, column=3, padx=10)

        # Beløb højre
        right_entry = tk.Entry(
            frame_top,
            textvariable=self.right_amount_var,
            font=("Arial", 20),
            width=10,
            relief="solid",
            justify="center",
            bg="white"
        )
        right_entry.grid(row=0, column=4, padx=10)

        # Når der skrives i venstre felt → konverter
        left_entry.bind("<KeyRelease>", lambda e: self.konverter())

        # ---- Valutakurser sektion ----
        frame_rates = tk.Frame(self, bg="white")
        frame_rates.pack(pady=30)

        # Funktion til at lave en række og returnere kurs-labelen
        def make_row(parent, valuta, kode, kurs):
            row = tk.Frame(parent, bg="white")
            row.pack(pady=5, fill="x", padx=50)

            widthBoks = 10

            tk.Label(
                row,
                text=valuta,
                font=("Arial", 16),
                relief="solid",
                width=18,
                bg="white"
            ).pack(side="left")
            tk.Label(
                row,
                text=kode,
                font=("Arial", 16),
                relief="solid",
                width=widthBoks,
                bg="white"
            ).pack(side="left")
            rate_label = tk.Label(
                row,
                text=kurs,
                font=("Arial", 16),
                relief="solid",
                width=widthBoks,
                bg="white"
            )
            rate_label.pack(side="right")

            return rate_label

        # Første række: Euro
        self.eur_label = make_row(
            frame_rates, "Euro", "EUR", self.dicdic["EUR"]["rate"]
        )

        # Anden række: SEK
        self.sek_label = make_row(
            frame_rates, "Svenske Kroner", "SEK", self.dicdic["SEK"]["rate"]
        )

        # Tredje række: GBP
        self.gbp_label = make_row(
            frame_rates, "Britiske Pund", "GBP", self.dicdic["GBP"]["rate"]
        )

        # Fjerde række: USD
        self.usd_label = make_row(
            frame_rates, "Amerikanske Dollar", "USD", self.dicdic["USD"]["rate"]
        )

        # Femte række: CHF
        self.chf_label = make_row(
            frame_rates, "Schweiziske Franc", "CHF", self.dicdic["CHF"]["rate"]
        )

    # ---------- VIEW LOGIK ----------

    def konverter(self):
        try:
            beløb = float(self.left_amount_var.get())
        except ValueError:
            self.right_amount_var.set("")
            return

        fra = self.left_currency_var.get()
        til = self.right_currency_var.get()

        resultat = (beløb * self.dicdic[fra]["rate"])/(self.dicdic[til]["rate"])
        self.right_amount_var.set(f"{resultat:.2f}")

    def _on_refresh_clicked(self):
        if self.controller:
            self.controller.refresh_rates()

    def _on_dato_changed(self, selected_dato):
        if self.controller:
            self.controller.change_dato(selected_dato)

    def _update_currency_menus(self):
        if not self.left_currency_menu or not self.right_currency_menu:
            return

        current_left = self.left_currency_var.get()
        current_right = self.right_currency_var.get()

        if current_left not in self.valutaer:
            self.left_currency_var.set(self.valutaer[0])
        if current_right not in self.valutaer:
            self.right_currency_var.set(self.valutaer[0])

        # venstre menu
        left_menu = self.left_currency_menu["menu"]
        left_menu.delete(0, "end")
        for code in self.valutaer:
            left_menu.add_command(
                label=code,
                command=lambda v=code: (self.left_currency_var.set(v), self.konverter())
            )

        # højre menu
        right_menu = self.right_currency_menu["menu"]
        right_menu.delete(0, "end")
        for code in self.valutaer:
            right_menu.add_command(
                label=code,
                command=lambda v=code: (self.right_currency_var.set(v), self.konverter())
            )

    def _update_rate_labels(self):
        try:
            self.eur_label.config(text=self.dicdic["EUR"]["rate"])
            self.sek_label.config(text=self.dicdic["SEK"]["rate"])
            self.gbp_label.config(text=self.dicdic["GBP"]["rate"])
            self.usd_label.config(text=self.dicdic["USD"]["rate"])
            self.chf_label.config(text=self.dicdic["CHF"]["rate"])
        except KeyError:
            pass

    def update_data(self, dicdic, datoer, current_dato):
        """Kaldes af controller når data skifter (ny dato eller refresh)."""
        self.dicdic = dicdic
        self.valutaer = list(self.dicdic.keys())
        self.datoer = sorted(datoer)
        self.current_dato = current_dato
        self.dato_var.set(current_dato)

        # opdater dato-dropdown menu
        if self.dato_menu is not None:
            menu = self.dato_menu["menu"]
            menu.delete(0, "end")
            for d in self.datoer:
                menu.add_command(
                    label=d,
                    command=lambda v=d: (self.dato_var.set(v), self._on_dato_changed(v))
                )

        # opdater valuta-dropdowns og labels
        self._update_currency_menus()
        self._update_rate_labels()
        self.konverter()



# main
if __name__ == "__main__":
    root = tk.Tk()
    root.title("ValutaKurser")
    root.geometry("900x500")
    root.configure(bg="white")

    model = Model("https://www.nationalbanken.dk/api/currencyratesxml?lang=da")

    # Hent kurser mindst én gang
    model.getValutas()
    datoer = model.getDatoer()
    seneste_dato = sorted(datoer)[-1]
    dicdic = model.dataFraDato(seneste_dato)

    view = View(root, dicdic, datoer, seneste_dato)
    view.pack(fill="both", expand=True)

    controller = Controller(model, view)
    view.set_controller(controller)

    root.mainloop()
