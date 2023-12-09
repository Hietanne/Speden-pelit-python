import tkinter as tk
import random

class SpeedGame:
    def __init__(self, root):
        self.root = root
        root.title("Speden pelit")
        root.geometry("600x400")  # Alkuperäinen ikkunan koko

        self.active_colors = ['#ff0000', '#0000ff', '#00ff00', '#ffff00']  # punainen, sininen, vihreä, keltainen
        self.color_keys = {'q': '#ff0000', 'w': '#0000ff', 'e': '#00ff00', 'r': '#ffff00'}
        self.inactive_color = '#000000'  # musta

        self.buttons = {}
        self.active_button = None
        self.score = 0
        self.game_running = False
        self.time_limit = 2000  # Aika millisekunteina

        self.create_widgets()
        self.setup_key_listener()

    def create_widgets(self):
        self.canvas_frames = []
        for idx, color in enumerate(self.active_colors):
            frame = tk.Frame(self.root)
            frame.grid(row=0, column=idx, sticky='nsew')
            self.root.grid_columnconfigure(idx, weight=1)
            self.root.grid_rowconfigure(0, weight=1)
            self.canvas_frames.append(frame)

            canvas = tk.Canvas(frame, bg='white', highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            ball = canvas.create_oval(10, 10, 90, 90, fill=self.inactive_color, outline=self.inactive_color)
            self.buttons[color] = (canvas, ball)

        self.score_label = tk.Label(self.root, text="Score: 0")
        self.score_label.grid(row=1, column=0, columnspan=4)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.grid(row=2, column=0, columnspan=4)

    def setup_key_listener(self):
        self.key_listener = tk.Entry(self.root, borderwidth=0, highlightthickness=0)
        self.key_listener.bind("<Key>", self.key_pressed)
        self.key_listener.grid(row=3, column=0, columnspan=4, sticky='ew')
        self.root.grid_rowconfigure(3, weight=1)
        self.key_listener.focus_set()

    def key_pressed(self, event):
        color = self.color_keys.get(event.char.lower(), None)  # Päivitetty käsittelemään pienet kirjaimet
        if color:
            self.button_pressed(color)
        self.key_listener.delete(0, tk.END)  # Poistaa kaiken tekstin tekstikentästä jokaisen painalluksen jälkeen


    def start_game(self):
        self.score = 0
        self.game_running = True
        self.time_limit = 2000
        self.score_label.config(text="Score: 0")
        self.activate_button()

    def activate_button(self):
        if self.game_running:
            self.active_button = random.choice(self.active_colors)
            canvas, ball = self.buttons[self.active_button]
            canvas.itemconfig(ball, fill=self.active_button)
            self.root.after(self.time_limit, self.check_button)

    def check_button(self):
        if self.active_button:
            self.end_game()
        else:
            self.increase_difficulty()
            self.activate_button()

    def button_pressed(self, color):
        if self.active_button == color:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            canvas, ball = self.buttons[color]
            canvas.itemconfig(ball, fill=self.inactive_color)
            self.active_button = None
        elif self.game_running:
            self.end_game()

    def increase_difficulty(self):
        self.time_limit = max(500, self.time_limit - 5)  # Hidastetaan pelin kiihtyvyyttä

    def end_game(self):
        self.game_running = False
        for color in self.active_colors:
            canvas, ball = self.buttons[color]
            canvas.itemconfig(ball, fill=self.inactive_color)
        self.active_button = None
        self.score_label.config(text=f"Game Over! Score: {self.score}")

def main():
    root = tk.Tk()
    game = SpeedGame(root)
    root.mainloop()

main()
