import tkinter as tk
#from tkinter import ttk

# Opret hovedvindue
root = tk.Tk()
root.title("ValutaKurser")
root.geometry("900x500")
root.configure(bg="white")

# Valutakurser dictenary
kurser = {
    "USD": 689.10,
    "DKK": 100.00,     
    "EUR": 804.29,
    "SEK": 68.06,
    "GBP": 848.24,
    "CHF": 804.90
}

# Liste til dropdown
valutaer = list(kurser.keys())

# Konverteringsfunktion
def konverter():
    try:
        beløb = float(left_amount_var.get())
    except ValueError:
        right_amount_var.set("")
        return

    fra = left_currency_var.get()
    til = right_currency_var.get()

    # Omregning: først til DKK, så til målvaluta
    resultat = (beløb * kurser[fra])/kurser[til] 
    #resultat = beløb_i_dkk / (kurser[til] / 100)

    right_amount_var.set(f"{resultat:.2f}")

# ---- Top overskrift ----
title = tk.Label(root, text="ValutaKurser", font=("Arial", 24, "bold"), padx=20, pady=10, bg="white")
title.pack(pady=20)

# ---- Øverste beløbssektion ----
frame_top = tk.Frame(root, bg="white")
frame_top.pack(pady=20)

# Beløb venstre
left_amount_var = tk.StringVar()
left_entry = tk.Entry(frame_top, textvariable=left_amount_var, font=("Arial", 20), width=10,
                      relief="solid", justify="center", bg="white")
left_entry.grid(row=0, column=0, padx=10)

# Dropdown venstre
left_currency_var = tk.StringVar(value="USD")
left_currency_menu = tk.OptionMenu(frame_top, left_currency_var, *valutaer)
left_currency_menu.config(font=("Arial", 16), bg="white")
left_currency_menu.grid(row=0, column=1, padx=10)

# Skillelinje
tk.Label(frame_top, text="→", font=("Arial", 26, "bold"), bg="white").grid(row=0, column=2, padx=20)

# Dropdown højre
right_currency_var = tk.StringVar(value="DKK")
right_currency_menu = tk.OptionMenu(frame_top, right_currency_var, *valutaer)
right_currency_menu.config(font=("Arial", 16), bg="white")
right_currency_menu.grid(row=0, column=3, padx=10)

# Beløb højre
right_amount_var = tk.StringVar()
right_entry = tk.Entry(frame_top, textvariable=right_amount_var, font=("Arial", 20), width=10,
                       relief="solid", justify="center", bg="white")
right_entry.grid(row=0, column=4, padx=10)

# Når der skrives i venstre felt → konverter
left_entry.bind("<KeyRelease>", lambda e: konverter())
left_currency_menu.bind("<Configure>", lambda e: konverter())
right_currency_menu.bind("<Configure>", lambda e: konverter())

# ---- Valutakurser sektion ----
frame_rates = tk.Frame(root, bg="white")
frame_rates.pack(pady=30)

# Funktion til at lave en række
def make_row(parent, valuta, kode, ændring, kurs):
    row = tk.Frame(parent, bg="white")
    row.pack(pady=5, fill="x", padx=50)

    widthBoks = 10

    tk.Label(row, text=valuta, font=("Arial", 16), relief="solid", width=18, bg="white").pack(side="left")
    tk.Label(row, text=kode, font=("Arial", 16), relief="solid", width=widthBoks, bg="white").pack(side="left")
    tk.Label(row, text=ændring, font=("Arial", 16), relief="solid", width=widthBoks, fg="green" if "↑" in ændring else "red", bg="white").pack(side="left", expand=True)
    tk.Label(row, text=kurs, font=("Arial", 16), relief="solid", width=widthBoks, bg="white").pack(side="right")

# Første række: Euro
make_row(frame_rates, "Euro", "EUR", "0.4% ↑", "804.29")

# Anden række: SEK
make_row(frame_rates, "Svenske Kroner", "SEK", "0.1% ↑", "68.06")

# Tredje række: GBP
make_row(frame_rates, "Britiske Pund", "GBP", "-0.3% ↓", "848.24")

# Fjerde række: USD
make_row(frame_rates, "Amerikanske Dollar", "USD", "-0.0% ↓", "689.10")

# Femte række: CHF
make_row(frame_rates, "Schweiziske Franc", "CHF", "0.4% ↑", "804.90")

root.mainloop()
