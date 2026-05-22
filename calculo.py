import tkinter as tk
import threading
import pyttsx3


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Acessível")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        # Cores
        self.colors = {
            "bg": "#2c3e50",
            "visor": "#ecf0f1",
            "text": "#2c3e50",
            "num": "#34495e",
            "op": "#e67e22",
            "eq": "#27ae60",
            "c": "#c0392b"
        }

        self.root.config(bg=self.colors["bg"])

        # Expressão
        self.expression = ""

        # Display
        self.display_var = tk.StringVar(value="0")

        # Inicializar voz
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)

        # Criar interface
        self.create_widgets()

        # Suporte ao teclado
        self.root.bind("<Key>", self.key_press)

    # =========================
    # Interface
    # =========================
    def create_widgets(self):

        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title_label = tk.Label(
            main_frame,
            text="Calculadora Acessível",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=self.colors["bg"]
        )
        title_label.pack(pady=(0, 15))

        # Visor
        display_frame = tk.Frame(
            main_frame,
            bg=self.colors["visor"],
            relief=tk.SUNKEN,
            bd=2
        )
        display_frame.pack(fill=tk.X, padx=5, pady=(0, 20))

        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Courier", 28, "bold"),
            fg=self.colors["text"],
            bg=self.colors["visor"],
            anchor="e",
            padx=10,
            pady=10
        )
        self.display_label.pack(fill=tk.BOTH, expand=True)

        # Botões
        buttons_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        buttons_frame.pack(fill=tk.BOTH, expand=True)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', 'C', '+']
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, btn in enumerate(row):
                self.create_button(
                    buttons_frame,
                    btn,
                    row_idx,
                    col_idx
                )

        # Botão "="
        equal_btn = tk.Button(
            buttons_frame,
            text="=",
            font=("Arial", 20, "bold"),
            fg="white",
            bg=self.colors["eq"],
            activebackground="#1e8449",
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=self.calculate
        )

        equal_btn.grid(
            row=4,
            column=0,
            columnspan=4,
            sticky="nsew",
            padx=3,
            pady=5
        )

        # Responsividade
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)

        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)

        # Rodapé
        footer = tk.Label(
            main_frame,
            text="Pressione Enter para calcular.",
            font=("Arial", 8),
            fg="#95a5a6",
            bg=self.colors["bg"]
        )

        footer.pack(pady=(15, 0))

    # =========================
    # Criar botão
    # =========================
    def create_button(self, parent, btn, row, col):

        if btn in ['/', '*', '-', '+']:
            bg_color = self.colors["op"]

        elif btn == 'C':
            bg_color = self.colors["c"]

        else:
            bg_color = self.colors["num"]

        button = tk.Button(
            parent,
            font=("Arial", 18, "bold"),
            fg="white",
            bg=bg_color,
            activebackground=self.lighten_color(bg_color),
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=lambda value=btn: self.button_action(value)
        )

        # Símbolos visuais
        if btn == '*':
            button.config(text='×')

        elif btn == '/':
            button.config(text='÷')

        else:
            button.config(text=btn)

        button.grid(
            row=row,
            column=col,
            sticky="nsew",
            padx=3,
            pady=5
        )

    # =========================
    # Clique do botão
    # =========================
    def button_action(self, value):

        if value == "C":
            self.clear()
            return

        self.handle_click(value)

    # =========================
    # Clarear cor
    # =========================
    def lighten_color(self, color):

        color = color.lstrip('#')

        rgb = tuple(
            int(color[i:i+2], 16)
            for i in (0, 2, 4)
        )

        return (
            f"#{min(int(rgb[0] * 1.2), 255):02x}"
            f"{min(int(rgb[1] * 1.2), 255):02x}"
            f"{min(int(rgb[2] * 1.2), 255):02x}"
        )

    # =========================
    # Voz
    # =========================
    def speak(self, text):

        threading.Thread(
            target=self._speak_thread,
            args=(text,),
            daemon=True
        ).start()

    def _speak_thread(self, text):

        try:
            self.engine.say(text)
            self.engine.runAndWait()

        except Exception as e:
            print("Erro no áudio:", e)

    # =========================
    # Entrada
    # =========================
    def handle_click(self, value):

        operators = "+-*/"

        # Impedir operadores duplicados
        if value in operators:

            if (
                self.expression == "" or
                self.expression[-1] in operators
            ):
                return

        # Impedir múltiplos pontos no mesmo número
        if value == ".":

            current_number = ""

            for char in reversed(self.expression):

                if char in operators:
                    break

                current_number += char

            if "." in current_number:
                return

        # Evitar múltiplos zeros iniciais
        if self.expression == "0" and value == "0":
            return

        # Permitir substituir 0 inicial
        if self.expression == "0" and value not in [".", "+", "-", "*", "/"]:
            self.expression = value

        else:
            self.expression += value

        self.display_var.set(self.expression)

    # =========================
    # Limpar
    # =========================
    def clear(self):

        self.expression = ""
        self.display_var.set("0")

    # =========================
    # Calcular
    # =========================
    def calculate(self):

        try:

            if not self.expression:
                return

            # Segurança
            allowed = "0123456789+-*/."

            if not all(char in allowed for char in self.expression):
                raise ValueError("Expressão inválida")

            result = eval(self.expression)

            # Remover .0 desnecessário
            if result == int(result):
                result = int(result)

            result_str = str(result)

            self.display_var.set(result_str)
            self.expression = result_str

            self.speak(f"O resultado é {result_str}")

        except ZeroDivisionError:

            self.display_var.set("Erro: divisão por zero")
            self.expression = ""

            self.speak("Erro de divisão por zero")

        except Exception:

            self.display_var.set("Erro")
            self.expression = ""

            self.speak("Erro na expressão")

    # =========================
    # Teclado
    # =========================
    def key_press(self, event):

        key = event.char

        if key in "0123456789+-*/.":
            self.handle_click(key)

        elif event.keysym == "Return":
            self.calculate()

        elif key.lower() == "c":
            self.clear()

        elif event.keysym == "BackSpace":

            self.expression = self.expression[:-1]

            if self.expression:
                self.display_var.set(self.expression)

            else:
                self.display_var.set("0")


# =========================
# Executar
# =========================
if __name__ == "__main__":

    root = tk.Tk()

    app = Calculator(root)

    root.mainloop()