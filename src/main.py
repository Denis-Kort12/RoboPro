import tkinter as tk
from tkinter import ttk
from parser_payload import ParserPaylod
from kinematic_work import KinematicCalculation
import numpy as np
import warnings
warnings.filterwarnings('ignore')

DH_PARAMS = [
    {"d": 0.21,  "a": 0,      "alpha": np.pi/2},
    {"d": 0.193, "a": -0.8,   "alpha": 0},
    {"d": -0.16, "a": -0.598, "alpha": 0},
    {"d": 0.25,  "a": 0,      "alpha": np.pi/2},
    {"d": 0.25,  "a": 0,      "alpha": -np.pi/2},
    {"d": 0.25,  "a": 0,      "alpha": 0}
]

def button_run(dh_params, tree):
    try:
        parserPaylod = ParserPaylod()
        kinematicCalculation = KinematicCalculation(dh_params, name="Robot")

        list_payloads = parserPaylod.get_payloads()
        for row in tree.get_children():
            tree.delete(row)

        for payload in list_payloads:
            pos = kinematicCalculation.compute_position(payload.theta)
            values = (payload.timestamp, *map(lambda v: f"{v:.3f}", pos))
            tree.insert('', 'end', values=values)
    except Exception as e:
        print("Error:", e)

def create_gui():

    root = tk.Tk()
    root.title("UDP Client")

    columns = ('timestamp', 'x', 'y', 'z')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill='both', expand=True)

    btn = tk.Button(root, text="Get data", command=lambda: button_run(dh_params=DH_PARAMS, tree=tree))
    btn.pack(pady=10)

    return root

if __name__ == "__main__":
    create_gui().mainloop()
