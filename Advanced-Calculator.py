import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")

        self.entry = ttk.Entry(root, width=40)
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('Plot', 5, 2, 2)
        ]

        for button in buttons:
            text = button[0]
            row = button[1]
            col = button[2]
            cs = button[3] if len(button) == 4 else 1
            
            ttk.Button(root, text=text, command=lambda t=text: self.on_button_click(t)).grid(row=row, column=col, columnspan=cs, padx=5, pady=5)

    def on_button_click(self, char):
        if char == '=':
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            
            except:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
       
        elif char.lower() == 'plot':
            self.plot_function()
        else:
            self.entry.insert(tk.END, char)

    def parse_expression(self, expression):
        try:
            func, params = expression.split('(')
            params = params.strip(')').split(',')
            if func in ['sin', 'cos', 'tan']:
                return f'np.{func}(np.linspace({params[0]}, {params[1]}, {params[2]}))'
        
        except:
            return expression

    def plot_function(self):
        try:
            expression = self.entry.get()
            parsed_expression = self.parse_expression(expression)
            x = np.linspace(-10, 10, 400)
            y = eval(parsed_expression)
            self.plot(x, y, expression)
        
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Invalid Expression")

    def plot(self, x, y, expression):
        plt.figure()
        plt.plot(x, y)
        plt.title(f'Graph of {expression}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.axhline(0, color='black', lw=0.5)
        plt.axvline(0, color='black', lw=0.5)
        plt.show()


def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
