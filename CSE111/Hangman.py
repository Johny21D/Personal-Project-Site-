import tkinter as tk
from tkinter import messagebox
import random

# ─────────────────────────────────────────
#  Word Categories
# ─────────────────────────────────────────
CATEGORIES = {
    "🎲  Random Mix":       None, 
    "💻  Technology":  [
        "python", "algorithm", "compiler", "database", "debugging",
        "framework", "function", "hardware", "interface", "iteration",
        "keyboard", "library", "network", "recursion", "security",
        "software", "syntax", "variable", "developer", "bandwidth",
    ],
    "🍕  Food": [
        "pizza", "burger", "spaghetti", "lasagna", "burrito",
        "pancake", "waffle", "sandwich", "noodles", "dumpling",
        "croissant", "omelette", "risotto", "quesadilla", "falafel",
        "samosa", "ramen", "paella", "kebab", "strudel",
    ],
    "🍎  Fruits": [
        "apple", "mango", "papaya", "banana", "cherry",
        "apricot", "avocado", "blueberry", "coconut", "dragonfruit",
        "elderberry", "fig", "grape", "guava", "kiwi",
        "lemon", "lychee", "melon", "nectarine", "persimmon",
    ],
    "🪐  Space & Planets": [
        "mercury", "venus", "earth", "mars", "jupiter",
        "saturn", "uranus", "neptune", "pluto", "asteroid",
        "comet", "galaxy", "nebula", "pulsar", "quasar",
        "supernova", "blackhole", "cosmos", "eclipse", "solstice",
    ],
    "🔬  Science": [
        "atom", "molecule", "electron", "neutron", "proton",
        "photon", "gravity", "magnetism", "evolution", "chromosome",
        "hypothesis", "catalyst", "osmosis", "entropy", "inertia",
        "refraction", "diffusion", "radiation", "isotope", "polymer",
    ],
    "🔷  Shapes": [
        "circle", "square", "triangle", "pentagon", "hexagon",
        "octagon", "ellipse", "rhombus", "trapezoid", "parallelogram",
        "cylinder", "pyramid", "cuboid", "sphere", "prism",
        "cone", "torus", "crescent", "heptagon", "decagon",
    ],
    "🐾  Animals": [
        "elephant", "giraffe", "penguin", "cheetah", "dolphin",
        "crocodile", "kangaroo", "porcupine", "flamingo", "chameleon",
        "wolverine", "platypus", "armadillo", "orangutan", "chimpanzee",
        "narwhal", "axolotl", "cassowary", "capybara", "meerkat",
    ],
    "🌍  Countries": [
        "brazil", "canada", "denmark", "ethiopia", "finland",
        "germany", "hungary", "indonesia", "jamaica", "kenya",
        "latvia", "morocco", "nigeria", "portugal", "romania",
        "singapore", "thailand", "ukraine", "vietnam", "zimbabwe",
    ],
    "⚽  Sports": [
        "football", "basketball", "volleyball", "badminton", "gymnastics",
        "swimming", "wrestling", "archery", "fencing", "cycling",
        "skateboard", "marathon", "triathlon", "rowing", "cricket",
        "lacrosse", "handball", "polo", "snooker", "bobsled",
    ],
    "🌊  Ocean & Sea": [
        "shark", "whale", "octopus", "jellyfish", "seahorse",
        "stingray", "lobster", "starfish", "barracuda", "clownfish",
        "manatee", "nautilus", "porpoise", "seadragon", "anglerfish",
        "cuttlefish", "manta", "urchin", "anemone", "plankton",
    ],
    "⚡  Mythology": [
        "zeus", "poseidon", "athena", "hermes", "apollo",
        "artemis", "hephaestus", "ares", "demeter", "dionysus",
        "minotaur", "cyclops", "medusa", "chimera", "hydra",
        "phoenix", "centaur", "griffin", "siren", "kraken",
    ],
    "🎵  Music": [
        "melody", "harmony", "rhythm", "tempo", "octave",
        "symphony", "concerto", "sonata", "cadence", "vibrato",
        "arpeggio", "staccato", "crescendo", "diminuendo", "treble",
        "soprano", "baritone", "overture", "serenade", "ballad",
    ],
    "🎨  Colors & Art": [
        "crimson", "turquoise", "magenta", "scarlet", "indigo",
        "cobalt", "vermillion", "chartreuse", "ochre", "sienna",
        "periwinkle", "cerulean", "maroon", "lavender", "fuchsia",
        "watercolor", "portrait", "mosaic", "fresco", "palette",
    ],
    "🌩️  Weather": [
        "hurricane", "tornado", "blizzard", "thunderstorm", "monsoon",
        "cyclone", "typhoon", "avalanche", "drought", "hailstorm",
        "rainbow", "lightning", "fogbank", "dewpoint", "overcast",
        "barometer", "humidity", "equinox", "solstice", "permafrost",
    ],
}

CATEGORIES["🎲  Random Mix"] = [
    w for cat, words in CATEGORIES.items()
    if words is not None for w in words
]

CATEGORY_NAMES = list(CATEGORIES.keys())

# ─────────────────────────────────────────
#  Layout / display constants
# ─────────────────────────────────────────
MAX_WRONG  = 6
CW, CH     = 340, 330
FIG_X      = 213
ROPE_Y     = 49
NECK_TOP   = 97

STARS = [(14,10),(42,26),(88,7),(138,19),(186,9),(223,30),(258,5),
         (28,50),(103,39),(198,21),(163,48),(53,17),(308,40),(280,68)]

BGTIMES = ["🌅 Morning", "☀️ Noon", "🌙 Night"]

# ─────────────────────────────────────────
#  Drawing Helpers
# ─────────────────────────────────────────

def _draw_bg(c, tod):
    if tod == "🌙 Night":
        c.create_rectangle(0, 0, CW, CH, fill="#080814", outline="")
        c.create_rectangle(0, CH-55, CW, CH, fill="#0f0800", outline="")
        c.create_oval(268, 16, 308, 56, fill="#fffde7", outline="")
        c.create_oval(279, 12, 317, 50, fill="#080814", outline="")
        for sx, sy in STARS:
            c.create_oval(sx, sy, sx+2, sy+2, fill="#d0d8ff", outline="")
        c.create_rectangle(0, CH-30, CW, CH, fill="#0c0700", outline="")

    elif tod == "🌅 Morning":
        strips = ["#1a0533","#3d1259","#7a2552","#c44a3a",
                  "#e8703a","#f5a24a","#ffc86a","#ffe098"]
        sh = (CH - 30) // len(strips)
        for i, col in enumerate(strips):
            c.create_rectangle(0, i*sh, CW, (i+1)*sh+1, fill=col, outline="")
        c.create_oval(CW//2-32, CH-62, CW//2+32, CH-4, fill="#ffdd00",
                      outline="#ffaa00", width=2)
        c.create_rectangle(0, CH-42, CW, CH-30, fill="#ff9900", outline="")
        c.create_rectangle(0, CH-30, CW, CH, fill="#1a0c00", outline="")

    elif tod == "☀️ Noon":
        c.create_rectangle(0, 0, CW, int(CH*0.55), fill="#3a7bd5", outline="")
        c.create_rectangle(0, int(CH*0.55), CW, CH-30, fill="#87cefa", outline="")
        c.create_oval(264, 10, 314, 60, fill="#ffe135", outline="#ffcc00", width=3)
        c.create_oval(274, 20, 304, 50, fill="#fff176", outline="")
        for bx, by, w, h in [(40,35,55,20),(160,18,60,18),(30,60,40,15)]:
            c.create_oval(bx, by, bx+w, by+h, fill="#ffffff", outline="")
            c.create_oval(bx+8, by-10, bx+w-8, by+8, fill="#ffffff", outline="")
        c.create_rectangle(0, CH-30, CW, CH, fill="#2d6a1a", outline="")
        c.create_rectangle(0, CH-32, CW, CH-27, fill="#3d8a22", outline="")

def _draw_gallows(c, tod):
    wood  = "#5c3010" if tod == "🌙 Night" else "#7a4520" if tod == "🌅 Morning" else "#8B5220"
    dark  = "#3a1c08" if tod == "🌙 Night" else "#4a2a10" if tod == "🌅 Morning" else "#6a3a10"
    rope  = "#6B5335"
    c.create_rectangle(12,  275, 162, 300, fill=wood, outline=dark)
    c.create_rectangle(76,  36,  93,  280, fill=wood, outline=dark)
    c.create_rectangle(82,  30,  238, 50,  fill=wood, outline=dark)
    c.create_line(77, 38, 128, 31, fill=dark, width=3)
    c.create_line(FIG_X, ROPE_Y, FIG_X, 95, fill=rope, width=4)
    c.create_oval(FIG_X-7, 88, FIG_X+7, 102, outline=rope, width=3)

def draw_scene(c, wrong, tod, dead=False):
    c.delete("all")
    _draw_bg(c, tod)
    _draw_gallows(c, tod)
    
    parts = [_head, _body, _left_arm, _right_arm, _left_leg, _right_leg]
    for i, fn in enumerate(parts):
        if wrong > i:
            if fn == _head:
                fn(c, dead)
            else:
                fn(c)

def _head(c, dead=False):
    cx, cy = FIG_X, 120
    c.create_rectangle(cx-4, 97, cx+4, 110, fill="#F0B8A8", outline="")
    c.create_oval(cx-15, cy-16, cx+15, cy+16, fill="#F5C5AE", outline="#C0876A", width=2)
    c.create_oval(cx-19, cy-5, cx-14, cy+5, fill="#EDAA9A", outline="#C0876A")
    c.create_oval(cx+14, cy-5, cx+19, cy+5, fill="#EDAA9A", outline="#C0876A")
    for hx, dy in zip([-12,-8,-4,0,4,8,12], [-22,-24,-25,-26,-25,-24,-22]):
        c.create_line(cx+hx, cy-15, cx+hx, cy+dy, fill="#3d2b1f", width=2, capstyle="round")
    if dead:
        for ex in [cx-9, cx+4]:
            c.create_line(ex, cy-10, ex+5, cy-5, fill="#1a0800", width=2)
            c.create_line(ex+5, cy-10, ex, cy-5, fill="#1a0800", width=2)
        c.create_arc(cx-7, cy+5, cx+7, cy+14, start=0, extent=180, style=tk.ARC, outline="#5c1a00", width=2)
        c.create_oval(cx-4, cy+12, cx+4, cy+19, fill="#d63031", outline="#b71c1c")
    else:
        for ex in [cx-11, cx+4]:
            c.create_oval(ex, cy-10, ex+7, cy-3, fill="white", outline="#aaa")
            c.create_oval(ex+2, cy-9, ex+5, cy-5, fill="#1a1000", outline="")
        c.create_line(cx-11, cy-14, cx-4, cy-11, fill="#5c3d2e", width=2)
        c.create_line(cx+4,  cy-11, cx+11, cy-14, fill="#5c3d2e", width=2)
        c.create_oval(cx-2, cy-1, cx+2, cy+3, fill="#E09888", outline="")
        c.create_arc(cx-6, cy+6, cx+6, cy+13, start=200, extent=140, style=tk.ARC, outline="#8B4513", width=2)

def _body(c):
    cx = FIG_X
    c.create_polygon([cx-13,134, cx+13,134, cx+14,202, cx-14,202], fill="#c0392b", outline="#922b21")
    c.create_line(cx-8, 134, cx, 148, cx+8, 134, fill="#7b241c", width=2)
    for by in [158, 171, 184, 197]:
        c.create_oval(cx-3, by-3, cx+3, by+3, fill="#7b241c", outline="#5c1a14")

def _arm(c, side):
    cx = FIG_X
    c.create_line(cx+side*10, 144, cx+side*34, 170, width=11, fill="#c0392b", capstyle="round")
    c.create_line(cx+side*34, 170, cx+side*47, 195, width=7, fill="#F5C5AE", capstyle="round")
    c.create_oval(cx+side*42, 191, cx+side*52, 201, fill="#F5C5AE", outline="#C0876A")

def _left_arm(c):  _arm(c, -1)
def _right_arm(c): _arm(c, +1)

def _leg(c, side):
    cx = FIG_X
    c.create_polygon([cx+side*2,200, cx+side*13,200, cx+side*17,258, cx+side*4,258],
                      fill="#2c3e50", outline="#1a252f")
    c.create_line(cx+side*10, 258, cx+side*14, 290, width=7, fill="#F5C5AE", capstyle="round")
    c.create_line(cx+side*14, 280, cx+side*14, 290, width=9, fill="#e0e0e0", capstyle="round")
    shoe = ([cx-24,287, cx-6,287, cx-3,296, cx-24,298, cx-28,292] if side < 0
            else [cx+6,287, cx+24,287, cx+28,292, cx+24,298, cx+3,296])
    c.create_polygon(shoe, fill="#1a1a1a", outline="#0d0d0d")

def _left_leg(c):  _leg(c, -1)
def _right_leg(c): _leg(c, +1)

# ─────────────────────────────────────────
#  App Class
# ─────────────────────────────────────────

class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚰  Hangman  ⚰")
        self.root.resizable(False, False)
        self.root.configure(bg="#080814")
        
        self.word = None
        self.guessed = None
        self.wrong = None
        self.current_tod = random.choice(BGTIMES)
        
        self.category_var = tk.StringVar(value=CATEGORY_NAMES[0])
        self._build_ui()
        self._new_game()

    def _build_ui(self):
        BG, DIM = "#080814", "#55557a"

        tk.Label(self.root, text="— H A N G M A N —", font=("Georgia", 22, "bold"),
                 bg=BG, fg="#e2b714").pack(pady=(14, 0))
        tk.Label(self.root, text="guess the word before it's too late…",
                 font=("Georgia", 9, "italic"), bg=BG, fg="#33334a").pack(pady=(2, 6))

        top = tk.Frame(self.root, bg=BG)
        top.pack(padx=20, pady=4)

        self.canvas = tk.Canvas(top, width=CW, height=CH, bg=BG,
                                highlightthickness=2, highlightbackground="#2d1800")
        self.canvas.pack(side=tk.LEFT, padx=(0, 14))

        info = tk.Frame(top, bg=BG)
        info.pack(side=tk.LEFT, anchor="n", pady=6)

        def lbl(text, font, fg, **kw):
            return tk.Label(info, text=text, font=font, bg=BG, fg=fg, **kw)
        def section(text):
            lbl(text, ("Georgia", 8, "bold"), DIM).pack(anchor="w")

        section("CATEGORY")
        cat_frame = tk.Frame(info, bg=BG)
        cat_frame.pack(anchor="w", pady=(4, 14), fill="x")

        menu = tk.OptionMenu(cat_frame, self.category_var, *CATEGORY_NAMES,
                             command=self._on_category_change)
        menu.config(font=("Georgia", 9), bg="#16162a", fg="#7eb8d4", width=17, relief="flat", bd=0)
        menu.pack(anchor="w")

        tk.Frame(info, bg="#1e1e30", height=1, width=165).pack(fill="x", pady=(0, 10))

        section("WRONG GUESSES")
        self.wrong_label = lbl("", ("Courier", 13, "bold"), "#e63946", wraplength=168, justify="left")
        self.wrong_label.pack(anchor="w", pady=(2, 12))

        section("LIVES REMAINING")
        self.lives_label = lbl("", ("Helvetica", 15), "#e2b714")
        self.lives_label.pack(anchor="w", pady=(2, 12))

        tk.Frame(info, bg="#1e1e30", height=1, width=165).pack(fill="x", pady=(0, 10))

        section("STATUS")
        self.status_label = lbl("", ("Georgia", 10, "italic"), "#a8dadc", wraplength=165, justify="left")
        self.status_label.pack(anchor="w", pady=(2, 0))

        word_outer = tk.Frame(self.root, bg="#0f0a00", bd=2, relief="sunken")
        word_outer.pack(padx=24, pady=(6, 8), fill="x")
        self.word_label = tk.Label(word_outer, text="", font=("Courier", 24, "bold"),
                                   bg="#0f0a00", fg="#f0e68c", pady=10, padx=12)
        self.word_label.pack()

        kb = tk.Frame(self.root, bg=BG)
        kb.pack(padx=20, pady=(0, 6))
        self.buttons = {}
        for row_str in ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]:
            row = tk.Frame(kb, bg=BG)
            row.pack(pady=2)
            for ch in row_str:
                btn = tk.Button(row, text=ch, width=3, height=1,
                                font=("Helvetica", 10, "bold"),
                                bg="#16162a", fg="#c0c0e0",
                                activebackground="#e2b714", activeforeground="#080814",
                                relief="raised", bd=2, cursor="hand2",
                                command=lambda c=ch: self._on_guess(c.lower()))
                btn.pack(side=tk.LEFT, padx=2)
                self.buttons[ch] = btn

        tk.Button(self.root, text="🔄  New Game", font=("Georgia", 12, "bold"),
                  bg="#e2b714", fg="#080814", relief="flat", padx=14, pady=7,
                  cursor="hand2", command=self._new_game).pack(pady=(4, 14))

    def _on_category_change(self, _=None):
        self._new_game()

    def _new_game(self):
        cat  = self.category_var.get()
        pool = CATEGORIES[cat]
        self.word    = random.choice(pool).lower()
        self.guessed = set()
        self.wrong   = set()
        self.current_tod = random.choice(BGTIMES) # Change background on reset
        
        for btn in self.buttons.values():
            btn.config(state=tk.NORMAL, bg="#16162a", fg="#c0c0e0")
        self._refresh_ui()

    def _on_guess(self, letter):
        if letter in self.guessed or letter in self.wrong:
            return
        (self.guessed if letter in self.word else self.wrong).add(letter)
        color = "#2a9d8f" if letter in self.word else "#e63946"
        self.buttons[letter.upper()].config(state=tk.DISABLED, bg=color, fg="white")
        self._refresh_ui()
        self._check_end()

    def _refresh_ui(self):
        w    = len(self.wrong)
        dead = w >= MAX_WRONG
        win  = all(l in self.guessed for l in self.word)
        
        draw_scene(self.canvas, w, self.current_tod, dead)
        
        self.word_label.config(
            text="  ".join(l.upper() if l in self.guessed else "_" for l in self.word))
        self.wrong_label.config(
            text="  ".join(sorted(self.wrong)).upper() if self.wrong else "—")
        
        rem = MAX_WRONG - w
        self.lives_label.config(text="♥ " * rem + "♡ " * w)
        
        if not self.wrong and not self.guessed:
            self.status_label.config(text="Guess a letter to begin!", fg="#a8dadc")
        elif dead:
            self.status_label.config(text="💀  You've been hanged!", fg="#e63946")
        elif win:
            self.status_label.config(text="🎉  You escaped the noose!", fg="#2a9d8f")
        else:
            self.status_label.config(text=f"Keep going!\n{rem} guesses left.", fg="#a8dadc")

    def _check_end(self):
        win  = all(l in self.guessed for l in self.word)
        dead = len(self.wrong) >= MAX_WRONG
        if win or dead:
            for btn in self.buttons.values():
                btn.config(state=tk.DISABLED)
            if win:
                messagebox.showinfo("🎉  You Escaped!", f"Word: {self.word.upper()}")
            else:
                messagebox.showerror("💀  Hanged!", f"The word was: {self.word.upper()}")
            self._new_game()

if __name__ == "__main__":
    root = tk.Tk()
    HangmanApp(root)
    root.mainloop()