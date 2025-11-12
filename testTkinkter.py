import tkinter as tk
from tkinter import ttk

# Opret hovedvindue
root = tk.Tk()
root.title("ValutaKurser")
root.geometry("900x500")
root.configure(bg="white")

# ---- Top overskrift ----
title = tk.Label(root, text="ValutaKurser", font=("Arial", 24, "bold"), padx=20, pady=10, bg="white")
title.pack(pady=20)

# ---- Øverste beløbssektion ----
frame_top = tk.Frame(root, bg="white")
frame_top.pack(pady=20)

# Beløb venstre
left_amount_var = tk.StringVar()
left_entry = tk.Entry(frame_top, textvariable=left_amount_var, font=("Arial", 20), width=10, relief="solid", justify="center")
left_entry.grid(row=0, column=0, padx=10)

tk.Label(frame_top, text="USD", font=("Arial", 20), bg="white").grid(row=0, column=1, padx=10)
tk.Label(frame_top, text="===", font=("Arial", 20, "bold"), bg="white").grid(row=0, column=2, padx=10)
tk.Label(frame_top, text="DKK", font=("Arial", 20), bg="white").grid(row=0, column=3, padx=10)

# Beløb højre
right_amount_var = tk.StringVar()
right_entry = tk.Entry(frame_top, textvariable=right_amount_var, font=("Arial", 20), width=10, relief="solid", justify="center")
right_entry.grid(row=0, column=4, padx=10)

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
