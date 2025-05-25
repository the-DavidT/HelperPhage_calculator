import tkinter as tk
from tkinter import ttk, messagebox
import re

# Set app theme and style
def setup_theme():
    style = ttk.Style()
    style.theme_use('clam')
    
    # iOS color palette
    ios_dark_bg = "#1C1C1E"       # Dark background
    ios_medium_bg = "#2C2C2E"     # Medium background for panels
    ios_light_text = "#FFFFFF"    # Light text
    ios_accent_orange = "#FF9500" # Orange accent (function buttons)
    ios_dark_orange = "#E67700"   # Darker orange for calculate button
    ios_accent_gray = "#D4D4D2"   # Light gray accent (number buttons)
    ios_result_bg = "#333333"     # Dark gray for display area
    
    # Configure colors for different states
    style.configure("TFrame", background=ios_dark_bg)
    style.configure("TLabel", background=ios_dark_bg, foreground=ios_light_text, 
                   font=('SF Pro Display', 11))  # iOS font
    style.configure("Title.TLabel", font=('SF Pro Display', 16, 'bold'), 
                   background=ios_dark_bg, foreground=ios_light_text)
    
    # Results box like iOS calculator display - with rounded corners
    style.configure("Result.TLabel", 
                   font=('SF Pro Display', 11), 
                   background=ios_result_bg,
                   foreground=ios_light_text,
                   padding=15)
    
    # Highlight box (main result) - iOS orange accent with rounded corners
    style.configure("Highlight.TFrame", 
                   background=ios_accent_orange,
                   borderwidth=0, 
                   relief="flat")
    style.configure("Highlight.TLabel", 
                   font=('SF Pro Display', 18, 'bold'),
                   background=ios_accent_orange,
                   foreground=ios_dark_bg,  # Dark text on orange for readability
                   padding=15)
    
    # Calculate button - iOS style with darker orange
    style.configure("Calculate.TButton", 
                   font=('SF Pro Display', 14, 'bold'),
                   background=ios_dark_orange,
                   foreground=ios_dark_bg)
    
    style.map('Calculate.TButton',
             background=[('active', '#D26500')])  # Even darker orange when clicked
    
    # Entry fields with iOS style
    style.configure("TEntry", 
                   font=('SF Pro Display', 12),
                   fieldbackground=ios_medium_bg,
                   foreground=ios_light_text,
                   bordercolor=ios_medium_bg)
    
    # Combobox with iOS style - make it consistent with entry fields
    style.configure("TCombobox", 
                   font=('SF Pro Display', 12),
                   background=ios_medium_bg,
                   fieldbackground=ios_medium_bg,
                   foreground=ios_light_text,
                   arrowcolor=ios_light_text)
    
    # Parameter label style
    style.configure("Param.TLabel",
                   font=('SF Pro Display', 11),
                   background=ios_dark_bg,
                   foreground=ios_accent_gray)  # Lighter text for labels
    
    # Rounded frame styles
    style.configure("Rounded.TFrame", background=ios_result_bg)
    style.configure("RoundedOrange.TFrame", background=ios_accent_orange)
    
    return ios_dark_bg  # Return background color for root window

# Multipliers for CFU/mL estimation
strain_multipliers = {
    "XL1-Blue": 8.0e8,
    "TG1": 8.5e8,
    "Lemo21": 6.5e8
}

class PhageCalculator:
    def __init__(self, root):
        self.root = root
        # Store the background color as an instance variable
        self.bg_color = setup_theme()
        self.root.title("Helper Phage Calculator")
        self.root.geometry("860x550")  # Fixed window size
        self.root.minsize(860, 550)    # Fixed minimum size
        self.root.configure(bg=self.bg_color)
        
        # Create main frames with proper padding
        self.main_frame = ttk.Frame(root, padding=15)
        self.main_frame.pack(fill="both", expand=True)
        
        # iOS style title
        self.title_label = ttk.Label(self.main_frame, text="Helper Phage Calculator", style="Title.TLabel")
        self.title_label.pack(pady=(0, 5))

        # Add explanation text with iOS styling - shorter text
        info_text = "Calculate helper phage volume based on bacterial density"
        info_label = ttk.Label(self.main_frame, text=info_text, justify="center")
        info_label.pack(pady=(0, 15))
        
        # Create two-column layout with fixed widths
        self.input_frame = ttk.Frame(self.main_frame, padding=10, width=380)
        self.input_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=5)
        self.input_frame.pack_propagate(False)  # Prevent shrinking
        
        self.result_frame = ttk.Frame(self.main_frame, padding=10, width=380)
        self.result_frame.pack(side="right", fill="both", expand=True, padx=(10, 5), pady=5)
        self.result_frame.pack_propagate(False)  # Prevent shrinking
        
        # Create input fields with iOS style
        self.create_input_fields()
        
        # Create result display with iOS style
        self.create_result_display()
        
        # Initial calculation
        self.calculate()
    
    def create_input_fields(self):
        # Title for input section - iOS styled
        input_title = ttk.Label(self.input_frame, text="Parameters", style="Title.TLabel")
        input_title.pack(anchor="w", pady=(0, 10))
        
        # Create inputs with iOS style - fixed width
        input_container = ttk.Frame(self.input_frame)
        input_container.pack(fill="x", pady=5)
        
        # Strain selection - iOS style
        strain_frame = ttk.Frame(input_container)
        strain_frame.pack(fill="x", pady=8)
        
        ttk.Label(strain_frame, text="Bacterial Strain", style="Param.TLabel").pack(side="left")
        
        # Alternative approach - replace the combobox with a custom dropdown
        self.strain_var = tk.StringVar(value="XL1-Blue")

        # Create a canvas for rounded corners
        combo_canvas = tk.Canvas(strain_frame, highlightthickness=0, 
                              background=self.bg_color, bd=0, height=30, width=150)
        combo_canvas.pack(side="right")

        # Create rounded rectangle background (same as entry fields)
        w, h = 150, 30
        self.round_rectangle(combo_canvas, 2, 2, w-2, h-2, radius=8, 
                          fill="#2C2C2E", outline="")  # ios_medium_bg

        # Create an OptionMenu styled like iOS
        options = list(strain_multipliers.keys())
        dropdown = tk.OptionMenu(combo_canvas, self.strain_var, *options, 
                                 command=lambda _: self.calculate())
        dropdown.config(bg="#2C2C2E", fg="#FFFFFF", highlightthickness=0, bd=0,
                       activebackground="#3C3C3E", activeforeground="#FFFFFF",
                       font=('SF Pro Display', 12), width=12)
        combo_canvas.create_window(w//2, h//2, window=dropdown)

        # Rest of input fields with adjusted padding
        # OD600 - iOS style
        od_frame = ttk.Frame(input_container)
        od_frame.pack(fill="x", pady=8)
        
        ttk.Label(od_frame, text="OD600", style="Param.TLabel").pack(side="left")
        
        self.od_var = tk.StringVar(value="0.2")
        od_entry = ttk.Entry(od_frame, textvariable=self.od_var, width=15, style="TEntry")
        od_entry.pack(side="right")
        od_entry.bind("<KeyRelease>", lambda e: self.calculate())
        
        # Volume - iOS style
        vol_frame = ttk.Frame(input_container)
        vol_frame.pack(fill="x", pady=8)
        
        ttk.Label(vol_frame, text="Culture Volume (mL)", style="Param.TLabel").pack(side="left")
        
        self.volume_var = tk.StringVar(value="1.0")
        vol_entry = ttk.Entry(vol_frame, textvariable=self.volume_var, width=15, style="TEntry")
        vol_entry.pack(side="right")
        vol_entry.bind("<KeyRelease>", lambda e: self.calculate())
        
        # MOI - iOS style
        moi_frame = ttk.Frame(input_container)
        moi_frame.pack(fill="x", pady=8)
        
        ttk.Label(moi_frame, text="MOI", style="Param.TLabel").pack(side="left")
        
        self.moi_var = tk.StringVar(value="10")
        moi_entry = ttk.Entry(moi_frame, textvariable=self.moi_var, width=15, style="TEntry")
        moi_entry.pack(side="right")
        moi_entry.bind("<KeyRelease>", lambda e: self.calculate())
        
        # Stock concentration - iOS style
        stock_frame = ttk.Frame(input_container)
        stock_frame.pack(fill="x", pady=8)
        
        ttk.Label(stock_frame, text="Phage Stock (PFU/mL)", style="Param.TLabel").pack(side="left")
        
        self.stock_var = tk.StringVar(value="2e12")
        stock_entry = ttk.Entry(stock_frame, textvariable=self.stock_var, width=15, style="TEntry")
        stock_entry.pack(side="right")
        stock_entry.bind("<KeyRelease>", lambda e: self.calculate())
        
        # Calculate button with fixed dimensions - adjusted height to match result highlight box
        calc_container = tk.Frame(input_container, bg=self.bg_color)
        calc_container.pack(pady=15, fill="x")
        
        # Create canvas with fixed dimensions and center it - match height with highlight box (70px)
        calc_canvas = tk.Canvas(calc_container, highlightthickness=0, 
                             background=self.bg_color, bd=0, height=70, width=350)
        calc_canvas.pack(fill="x")
        
        # Create rounded rectangle for button - use predefined size
        # Don't rely on automatic sizing which can cause layout issues
        w, h = 350, 70  # Fixed size - match height with highlight box (70px)
        self.round_rectangle(calc_canvas, 2, 2, w-2, h-2, radius=15, 
                      fill="#E67700", outline="")
        
        # Create button text directly on canvas instead of using a label
        # This eliminates any frame or border issues
        calc_canvas.create_text(w//2, h//2, 
                           text="Calculate", 
                           fill="#1C1C1E",  # Dark text for contrast
                           font=('SF Pro Display', 14, 'bold'))

        # Bind click event to canvas
        def on_click(event):
            self.calculate()
            # Visual feedback
            calc_canvas.itemconfig(1, fill="#D26500")
            calc_canvas.after(100, lambda: calc_canvas.itemconfig(1, fill="#E67700"))

        calc_canvas.bind("<Button-1>", on_click)
    
    def create_result_display(self):
        # Title for results section
        result_title = ttk.Label(self.result_frame, text="Results", style="Title.TLabel")
        result_title.pack(anchor="w", pady=(0, 10))
        
        # Calculate the available height for the results area
        # We need to leave space for the title (approx 30px) and highlight box (70px + padding)
        available_height = 380  # Total height of result frame minus padding
        results_height = available_height - 30 - 70 - 30  # Title, highlight, padding
        
        # Create a canvas for the results box with proper dimensions
        result_canvas = tk.Canvas(self.result_frame, highlightthickness=0, 
                              background=self.bg_color, bd=0, height=results_height)
        result_canvas.pack(fill="both", expand=False, padx=5, pady=5)
        
        # Draw rounded rectangle with darker background - fixed size
        w, h = 370, results_height  # Properly sized to fit
        self.round_rectangle(result_canvas, 2, 2, w-2, h-2, radius=15, fill="#333333", outline="")
        
        # Create text label inside the rounded rectangle
        self.result_label = ttk.Label(result_canvas, text="", justify="left", 
                                   style="Result.TLabel", wraplength=330)
        result_canvas.create_window(w//2, h//2, window=self.result_label)
        
        # Create a canvas for the highlighted result with proper positioning
        highlight_canvas = tk.Canvas(self.result_frame, highlightthickness=0, 
                                  background=self.bg_color, bd=0, height=70)
        highlight_canvas.pack(fill="x", padx=5, pady=(5, 15))  # Reduced top padding
        
        # Draw rounded rectangle with orange accent
        w, h = 370, 70  # Use fixed size for highlight box - match with calculate button
        self.round_rectangle(highlight_canvas, 2, 2, w-2, h-2, radius=15, fill="#FF9500", outline="")
        
        # Create text label inside the rounded rectangle
        self.highlight_label = ttk.Label(highlight_canvas, 
                                      text="Add 0.0 µL of helper phage", 
                                      style="Highlight.TLabel",
                                      background="#FF9500",
                                      justify="center")
        highlight_canvas.create_window(w//2, h//2, window=self.highlight_label)
    
    # Your existing format_scientific, get_superscript, and calculate methods remain the same
    def format_scientific(self, number):
        """Format scientific notation as 10ⁿ with superscript"""
        # Convert to scientific notation string
        sci_str = f"{number:.2e}"
        
        # Match the mantissa and exponent parts
        match = re.match(r"(\d+\.\d+)e([+-])(\d+)", sci_str)
        if match:
            mantissa, sign, exponent = match.groups()
            # Convert to float and round to 2 decimal places
            mantissa_float = float(mantissa)
            # Handle exponent sign
            if sign == "-":
                exponent = "-" + exponent
            # Remove leading zeros from exponent
            exponent = str(int(exponent))
            # Format as coefficient × 10^exponent
            return f"{mantissa_float:.2f} × 10{self.get_superscript(exponent)}"
        return sci_str
    
    def get_superscript(self, text):
        """Convert text to Unicode superscript"""
        normal = "0123456789-+"
        superscript = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺"
        translation = str.maketrans(normal, superscript)
        return text.translate(translation)
    
    def calculate(self):
        try:
            # Calculations
            stock_conc = float(self.stock_var.get())
            moi = float(self.moi_var.get())
            volume_ml = float(self.volume_var.get())
            od600 = float(self.od_var.get())
            strain = self.strain_var.get()
            
            # Calculate CFU/mL
            cfu_ml = od600 * strain_multipliers[strain]
            
            # Total cells in culture
            total_cells = cfu_ml * volume_ml
            
            # Required phage
            required_phage = total_cells * moi
            
            # Phage volume in µL
            phage_vol_ul = (required_phage / stock_conc) * 1000
            
            # Update results with better scientific notation - iOS style
            result = f"CFU/mL for {strain} at OD600 = {od600}\n"
            result += f"CFU/mL: {self.format_scientific(cfu_ml)}\n"
            result += f"Total Cells: {self.format_scientific(total_cells)}\n\n"
            result += f"Helper Phage Required:\n"
            result += f"{self.format_scientific(required_phage)} PFU\n"
            
            self.result_label.config(text=result)
            
            highlight_text = f"Add {round(phage_vol_ul, 2)} µL of helper phage"
            self.highlight_label.config(text=highlight_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def round_rectangle(self, canvas, x1, y1, x2, y2, radius=20, **kwargs):
        points = [x1+radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhageCalculator(root)
    root.mainloop()