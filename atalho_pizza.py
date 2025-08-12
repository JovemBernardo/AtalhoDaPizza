import customtkinter as ctk
import json
import os
import tkinter.filedialog as filedialog
from PIL import Image, ImageDraw, ImageFont
import webbrowser
import subprocess
import hashlib
import sys

class AtalhoDaPizza(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Atalho da Pizza")
        self.geometry("1000x700")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")  # Forçando o modo escuro para corresponder às imagens
        ctk.set_default_color_theme("blue")  # Manter o tema azul para elementos padrão, mas sobrescreveremos as cores

        # Configurar o layout da grade (grid) para a janela principal
        self.grid_rowconfigure(0, weight=0)  # Cabeçalho
        self.grid_rowconfigure(1, weight=1)  # Conteúdo principal (cards)
        self.grid_columnconfigure(0, weight=1)

        self.shortcuts_file = os.path.join(os.path.dirname(__file__), "atalhos.json")
        self.icon_cache_dir = os.path.join(os.path.dirname(__file__), "icon_cache")
        os.makedirs(self.icon_cache_dir, exist_ok=True)
        self.icon_cache = {}

        self.shortcuts = self.read_shortcuts()

        self.create_widgets()
        self.display_shortcuts()

        # Definir a cor de fundo da janela principal
        self.configure(fg_color="#1F1E2E") # Cor de fundo principal

    def read_shortcuts(self):
        if os.path.exists(self.shortcuts_file):
            with open(self.shortcuts_file, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print(f"Erro ao decodificar JSON em {self.shortcuts_file}. Retornando lista vazia.")
                    return []
        return []

    def save_shortcuts(self):
        try:
            with open(self.shortcuts_file, "w", encoding="utf-8") as f:
                json.dump(self.shortcuts, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Erro ao salvar atalhos em {self.shortcuts_file}: {e}")

    def create_widgets(self):
        # Cabeçalho
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1F1E2E") # Cor de fundo do cabeçalho
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(0, weight=0) # Icon
        header_frame.grid_columnconfigure(1, weight=1) # Title
        header_frame.grid_columnconfigure(2, weight=0) # Search
        header_frame.grid_columnconfigure(3, weight=0) # Add button

        # Ícone da pizza
        pizza_image_path = os.path.join(os.path.dirname(__file__), "assets", "pizza.png")
        try:
            pizza_img = Image.open(pizza_image_path).resize((40, 40)) # Aumentado o tamanho do ícone
            pizza_photo = ctk.CTkImage(light_image=pizza_img, dark_image=pizza_img, size=(40, 40))
            pizza_icon_label = ctk.CTkLabel(header_frame, image=pizza_photo, text="")
            pizza_icon_label.image = pizza_photo # Keep a reference
            pizza_icon_label.grid(row=0, column=0, padx=20, pady=25) # Aumentado pady para aumentar altura do cabeçalho
        except Exception as e:
            print(f"Erro ao carregar ícone da pizza: {e}")
            pizza_icon_label = ctk.CTkLabel(header_frame, text="🍕", font=ctk.CTkFont(size=40), text_color="white") # Aumentado font size
            pizza_icon_label.grid(row=0, column=0, padx=20, pady=25) # Aumentado pady

        # Título
        title_label = ctk.CTkLabel(header_frame, text="Atalho da Pizza", font=ctk.CTkFont(size=28, weight="bold"), text_color="white") # Aumentado font size
        title_label.grid(row=0, column=1, sticky="w", pady=25) # Aumentado pady

        # Campo de pesquisa (adicionado para corresponder à imagem)
        search_entry = ctk.CTkEntry(header_frame, placeholder_text="Pesquisar atalhos...", width=250, height=35, text_color="white", placeholder_text_color="gray", fg_color="#2B2A3A", border_color="#2b2b2b") # Aumentado width e height
        search_entry.grid(row=0, column=2, padx=10, pady=25, sticky="e") # Aumentado pady

        # Botão + Adicionar Item
        add_button = ctk.CTkButton(header_frame, text="Adicionar Item", command=self.open_add_shortcut_window, fg_color="#4CAF50", hover_color="#45a049", text_color="white", height=35) # Aumentado height
        add_button.grid(row=0, column=3, padx=20, pady=25) # Aumentado pady

        # Frame para os cards (conteúdo principal)
        self.cards_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="#1F1E2E") # Cor de fundo do frame de cards
        self.cards_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(5, 0))
        self.cards_frame.grid_columnconfigure(0, weight=1) # Coluna para os cards

    def display_shortcuts(self):
        # Limpa os cards existentes
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        # Exibe os atalhos como cards
        for i, shortcut in enumerate(self.shortcuts):
            # Card Frame - Minimalista, sem bordas, altura ajustada
            card_frame = ctk.CTkFrame(self.cards_frame, height=70, corner_radius=8, fg_color="#2D3E50") # Cor de fundo do card, corner_radius para bordas arredondadas
            card_frame.pack(fill="x", padx=10, pady=5) # Empilha os cards verticalmente
            card_frame.grid_propagate(False) # Impede que o frame se ajuste ao conteúdo

            # Configurar o grid interno do card
            card_frame.grid_columnconfigure(0, weight=0) # Coluna do ícone (tamanho fixo)
            card_frame.grid_columnconfigure(1, weight=1) # Coluna do nome e caminho (expansível)
            card_frame.grid_columnconfigure(2, weight=0) # Coluna dos botões (tamanho fixo)
            card_frame.grid_rowconfigure(0, weight=1) # Linha única para o conteúdo do card

            # Ícone do atalho (Coluna 0)
            icon_path = self.get_shortcut_icon(shortcut)
            if icon_path and os.path.exists(icon_path):
                try:
                    img = Image.open(icon_path).resize((40, 40)) # Tamanho menor para o ícone no card
                    photo = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
                    icon_label = ctk.CTkLabel(card_frame, image=photo, text="")
                    icon_label.image = photo # Keep a reference
                    icon_label.grid(row=0, column=0, padx=(15, 5), pady=5) # Ajuste de padding para centralizar visualmente
                except Exception as e:
                    print(f"Erro ao carregar ícone {icon_path}: {e}")
                    icon_label = ctk.CTkLabel(card_frame, text="❓", font=ctk.CTkFont(size=28), text_color="white") # Tamanho de fonte ajustado
                    icon_label.grid(row=0, column=0, padx=(15, 5), pady=5) # Ajuste de padding
            else:
                icon_label = ctk.CTkLabel(card_frame, text="❓", font=ctk.CTkFont(size=28), text_color="white") # Tamanho de fonte ajustado
                icon_label.grid(row=0, column=0, padx=(15, 5), pady=5) # Ajuste de padding

            # Frame para Nome e Caminho (Coluna 1)
            text_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            text_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            text_frame.grid_rowconfigure(0, weight=1)
            text_frame.grid_rowconfigure(1, weight=1)
            text_frame.grid_columnconfigure(0, weight=1)

            # Nome do atalho (Linha 0 da text_frame)
            name_label = ctk.CTkLabel(text_frame, text=shortcut["nome"], font=ctk.CTkFont(size=15, weight="bold"), text_color="white", anchor="w")
            name_label.grid(row=0, column=0, sticky="w", pady=(0, 0)) # Espaçamento mínimo

            # Caminho do atalho (Linha 1 da text_frame)
            path_display_label = ctk.CTkLabel(text_frame, text=shortcut["caminho"], font=ctk.CTkFont(size=11), text_color="gray", anchor="w")
            path_display_label.grid(row=1, column=0, sticky="w", pady=(0, 0)) # Espaçamento mínimo

            # Frame para Botões (Coluna 2)
            buttons_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            buttons_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 15), pady=5) # Ajuste de padding
            buttons_frame.grid_rowconfigure(0, weight=1)
            buttons_frame.grid_columnconfigure(0, weight=1)
            buttons_frame.grid_columnconfigure(1, weight=1)

            # Cor personalizada (padrão para os dois botões (Abrir e remover))
            botao_fg = "#1a73e8"
            botao_hover = "#1666cc"

            # Botão de execução
            execute_button = ctk.CTkButton(buttons_frame, text="Abrir", command=lambda s=shortcut: self.execute_shortcut(s), width=70, height=28, font=ctk.CTkFont(size=12), fg_color=botao_fg, hover_color=botao_hover)
            execute_button.grid(row=0, column=0, padx=5, sticky="e")

            # Botão de remover
            remove_button = ctk.CTkButton(buttons_frame, text="Remover", command=lambda s=shortcut: self.remove_shortcut(s), width=70, height=28, font=ctk.CTkFont(size=12), fg_color=botao_fg, hover_color=botao_hover)
            remove_button.grid(row=0, column=1, padx=5, sticky="e")

    def get_shortcut_icon(self, shortcut):
        # Primeiro, verifica se um caminho de ícone explícito foi fornecido e existe
        if shortcut.get("icone") and os.path.exists(shortcut["icone"]):
            return shortcut["icone"]
        else:
            # Determina o tipo do caminho principal do atalho
            shortcut_type = self.determine_shortcut_type(shortcut["caminho"])

            # Se o caminho do atalho for uma imagem, usa-o diretamente como ícone
            if shortcut_type == "image":
                return shortcut["caminho"]
            else:
                # Caso contrário, gera um ícone genérico com base no tipo determinado
                return self.generate_generic_icon(shortcut_type) # Passa apenas o tipo

    def determine_shortcut_type(self, path):
        image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico"] # Adicionadas extensões de imagem
        if path.startswith("http://" ) or path.startswith("https://" ):
            return "link"
        elif os.path.isfile(path):
            # Verifica se é um arquivo de imagem
            ext = os.path.splitext(path)[1].lower()
            if ext in image_extensions:
                return "image"
            return "file"
        elif os.path.isdir(path):
            return "folder"
        else:
            return "command" # Assumir que é um comando se não for link, arquivo, pasta ou imagem

    def generate_generic_icon(self, shortcut_type): # Removido 'name' do argumento
        # Criar um hash para o tipo para o cache (agora apenas baseado no tipo)
        icon_hash = hashlib.md5(shortcut_type.encode()).hexdigest()
        cached_icon_path = os.path.join(self.icon_cache_dir, f"{icon_hash}.png")

        if cached_icon_path in self.icon_cache:
            return self.icon_cache[cached_icon_path]
        elif os.path.exists(cached_icon_path):
            self.icon_cache[cached_icon_path] = cached_icon_path
            return cached_icon_path

        # Gerar o ícone
        img_size = (128, 128)
        img = Image.new("RGBA", img_size, (255, 255, 255, 0)) # Transparente
        draw = ImageDraw.Draw(img)

        # Definir texto e cor baseados no tipo
        text = ""
        fill_color = "blue"
        if shortcut_type == "link":
            text = "🌐"
            fill_color = "#3498db"
        elif shortcut_type == "file":
            text = "📄"
            fill_color = "#2ecc71"
        elif shortcut_type == "folder":
            text = "📁"
            fill_color = "#f1c40f"
        elif shortcut_type == "command":
            text = "💻"
            fill_color = "#9b59b6"
        elif shortcut_type == "image": # Adicionado tipo imagem para ícone genérico, embora ele use a própria imagem
            text = "🖼️"
            fill_color = "#e74c3c"
        else:
            text = "❓"
            fill_color = "#7f8c8d"

        # Tentar carregar fontes de emoji
        font_paths = []
        if sys.platform == "win32":
            font_paths.append("C:/Windows/Fonts/seguiemj.ttf") # Segoe UI Emoji
            font_paths.append("C:/Windows/Fonts/arial.ttf") # Arial (fallback)
        else: # Linux/macOS
            font_paths.append("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf") # Noto Color Emoji
            font_paths.append("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") # DejaVu Sans (fallback)
            font_paths.append("/System/Library/Fonts/Apple Color Emoji.ttc") # macOS

        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 80)
                break
            except IOError:
                continue
        
        if font is None: # Fallback para fonte padrão se nenhuma for encontrada
            font = ImageFont.load_default()
            # Se a fonte padrão não suportar emojis, desenhe um texto alternativo
            if text in ["🌐", "📄", "📁", "💻", "❓", "🖼️"]:
                if shortcut_type == "link": text = "WEB"
                elif shortcut_type == "file": text = "FILE"
                elif shortcut_type == "folder": text = "DIR"
                elif shortcut_type == "command": text = "CMD"
                elif shortcut_type == "image": text = "IMG"
                else: text = "?"
                font = ImageFont.truetype("arial.ttf", 40) if sys.platform == "win32" else ImageFont.truetype("DejaVuSans-Bold.ttf", 40) # Tentar uma fonte mais comum para texto

        # Desenhar o texto centralizado
        text_bbox = draw.textbbox((0,0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (img_size[0] - text_width) / 2
        text_y = (img_size[1] - text_height) / 2 - 10 # Ajuste fino
        draw.text((text_x, text_y), text, font=font, fill=fill_color)

        try:
            img.save(cached_icon_path)
            self.icon_cache[cached_icon_path] = cached_icon_path
            return cached_icon_path
        except Exception as e:
            print(f"Erro ao salvar ícone em cache {cached_icon_path}: {e}")
            return None

    def open_add_shortcut_window(self):
        add_window = ctk.CTkToplevel(self)
        add_window.title("Novo Atalho - Atalho da Pizza")
        add_window.geometry("600x550") # Ajustado novamente para acomodar a dica
        add_window.transient(self) # Faz a janela ser modal
        add_window.grab_set() # Bloqueia interação com a janela principal

        # Definir a cor de fundo da janela de adicionar atalho
        add_window.configure(fg_color="#1F1E2E") # Cor de fundo da janela de adicionar atalho

        # Configurar o layout da grade para a janela de adicionar atalho
        add_window.grid_columnconfigure(0, weight=1)
        add_window.grid_columnconfigure(1, weight=1)
        add_window.grid_columnconfigure(2, weight=1)

        # Título "Novo Atalho"
        new_shortcut_title = ctk.CTkLabel(add_window, text="Novo Atalho", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        new_shortcut_title.grid(row=0, column=0, columnspan=3, pady=20)

        # Nome do Atalho
        name_label = ctk.CTkLabel(add_window, text="Nome do Atalho:", text_color="white")
        name_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=50, pady=(10,0))
        name_entry = ctk.CTkEntry(add_window, placeholder_text="Ex: Google Chrome, Minha Pasta, https://google.com", text_color="white", placeholder_text_color="gray", fg_color="#2B2A3A", border_color="#3a3a3a"  )
        name_entry.grid(row=2, column=0, columnspan=3, sticky="ew", padx=50, pady=(0,10))

        # Caminho/URL
        path_label = ctk.CTkLabel(add_window, text="Caminho/URL:", text_color="white")
        path_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=50, pady=(10,0))
        # Aumentar a largura do campo de entrada e ajustar os botões
        path_entry = ctk.CTkEntry(add_window, placeholder_text="Selecione arquivo/pasta ou digite uma URL", text_color="gray", placeholder_text_color="gray", fg_color="#2B2A3A", border_color="#3a3a3a")
        path_entry.grid(row=4, column=0, sticky="ew", padx=(50, 5), pady=(0,10))
        add_window.grid_columnconfigure(0, weight=3) # Dar mais peso para a coluna do entry

        # Botões Arquivo e Pasta (menores)
        select_file_button = ctk.CTkButton(add_window, text="Arquivo", command=lambda: self.select_file_path(path_entry), fg_color="#1a73e8", hover_color="#1666cc", text_color="white", width=80) # Reduzir largura
        select_file_button.grid(row=4, column=1, sticky="ew", padx=(5, 5), pady=(0,10))

        select_folder_button = ctk.CTkButton(add_window, text="Pasta", command=lambda: self.select_folder_path(path_entry), fg_color="#1a73e8", hover_color="#1666cc", text_color="white", width=80) # Reduzir largura
        select_folder_button.grid(row=4, column=2, sticky="ew", padx=(5, 50), pady=(0,10))

        # Caminho do Ícone (Opcional)
        icon_path_label = ctk.CTkLabel(add_window, text="Caminho do Ícone (Opcional):")
        icon_path_label.grid(row=5, column=0, columnspan=3, sticky="w", padx=50, pady=(10,0))
        icon_entry = ctk.CTkEntry(add_window, placeholder_text="Selecione um arquivo de imagem para o ícone", text_color="white", placeholder_text_color="gray", fg_color="#2B2A3A", border_color="#3a3a3a")
        icon_entry.grid(row=6, column=0, columnspan=2, sticky="ew", padx=(50, 5), pady=(0,10))

        # Botão Procurar Ícone (menor)
        select_icon_button = ctk.CTkButton(add_window, text="Procurar", command=lambda: self.select_icon_path(icon_entry), fg_color="#1a73e8", hover_color="#1666cc", text_color="white", width=80) # Reduzir largura
        select_icon_button.grid(row=6, column=2, sticky="ew", padx=(5, 50), pady=(0,10))

        # Dica para sites (RECOLOCADA AQUI)
        hint_label = ctk.CTkLabel(add_window, text="💡 Dica: Para sites, digite a URL completa (ex: https://google.com  )", font=ctk.CTkFont(size=12), text_color="white")
        hint_label.grid(row=7, column=0, columnspan=3, sticky="w", padx=50, pady=(10, 5)) # Ajuste de pady

        # Label para mensagens de erro/sucesso na janela de adicionar atalho
        self.add_window_message_label = ctk.CTkLabel(add_window, text="", text_color="red")
        self.add_window_message_label.grid(row=8, column=0, columnspan=3, pady=(0, 20)) # Ajuste de row e pady

        # Botões Adicionar e Cancelar
        add_button = ctk.CTkButton(add_window, text="Adicionar", command=lambda: self.save_new_shortcut(name_entry.get(), path_entry.get(), icon_entry.get(), add_window), fg_color="#1a73e8", hover_color="#1666cc", text_color="white")
        add_button.grid(row=9, column=0, columnspan=2, sticky="e", padx=(0, 10), pady=20)

        cancel_button = ctk.CTkButton(add_window, text="Cancelar", command=add_window.destroy, fg_color="#6c757d", hover_color="#5a6268", text_color="white")
        cancel_button.grid(row=9, column=2, sticky="w", padx=(10, 0), pady=20)

    def select_file_path(self, entry_widget):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, file_path)

    def select_folder_path(self, entry_widget):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, folder_path)

    def select_icon_path(self, entry_widget):
        icon_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico *.webp")]) # Adicionado .webp
        if icon_path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, icon_path)

    def save_new_shortcut(self, name, path, icon_path, window):
        # Limpa qualquer mensagem anterior
        self.add_window_message_label.configure(text="")

        if not name or not path:
            self.add_window_message_label.configure(text="Nome e Caminho/URL são obrigatórios!", text_color="red")
            return

        # Verifica se já existe um atalho com o mesmo nome E caminho
        for shortcut in self.shortcuts:
            if shortcut["nome"] == name and shortcut["caminho"] == path:
                self.add_window_message_label.configure(text="Um atalho com este nome e caminho já existe!", text_color="orange")
                return

        # Se chegou aqui, o atalho é válido e não é duplicado
        new_shortcut = {"nome": name, "caminho": path, "icone": icon_path}
        self.shortcuts.append(new_shortcut)
        self.save_shortcuts()
        self.display_shortcuts()
        window.destroy()

    def execute_shortcut(self, shortcut):
        path = shortcut["caminho"]
        shortcut_type = self.determine_shortcut_type(path)

        try:
            if shortcut_type == "link":
                webbrowser.open(path)
            elif shortcut_type == "file" or shortcut_type == "image": # Adicionado "image" para abrir imagens
                if sys.platform == "win32":
                    os.startfile(path) # Funciona no Windows
                else:
                    subprocess.Popen(["xdg-open", path]) # Para Linux/macOS
            elif shortcut_type == "folder":
                if sys.platform == "win32":
                    os.startfile(path) # Funciona no Windows
                else:
                    subprocess.Popen(["xdg-open", path]) # Para Linux/macOS
            elif shortcut_type == "command":
                if sys.platform == "win32":
                    # Para comandos no Windows, pode ser necessário ajustar dependendo do comando
                    # Ex: 'notepad.exe', 'cmd.exe /c dir'
                    subprocess.Popen(path, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    subprocess.Popen(["bash", "-c", path]) # Para Linux/macOS
        except Exception as e:
            print(f"Erro ao executar atalho {shortcut['nome']}: {e}")
            # Poderíamos adicionar uma mensagem de erro na interface aqui também

    def remove_shortcut(self, shortcut):
        self.shortcuts.remove(shortcut)
        self.save_shortcuts()
        self.display_shortcuts()

if __name__ == "__main__":
    app = AtalhoDaPizza()
    app.mainloop()