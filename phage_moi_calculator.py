import tkinter as tk
from tkinter import ttk, messagebox

# Multipliers for CFU/mL estimation
strain_multipliers = {
    "XL1-Blue": 8.0e8,
    "TG1": 8.5e8,
    "Lemo21": 6.5e8
}

def calculate():
    try:
        strain = strain_var.get()
        od600 = float(od_entry.get())
        volume_ml = float(volume_entry.get())
        moi = float(moi_entry.get())
        stock_conc = float(stock_entry.get())

        cfu_ml = od600 * strain_multipliers[strain]
        total_cells = cfu_ml * volume_ml
        required_phage = total_cells * moi
        phage_vol_ul = (required_phage / stock_conc) * 1000

        result = (
            f"Estimated CFU/mL: {int(cfu_ml):,}\n"
            f"Total Cells: {int(total_cells):,}\n"
            f"Helper Phage Required: {int(required_phage):,} PFU\n"
            f"→ Add {round(phage_vol_ul, 2)} µL of helper phage"
        )
        result_label.config(text=result)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# GUI setup
root = tk.Tk()
root.title("Helper Phage MOI Calculator")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

strain_var = tk.StringVar(value="XL1-Blue")
ttk.Label(frame, text="Strain:").grid(column=0, row=0, sticky="e")
strain_menu = ttk.OptionMenu(frame, strain_var, "XL1-Blue", *strain_multipliers.keys())
strain_menu.grid(column=1, row=0)

ttk.Label(frame, text="OD600:").grid(column=0, row=1, sticky="e")
od_entry = ttk.Entry(frame)
od_entry.insert(0, "0.2")
od_entry.grid(column=1, row=1)

ttk.Label(frame, text="Culture Volume (mL):").grid(column=0, row=2, sticky="e")
volume_entry = ttk.Entry(frame)
volume_entry.insert(0, "1.0")
volume_entry.grid(column=1, row=2)

ttk.Label(frame, text="MOI (Helper phage ratio):").grid(column=0, row=3, sticky="e")
moi_entry = ttk.Entry(frame)
moi_entry.insert(0, "10")
moi_entry.grid(column=1, row=3)

ttk.Label(frame, text="Phage Stock (PFU/mL):").grid(column=0, row=4, sticky="e")
stock_entry = ttk.Entry(frame)
stock_entry.insert(0, "2e12")
stock_entry.grid(column=1, row=4)

ttk.Button(frame, text="Calculate", command=calculate).grid(column=0, row=5, columnspan=2, pady=10)

result_label = ttk.Label(frame, text="", justify="left")
result_label.grid(column=0, row=6, columnspan=2)

root.mainloop()
