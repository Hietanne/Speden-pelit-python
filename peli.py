import tkinter as tk
import random

class Spedenpelit:
    def __init__(self, root):
        self.root = root
        root.title("Speden pelit")
        root.geometry("600x400")  # Alkuperäinen ikkunan koko

        self.active_colors = ['#ff0000', '#0000ff', '#00ff00', '#ffff00']  # punainen, sininen, vihreä, keltainen
        self.color_keys = {'q': '#ff0000', 'w': '#0000ff', 'e': '#00ff00', 'r': '#ffff00'}
        self.inactive_color = '#000000'  # musta

        self.buttons = {}
        self.aktiivinen_nappi = None
        self.pisteet = 0
        self.peli_menossa = False
        self.aika_ms = 2000  # Aika millisekunteina

        self.create_widgets()
        self.aloita_nappainten_kuuntelu()

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

        self.pisteet_label = tk.Label(self.root, text="pisteet: 0")
        self.pisteet_label.grid(row=1, column=0, columnspan=4)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.aloita_peli)
        self.start_button.grid(row=2, column=0, columnspan=4)

    def aloita_nappainten_kuuntelu(self):
        self.key_listener = tk.Entry(self.root, borderwidth=0, highlightthickness=0)
        self.key_listener.bind("<Key>", self.nappainta_painettu)
        self.key_listener.grid(row=3, column=0, columnspan=4, sticky='ew')
        self.root.grid_rowconfigure(3, weight=1)
        self.key_listener.focus_set()

    def nappainta_painettu(self, event):                               # Funktio joka seuraa napin painalluksia
        color = self.color_keys.get(event.char.lower(), None)
        if color:
            self.nappia_painettu(color)
        self.key_listener.delete(0, tk.END)                     # Poistetaan viimeinen näppäin


    def aloita_peli(self):
        self.pisteet = 0                                          
        self.peli_menossa = True
        self.aika_ms = 2000
        self.pisteet_label.config(text="pisteet: 0")
        self.aktivoi_nappi()

    def aktivoi_nappi(self):
        if self.peli_menossa:
            self.aktiivinen_nappi = random.choice(self.active_colors)
            canvas, ball = self.buttons[self.aktiivinen_nappi]
            canvas.itemconfig(ball, fill=self.aktiivinen_nappi)
            self.root.after(self.aika_ms, self.tarkasta_nappi)

    def tarkasta_nappi(self):
        if self.aktiivinen_nappi:
            self.lopeta_peli()
        else:
            self.nosta_vaikeustasoa()
            self.aktivoi_nappi()

    def nappia_painettu(self, color):
        if self.aktiivinen_nappi == color:
            self.pisteet += 1
            self.pisteet_label.config(text=f"pisteet: {self.pisteet}")
            canvas, ball = self.buttons[color]
            canvas.itemconfig(ball, fill=self.inactive_color)
            self.aktiivinen_nappi = None
        elif self.peli_menossa:
            self.lopeta_peli()

    def nosta_vaikeustasoa(self):
        miinus_aika = 5             # Aika mikä miinustetaan
        max_aika = 750              # Aika ei voi mennä alle tämän
        self.aika_ms = max(max_aika, self.aika_ms - miinus_aika)  # Hidastetaan pelin kiihtyvyyttä

    def lopeta_peli(self):
        self.peli_menossa = False
        for color in self.active_colors:
            canvas, ball = self.buttons[color]
            canvas.itemconfig(ball, fill=self.inactive_color)
        self.aktiivinen_nappi = None
        self.pisteet_label.config(text=f"Peli ohi! pisteet: {self.pisteet}")

def main():
    root = tk.Tk()
    game = Spedenpelit(root)
    root.mainloop()

main()
