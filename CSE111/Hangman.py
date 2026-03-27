import tkinter as tk
from tkinter import messagebox
import random
import math

# ─────────────────────────────────────────
#  Word List
# ─────────────────────────────────────────
WORD_LIST = [
    "python", "hangman", "keyboard", "function", "variable",
    "algorithm", "developer", "database", "interface", "compiler",
    "network", "security", "software", "hardware", "library",
    "framework", "debugging", "iteration", "recursion", "syntax",
]

MAX_WRONG = 6

# Canvas / figure constants
CW, CH = 340, 330        # canvas width / height
FIG_X   = 213            # horizontal centre of the figure
ROPE_Y  = 49             # bottom of beam / top of rope


# ─────────────────────────────────────────
#  Game Logic
# ─────────────────────────────────────────

def choose_word():
    return random.choice(WORD_LIST).lower()

def build_display(word, guessed):
    return "  ".join(letter.upper() if letter in guessed else "_" for letter in word)

def check_win(word, guessed):
    return all(letter in guessed for letter in word)


# ─────────────────────────────────────────
#  Scene Drawing
# ─────────────────────────────────────────

def draw_scene(canvas, wrong_count, dead=False):
    c = canvas
    c.delete("all")

    # ── Night-sky background ──────────────────────────────────────────────
    c.create_rectangle(0, 0, CW, CH, fill="#080814", outline="")
    # Horizon glow
    c.create_rectangle(0, CH - 55, CW, CH, fill="#0f0800", outline="")
    c.create_rectangle(0, CH - 57, CW, CH - 52, fill="#1c0f00", outline="")

    # Crescent moon
    c.create_oval(268, 16, 308, 56, fill="#fffde7", outline="")
    c.create_oval(279, 12, 317, 50, fill="#080814", outline="")   # bite-out

    # Stars (fixed seed so they don't flicker on redraw)
    STARS = [(14,10),(42,26),(88,7),(138,19),(186,9),(223,30),(258,5),
             (28,50),(103,39),(198,21),(163,48),(53,17),(308,40),(280,68),
             (70,30),(150,60),(235,45),(10,70),(300,20),(120,55)]
    for sx, sy in STARS:
        c.create_oval(sx, sy, sx+2, sy+2, fill="#d0d8ff", outline="")

    # ── Ground platform ───────────────────────────────────────────────────
    c.create_rectangle(0, CH - 30, CW, CH, fill="#0c0700", outline="")
    # Edge highlight
    c.create_line(0, CH - 30, CW, CH - 30, fill="#1e1000", width=2)

    # ── Gallows: base log ─────────────────────────────────────────────────
    # bottom shadow face
    c.create_rectangle(12, 288, 162, 302, fill="#2d1608", outline="")
    # front face
    c.create_rectangle(12, 278, 162, 288, fill="#5c3010", outline="")
    # top highlight face
    c.create_rectangle(12, 275, 162, 279, fill="#7a4520", outline="")
    # End caps
    c.create_oval(9, 274, 20, 302, fill="#4a2510", outline="#2d1608")
    c.create_oval(155, 274, 166, 302, fill="#4a2510", outline="#2d1608")

    # ── Gallows: vertical pole ────────────────────────────────────────────
    # right shadow strip
    c.create_rectangle(88, 36, 93, 280, fill="#3a1c08", outline="")
    # front face
    c.create_rectangle(76, 36, 88, 280, fill="#5c3010", outline="")
    # left highlight strip
    c.create_rectangle(76, 36, 80, 280, fill="#7a4520", outline="")
    # wood grain on pole
    for gy in range(52, 278, 22):
        c.create_line(77, gy, 92, gy + 9, fill="#4a2510", width=1)

    # ── Gallows: horizontal beam ──────────────────────────────────────────
    # bottom shadow face
    c.create_rectangle(82, 44, 238, 50, fill="#3a1c08", outline="")
    # front face
    c.create_rectangle(82, 33, 238, 44, fill="#5c3010", outline="")
    # top highlight face
    c.create_rectangle(82, 30, 238, 34, fill="#7a4520", outline="")
    # grain on beam
    for gx in range(98, 236, 26):
        c.create_line(gx, 31, gx + 5, 49, fill="#4a2510", width=1)

    # ── Gallows: diagonal brace ───────────────────────────────────────────
    c.create_polygon(77, 38, 93, 38, 130, 31, 127, 42,
                     fill="#4a2510", outline="#3a1c08", width=1)
    c.create_line(77, 38, 128, 31, fill="#7a4520", width=1)

    # Metal bolts at beam joints
    for bx, by in [(79, 33), (228, 33)]:
        c.create_oval(bx, by, bx + 8, by + 8, fill="#666", outline="#333")
        c.create_oval(bx + 2, by + 2, bx + 6, by + 6, fill="#aaa", outline="")

    # ── Rope ──────────────────────────────────────────────────────────────
    rx = FIG_X
    # twisted braid effect
    for i in range(10):
        y1 = ROPE_Y + i * 4
        y2 = y1 + 3
        twist = 2 if (i % 2 == 0) else -2
        c.create_line(rx + twist, y1, rx - twist, y2,
                      fill="#8B7355", width=3, capstyle="round")
    # straight drop to noose
    c.create_line(rx, 89, rx, 95, fill="#6B5335", width=4)
    # noose loop
    c.create_oval(rx - 7, 88, rx + 7, 102,
                  outline="#6B5335", width=3, fill="")

    # ── Figure (drawn in order of wrong guesses) ──────────────────────────
    if wrong_count >= 1:
        _draw_head(c, dead)
    if wrong_count >= 2:
        _draw_body(c)
    if wrong_count >= 3:
        _draw_left_arm(c)
    if wrong_count >= 4:
        _draw_right_arm(c)
    if wrong_count >= 5:
        _draw_left_leg(c)
    if wrong_count >= 6:
        _draw_right_leg(c)


# ── Figure part helpers ───────────────────────────────────────────────────

def _draw_head(c, dead=False):
    cx, cy = FIG_X, 120
    # Neck
    c.create_rectangle(cx - 4, 97, cx + 4, 110, fill="#F0B8A8", outline="")
    # Drop shadow
    c.create_oval(cx - 17, cy - 13, cx + 19, cy + 19, fill="#04020a", outline="")
    # Head oval
    c.create_oval(cx - 15, cy - 16, cx + 15, cy + 16,
                  fill="#F5C5AE", outline="#C0876A", width=2)
    # Ears
    c.create_oval(cx - 19, cy - 5, cx - 14, cy + 5, fill="#EDAA9A", outline="#C0876A")
    c.create_oval(cx + 14, cy - 5, cx + 19, cy + 5, fill="#EDAA9A", outline="#C0876A")
    # Hair (fixed offsets)
    HAIR_X = [-12, -8, -4, 0, 4, 8, 12]
    HAIR_DY = [-22, -24, -25, -26, -25, -24, -22]
    for hx, dy in zip(HAIR_X, HAIR_DY):
        c.create_line(cx + hx, cy - 15, cx + hx, cy + dy,
                      fill="#3d2b1f", width=2, capstyle="round")

    if dead:
        # ✕ eyes
        for ex in [cx - 9, cx + 4]:
            c.create_line(ex, cy - 10, ex + 5, cy - 5, fill="#1a0800", width=2)
            c.create_line(ex + 5, cy - 10, ex, cy - 5, fill="#1a0800", width=2)
        # Open frown
        c.create_arc(cx - 7, cy + 5, cx + 7, cy + 14,
                     start=0, extent=180, style=tk.ARC, outline="#5c1a00", width=2)
        # Dangling tongue
        c.create_oval(cx - 4, cy + 12, cx + 4, cy + 19,
                      fill="#d63031", outline="#b71c1c")
    else:
        # Eyes: whites + pupils + highlight
        for ex in [cx - 11, cx + 4]:
            c.create_oval(ex, cy - 10, ex + 7, cy - 3, fill="white", outline="#aaa")
            c.create_oval(ex + 2, cy - 9, ex + 5, cy - 5, fill="#1a1000", outline="")
            c.create_oval(ex + 2, cy - 9, ex + 3, cy - 8, fill="white", outline="")
        # Worried angled eyebrows
        c.create_line(cx - 11, cy - 14, cx - 4, cy - 11, fill="#5c3d2e", width=2)
        c.create_line(cx + 4,  cy - 11, cx + 11, cy - 14, fill="#5c3d2e", width=2)
        # Nose
        c.create_oval(cx - 2, cy - 1, cx + 2, cy + 3, fill="#E09888", outline="")
        # Nervous mouth (slight frown arc)
        c.create_arc(cx - 6, cy + 6, cx + 6, cy + 13,
                     start=200, extent=140, style=tk.ARC, outline="#8B4513", width=2)


def _draw_body(c):
    cx = FIG_X
    # Shirt torso (slight trapezoid for depth)
    pts = [cx - 13, 134, cx + 13, 134, cx + 14, 202, cx - 14, 202]
    c.create_polygon(pts, fill="#c0392b", outline="#922b21", width=1)
    # Left highlight panel
    c.create_polygon([cx - 13, 134, cx - 6, 134, cx - 7, 202, cx - 14, 202],
                     fill="#e74c3c", outline="")
    # V-collar
    c.create_line(cx - 8, 134, cx, 148, cx + 8, 134, fill="#7b241c", width=2)
    # Buttons
    for by in [158, 171, 184, 197]:
        c.create_oval(cx - 3, by - 3, cx + 3, by + 3, fill="#7b241c", outline="#5c1a14")


def _draw_left_arm(c):
    cx = FIG_X
    # Sleeve (upper arm — wider line for shirt fabric)
    c.create_line(cx - 10, 144, cx - 34, 170, width=11, fill="#c0392b", capstyle="round")
    c.create_line(cx - 10, 144, cx - 34, 170, width=7,  fill="#e74c3c", capstyle="round")
    # Forearm (skin)
    c.create_line(cx - 34, 170, cx - 47, 195, width=7, fill="#F5C5AE", capstyle="round")
    # Hand
    c.create_oval(cx - 52, 191, cx - 42, 201, fill="#F5C5AE", outline="#C0876A")


def _draw_right_arm(c):
    cx = FIG_X
    c.create_line(cx + 10, 144, cx + 34, 170, width=11, fill="#c0392b", capstyle="round")
    c.create_line(cx + 10, 144, cx + 34, 170, width=7,  fill="#e74c3c", capstyle="round")
    c.create_line(cx + 34, 170, cx + 47, 195, width=7,  fill="#F5C5AE", capstyle="round")
    c.create_oval(cx + 42, 191, cx + 52, 201, fill="#F5C5AE", outline="#C0876A")


def _draw_left_leg(c):
    cx = FIG_X
    # Pants (dark jeans)
    c.create_polygon([cx - 13, 200, cx - 2, 200, cx - 4, 258, cx - 17, 258],
                     fill="#2c3e50", outline="#1a252f")
    c.create_polygon([cx - 13, 200, cx - 7, 200, cx - 9, 258, cx - 17, 258],
                     fill="#34495e", outline="")
    # Lower leg (skin)
    c.create_line(cx - 10, 258, cx - 14, 290, width=7, fill="#F5C5AE", capstyle="round")
    # White sock peek
    c.create_line(cx - 14, 280, cx - 14, 290, width=9, fill="#e0e0e0", capstyle="round")
    # Shoe
    c.create_polygon([cx - 24, 287, cx - 6, 287, cx - 3, 296, cx - 24, 298, cx - 28, 292],
                     fill="#1a1a1a", outline="#0d0d0d")
    c.create_line(cx - 24, 287, cx - 6, 287, fill="#333", width=1)   # sole seam


def _draw_right_leg(c):
    cx = FIG_X
    c.create_polygon([cx + 2, 200, cx + 13, 200, cx + 17, 258, cx + 4, 258],
                     fill="#2c3e50", outline="#1a252f")
    c.create_polygon([cx + 7,  200, cx + 13, 200, cx + 17, 258, cx + 9,  258],
                     fill="#34495e", outline="")
    c.create_line(cx + 10, 258, cx + 14, 290, width=7, fill="#F5C5AE", capstyle="round")
    c.create_line(cx + 14, 280, cx + 14, 290, width=9, fill="#e0e0e0", capstyle="round")
    c.create_polygon([cx + 6, 287, cx + 24, 287, cx + 28, 292, cx + 24, 298, cx + 3, 296],
                     fill="#1a1a1a", outline="#0d0d0d")
    c.create_line(cx + 6, 287, cx + 24, 287, fill="#333", width=1)


# ─────────────────────────────────────────
#  GUI App Class
# ─────────────────────────────────────────

class HangmanApp:
    def __init__(self, root):
        self.root  = root
        self.root.title("⚰  Hangman  ⚰")
        self.root.resizable(False, False)
        self.root.configure(bg="#080814")

        self.word    = ""
        self.guessed = set()
        self.wrong   = set()
        self.buttons = {}

        self._build_ui()
        self._new_game()

    # ── UI Construction ──────────────────────────────────────────────────

    def _build_ui(self):
        BG  = "#080814"
        DIM = "#55557a"

        # ── Title bar ──────────────────────────────────────────────────
        tk.Label(self.root,
                 text="— H A N G M A N —",
                 font=("Georgia", 22, "bold"),
                 bg=BG, fg="#e2b714").pack(pady=(14, 0))
        tk.Label(self.root,
                 text="guess the word before it's too late…",
                 font=("Georgia", 9, "italic"),
                 bg=BG, fg="#33334a").pack(pady=(2, 6))

        # ── Top row: canvas | info panel ───────────────────────────────
        top = tk.Frame(self.root, bg=BG)
        top.pack(padx=20, pady=4)

        # Canvas
        self.canvas = tk.Canvas(top, width=CW, height=CH,
                                bg=BG,
                                highlightthickness=2,
                                highlightbackground="#2d1800")
        self.canvas.pack(side=tk.LEFT, padx=(0, 14))

        # Info panel
        info = tk.Frame(top, bg=BG)
        info.pack(side=tk.LEFT, anchor="n", pady=6)

        def section(text):
            tk.Label(info, text=text, font=("Georgia", 8, "bold"),
                     bg=BG, fg=DIM).pack(anchor="w")

        section("WRONG GUESSES")
        self.wrong_label = tk.Label(info, text="", font=("Courier", 13, "bold"),
                                    bg=BG, fg="#e63946",
                                    wraplength=168, justify="left")
        self.wrong_label.pack(anchor="w", pady=(2, 12))

        section("LIVES REMAINING")
        self.lives_label = tk.Label(info, text="", font=("Helvetica", 15),
                                    bg=BG, fg="#e2b714")
        self.lives_label.pack(anchor="w", pady=(2, 12))

        section("CATEGORY")
        tk.Label(info, text="💻  Programming / Tech",
                 font=("Georgia", 10, "italic"),
                 bg=BG, fg="#7eb8d4").pack(anchor="w", pady=(2, 16))

        # Thin divider
        tk.Frame(info, bg="#1e1e30", height=1, width=165).pack(fill="x", pady=(0, 12))

        section("STATUS")
        self.status_label = tk.Label(info, text="",
                                     font=("Georgia", 10, "italic"),
                                     bg=BG, fg="#a8dadc",
                                     wraplength=165, justify="left")
        self.status_label.pack(anchor="w", pady=(2, 0))

        # ── Word display ───────────────────────────────────────────────
        word_outer = tk.Frame(self.root, bg="#0f0a00", bd=2, relief="sunken")
        word_outer.pack(padx=24, pady=(6, 8), fill="x")
        self.word_label = tk.Label(word_outer, text="",
                                   font=("Courier", 24, "bold"),
                                   bg="#0f0a00", fg="#f0e68c",
                                   pady=10, padx=12)
        self.word_label.pack()

        # ── Keyboard ───────────────────────────────────────────────────
        kb = tk.Frame(self.root, bg=BG)
        kb.pack(padx=20, pady=(0, 6))

        for row_str in ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]:
            row = tk.Frame(kb, bg=BG)
            row.pack(pady=2)
            for ch in row_str:
                btn = tk.Button(
                    row, text=ch, width=3, height=1,
                    font=("Helvetica", 10, "bold"),
                    bg="#16162a", fg="#c0c0e0",
                    activebackground="#e2b714",
                    activeforeground="#080814",
                    relief="raised", bd=2, cursor="hand2",
                    command=lambda c=ch: self._on_guess(c.lower())
                )
                btn.pack(side=tk.LEFT, padx=2)
                self.buttons[ch] = btn

        # ── New game button ────────────────────────────────────────────
        tk.Button(self.root,
                  text="🔄  New Game",
                  font=("Georgia", 12, "bold"),
                  bg="#e2b714", fg="#080814",
                  relief="flat", padx=14, pady=7,
                  cursor="hand2",
                  command=self._new_game).pack(pady=(4, 14))

    # ── Game Logic ───────────────────────────────────────────────────────

    def _new_game(self):
        self.word    = choose_word()
        self.guessed = set()
        self.wrong   = set()
        for btn in self.buttons.values():
            btn.config(state=tk.NORMAL, bg="#16162a", fg="#c0c0e0")
        self._refresh_ui()

    def _on_guess(self, letter):
        if letter in self.guessed or letter in self.wrong:
            return
        if letter in self.word:
            self.guessed.add(letter)
            self.buttons[letter.upper()].config(
                state=tk.DISABLED, bg="#2a9d8f", fg="white")
        else:
            self.wrong.add(letter)
            self.buttons[letter.upper()].config(
                state=tk.DISABLED, bg="#e63946", fg="white")
        self._refresh_ui()
        self._check_end()

    def _refresh_ui(self):
        w        = len(self.wrong)
        is_dead  = (w >= MAX_WRONG)
        is_win   = check_win(self.word, self.guessed)

        draw_scene(self.canvas, w, dead=is_dead)

        self.word_label.config(text=build_display(self.word, self.guessed))

        self.wrong_label.config(
            text="  ".join(sorted(self.wrong)).upper() if self.wrong else "—")

        remaining = MAX_WRONG - w
        self.lives_label.config(text="♥ " * remaining + "♡ " * w)

        if not self.wrong and not self.guessed:
            self.status_label.config(
                text="Guess a letter to begin!", fg="#a8dadc")
        elif is_dead:
            self.status_label.config(
                text="💀  You've been hanged!", fg="#e63946")
        elif is_win:
            self.status_label.config(
                text="🎉  You escaped the noose!", fg="#2a9d8f")
        else:
            pl = "guesses" if remaining != 1 else "guess"
            self.status_label.config(
                text=f"Keep going!\n{remaining} wrong {pl} left.", fg="#a8dadc")

    def _check_end(self):
        if check_win(self.word, self.guessed):
            self._disable_all()
            messagebox.showinfo(
                "🎉  You Escaped!",
                f"Brilliant! You guessed:\n\n  {self.word.upper()}"
                "\n\nClick OK to play again.")
            self._new_game()
        elif len(self.wrong) >= MAX_WRONG:
            self._disable_all()
            messagebox.showerror(
                "💀  You Were Hanged!",
                f"You ran out of guesses!\n\nThe word was:\n\n  {self.word.upper()}"
                "\n\nClick OK to try again.")
            self._new_game()

    def _disable_all(self):
        for btn in self.buttons.values():
            btn.config(state=tk.DISABLED)


# ─────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────

def main():
    root = tk.Tk()
    HangmanApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()