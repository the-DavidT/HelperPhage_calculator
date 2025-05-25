# 📱 Helper Phage Calculator

A sleek, iOS-styled desktop application built with `tkinter` to help biologists calculate the volume of helper phage required based on bacterial culture parameters.

---

## 🚀 Features

- Elegant **iOS-style UI** using custom themes and rounded elements
- Live calculation of:
  - CFU/mL based on OD<sub>600</sub> and strain
  - Total cells in culture
  - Required helper phage in PFU and µL
- Dynamic updates as you type (no need to press "Enter")
- Clean, readable **scientific notation formatting** (e.g., 1.20 × 10⁹)
- Predefined strain multipliers:
  - `XL1-Blue`
  - `TG1`
  - `Lemo21`
- User-friendly error messages

---

## 🧪 Use Case

Designed for molecular biology labs using helper phages (e.g., M13K07) during phagemid amplification. Enter culture conditions and the app calculates the precise amount of helper phage stock to add.

---

## 🖼️ Interface

- Left panel: Input parameters
- Right panel: Calculated results
- Highlighted orange box shows **µL of helper phage to add**

---

## 🛠️ Requirements

- Python 3.7+
- Tkinter (usually pre-installed with Python)
- Font: `SF Pro Display` (optional for exact iOS-style appearance)

---

## 📦 Installation

Use precompiled releases or compile by yourself:

1. Clone the repository:

   ```bash
   mkdir phage-calculator
   git clone https://github.com/the-DavidT/HelperPhage_calculator.git
   cd phage-calculator
   ```

2. Create the app:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pyinstaller --onefile -D --windowed /PATH/TO/Hphage_calc2.py
   ```

3. Run the app:

   ```bash
   python app.py
   ```

---

## 🧮 Calculation Logic

The app computes the phage volume with the following formula:

```
CFU/mL = OD600 × strain_multiplier
Total cells = CFU/mL × culture volume
Required PFU = Total cells × MOI
Phage Volume (µL) = (Required PFU / Stock PFU per mL) × 1000
```

---

## 🧬 Example

For strain `XL1-Blue`, OD<sub>600</sub> = `0.2`, culture volume = `1 mL`, MOI = `10`, and stock = `2e12 PFU/mL`, the result is:

```
Add 0.8 µL of helper phage
```

---

## 🧠 Customization

To add more strains, simply modify the `strain_multipliers` dictionary:

```python
strain_multipliers = {
    "XL1-Blue": 8.0e8,
    "TG1": 8.5e8,
    "Lemo21": 6.5e8,
    "YourNewStrain": your_multiplier
}
```


---

No License - Free to use and reproduce

---

## ✨ Author

Developed by **[the-DavidT]**  
