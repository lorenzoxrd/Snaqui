import tkinter as tk
import random

class SnaquiGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snaqui")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        self.loading_screen()
        
    def loading_screen(self):
        self.loading_label = tk.Label(self.root, text="Cargando...", font=("Arial", 24))
        self.loading_label.pack(expand=True)
        self.root.after(2000, self.main_menu)
        
    def main_menu(self):
        self.loading_label.pack_forget()
        self.title_label = tk.Label(self.root, text="Snaqui", font=("Arial", 24))
        self.title_label.pack(pady=20)
        
        self.start_button = tk.Button(self.root, text="Iniciar", command=self.start_game)
        self.start_button.pack(pady=10)
        
        self.exit_button = tk.Button(self.root, text="Salir", command=self.root.quit)
        self.exit_button.pack(pady=10)
        
    def start_game(self):
        self.title_label.pack_forget()
        self.start_button.pack_forget()
        self.exit_button.pack_forget()
        
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()
        
        self.canvas = tk.Canvas(self.game_frame, width=320, height=320, bg="black")
        self.canvas.pack()
        
        self.pause_button = tk.Button(self.root, text="Pausa", command=self.pause_game)
        self.pause_button.pack()
        
        self.snake = [(4, 4)]
        self.direction = "Right"
        self.food = self.place_food()
        self.score = 0
        self.game_running = False
        
        self.root.bind("<KeyPress>", self.change_direction)
        
        self.countdown_label = tk.Label(self.root, text="", font=("Arial", 24))
        self.countdown_label.pack()
        self.countdown(3)
        
    def countdown(self, count):
        if count > 0:
            self.countdown_label.config(text=str(count))
            self.root.after(1000, self.countdown, count-1)
        else:
            self.countdown_label.pack_forget()
            self.game_running = True
            self.update_game()
        
    def place_food(self):
        while True:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if (x, y) not in self.snake:
                return (x, y)
                
    def update_game(self):
        if not self.game_running:
            return
        
        head_x, head_y = self.snake[0]
        if self.direction == "Right":
            head_x += 1
        elif self.direction == "Left":
            head_x -= 1
        elif self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1
            
        new_head = (head_x, head_y)
        
        if new_head in self.snake or not (0 <= head_x < 8 and 0 <= head_y < 8):
            self.game_over()
            return
        
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.food = self.place_food()
            self.score += 1
        else:
            self.snake.pop()
        
        self.draw_game()
        self.root.after(200, self.update_game)
        
    def draw_game(self):
        self.canvas.delete("all")
        for x, y in self.snake:
            self.canvas.create_rectangle(x*40, y*40, x*40+40, y*40+40, fill="green")
        food_x, food_y = self.food
        self.canvas.create_rectangle(food_x*40, food_y*40, food_x*40+40, food_y*40+40, fill="red")
        
    def change_direction(self, event):
        if event.keysym in ["Left", "a"] and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym in ["Right", "d"] and self.direction != "Left":
            self.direction = "Right"
        elif event.keysym in ["Up", "w"] and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym in ["Down", "s"] and self.direction != "Up":
            self.direction = "Down"
        
    def pause_game(self):
        self.game_running = False
        self.pause_window = tk.Toplevel(self.root)
        self.pause_window.title("Pausa")
        
        pause_label = tk.Label(self.pause_window, text="Pausa", font=("Arial", 24))
        pause_label.pack(pady=10)
        
        resume_button = tk.Button(self.pause_window, text="Continuar", command=self.resume_game)
        resume_button.pack(pady=5)
        
        restart_button = tk.Button(self.pause_window, text="Reiniciar", command=self.restart_game)
        restart_button.pack(pady=5)
        
        main_menu_button = tk.Button(self.pause_window, text="Menú Principal", command=self.go_to_main_menu)
        main_menu_button.pack(pady=5)
        
        exit_button = tk.Button(self.pause_window, text="Salir", command=self.root.quit)
        exit_button.pack(pady=5)
        
    def resume_game(self):
        self.pause_window.destroy()
        self.game_running = True
        self.update_game()
        
    def restart_game(self):
        if hasattr(self, 'pause_window'):
            self.pause_window.destroy()
        if hasattr(self, 'game_over_window'):
            self.game_over_window.destroy()
        self.reset_game()
        
    def go_to_main_menu(self):
        if hasattr(self, 'pause_window'):
            self.pause_window.destroy()
        if hasattr(self, 'game_over_window'):
            self.game_over_window.destroy()
        self.game_frame.pack_forget()
        self.pause_button.pack_forget()
        self.main_menu()
        
    def reset_game(self):
        self.snake = [(4, 4)]
        self.direction = "Right"
        self.food = self.place_food()
        self.score = 0
        self.game_running = False
        self.countdown_label.pack()
        self.countdown(3)
        self.root.bind("<KeyPress>", self.change_direction)
        
    def game_over(self):
        self.game_running = False
        self.game_over_window = tk.Toplevel(self.root)
        self.game_over_window.title("Fin del Juego")
        
        game_over_label = tk.Label(self.game_over_window, text="Fin del Juego", font=("Arial", 24))
        game_over_label.pack(pady=10)
        
        score_label = tk.Label(self.game_over_window, text=f"Puntuación: {self.score}", font=("Arial", 18))
        score_label.pack(pady=10)
        
        restart_button = tk.Button(self.game_over_window, text="Reiniciar", command=self.restart_game)
        restart_button.pack(pady=5)
        
        main_menu_button = tk.Button(self.game_over_window, text="Menú Principal", command=self.go_to_main_menu)
        main_menu_button.pack(pady=5)
        
        exit_button = tk.Button(self.game_over_window, text="Salir", command=self.root.quit)
        exit_button.pack(pady=5)
        
if __name__ == "__main__":
    root = tk.Tk()
    game = SnaquiGame(root)
    root.mainloop()