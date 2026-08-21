"""
Desktop Calculator App (Python + tkinter)
Run with: python calculator_gui.py
tkinter is built into Python, so no extra installs are needed.
"""

import tkinter as tk

# ---- Colors ----
BG_COLOR = "#1e1e1e"
DISPLAY_BG = "#2d2d2d"
DISPLAY_FG = "#ffffff"
NUM_BTN_BG = "#3a3a3a"
NUM_BTN_FG = "#ffffff"
OP_BTN_BG = "#ff9500"
OP_BTN_FG = "#ffffff"
FUNC_BTN_BG = "#5a5a5a"
FUNC_BTN_FG = "#ffffff"


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Holds the full expression as a string, e.g. "12+7"
        self.expression = ""

        self.build_display()
        self.build_buttons()
        self.bind_keyboard()

    def build_display(self):
        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            font=("Segoe UI", 28),
            bg=DISPLAY_BG,
            fg=DISPLAY_FG,
            bd=0,
            justify="right",
            state="readonly",
            readonlybackground=DISPLAY_BG,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=(15, 10), ipady=20)

    def build_buttons(self):
        # (label, row, col, colspan, bg, fg)
        buttons = [
            ("C", 1, 0, 1, FUNC_BTN_BG, FUNC_BTN_FG),
            ("⌫", 1, 1, 1, FUNC_BTN_BG, FUNC_BTN_FG),
            ("%", 1, 2, 1, FUNC_BTN_BG, FUNC_BTN_FG),
            ("/", 1, 3, 1, OP_BTN_BG, OP_BTN_FG),

            ("7", 2, 0, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("8", 2, 1, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("9", 2, 2, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("*", 2, 3, 1, OP_BTN_BG, OP_BTN_FG),

            ("4", 3, 0, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("5", 3, 1, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("6", 3, 2, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("-", 3, 3, 1, OP_BTN_BG, OP_BTN_FG),

            ("1", 4, 0, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("2", 4, 1, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("3", 4, 2, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("+", 4, 3, 1, OP_BTN_BG, OP_BTN_FG),

            ("0", 5, 0, 2, NUM_BTN_BG, NUM_BTN_FG),
            (".", 5, 2, 1, NUM_BTN_BG, NUM_BTN_FG),
            ("=", 5, 3, 1, OP_BTN_BG, OP_BTN_FG),
        ]

        for (label, row, col, colspan, bg, fg) in buttons:
            btn = tk.Button(
                self.root,
                text=label,
                font=("Segoe UI", 18),
                bg=bg,
                fg=fg,
                bd=0,
                activebackground="#666666",
                activeforeground="#ffffff",
                command=lambda l=label: self.on_button_click(l),
            )
            btn.grid(
                row=row, column=col, columnspan=colspan,
                sticky="nsew", padx=4, pady=4, ipady=15,
            )

        # Make rows/columns stretch evenly so the window looks balanced
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def bind_keyboard(self):
        # Lets the user type on their keyboard too, not just click buttons
        self.root.bind("<Key>", self.on_key_press)

    # ---- Logic ----

    def on_button_click(self, label):
        if label == "C":
            self.clear()
        elif label == "⌫":
            self.backspace()
        elif label == "=":
            self.calculate()
        elif label == "%":
            self.expression += "/100"
            self.update_display(self.expression)
        else:
            self.expression += label
            self.update_display(self.expression)

    def on_key_press(self, event):
        char = event.char
        if char in "0123456789+-*/.":
            self.expression += char
            self.update_display(self.expression)
        elif event.keysym == "Return":
            self.calculate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear()

    def clear(self):
        self.expression = ""
        self.update_display("0")

    def backspace(self):
        self.expression = self.expression[:-1]
        self.update_display(self.expression if self.expression else "0")

    def calculate(self):
        try:
            # eval() is safe here because on_button_click and on_key_press
            # only ever add digits, ".", and + - * / to self.expression
            result = eval(self.expression)
            self.expression = str(result)
            self.update_display(self.expression)
        except (SyntaxError, ZeroDivisionError):
            self.update_display("Error")
            self.expression = ""

    def update_display(self, text):
        self.display_var.set(text)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
