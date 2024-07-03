import tkinter as tk
from tkinter import ttk
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plotting and Arithmetic Calculator")
        self.create_widgets()

    def create_widgets(self) -> None:  # Creates general UI
        self.entry = ttk.Entry(self.root, width=40)
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('Plot', 5, 2, 2)
        ]

        for text, row, col, *cs in buttons:
            cs = cs[0] if cs else 1
            self.create_button(text, row, col, cs)

    def create_button(self, text: str, row: int, col: int, colspan: int = 1) -> None:
        ttk.Button(self.root, text=text, command=lambda t=text: self.on_button_click(t)).grid(
            row=row, column=col, columnspan=colspan, padx=5, pady=5
        )

    def on_button_click(self, char: str) -> None:
        if char == '=':
            self.evaluate_expression()
        
        elif char.lower() == 'plot':
            self.plot_function()
        
        else:
            self.entry.insert(tk.END, char)

    def evaluate_expression(self) -> None:
        try:
            result = eval(self.entry.get(), {}, {"np": np})
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")

    def parse_expression(self, expression: str) -> Tuple[str, float, float, int]:  # Parse graphing functions
        try:
            func_name, params = expression.split('(')
            params = params.rstrip(')').split(',')

            xmin, xmax, num_points = map(float, params)
            func_name = func_name.strip().lower()

            if func_name in ['sin', 'cos', 'tan']:
                return func_name, xmin, xmax, int(num_points)
        
        except Exception:
            pass
        
        raise ValueError('Invalid expression format')

    def plot_function(self) -> None:
        try:
            expression = self.entry.get()
            func_name, xmin, xmax, num_points = self.parse_expression(expression)
            
            x = np.linspace(xmin, xmax, num_points)
            y = getattr(np, func_name)(x)
            
            self.plot(x, y, f'{func_name}(x) from {xmin} to {xmax} with {num_points} points')
        
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Invalid Expression")

    def plot(self, x, y, title: str) -> None:  # Calculate plotting and adds additional text for info
        plt.figure()
        plt.plot(x, y)
        plt.title(f'Graph of {title}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)

        for axline in [plt.axvline, plt.axhline]:
            axline(0, color='black', lw=0.5)

        plt.show()

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
