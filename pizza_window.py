import tkinter as tk
import json
import os
import math
import webbrowser
import subprocess
import sys
from tkinter import Canvas
from PIL import Image, ImageTk, ImageDraw, ImageFont
import hashlib
from icon_generator import IconGenerator

class PizzaWindow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.window = None
        self.canvas = None
        self.shortcuts = []
        self.add_special_shortcut()
        self.pizza_radius = 180 # Aumentado de 120 para 180
        
        self.center_x = self.pizza_radius + 10
        self.center_y = self.pizza_radius + 10
        self.window_size = (self.pizza_radius * 2 + 20, self.pizza_radius * 2 + 20)
        self.hovered_slice = -1
        self.slices = []
        self.last_shortcuts_count = 0
        self.icon_cache = {}  # Cache de imagens
        self.icon_cache_dir = os.path.join(os.path.dirname(__file__), "icon_cache")
        os.makedirs(self.icon_cache_dir, exist_ok=True)
        self.icon_generator = IconGenerator(self.icon_cache_dir)

        # Cor para o fundo das fatias (quando não estão em hover)
        self.bg_color = "#000000"
        self.hover_color = "#808080"
        self.text_color = "#FFFFFF" # Cor do texto e das bordas internas

        # Nova cor para o fundo transparente da janela/canvas
        self.transparent_key_color = "#123456" # Uma cor única que não será usada em outro lugar

        self.load_shortcuts()
        self.create_window()

    def load_shortcuts(self):
        shortcuts_file = os.path.join(os.path.dirname(__file__), "atalhos.json")
        if os.path.exists(shortcuts_file):
            try:
                with open(shortcuts_file, "r", encoding="utf-8") as f:
                    new_shortcuts = json.load(f)
                    if new_shortcuts != self.shortcuts:
                        self.shortcuts = new_shortcuts
                        self.last_shortcuts_count = len(self.shortcuts)
                        return True
            except (json.JSONDecodeError, IOError) as e:
                print(f"Erro ao carregar atalhos: {e}")
                self.shortcuts = []
        else:
            self.shortcuts = []
        return False

    def create_window(self):
        self.window = tk.Toplevel()
        # Adiciona esta linha para ocultar a janela imediatamente após a criação
        self.window.withdraw() 

        self.window.title("Pizza")
        # Ajusta a posição da janela para centralizar a pizza no clique do mouse
        self.window.geometry(f"{self.window_size[0]}x{self.window_size[1]}+{self.x-self.pizza_radius-10}+{self.y-self.pizza_radius-10}")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        
        # Define a cor de fundo da janela para a cor transparente
        self.window.configure(bg=self.transparent_key_color)
        # Define a cor que será transparente na janela
        self.window.attributes("-transparentcolor", self.transparent_key_color)

        # Define a cor de fundo do canvas para a cor transparente
        self.canvas = Canvas(self.window, width=self.window_size[0], height=self.window_size[1], bg=self.transparent_key_color, highlightthickness=0)
        self.canvas.pack()

        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Leave>", self.on_mouse_leave)
        self.window.bind("<FocusOut>", self.on_focus_out)

        self.draw_pizza()

    def draw_pizza(self):
        self.canvas.delete("all")
        self.slices = []
        self.load_shortcuts()

        if not self.shortcuts:
            self.draw_no_shortcuts()
        elif len(self.shortcuts) == 1:
            self.draw_single_shortcut()
        else:
            self.draw_multiple_shortcuts()
        
        # Desenha as linhas radiais entre as fatias (se houver mais de uma)
        if len(self.shortcuts) > 1:
            num_shortcuts = len(self.shortcuts)
            angle_per_slice = 360.0 / num_shortcuts
            for i in range(num_shortcuts):
                # Calcula o ângulo de início de cada fatia
                current_angle = i * angle_per_slice
                # Converte para radianos e ajusta para o sistema de coordenadas do Tkinter
                rad = math.radians(current_angle - 90) 
                x_end = self.center_x + self.pizza_radius * math.cos(rad)
                y_end = self.center_y + self.pizza_radius * math.sin(rad)
                # Linha branca de 1px (o mais fino possível)
                self.canvas.create_line(self.center_x, self.center_y, x_end, y_end, 
                                        fill=self.text_color, width=1) 

    def draw_no_shortcuts(self):
        self.canvas.create_oval(
            self.center_x - self.pizza_radius,
            self.center_y - self.pizza_radius,
            self.center_x + self.pizza_radius,
            self.center_y + self.pizza_radius,
            fill=self.bg_color, 
            outline="",
            width=0
        )
        self.canvas.create_text(self.center_x, self.center_y, text="Nenhum atalho", fill=self.text_color, font=("Arial", 12, "bold"), justify=tk.CENTER)

    def draw_single_shortcut(self):
        shortcut = self.shortcuts[0]
        color = self.hover_color if self.hovered_slice == 0 else self.bg_color
        self.canvas.create_oval(
            self.center_x - self.pizza_radius,
            self.center_y - self.pizza_radius,
            self.center_x + self.pizza_radius,
            self.center_y + self.pizza_radius,
            fill=color,
            outline="", 
            width=0,
            tags="slice_0"
        )

        icon_path = self.get_shortcut_image_path(shortcut)
        if icon_path and os.path.exists(icon_path):
            try:
                if icon_path not in self.icon_cache:
                    img = Image.open(icon_path).resize((40, 40), Image.LANCZOS)
                    self.icon_cache[icon_path] = ImageTk.PhotoImage(img)
                photo_image = self.icon_cache[icon_path]
                self.canvas.create_image(self.center_x, self.center_y - 20, image=photo_image, tags="slice_0")
            except Exception as e:
                print(f"Erro ao carregar imagem do ícone {icon_path}: {e}")
                emoji = self.icon_generator.get_shortcut_emoji(self.icon_generator.determine_shortcut_type(shortcut["caminho"]))
                self.canvas.create_text(self.center_x, self.center_y - 20, text=emoji, fill=self.text_color, font=("Arial", 24), tags="slice_0")
        else:
            emoji = self.icon_generator.get_shortcut_emoji(self.icon_generator.determine_shortcut_type(shortcut["caminho"]))
            self.canvas.create_text(self.center_x, self.center_y - 20, text=emoji, fill=self.text_color, font=("Arial", 24), tags="slice_0")

        name = self.truncate_text(shortcut["nome"], 15)
        self.canvas.create_text(self.center_x, self.center_y + 15, text=name, fill=self.text_color, font=("Arial", 10, "bold"), tags="slice_0")
        self.slices.append({"shortcut": shortcut, "start_angle": 0, "end_angle": 360, "center_x": self.center_x, "center_y": self.center_y})

    def draw_multiple_shortcuts(self):
        num_shortcuts = len(self.shortcuts)
        angle_per_slice = 360.0 / num_shortcuts

        for i, shortcut in enumerate(self.shortcuts):
            start_angle = i * angle_per_slice
            end_angle = (i + 1) * angle_per_slice
            color = self.hover_color if self.hovered_slice == i else self.bg_color
            slice_coords = self.get_slice_coordinates_optimized(start_angle, end_angle)

            try:
                # As fatias não terão borda individual (outline="", width=0)
                self.canvas.create_polygon(slice_coords, fill=color, outline="", width=0, tags=f"slice_{i}")
            except tk.TclError as e:
                print(f"Erro ao criar fatia {i}: {e}")
                continue

            mid_angle = math.radians(start_angle + angle_per_slice / 2 - 90)
            # Ajusta o raio do texto para a nova pizza maior
            text_radius = self.pizza_radius * 0.6 
            text_x = self.center_x + text_radius * math.cos(mid_angle)
            text_y = self.center_y + text_radius * math.sin(mid_angle)

            icon_path = self.get_shortcut_image_path(shortcut)
            if icon_path and os.path.exists(icon_path):
                try:
                    if icon_path not in self.icon_cache:
                        img = Image.open(icon_path).resize((32, 32), Image.LANCZOS)
                        self.icon_cache[icon_path] = ImageTk.PhotoImage(img)
                    photo_image = self.icon_cache[icon_path]
                    self.canvas.create_image(text_x, text_y - 10, image=photo_image, tags=f"slice_{i}")
                except Exception as e:
                    print(f"Erro ao carregar imagem do ícone {icon_path}: {e}")
                    emoji = self.icon_generator.get_shortcut_emoji(self.icon_generator.determine_shortcut_type(shortcut["caminho"]))
                    self.canvas.create_text(text_x, text_y - 10, text=emoji, fill=self.text_color, font=("Arial", max(12, 20 - num_shortcuts)), tags=f"slice_{i}")
            else:
                emoji = self.icon_generator.get_shortcut_emoji(self.icon_generator.determine_shortcut_type(shortcut["caminho"]))
                self.canvas.create_text(text_x, text_y - 10, text=emoji, fill=self.text_color, font=("Arial", max(12, 20 - num_shortcuts)), tags=f"slice_{i}")

            max_chars = max(4, 12 - num_shortcuts)
            name = self.truncate_text(shortcut["nome"], max_chars)
            try:
                self.canvas.create_text(text_x, text_y + 8, text=name, fill=self.text_color, font=("Arial", max(6, 10 - num_shortcuts // 2), "bold"), tags=f"slice_{i}")
            except tk.TclError as e:
                print(f"Erro ao criar texto do nome da fatia {i}: {e}")
                continue

            self.slices.append({"shortcut": shortcut, "start_angle": start_angle, "end_angle": end_angle, "center_x": text_x, "center_y": text_y})

    def get_slice_coordinates_optimized(self, start_angle, end_angle):
        coords = [self.center_x, self.center_y]
        angle_diff = end_angle - start_angle
        step = max(2, min(10, angle_diff / 10))
        angle = start_angle
        while angle <= end_angle:
            rad = math.radians(angle - 90)
            x = self.center_x + self.pizza_radius * math.cos(rad)
            y = self.center_y + self.pizza_radius * math.sin(rad)
            coords.extend([x, y])
            angle += step
        if angle - step < end_angle:
            rad = math.radians(end_angle - 90)
            x = self.center_x + self.pizza_radius * math.cos(rad)
            y = self.center_y + self.pizza_radius * math.sin(rad)
            coords.extend([x, y])
        return coords

    def get_shortcut_image_path(self, shortcut):
        icon_path = shortcut.get("icone")
        if icon_path and os.path.exists(icon_path):
            return icon_path
        else:
            shortcut_type = self.icon_generator.determine_shortcut_type(shortcut["caminho"])
            if shortcut_type == "image":
                return shortcut["caminho"]
            else:
                return self.icon_generator.generate_generic_icon(shortcut_type)

    def truncate_text(self, text, max_length):
        return text if len(text) <= max_length else text[:max_length-3] + "..."

    def on_mouse_move(self, event):
        try:
            mouse_x = event.x
            mouse_y = event.y
            distance = math.sqrt((mouse_x - self.center_x)**2 + (mouse_y - self.center_y)**2)
            new_hovered = -1
            if distance <= self.pizza_radius and self.shortcuts:
                if len(self.shortcuts) == 1:
                    new_hovered = 0
                elif len(self.shortcuts) > 1:
                    angle = math.degrees(math.atan2(mouse_y - self.center_y, mouse_x - self.center_x))
                    angle = (angle + 90) % 360
                    angle_per_slice = 360.0 / len(self.shortcuts)
                    slice_index = int(angle / angle_per_slice)
                    if 0 <= slice_index < len(self.shortcuts):
                        new_hovered = slice_index
            if new_hovered != self.hovered_slice:
                self.hovered_slice = new_hovered
                self.draw_pizza()
        except Exception as e:
            print(f"Erro no mouse move: {e}")

    def on_click(self, event):
        try:
            if 0 <= self.hovered_slice < len(self.shortcuts):
                shortcut = self.shortcuts[self.hovered_slice]
                self.execute_shortcut(shortcut)
                self.close()
        except Exception as e:
            print(f"Erro no clique: {e}")

    def on_mouse_leave(self, event):
        self.close()

    def on_focus_out(self, event):
        self.close()

    def execute_shortcut(self, shortcut):
        try:
            path = shortcut["caminho"]
            if path == "__OPEN_ATALHO_PIZZA__":
                self.open_atalho_pizza()
            elif path.startswith("http://" ) or path.startswith("https://" ):
                webbrowser.open(path)
            elif os.path.exists(path):
                if sys.platform == "win32":
                    os.startfile(path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", path])
                else:
                    subprocess.run(["xdg-open", path])
            else:
                subprocess.run(path, shell=True)
        except Exception as e:
            print(f"Erro ao executar atalho '{shortcut.get('nome', 'Desconhecido')}': {e}")

    def show(self):
        if self.window:
            self.window.deiconify()
            self.window.focus_force()

    def close(self):
        try:
            if self.window:
                self.window.destroy()
        except Exception as e:
            print(f"Erro ao fechar janela: {e}")

    def winfo_exists(self):
        try:
            return self.window and self.window.winfo_exists()
        except tk.TclError:
            return False

    def open_atalho_pizza(self):
        try:
            # Determina o caminho do executável Python
            python_executable = sys.executable
            # Determina o caminho do script atalho_pizza.py
            script_path = os.path.join(os.path.dirname(__file__), "atalho_pizza.py")
            
            # Abre o atalho_pizza.py em um novo processo, sem bloquear a pizza_window
            subprocess.Popen([python_executable, script_path])
        except Exception as e:
            print(f"Erro ao abrir Atalho_pizza: {e}")




    def add_special_shortcut(self):
        # Adiciona um atalho especial para abrir o Atalho_pizza
        special_shortcut = {
            "nome": "Gerenciar Atalhos",
            "caminho": "__OPEN_ATALHO_PIZZA__", # Um identificador único
            "icone": ""
        }
        self.shortcuts.insert(0, special_shortcut) # Adiciona no início da lista


