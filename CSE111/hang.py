import tkinter as tk
from tkinter import messagebox
import random

# ─────────────────────────────────────────
#  Word Categories
# ─────────────────────────────────────────
CATEGORIES = {
    "🎲  Random Mix":      None,
    "💻  Technology": [
        "python","algorithm","compiler","database","debugging","framework",
        "function","hardware","interface","iteration","keyboard","library",
        "network","recursion","security","software","syntax","variable",
        "developer","bandwidth",
    ],
    "🍕  Food": [
        "pizza","burger","spaghetti","lasagna","burrito","pancake","waffle",
        "sandwich","noodles","dumpling","croissant","omelette","risotto",
        "quesadilla","falafel","samosa","ramen","paella","kebab","strudel",
    ],
    "🍎  Fruits": [
        "apple","mango","papaya","banana","cherry","apricot","avocado",
        "blueberry","coconut","dragonfruit","elderberry","fig","grape",
        "guava","kiwi","lemon","lychee","melon","nectarine","persimmon",
    ],
    "🪐  Space & Planets": [
        "mercury","venus","earth","mars","jupiter","saturn","uranus",
        "neptune","pluto","asteroid","comet","galaxy","nebula","pulsar",
        "quasar","supernova","blackhole","cosmos","eclipse","solstice",
    ],
    "🔬  Science": [
        "atom","molecule","electron","neutron","proton","photon","gravity",
        "magnetism","evolution","chromosome","hypothesis","catalyst",
        "osmosis","entropy","inertia","refraction","diffusion","radiation",
        "isotope","polymer",
    ],
    "🔷  Shapes": [
        "circle","square","triangle","pentagon","hexagon","octagon",
        "ellipse","rhombus","trapezoid","parallelogram","cylinder",
        "pyramid","cuboid","sphere","prism","cone","torus","crescent",
        "heptagon","decagon",
    ],
    "🐾  Animals": [
        "elephant","giraffe","penguin","cheetah","dolphin","crocodile",
        "kangaroo","porcupine","flamingo","chameleon","wolverine",
        "platypus","armadillo","orangutan","chimpanzee","narwhal",
        "axolotl","cassowary","capybara","meerkat",
    ],
    "🌍  Countries": [
        "brazil","canada","denmark","ethiopia","finland","germany",
        "hungary","indonesia","jamaica","kenya","latvia","morocco",
        "nigeria","portugal","romania","singapore","thailand","ukraine",
        "vietnam","zimbabwe",
    ],
    "⚽  Sports": [
        "football","basketball","volleyball","badminton","gymnastics",
        "swimming","wrestling","archery","fencing","cycling","skateboard",
        "marathon","triathlon","rowing","cricket","lacrosse","handball",
        "polo","snooker","bobsled",
    ],
    "🌊  Ocean & Sea": [
        "shark","whale","octopus","jellyfish","seahorse","stingray",
        "lobster","starfish","barracuda","clownfish","manatee","nautilus",
        "porpoise","seadragon","anglerfish","cuttlefish","manta","urchin",
        "anemone","plankton",
    ],
    "⚡  Mythology": [
        "zeus","poseidon","athena","hermes","apollo","artemis",
        "hephaestus","ares","demeter","dionysus","minotaur","cyclops",
        "medusa","chimera","hydra","phoenix","centaur","griffin",
        "siren","kraken",
    ],
    "🎵  Music": [
        "melody","harmony","rhythm","tempo","octave","symphony","concerto",
        "sonata","cadence","vibrato","arpeggio","staccato","crescendo",
        "diminuendo","treble","soprano","baritone","overture","serenade",
        "ballad",
    ],
    "🎨  Colors & Art": [
        "crimson","turquoise","magenta","scarlet","indigo","cobalt",
        "vermillion","chartreuse","ochre","sienna","periwinkle","cerulean",
        "maroon","lavender","fuchsia","watercolor","portrait","mosaic",
        "fresco","palette",
    ],
    "🌩️  Weather": [
        "hurricane","tornado","blizzard","thunderstorm","monsoon","cyclone",
        "typhoon","avalanche","drought","hailstorm","rainbow","lightning",
        "fogbank","dewpoint","overcast","barometer","humidity","equinox",
        "solstice","permafrost",
    ],
}
CATEGORIES["🎲  Random Mix"] = [w for k,v in CATEGORIES.items() if v for w in v]
CATEGORY_NAMES = list(CATEGORIES.keys())

# ─────────────────────────────────────────
#  Character Configs
#  head_r  : head radius
#  neck_w  : half-width of neck rectangle
#  body_w  : half-width of torso at widest (belly bulge adds to this)
#  body_h  : torso height in pixels
#  leg_h   : leg height in pixels (body_bottom → sole)
#  arm_dx  : horizontal reach of upper arm
#  arm_dy  : vertical drop of upper arm
#  fore    : extra horizontal reach of forearm beyond arm_dx
#  shirt / shirtdk / pant / skin / hair : colours
# ─────────────────────────────────────────
CHAR_CFG = {
    # Johny – fit, 5'9" → slim shoulders, long legs
    "Johny": dict(head_r=15, neck_w=4, body_w=13, body_h=65, leg_h=90,
                  arm_dx=34, arm_dy=30, fore=13,
                  skin="#F5C5AE", hair="#3d2b1f",
                  shirt="#2980b9", shirtdk="#1a5276", pant="#2c3e50"),
    # Holly – tall + kinda fat → wide torso, long legs
    "Holly": dict(head_r=17, neck_w=5, body_w=21, body_h=70, leg_h=88,
                  arm_dx=42, arm_dy=34, fore=14,
                  skin="#F5D0BE", hair="#c0392b",
                  shirt="#e84393", shirtdk="#9b1a5c", pant="#6c3483"),
    # John  – fat + tall → very wide torso, big head, long legs
    "John":  dict(head_r=20, neck_w=7, body_w=26, body_h=72, leg_h=88,
                  arm_dx=48, arm_dy=38, fore=15,
                  skin="#F0C090", hair="#1a1a1a",
                  shirt="#27ae60", shirtdk="#1a7040", pant="#1a252f"),
    # Adam  – chubby, 5'8" → medium height, wide-ish torso
    "Adam":  dict(head_r=17, neck_w=5, body_w=19, body_h=62, leg_h=83,
                  arm_dx=38, arm_dy=30, fore=13,
                  skin="#F5C5AE", hair="#3d2b1f",
                  shirt="#8e44ad", shirtdk="#5e2d73", pant="#2c3e50"),
    # Addison – short, 5'5" → smaller overall
    "Addison": dict(head_r=14, neck_w=4, body_w=12, body_h=52, leg_h=73,
                    arm_dx=30, arm_dy=26, fore=12,
                    skin="#FDDBB4", hair="#8B4513",
                    shirt="#e67e22", shirtdk="#a04010", pant="#784212"),
    # Monkey – drawn separately
    "🐒 Monkey": None,
}
CHARS = list(CHAR_CFG.keys())

# ─────────────────────────────────────────
#  Layout / display constants
# ─────────────────────────────────────────
MAX_WRONG  = 6
CW, CH     = 340, 330
FIG_X      = 213
ROPE_Y     = 49
NECK_TOP   = 97      # y where noose meets the top of the neck

STARS = [(14,10),(42,26),(88,7),(138,19),(186,9),(223,30),(258,5),
         (28,50),(103,39),(198,21),(163,48),(53,17),(308,40),(280,68)]

BGTIMES = ["🌅 Morning", "☀️ Noon", "🌙 Night"]

# ─────────────────────────────────────────
#  Background helpers
# ─────────────────────────────────────────

def _draw_bg(c, tod):
    if tod == "🌙 Night":
        c.create_rectangle(0, 0, CW, CH, fill="#080814", outline="")
        c.create_rectangle(0, CH-55, CW, CH, fill="#0f0800", outline="")
        # crescent moon
        c.create_oval(268, 16, 308, 56, fill="#fffde7", outline="")
        c.create_oval(279, 12, 317, 50, fill="#080814", outline="")
        for sx, sy in STARS:
            c.create_oval(sx, sy, sx+2, sy+2, fill="#d0d8ff", outline="")
        c.create_rectangle(0, CH-30, CW, CH, fill="#0c0700", outline="")

    elif tod == "🌅 Morning":
        # simulated sunrise gradient with strips
        strips = ["#1a0533","#3d1259","#7a2552","#c44a3a",
                  "#e8703a","#f5a24a","#ffc86a","#ffe098"]
        sh = (CH - 30) // len(strips)
        for i, col in enumerate(strips):
            c.create_rectangle(0, i*sh, CW, (i+1)*sh+1, fill=col, outline="")
        # rising sun peeking at horizon (partially covered by ground)
        c.create_oval(CW//2-32, CH-62, CW//2+32, CH-4, fill="#ffdd00",
                      outline="#ffaa00", width=2)
        # horizon warm glow band
        c.create_rectangle(0, CH-42, CW, CH-30, fill="#ff9900", outline="")
        # ground
        c.create_rectangle(0, CH-30, CW, CH, fill="#1a0c00", outline="")

    elif tod == "☀️ Noon":
        # sky gradient: deeper blue top, lighter near horizon
        c.create_rectangle(0, 0, CW, int(CH*0.55), fill="#3a7bd5", outline="")
        c.create_rectangle(0, int(CH*0.55), CW, CH-30, fill="#87cefa", outline="")
        # bright sun (top-right corner where moon lives at night)
        c.create_oval(264, 10, 314, 60, fill="#ffe135", outline="#ffcc00", width=3)
        # sun inner disc highlight
        c.create_oval(274, 20, 304, 50, fill="#fff176", outline="")
        # clouds
        for bx, by, w, h in [(40,35,55,20),(160,18,60,18),(30,60,40,15)]:
            c.create_oval(bx, by, bx+w, by+h, fill="#ffffff", outline="")
            c.create_oval(bx+8, by-10, bx+w-8, by+8, fill="#ffffff", outline="")
        # green grass ground
        c.create_rectangle(0, CH-30, CW, CH, fill="#2d6a1a", outline="")
        c.create_rectangle(0, CH-32, CW, CH-27, fill="#3d8a22", outline="")


def _draw_gallows(c, tod):
    wood  = "#5c3010" if tod == "🌙 Night" else "#7a4520" if tod == "🌅 Morning" else "#8B5220"
    dark  = "#3a1c08" if tod == "🌙 Night" else "#4a2a10" if tod == "🌅 Morning" else "#6a3a10"
    rope  = "#6B5335"
    c.create_rectangle(12,  275, 162, 300, fill=wood, outline=dark)  # base
    c.create_rectangle(76,  36,  93,  280, fill=wood, outline=dark)  # pole
    c.create_rectangle(82,  30,  238, 50,  fill=wood, outline=dark)  # beam
    c.create_line(77, 38, 128, 31, fill=dark, width=3)               # brace
    c.create_line(FIG_X, ROPE_Y, FIG_X, 95, fill=rope, width=4)     # rope
    c.create_oval(FIG_X-7, 88, FIG_X+7, 102, outline=rope, width=3) # noose

# ─────────────────────────────────────────
#  Human figure helpers
# ─────────────────────────────────────────

def _h_coords(cfg):
    """Return (head_cy, body_top, body_bot) derived from cfg."""
    hcy = NECK_TOP + cfg['head_r'] + 5
    bt  = hcy + cfg['head_r'] + 2
    bb  = bt  + cfg['body_h']
    return hcy, bt, bb


def _h_head(c, cx, cfg, dead):
    hr  = cfg['head_r']
    hcy = NECK_TOP + hr + 5
    nw  = cfg['neck_w']
    sk  = cfg['skin']
    so  = "#C0876A"
    # neck
    c.create_rectangle(cx-nw, NECK_TOP, cx+nw, hcy-hr+2, fill=sk, outline="")
    # head oval
    c.create_oval(cx-hr, hcy-hr, cx+hr, hcy+hr, fill=sk, outline=so, width=2)
    # ears
    c.create_oval(cx-hr-5, hcy-5, cx-hr+1, hcy+6, fill=sk, outline=so)
    c.create_oval(cx+hr-1, hcy-5, cx+hr+5, hcy+6, fill=sk, outline=so)
    # hair tufts
    for hx in range(-hr+3, hr-2, 4):
        c.create_line(cx+hx, hcy-hr+2, cx+hx, hcy-hr-9,
                      fill=cfg['hair'], width=2, capstyle="round")
    # eye positions (slightly left-of-centre for worried look)
    le = cx - hr//2 - 2   # left-eye left edge
    re = cx + hr//8        # right-eye left edge
    ew = hr//2 + 1         # eye oval width

    if dead:
        for ex in [le, re]:
            c.create_line(ex, hcy-8, ex+ew, hcy-2, fill="#1a0800", width=2)
            c.create_line(ex+ew, hcy-8, ex, hcy-2, fill="#1a0800", width=2)
        c.create_arc(cx-6, hcy+4, cx+6, hcy+11,
                     start=0, extent=180, style=tk.ARC, outline="#5c1a00", width=2)
        c.create_oval(cx-3, hcy+9, cx+3, hcy+15, fill="#d63031", outline="#b71c1c")
    else:
        for ex in [le, re]:
            c.create_oval(ex, hcy-9, ex+ew+1, hcy-3, fill="white", outline="#aaa")
            c.create_oval(ex+2, hcy-8, ex+ew-1, hcy-5, fill="#1a1000", outline="")
        # worried eyebrows
        c.create_line(le-1, hcy-hr+4, le+ew+1, hcy-hr+7, fill=cfg['hair'], width=2)
        c.create_line(re-1, hcy-hr+7, re+ew+2, hcy-hr+4, fill=cfg['hair'], width=2)
        c.create_oval(cx-2, hcy-2, cx+2, hcy+2, fill="#E09888", outline="")
        c.create_arc(cx-5, hcy+5, cx+5, hcy+11,
                     start=200, extent=140, style=tk.ARC, outline="#8B4513", width=2)


def _h_body(c, cx, bt, bb, cfg):
    bw  = cfg['body_w']
    # belly bulge on wider characters
    bulge = max(0, bw - 14)
    mid   = (bt + bb) // 2
    pts   = [cx-bw, bt,  cx+bw, bt,
             cx+bw+bulge, mid,
             cx+bw, bb,  cx-bw, bb,
             cx-bw-bulge, mid]
    c.create_polygon(pts, fill=cfg['shirt'], outline=cfg['shirtdk'])
    # V-collar
    c.create_line(cx-bw//2, bt, cx, bt+14, cx+bw//2, bt,
                  fill=cfg['shirtdk'], width=2)
    # buttons
    for by in range(mid-6, bb-8, 13):
        c.create_oval(cx-3, by-3, cx+3, by+3, fill=cfg['shirtdk'], outline="")


def _h_arm(c, cx, side, bt, cfg):
    bw = cfg['body_w']
    sk = cfg['skin']
    sw = max(9, int(bw * 0.78))   # sleeve thickness scales with body
    x1 = cx + side * int(bw * 0.8)
    y1 = bt + 10
    x2 = cx + side * cfg['arm_dx']
    y2 = y1 + cfg['arm_dy']
    x3 = cx + side * (cfg['arm_dx'] + cfg['fore'])
    y3 = y2 + 22
    c.create_line(x1, y1, x2, y2, width=sw,  fill=cfg['shirt'], capstyle="round")
    c.create_line(x2, y2, x3, y3, width=6,   fill=sk,           capstyle="round")
    c.create_oval(x3-5, y3-4, x3+5, y3+4,   fill=sk, outline="#C0876A")


def _h_leg(c, cx, side, bb, cfg):
    bw = cfg['body_w']
    lh = cfg['leg_h']
    s  = side

    pb  = bb + int(lh * 0.62)   # pant hem / knee y
    fy  = bb + lh                # sole y

    xi  = cx + s * 2             # inner pant edge
    xo  = cx + s * bw            # outer pant edge
    xs  = cx + s * (bw + 5)      # shin x (slightly beyond outer edge)

    # pant leg polygon (slight taper inward at knee)
    c.create_polygon([xi, bb,  xo, bb,  xs, pb,  xi, pb],
                     fill=cfg['pant'], outline="#1a252f")
    # shin (skin)
    c.create_line(xs, pb, xs, fy-6, width=7, fill=cfg['skin'], capstyle="round")
    # sock
    c.create_line(xs, fy-14, xs, fy-6, width=9, fill="#e0e0e0", capstyle="round")
    # shoe
    sy = fy - 6
    if s < 0:
        shoe = [xs-16, sy,  xs+6, sy,  xs+8, fy,  xs-16, fy+2,  xs-20, sy+4]
    else:
        shoe = [xs-6,  sy,  xs+16, sy,  xs+20, sy+4,  xs+16, fy+2,  xs-8, fy]
    c.create_polygon(shoe, fill="#1a1a1a", outline="#0d0d0d")


def draw_human(c, wrong, dead, cfg):
    cx = FIG_X
    hcy, bt, bb = _h_coords(cfg)
    if wrong >= 1: _h_head(c, cx, cfg, dead)
    if wrong >= 2: _h_body(c, cx, bt, bb, cfg)
    if wrong >= 3: _h_arm(c, cx, -1, bt, cfg)
    if wrong >= 4: _h_arm(c, cx, +1, bt, cfg)
    if wrong >= 5: _h_leg(c, cx, -1, bb, cfg)
    if wrong >= 6: _h_leg(c, cx, +1, bb, cfg)


# ─────────────────────────────────────────
#  Monkey figure
# ─────────────────────────────────────────

def draw_monkey(c, wrong, dead):
    cx  = FIG_X
    FUR = "#8B4513"
    PAL = "#D2A679"   # palm / muzzle

    if wrong >= 1:
        # neck
        c.create_rectangle(cx-3, NECK_TOP, cx+3, 104, fill=FUR, outline="")
        # head (rounder, wider)
        c.create_oval(cx-19, 100, cx+19, 138, fill=FUR, outline="#6B3410", width=2)
        # big round ears
        for ex, ew in [(-30, 14), (16, 14)]:
            c.create_oval(cx+ex, 110, cx+ex+ew*2, 130, fill=FUR, outline="#6B3410")
            c.create_oval(cx+ex+3, 113, cx+ex+ew*2-3, 127, fill="#c47a52", outline="")
        # muzzle bump
        c.create_oval(cx-12, 120, cx+12, 137, fill=PAL, outline="#A0622A")
        # nostrils
        c.create_oval(cx-5, 124, cx-2, 128, fill="#5c2e00", outline="")
        c.create_oval(cx+2, 124, cx+5, 128, fill="#5c2e00", outline="")
        # eyes
        if dead:
            for ox in [cx-10, cx+4]:
                c.create_line(ox, 106, ox+6, 113, fill="#1a0800", width=2)
                c.create_line(ox+6, 106, ox, 113, fill="#1a0800", width=2)
        else:
            c.create_oval(cx-12, 106, cx-5,  114, fill="#FFD700", outline="#8B6914")
            c.create_oval(cx+5,  106, cx+12, 114, fill="#FFD700", outline="#8B6914")
            c.create_oval(cx-10, 108, cx-7,  112, fill="#1a0800", outline="")
            c.create_oval(cx+7,  108, cx+10, 112, fill="#1a0800", outline="")
        # mouth
        if dead:
            c.create_arc(cx-8, 129, cx+8, 137, start=0, extent=180,
                         style=tk.ARC, outline="#5c2e00", width=2)
        else:
            c.create_arc(cx-7, 128, cx+7, 135, start=200, extent=140,
                         style=tk.ARC, outline="#5c2e00", width=2)

    if wrong >= 2:
        # round body
        c.create_oval(cx-16, 137, cx+16, 197, fill=FUR, outline="#6B3410", width=2)
        # lighter belly patch
        c.create_oval(cx-9, 147, cx+9, 190, fill="#a0522d", outline="")

    if wrong >= 3:
        # left arm – long ape arm droops low
        c.create_line(cx-14, 148, cx-52, 205, width=11, fill=FUR, capstyle="round")
        c.create_line(cx-52, 205, cx-57, 240, width=9,  fill=FUR, capstyle="round")
        c.create_oval(cx-64, 235, cx-50, 247, fill=PAL, outline="#6B3410")

    if wrong >= 4:
        c.create_line(cx+14, 148, cx+52, 205, width=11, fill=FUR, capstyle="round")
        c.create_line(cx+52, 205, cx+57, 240, width=9,  fill=FUR, capstyle="round")
        c.create_oval(cx+50, 235, cx+64, 247, fill=PAL, outline="#6B3410")

    if wrong >= 5:
        # left leg (short, monkey-style)
        c.create_line(cx-9,  195, cx-16, 252, width=10, fill=FUR, capstyle="round")
        c.create_oval(cx-24, 247, cx-8,  259, fill=PAL, outline="#6B3410")

    if wrong >= 6:
        c.create_line(cx+9,  195, cx+16, 252, width=10, fill=FUR, capstyle="round")
        c.create_oval(cx+8,  247, cx+24, 259, fill=PAL, outline="#6B3410")
        # tail (curving from lower back)
        c.create_line(cx+14, 188, cx+42, 207, cx+58, 192, cx+54, 174,
                      fill=FUR, width=6, smooth=True, capstyle="round")


# ─────────────────────────────────────────
#  Master scene draw
# ─────────────────────────────────────────

def draw_scene(c, wrong, dead, tod, char):
    c.delete("all")
    _draw_bg(c, tod)
    _draw_gallows(c, tod)
    if char == "🐒 Monkey":
        draw_monkey(c, wrong, dead)
    else:
        draw_human(c, wrong, dead, CHAR_CFG[char])


# ─────────────────────────────────────────
#  App
# ─────────────────────────────────────────

class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚰  Hangman  ⚰")
        self.root.resizable(False, False)
        self.root.configure(bg="#080814")

        self.category_var = tk.StringVar(value=CATEGORY_NAMES[0])
        self.bg_var       = tk.StringVar(value="🌙 Night")
        self.char_var     = tk.StringVar(value="Johny")

        self.word = self.guessed = self.wrong = self.buttons = None
        self._build_ui()
        self._new_game()

    # ── UI construction ──────────────────────────────────────────────────

    def _build_ui(self):
        BG, DIM = "#080814", "#55557a"

        tk.Label(self.root, text="— H A N G M A N —",
                 font=("Georgia", 22, "bold"), bg=BG, fg="#e2b714").pack(pady=(14,0))
        tk.Label(self.root, text="guess the word before it's too late…",
                 font=("Georgia", 9, "italic"), bg=BG, fg="#33334a").pack(pady=(2,6))

        top = tk.Frame(self.root, bg=BG)
        top.pack(padx=20, pady=4)

        self.canvas = tk.Canvas(top, width=CW, height=CH, bg=BG,
                                highlightthickness=2, highlightbackground="#2d1800")
        self.canvas.pack(side=tk.LEFT, padx=(0,14))

        info = tk.Frame(top, bg=BG)
        info.pack(side=tk.LEFT, anchor="n", pady=6)

        def lbl(text, font, fg, **kw):
            return tk.Label(info, text=text, font=font, bg=BG, fg=fg, **kw)

        def section(text):
            lbl(text, ("Georgia", 8, "bold"), DIM).pack(anchor="w", pady=(6,0))

        def dropdown(var, choices, cmd, width=15):
            """Styled OptionMenu that matches the dark theme."""
            m = tk.OptionMenu(info, var, *choices, command=cmd)
            m.config(font=("Georgia", 9), bg="#16162a", fg="#7eb8d4",
                     activebackground="#e2b714", activeforeground="#080814",
                     highlightthickness=0, relief="flat", width=width)
            m["menu"].config(font=("Georgia", 9), bg="#16162a", fg="#c0c0e0",
                             activebackground="#e2b714", activeforeground="#080814",
                             tearoff=False)
            m.pack(anchor="w", pady=(3,0))
            return m

        # ── Background picker ─────────────────────────────────────────────
        section("BACKGROUND")
        dropdown(self.bg_var, BGTIMES,
                 lambda _: self._refresh_ui(), width=12)

        # ── Character picker ──────────────────────────────────────────────
        section("CHARACTER")
        dropdown(self.char_var, CHARS,
                 lambda _: self._refresh_ui(), width=12)

        # ── Category picker ───────────────────────────────────────────────
        section("CATEGORY")
        dropdown(self.category_var, CATEGORY_NAMES,
                 lambda _: self._new_game(), width=17)

        tk.Frame(info, bg="#1e1e30", height=1, width=165).pack(fill="x", pady=(10,4))

        # ── Stats ─────────────────────────────────────────────────────────
        section("WRONG GUESSES")
        self.wrong_label = lbl("", ("Courier", 13, "bold"), "#e63946",
                               wraplength=168, justify="left")
        self.wrong_label.pack(anchor="w", pady=(2,8))

        section("LIVES REMAINING")
        self.lives_label = lbl("", ("Helvetica", 14), "#e2b714")
        self.lives_label.pack(anchor="w", pady=(2,8))

        tk.Frame(info, bg="#1e1e30", height=1, width=165).pack(fill="x", pady=(2,6))

        section("STATUS")
        self.status_label = lbl("", ("Georgia", 10, "italic"), "#a8dadc",
                                wraplength=165, justify="left")
        self.status_label.pack(anchor="w", pady=(2,0))

        # ── Word display ──────────────────────────────────────────────────
        word_outer = tk.Frame(self.root, bg="#0f0a00", bd=2, relief="sunken")
        word_outer.pack(padx=24, pady=(6,8), fill="x")
        self.word_label = tk.Label(word_outer, text="",
                                   font=("Courier", 24, "bold"),
                                   bg="#0f0a00", fg="#f0e68c", pady=10, padx=12)
        self.word_label.pack()

        # ── Keyboard ──────────────────────────────────────────────────────
        kb = tk.Frame(self.root, bg=BG)
        kb.pack(padx=20, pady=(0,6))
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

        tk.Button(self.root, text="🔄  New Game",
                  font=("Georgia", 12, "bold"),
                  bg="#e2b714", fg="#080814", relief="flat",
                  padx=14, pady=7, cursor="hand2",
                  command=self._new_game).pack(pady=(4,14))

    # ── Game logic ───────────────────────────────────────────────────────

    def _new_game(self):
        pool = CATEGORIES[self.category_var.get()]
        self.word    = random.choice(pool).lower()
        self.guessed = set()
        self.wrong   = set()
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
        draw_scene(self.canvas, w, dead,
                   self.bg_var.get(), self.char_var.get())
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
            pl = "guess" if rem == 1 else "guesses"
            self.status_label.config(
                text=f"Keep going!\n{rem} wrong {pl} left.", fg="#a8dadc")

    def _check_end(self):
        win  = all(l in self.guessed for l in self.word)
        dead = len(self.wrong) >= MAX_WRONG
        if win or dead:
            for btn in self.buttons.values():
                btn.config(state=tk.DISABLED)
            if win:
                messagebox.showinfo("🎉  You Escaped!",
                    f"Brilliant! You guessed:\n\n  {self.word.upper()}"
                    "\n\nClick OK to play again.")
            else:
                messagebox.showerror("💀  You Were Hanged!",
                    f"The word was:\n\n  {self.word.upper()}"
                    "\n\nClick OK to try again.")
            self._new_game()


if __name__ == "__main__":
    root = tk.Tk()
    HangmanApp(root)
    root.mainloop()