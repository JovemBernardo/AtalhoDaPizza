import threading
import time
import sys
import os
from pynput import mouse, keyboard
import tkinter as tk
from atalho_pizza import AtalhoDaPizza
from pizza_window import PizzaWindow

class AtalhoPizzaApp:
    def __init__(self):
        self.main_window = None
        self.pizza_window = None
        self.keyboard_listener = None
        self.running = True
        self.alt_pressed = False
        
    def start_main_window(self):
        """Inicia a janela principal de gerenciamento de atalhos"""
        try:
            self.main_window = AtalhoDaPizza()
            # Adiciona esta linha para ocultar a janela principal imediatamente após a criação
            self.main_window.withdraw() 
            self.main_window.protocol("WM_DELETE_WINDOW", self.on_main_window_close)
            self.main_window.mainloop()
        except Exception as e:
            print(f"Erro ao iniciar janela principal: {e}")
            
    def on_main_window_close(self):
        """Callback para quando a janela principal é fechada"""
        self.running = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.main_window:
            self.main_window.destroy()
        sys.exit(0)
        
    def on_key_press(self, key):
        """Callback para quando uma tecla é pressionada"""
        try:
            if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = True
            elif self.alt_pressed and hasattr(key, 'char') and key.char == 'y':
                # Alt + Y foi pressionado - Abre a PizzaWindow
                current_mouse_x, current_mouse_y = mouse.Controller().position
                
                try:
                    if self.pizza_window and self.pizza_window.winfo_exists():
                        self.pizza_window.destroy()
                        
                    self.pizza_window = PizzaWindow(current_mouse_x, current_mouse_y)
                    self.pizza_window.show()
                    
                except Exception as e:
                    print(f"Erro ao abrir janela da pizza: {e}")
        except AttributeError:
            pass

    def on_key_release(self, key):
        """Callback para quando uma tecla é liberada"""
        if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            self.alt_pressed = False
                
    def start_keyboard_listener(self):
        """Inicia o listener global do teclado"""
        try:
            self.keyboard_listener = keyboard.Listener(
                on_press=self.on_key_press,
                on_release=self.on_key_release
            )
            self.keyboard_listener.start()
            print("Listener do teclado iniciado. Pressione Alt+Y para abrir a pizza.")
            # Você precisará de um atalho para abrir a janela principal (AtalhoDaPizza)
            print("A janela de gerenciamento de atalhos está oculta. Defina um atalho para abri-la se necessário.")
        except Exception as e:
            print(f"Erro ao iniciar listener do teclado: {e}")
            
    def run(self):
        """Executa a aplicação"""
        keyboard_thread = threading.Thread(target=self.start_keyboard_listener, daemon=True)
        keyboard_thread.start()
        
        self.start_main_window()

def main():
    """Função principal"""
    try:
        required_files = ['atalho_pizza.py', 'pizza_window.py']
        for file in required_files:
            if not os.path.exists(file):
                print(f"Erro: Arquivo {file} não encontrado!")
                return
                
        app = AtalhoPizzaApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\nAplicação interrompida pelo usuário.")
    except Exception as e:
        print(f"Erro fatal: {e}")
        
if __name__ == "__main__":
    main()