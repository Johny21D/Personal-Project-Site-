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
CW, CH   = 360, 340      # canvas size (slightly wider for big characters)
FIG_X    = 220           # horizontal anchor (rope centre)
ROPE_Y   = 49            # top of rope / bottom of beam

# ─────────────────────────────────────────
#  Characters
# ─────────────────────────────────────────
CHARACTERS = {
    "Addison": {
        "weight_lbs": 165, "height_ft": "5'5\"",
        "sw": 0.80,  "sh": 0.92,          # width / height scale vs Johnny baseline
        "skin": "#F8D5B0", "hair": "#8B1A1A",
        "shirt": "#9b59b6", "pants": "#4a235a",
        "gender": "f",
        "btn_bg": "#3d1060", "btn_fg": "#f0c0ff",
    },
    "Johnny": {
        "weight_lbs": 180, "height_ft": "5'9\"",
        "sw": 1.00,  "sh": 1.00,
        "skin": "#C68642", "hair": "#1a1a1a",
        "shirt": "#c0392b", "pants": "#2c3e50",
        "gender": "m",
        "btn_bg": "#4a1500", "btn_fg": "#ffc8a0",
    },
    "Adam": {
        "weight_lbs": 220, "height_ft": "5'8\"",
        "sw": 1.30,  "sh": 0.99,
        "skin": "#D4956A", "hair": "#2c1810",
        "shirt": "#2471a3", "pants": "#1a252f",
        "gender": "m",
        "btn_bg": "#0d3060", "btn_fg": "#b0d8ff",
    },
    "Hollie": {
        "weight_lbs": 220, "height_ft": "5'10\"",
        "sw": 1.22,  "sh": 1.04,
        "skin": "#FFD8B1", "hair": "#DAA520",
        "shirt": "#d81b8a", "pants": "#4a0060",
        "gender": "f",
        "btn_bg": "#6a0050", "btn_fg": "#ffc0e0",
    },
    "John": {
        "weight_lbs": 260, "height_ft": "6'0\"",
        "sw": 1.60,  "sh": 1.08,
        "skin": "#FDBCB4", "hair": "#8B0000",
        "shirt": "#1e8449", "pants": "#145a32",
        "gender": "m",
        "btn_bg": "#0d3d1f", "btn_fg": "#a0f0c0",
    },
}

# ─────────────────────────────────────────
#  Time-of-day colour palettes
# ─────────────────────────────────────────
THEMES = {
    "night": {
        "root_bg": "#080814", "border": "#2d1800",
        "label_dim": "#55557a", "label_fg": "#e2b714",
        "status_fg": "#a8dadc", "word_bg": "#0f0a00", "word_fg": "#f0e68c",
        "title_fg": "#e2b714", "sub_fg": "#33334a",
        "btn_bg": "#16162a", "btn_fg": "#c0c0e0",
    },
    "morning": {
        "root_bg": "#1a0a2e", "border": "#6d4c41",
        "label_dim": "#8d6e63", "label_fg": "#ff8f00",
        "status_fg": "#ffcc80", "word_bg": "#120800", "word_fg": "#ffe082",
        "title_fg": "#ff8f00", "sub_fg": "#4e342e",
        "btn_bg": "#1c0f00", "btn_fg": "#ffcc80",
    },
    "day": {
        "root_bg": "#3a9bd5", "border": "#5d4037",
        "label_dim": "#1a5276", "label_fg": "#e65100",
        "status_fg": "#0d3349", "word_bg": "#fdf6e3", "word_fg": "#4a1500",
        "title_fg": "#bf360c", "sub_fg": "#78909c",
        "btn_bg": "#b3e5fc", "btn_fg": "#01579b",
    },
}

# ─────────────────────────────────────────
#  Colour utilities
# ─────────────────────────────────────────

def _adj(hex_col, factor):
    h = hex_col.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    r = min(255, max(0, int(r * factor)))
    g = min(255, max(0, int(g * factor)))
    b = min(255, max(0, int(b * factor)))
    return f"#{r:02x}{g:02x}{b:02x}"

def _dk(c): return _adj(c, 0.68)
def _lt(c): return _adj(c, 1.30)


# ─────────────────────────────────────────
#  Game logic
# ─────────────────────────────────────────

def choose_word():
    return random.choice(WORD_LIST).lower()

def build_display(word, guessed):
    return "  ".join(l.upper() if l in guessed else "_" for l in word)

def check_win(word, guessed):
    return all(l in guessed for l in word)


# ─────────────────────────────────────────
#  Body coordinate calculator
# ─────────────────────────────────────────

def compute_body(sw=1.0, sh=1.0):
    """Return a dict of all key figure coordinates scaled by sw (width) and sh (height)."""
    cx = FIG_X

    def iw(v): return max(1, int(v * sw))   # scale by width
    def ih(v): return max(1, int(v * sh))   # scale by height
    def iwa(v, mn): return max(mn, int(v * sw))
    def iha(v, mn): return max(mn, int(v * sh))

    # ── Neck ──────────────────────────────
    neck_top = 97
    neck_h   = iha(10, 7)
    neck_bot = neck_top + neck_h
    neck_hw  = iwa(4, 3)

    # ── Head ──────────────────────────────
    # head_rx uses a direct formula (NOT iwa) because sw is already embedded in it.
    # iwa would multiply by sw a second time, making heavy characters grotesquely wide.
    head_rx  = max(12, int(15 * (0.62 + 0.38 * sw)))   # heavier → wider face
    head_ry  = iha(16, 13)
    head_cy  = neck_bot + head_ry

    # ── Torso ─────────────────────────────
    torso_top = neck_bot + 2
    torso_hw  = iwa(13, 10)
    torso_h   = iha(68, 55)
    torso_bot = torso_top + torso_h

    # belly bulge for heavier characters (sw > 1.1) — direct formula, not iwa
    belly_extra = max(0, int((sw - 1.0) * 18))

    # ── Arms ──────────────────────────────
    shoulder_y    = torso_top + iha(10, 7)
    shoulder_hw   = iwa(10, 8)          # half-width at shoulder
    sleeve_dx     = iwa(24, 16)         # upper arm horizontal reach
    sleeve_dy     = iha(26, 20)         # upper arm vertical drop
    elbow_lx      = cx - shoulder_hw - sleeve_dx
    elbow_rx      = cx + shoulder_hw + sleeve_dx
    elbow_y       = shoulder_y + sleeve_dy
    fa_dx         = iwa(13, 9)          # forearm horizontal reach
    fa_dy         = iha(25, 20)         # forearm vertical drop
    lhand_x       = elbow_lx - fa_dx
    rhand_x       = elbow_rx + fa_dx
    hand_y        = elbow_y + fa_dy
    hand_r        = iwa(5, 4)
    arm_sleeve_w  = iwa(11, 7)
    arm_skin_w    = iwa(7, 5)

    # ── Legs ──────────────────────────────
    hip_y    = torso_bot
    leg_hw   = iwa(13, 10)              # pants half-width per leg
    pants_h  = iha(58, 48)
    knee_y   = hip_y + pants_h
    shin_dy  = iha(32, 26)
    ankle_y  = knee_y + shin_dy
    ankle_off = iha(4, 3)               # ankles splay out slightly
    leg_skin_w = iwa(7, 5)
    sock_w   = iwa(9, 7)

    # ── Shoe ──────────────────────────────
    shoe_ext  = iwa(14, 10)             # how far shoe sticks out
    shoe_toe  = iwa(3, 2)              # toe rise
    shoe_bot  = ankle_y + iha(10, 8)

    return dict(
        cx=cx, sw=sw, sh=sh,
        neck_top=neck_top, neck_bot=neck_bot, neck_hw=neck_hw,
        head_rx=head_rx, head_ry=head_ry, head_cy=head_cy,
        torso_top=torso_top, torso_hw=torso_hw, torso_h=torso_h,
        torso_bot=torso_bot, belly_extra=belly_extra,
        shoulder_y=shoulder_y, shoulder_hw=shoulder_hw,
        elbow_lx=elbow_lx, elbow_rx=elbow_rx, elbow_y=elbow_y,
        lhand_x=lhand_x, rhand_x=rhand_x, hand_y=hand_y,
        hand_r=hand_r, arm_sleeve_w=arm_sleeve_w, arm_skin_w=arm_skin_w,
        hip_y=hip_y, leg_hw=leg_hw, knee_y=knee_y,
        ankle_y=ankle_y, ankle_off=ankle_off,
        leg_skin_w=leg_skin_w, sock_w=sock_w,
        shoe_ext=shoe_ext, shoe_toe=shoe_toe, shoe_bot=shoe_bot,
    )


# ─────────────────────────────────────────
#  Main scene draw entry point
# ─────────────────────────────────────────

def draw_scene(canvas, wrong_count, time_of_day="night", char_key="Johnny", dead=False):
    c = canvas
    c.delete("all")
    char = CHARACTERS[char_key]
    b    = compute_body(char["sw"], char["sh"])

    # Sky
    if time_of_day == "night":   _draw_night_sky(c)
    elif time_of_day == "morning": _draw_morning_sky(c)
    else:                         _draw_day_sky(c)

    _draw_gallows(c)
    _draw_rope(c)

    if wrong_count >= 1: _draw_head(c, b, char, dead)
    if wrong_count >= 2: _draw_body(c, b, char)
    if wrong_count >= 3: _draw_left_arm(c, b, char)
    if wrong_count >= 4: _draw_right_arm(c, b, char)
    if wrong_count >= 5: _draw_left_leg(c, b, char)
    if wrong_count >= 6: _draw_right_leg(c, b, char)


# ─────────────────────────────────────────
#  Sky painters
# ─────────────────────────────────────────

def _draw_night_sky(c):
    c.create_rectangle(0, 0, CW, CH, fill="#080814", outline="")
    c.create_rectangle(0, CH-55, CW, CH, fill="#0f0800", outline="")
    c.create_rectangle(0, CH-57, CW, CH-52, fill="#1c0f00", outline="")
    # Crescent moon
    c.create_oval(278, 16, 318, 56, fill="#fffde7", outline="")
    c.create_oval(289, 12, 327, 50, fill="#080814", outline="")
    # Stars
    for sx,sy in [(14,10),(42,26),(88,7),(145,19),(192,9),(230,30),(265,5),
                  (28,50),(110,39),(204,21),(168,48),(55,17),(320,40),(286,68),
                  (72,30),(155,60),(240,45),(12,70),(308,20),(124,55)]:
        c.create_oval(sx, sy, sx+2, sy+2, fill="#d0d8ff", outline="")
    c.create_rectangle(0, CH-30, CW, CH, fill="#0c0700", outline="")
    c.create_line(0, CH-30, CW, CH-30, fill="#1e1000", width=2)


def _draw_morning_sky(c):
    for y1,y2,col in [(0,60,"#1a0a2e"),(60,120,"#6a1b4d"),
                      (120,180,"#c62828"),(180,230,"#ef6c00"),
                      (230,270,"#ff8f00"),(270,310,"#ffca28")]:
        c.create_rectangle(0, y1, CW, y2, fill=col, outline="")
    for sx,sy in [(14,10),(42,18),(92,7),(145,14),(195,9),(56,12),(12,22),(310,14)]:
        c.create_oval(sx, sy, sx+2, sy+2, fill="#e8d5ff", outline="")
    # Rising sun (right side)
    sx, sy = 308, 290
    for r,col in [(40,"#fff9c4"),(30,"#ffe57f"),(22,"#ffca28")]:
        c.create_arc(sx-r, sy-r, sx+r, sy+r, start=0, extent=180, fill=col, outline="")
    c.create_rectangle(0, 260, CW, 278, fill="#ffca28", outline="")
    c.create_rectangle(0, 270, CW, 310, fill="#ff8f00", outline="")
    for tx in [10,35,58,300,320,340]:
        c.create_polygon(tx,272, tx+10,250, tx+20,272, fill="#1a0a00", outline="")
    c.create_rectangle(0, CH-30, CW, CH, fill="#1b0000", outline="")
    c.create_line(0, CH-30, CW, CH-30, fill="#3e1010", width=2)


def _draw_day_sky(c):
    for y1,y2,col in [(0,50,"#2980b9"),(50,110,"#3a9bd5"),(110,180,"#52c2f5"),
                      (180,250,"#74d7f7"),(250,310,"#a8e6ff")]:
        c.create_rectangle(0, y1, CW, y2, fill=col, outline="")
    sx, sy = 310, 45
    for r,col in [(34,"#fff9c4"),(26,"#fff176"),(18,"#ffee58"),(12,"#ffd600")]:
        c.create_oval(sx-r, sy-r, sx+r, sy+r, fill=col, outline="")
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        c.create_line(sx+20*math.cos(a), sy+20*math.sin(a),
                      sx+34*math.cos(a), sy+34*math.sin(a),
                      fill="#ffd600", width=2, capstyle="round")
    def cloud(cx2,cy2,s=1.0):
        for bx,by,br in [(-28,6,22),(-10,0,28),(12,0,28),(30,6,22),(0,-8,22)]:
            r=int(br*s); bx2=int(bx*s); by2=int(by*s)
            c.create_oval(cx2+bx2-r,cy2+by2-r,cx2+bx2+r,cy2+by2+r,fill="white",outline="white")
    cloud(80,55,1.0); cloud(200,40,0.75); cloud(28,92,0.6)
    c.create_rectangle(0, CH-30, CW, CH, fill="#2e7d32", outline="")
    for gx in range(0, CW, 18):
        c.create_line(gx, CH-30, gx+8, CH, fill="#256427", width=1)


# ─────────────────────────────────────────
#  Gallows & Rope  (fixed, no per-character scaling)
# ─────────────────────────────────────────

def _draw_gallows(c):
    # Base log
    c.create_rectangle(12,290,162,304,fill="#2d1608",outline="")
    c.create_rectangle(12,280,162,290,fill="#5c3010",outline="")
    c.create_rectangle(12,277,162,281,fill="#7a4520",outline="")
    c.create_oval(9,276,20,304,fill="#4a2510",outline="#2d1608")
    c.create_oval(155,276,166,304,fill="#4a2510",outline="#2d1608")
    # Vertical pole
    c.create_rectangle(90,36,95,282,fill="#3a1c08",outline="")
    c.create_rectangle(78,36,90,282,fill="#5c3010",outline="")
    c.create_rectangle(78,36,82,282,fill="#7a4520",outline="")
    for gy in range(52,280,22):
        c.create_line(79,gy,94,gy+9,fill="#4a2510",width=1)
    # Horizontal beam
    c.create_rectangle(84,44,242,50,fill="#3a1c08",outline="")
    c.create_rectangle(84,33,242,44,fill="#5c3010",outline="")
    c.create_rectangle(84,30,242,34,fill="#7a4520",outline="")
    for gx in range(100,240,26):
        c.create_line(gx,31,gx+5,49,fill="#4a2510",width=1)
    # Diagonal brace
    c.create_polygon(79,38,95,38,132,31,129,42,fill="#4a2510",outline="#3a1c08",width=1)
    c.create_line(79,38,130,31,fill="#7a4520",width=1)
    # Bolts
    for bx,by in [(81,33),(232,33)]:
        c.create_oval(bx,by,bx+8,by+8,fill="#666",outline="#333")
        c.create_oval(bx+2,by+2,bx+6,by+6,fill="#aaa",outline="")


def _draw_rope(c):
    rx = FIG_X
    for i in range(10):
        y1=ROPE_Y+i*4; y2=y1+3
        tw=2 if i%2==0 else -2
        c.create_line(rx+tw,y1,rx-tw,y2,fill="#8B7355",width=3,capstyle="round")
    c.create_line(rx,89,rx,96,fill="#6B5335",width=4)
    c.create_oval(rx-7,88,rx+7,103,outline="#6B5335",width=3,fill="")


# ─────────────────────────────────────────
#  Figure part drawers (all parameterised)
# ─────────────────────────────────────────

def _draw_head(c, b, char, dead=False):
    cx   = b["cx"]
    cy   = b["head_cy"]
    rx   = b["head_rx"]
    ry   = b["head_ry"]
    sw   = b["sw"]
    skin = char["skin"]
    hair = char["hair"]
    gen  = char["gender"]

    # Neck
    c.create_rectangle(cx - b["neck_hw"], b["neck_top"],
                       cx + b["neck_hw"], b["neck_bot"],
                       fill=skin, outline="")
    # Drop shadow
    c.create_oval(cx-rx-2, cy-ry-3, cx+rx+4, cy+ry+5, fill="#04020a", outline="")
    # Head oval
    c.create_oval(cx-rx, cy-ry, cx+rx, cy+ry,
                  fill=skin, outline=_dk(skin), width=2)
    # Ears
    ew = max(4, int(5*sw))
    c.create_oval(cx-rx-ew, cy-ew, cx-rx, cy+ew, fill=_dk(skin), outline=_dk(skin))
    c.create_oval(cx+rx, cy-ew, cx+rx+ew, cy+ew,    fill=_dk(skin), outline=_dk(skin))

    # ── Hair ──────────────────────────────────────────────────
    hw = max(2, int(2.2*sw))   # hair strand width
    if gen == "f":
        # Crown strands
        for hx,extra in [(-rx+3,6),(-rx//2,9),(0,10),(rx//2,9),(rx-3,6)]:
            c.create_line(cx+hx, cy-ry+2, cx+hx, cy-ry-extra,
                          fill=hair, width=hw, capstyle="round")
        # Long side locks (down to shoulder area)
        lock_len = max(40, int(48 * b["sh"]))
        for lx_off in [cx-rx+3, cx-rx+9]:
            c.create_line(lx_off, cy, lx_off-4, cy+lock_len,
                          fill=hair, width=max(3,int(4*sw)), capstyle="round")
        for lx_off in [cx+rx-3, cx+rx-9]:
            c.create_line(lx_off, cy, lx_off+4, cy+lock_len,
                          fill=hair, width=max(3,int(4*sw)), capstyle="round")
    else:
        # Short male hair
        for hx,extra in [(-rx+3,6),(-rx//2+1,8),(0,9),(rx//2-1,8),(rx-3,6)]:
            c.create_line(cx+hx, cy-ry+2, cx+hx, cy-ry-extra,
                          fill=hair, width=hw, capstyle="round")

    # ── Face ──────────────────────────────────────────────────
    ey1 = cy - max(5, int(7*sw))
    ey2 = cy - max(1, int(1*sw))
    ew2 = max(5, int(7*sw))

    if dead:
        for ex in [cx - max(7,int(9*sw)), cx + max(2,int(4*sw))]:
            esz = max(4, int(5*sw))
            c.create_line(ex, ey1, ex+esz, ey2, fill="#1a0800", width=2)
            c.create_line(ex+esz, ey1, ex, ey2, fill="#1a0800", width=2)
        c.create_arc(cx-max(5,int(7*sw)), cy+max(3,int(5*sw)),
                     cx+max(5,int(7*sw)), cy+max(11,int(14*sw)),
                     start=0, extent=180, style=tk.ARC, outline="#5c1a00", width=2)
        c.create_oval(cx-max(3,int(4*sw)), cy+max(9,int(12*sw)),
                      cx+max(3,int(4*sw)), cy+max(16,int(19*sw)),
                      fill="#d63031", outline="#b71c1c")
    else:
        for ex in [cx-max(9,int(11*sw)), cx+max(2,int(4*sw))]:
            c.create_oval(ex, ey1, ex+ew2, ey2, fill="white", outline="#aaa")
            c.create_oval(ex+max(1,int(2*sw)), ey1+1, ex+max(4,int(5*sw)), ey2-1,
                          fill="#1a1000", outline="")
            c.create_oval(ex+max(1,int(2*sw)), ey1+1, ex+max(2,int(3*sw)), ey1+2,
                          fill="white", outline="")
        # Worried eyebrows
        by0 = ey1 - max(2,int(3*sw))
        c.create_line(cx-max(9,int(11*sw)), by0, cx-max(3,int(4*sw)), by0+2,
                      fill=_dk(hair), width=2)
        c.create_line(cx+max(3,int(4*sw)), by0+2, cx+max(9,int(11*sw)), by0,
                      fill=_dk(hair), width=2)
        # Nose
        nr = max(2, int(2*sw))
        c.create_oval(cx-nr, cy-nr, cx+nr, cy+nr, fill=_dk(skin), outline="")
        # Nervous frown
        c.create_arc(cx-max(5,int(6*sw)), cy+max(4,int(6*sw)),
                     cx+max(5,int(6*sw)), cy+max(11,int(13*sw)),
                     start=200, extent=140, style=tk.ARC, outline="#8B4513", width=2)


def _draw_body(c, b, char):
    cx  = b["cx"]
    tt  = b["torso_top"]
    tb  = b["torso_bot"]
    hw  = b["torso_hw"]
    bex = b["belly_extra"]   # belly bulge amount
    sw  = b["sw"]
    sh  = char["shirt"]
    mid = tt + (tb - tt) // 2   # vertical midpoint for belly

    # Torso polygon — bulges at belly for heavier builds
    outer = [
        cx-hw, tt,
        cx+hw, tt,
        cx+hw+bex, mid,
        cx+hw, tb,
        cx-hw, tb,
        cx-hw-bex, mid,
    ]
    c.create_polygon(outer, fill=sh, outline=_dk(sh), width=1)

    # Left highlight strip
    hl_pts = [
        cx-hw, tt,
        cx-hw+max(5,int(7*sw)), tt,
        cx-hw+max(4,int(6*sw))-bex//3, mid,
        cx-hw+max(5,int(7*sw)), tb,
        cx-hw, tb,
        cx-hw-bex, mid,
    ]
    c.create_polygon(hl_pts, fill=_lt(sh), outline="")

    # V-collar
    cw2 = max(6, int(8*sw))
    c.create_line(cx-cw2, tt, cx, tt+max(14,int(16*sw)), cx+cw2, tt,
                  fill=_dk(sh), width=2)

    # Buttons
    btn_gap = max(13, int(15*sw))
    btn_start = tt + max(20, int(22*sw))
    bsz = max(2, int(3*sw))
    for i in range(4):
        by = btn_start + i * btn_gap
        if by < tb - 4:
            c.create_oval(cx-bsz, by-bsz, cx+bsz, by+bsz,
                          fill=_dk(sh), outline=_dk(_dk(sh)))


def _draw_left_arm(c, b, char):
    cx  = b["cx"]
    sh  = char["shirt"]
    sk  = char["skin"]
    slw = b["arm_sleeve_w"]
    skw = b["arm_skin_w"]
    # Sleeve (upper arm) — two passes for highlight
    c.create_line(cx-b["shoulder_hw"], b["shoulder_y"],
                  b["elbow_lx"], b["elbow_y"],
                  width=slw+2, fill=sh,      capstyle="round")
    c.create_line(cx-b["shoulder_hw"], b["shoulder_y"],
                  b["elbow_lx"], b["elbow_y"],
                  width=slw-2, fill=_lt(sh), capstyle="round")
    # Forearm
    c.create_line(b["elbow_lx"], b["elbow_y"],
                  b["lhand_x"],  b["hand_y"],
                  width=skw, fill=sk, capstyle="round")
    # Hand
    hr = b["hand_r"]
    hx = b["lhand_x"]; hy = b["hand_y"]
    c.create_oval(hx-hr, hy-hr, hx+hr, hy+hr, fill=sk, outline=_dk(sk))


def _draw_right_arm(c, b, char):
    cx  = b["cx"]
    sh  = char["shirt"]
    sk  = char["skin"]
    slw = b["arm_sleeve_w"]
    skw = b["arm_skin_w"]
    c.create_line(cx+b["shoulder_hw"], b["shoulder_y"],
                  b["elbow_rx"], b["elbow_y"],
                  width=slw+2, fill=sh,      capstyle="round")
    c.create_line(cx+b["shoulder_hw"], b["shoulder_y"],
                  b["elbow_rx"], b["elbow_y"],
                  width=slw-2, fill=_lt(sh), capstyle="round")
    c.create_line(b["elbow_rx"], b["elbow_y"],
                  b["rhand_x"],  b["hand_y"],
                  width=skw, fill=sk, capstyle="round")
    hr = b["hand_r"]
    hx = b["rhand_x"]; hy = b["hand_y"]
    c.create_oval(hx-hr, hy-hr, hx+hr, hy+hr, fill=sk, outline=_dk(sk))


def _draw_left_leg(c, b, char):
    cx   = b["cx"]
    hw   = b["leg_hw"]
    hy   = b["hip_y"]
    ky   = b["knee_y"]
    ay   = b["ankle_y"]
    aoff = b["ankle_off"]
    sk   = char["skin"]
    pnt  = char["pants"]

    lax  = cx - aoff     # left ankle x (slightly left of centre)

    # Pants leg polygon
    c.create_polygon([cx-2, hy, cx-hw, hy, cx-hw-aoff, ky, cx-aoff, ky],
                     fill=pnt, outline=_dk(pnt))
    # Highlight strip on pants
    c.create_polygon([cx-2, hy, cx-hw//2, hy, cx-hw//2-aoff//2, ky, cx-aoff, ky],
                     fill=_lt(pnt), outline="")
    # Shin (skin)
    c.create_line(lax, ky, lax-aoff//2, ay, width=b["leg_skin_w"], fill=sk, capstyle="round")
    # Sock
    c.create_line(lax-aoff//2, ay-6, lax-aoff//2, ay+4,
                  width=b["sock_w"], fill="#e0e0e0", capstyle="round")
    # Shoe
    ext = b["shoe_ext"]
    bty = b["shoe_bot"]
    sx  = lax - aoff//2
    c.create_polygon([sx-ext, ay, sx+4, ay, sx+6, bty, sx-ext-2, bty+2, sx-ext-4, ay+4],
                     fill="#1a1a1a", outline="#0d0d0d")
    c.create_line(sx-ext, ay, sx+4, ay, fill="#333", width=1)


def _draw_right_leg(c, b, char):
    cx   = b["cx"]
    hw   = b["leg_hw"]
    hy   = b["hip_y"]
    ky   = b["knee_y"]
    ay   = b["ankle_y"]
    aoff = b["ankle_off"]
    sk   = char["skin"]
    pnt  = char["pants"]

    rax = cx + aoff

    c.create_polygon([cx+2, hy, cx+hw, hy, cx+hw+aoff, ky, cx+aoff, ky],
                     fill=pnt, outline=_dk(pnt))
    c.create_polygon([cx+hw//2, hy, cx+hw, hy, cx+hw+aoff, ky, cx+hw//2+aoff//2, ky],
                     fill=_lt(pnt), outline="")
    c.create_line(rax, ky, rax+aoff//2, ay, width=b["leg_skin_w"], fill=sk, capstyle="round")
    c.create_line(rax+aoff//2, ay-6, rax+aoff//2, ay+4,
                  width=b["sock_w"], fill="#e0e0e0", capstyle="round")
    ext = b["shoe_ext"]
    bty = b["shoe_bot"]
    sx  = rax + aoff//2
    c.create_polygon([sx-4, ay, sx+ext, ay, sx+ext+4, ay+4, sx+ext+2, bty+2, sx-6, bty],
                     fill="#1a1a1a", outline="#0d0d0d")
    c.create_line(sx-4, ay, sx+ext, ay, fill="#333", width=1)


# ─────────────────────────────────────────
#  Character selection dialog
# ─────────────────────────────────────────

class CharacterDialog(tk.Toplevel):
    def __init__(self, parent, current="Johnny"):
        super().__init__(parent)
        self.result = current
        self.title("🪢  Choose Your Victim")
        self.resizable(False, False)
        self.configure(bg="#0d0d1a")
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(self, text="🪢  Who Gets Hanged?",
                 font=("Georgia", 15, "bold"), bg="#0d0d1a", fg="#e2b714").pack(pady=(20,4))
        tk.Label(self, text="Their figure will reflect their real build.",
                 font=("Georgia", 9, "italic"), bg="#0d0d1a", fg="#44445a").pack(pady=(0,16))

        for name, ch in CHARACTERS.items():
            symbol = "♀" if ch["gender"] == "f" else "♂"
            lbl    = f"{symbol}  {name:<10}  {ch['weight_lbs']} lbs  •  {ch['height_ft']}"
            tk.Button(self, text=lbl,
                      font=("Courier", 11, "bold"),
                      bg=ch["btn_bg"], fg=ch["btn_fg"],
                      relief="flat", padx=16, pady=10,
                      cursor="hand2", width=28,
                      command=lambda n=name: self._pick(n)).pack(pady=4)

        tk.Frame(self, bg="#0d0d1a", height=16).pack()
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()//2  - self.winfo_width()//2
        py = parent.winfo_rooty() + parent.winfo_height()//2 - self.winfo_height()//2
        self.geometry(f"+{px}+{py}")
        parent.wait_window(self)

    def _pick(self, name):
        self.result = name
        self.destroy()


# ─────────────────────────────────────────
#  Time-of-day dialog
# ─────────────────────────────────────────

class TimeDialog(tk.Toplevel):
    OPTIONS = [
        ("night",   "🌙",  "Night",          "#1a1a3e", "#c0c8ff"),
        ("morning", "🌅",  "Morning  (Dawn)","#3e1500", "#ffcc80"),
        ("day",     "☀️",  "Day",             "#0d3b6e", "#aee6ff"),
    ]

    def __init__(self, parent, current="night"):
        super().__init__(parent)
        self.result = current
        self.title("⏰  Time of Day")
        self.resizable(False, False)
        self.configure(bg="#0d0d1a")
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(self, text="⏰  Choose the Time of Day",
                 font=("Georgia", 14, "bold"), bg="#0d0d1a", fg="#e2b714").pack(pady=(20,4))
        tk.Label(self, text="The sky and atmosphere will match your choice.",
                 font=("Georgia", 9, "italic"), bg="#0d0d1a", fg="#44445a").pack(pady=(0,16))

        for key, emoji, label, bg, fg in self.OPTIONS:
            tk.Button(self, text=f"{emoji}  {label}",
                      font=("Georgia", 12, "bold"),
                      bg=bg, fg=fg,
                      relief="flat", padx=24, pady=10,
                      cursor="hand2", width=22,
                      command=lambda k=key: self._pick(k)).pack(pady=5)

        tk.Frame(self, bg="#0d0d1a", height=14).pack()
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()//2  - self.winfo_width()//2
        py = parent.winfo_rooty() + parent.winfo_height()//2 - self.winfo_height()//2
        self.geometry(f"+{px}+{py}")
        parent.wait_window(self)

    def _pick(self, choice):
        self.result = choice
        self.destroy()


# ─────────────────────────────────────────
#  GUI App
# ─────────────────────────────────────────

class HangmanApp:
    def __init__(self, root):
        self.root        = root
        self.root.title("⚰  Hangman  ⚰")
        self.root.resizable(False, False)

        self.word        = ""
        self.guessed     = set()
        self.wrong       = set()
        self.buttons     = {}
        self.char_key    = "Johnny"
        self.time_of_day = "night"
        self.section_labels = []

        self._build_ui()

        # Ask character first, then time
        self._ask_character()
        self._ask_time()

        self._apply_theme()
        self._new_game()

    # ── Theme ──────────────────────────────────────────────────────────

    def _apply_theme(self):
        t  = THEMES[self.time_of_day]
        BG = t["root_bg"]
        self.root.configure(bg=BG)

        def recolour(w):
            cls = w.winfo_class()
            try:
                if cls in ("Label", "Frame"):
                    w.configure(bg=BG)
                if cls == "Canvas":
                    w.configure(bg=BG, highlightbackground=t["border"])
            except tk.TclError:
                pass
            for child in w.winfo_children():
                recolour(child)
        recolour(self.root)

        self.title_lbl.config(fg=t["title_fg"], bg=BG)
        self.sub_lbl.config(fg=t["sub_fg"], bg=BG)
        self.wrong_label.config(fg="#e63946", bg=BG)
        self.lives_label.config(fg=t["label_fg"], bg=BG)
        self.status_label.config(fg=t["status_fg"], bg=BG)
        self.victim_lbl.config(fg=t["label_fg"], bg=BG)
        self.word_outer.config(bg=t["word_bg"])
        self.word_label.config(bg=t["word_bg"], fg=t["word_fg"])
        for lbl in self.section_labels:
            lbl.config(bg=BG, fg=t["label_dim"])
        self.divider.config(bg=t["label_dim"])
        for btn in self.buttons.values():
            if btn.cget("state") == tk.NORMAL:
                btn.config(bg=t["btn_bg"], fg=t["btn_fg"])

    # ── UI Build ───────────────────────────────────────────────────────

    def _build_ui(self):
        BG = "#080814"; DIM = "#55557a"

        self.title_lbl = tk.Label(self.root, text="— H A N G M A N —",
                                  font=("Georgia", 22, "bold"), bg=BG, fg="#e2b714")
        self.title_lbl.pack(pady=(14, 0))

        self.sub_lbl = tk.Label(self.root,
                                text="guess the word before it's too late…",
                                font=("Georgia", 9, "italic"), bg=BG, fg="#33334a")
        self.sub_lbl.pack(pady=(2, 6))

        top = tk.Frame(self.root, bg=BG)
        top.pack(padx=20, pady=4)

        self.canvas = tk.Canvas(top, width=CW, height=CH, bg=BG,
                                highlightthickness=2, highlightbackground="#2d1800")
        self.canvas.pack(side=tk.LEFT, padx=(0, 14))

        info = tk.Frame(top, bg=BG)
        info.pack(side=tk.LEFT, anchor="n", pady=6)

        def section(text):
            lbl = tk.Label(info, text=text, font=("Georgia", 8, "bold"), bg=BG, fg=DIM)
            lbl.pack(anchor="w")
            self.section_labels.append(lbl)
            return lbl

        section("VICTIM")
        self.victim_lbl = tk.Label(info, text="",
                                   font=("Courier", 12, "bold"),
                                   bg=BG, fg="#e2b714", wraplength=170, justify="left")
        self.victim_lbl.pack(anchor="w", pady=(2, 12))

        section("WRONG GUESSES")
        self.wrong_label = tk.Label(info, text="", font=("Courier", 13, "bold"),
                                    bg=BG, fg="#e63946", wraplength=168, justify="left")
        self.wrong_label.pack(anchor="w", pady=(2, 12))

        section("LIVES REMAINING")
        self.lives_label = tk.Label(info, text="", font=("Helvetica", 14),
                                    bg=BG, fg="#e2b714")
        self.lives_label.pack(anchor="w", pady=(2, 12))

        section("CATEGORY")
        tk.Label(info, text="💻  Programming / Tech",
                 font=("Georgia", 10, "italic"), bg=BG, fg="#7eb8d4").pack(anchor="w", pady=(2,14))

        self.divider = tk.Frame(info, bg="#1e1e30", height=1, width=165)
        self.divider.pack(fill="x", pady=(0, 10))

        section("STATUS")
        self.status_label = tk.Label(info, text="",
                                     font=("Georgia", 10, "italic"),
                                     bg=BG, fg="#a8dadc",
                                     wraplength=165, justify="left")
        self.status_label.pack(anchor="w", pady=(2, 0))

        self.word_outer = tk.Frame(self.root, bg="#0f0a00", bd=2, relief="sunken")
        self.word_outer.pack(padx=24, pady=(6, 8), fill="x")
        self.word_label = tk.Label(self.word_outer, text="",
                                   font=("Courier", 24, "bold"),
                                   bg="#0f0a00", fg="#f0e68c", pady=10, padx=12)
        self.word_label.pack()

        kb = tk.Frame(self.root, bg=BG)
        kb.pack(padx=20, pady=(0, 6))
        for row_str in ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]:
            row = tk.Frame(kb, bg=BG)
            row.pack(pady=2)
            for ch in row_str:
                btn = tk.Button(row, text=ch, width=3, height=1,
                                font=("Helvetica", 10, "bold"),
                                bg="#16162a", fg="#c0c0e0",
                                relief="raised", bd=2, cursor="hand2",
                                command=lambda c=ch: self._on_guess(c.lower()))
                btn.pack(side=tk.LEFT, padx=2)
                self.buttons[ch] = btn

        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(pady=(4, 14))
        for txt, col, fg2, cmd in [
            ("🔄  New Game",        "#e2b714", "#080814", self._new_game),
            ("🧍  Change Victim",   "#444466", "#c0c8ff", self._change_character),
            ("⏰  Change Time",     "#334455", "#a0d8ff", self._change_time),
        ]:
            tk.Button(bottom, text=txt, font=("Georgia", 10, "bold"),
                      bg=col, fg=fg2, relief="flat", padx=10, pady=6,
                      cursor="hand2", command=cmd).pack(side=tk.LEFT, padx=4)

    # ── Dialog helpers ─────────────────────────────────────────────────

    def _ask_character(self):
        dlg = CharacterDialog(self.root, current=self.char_key)
        self.char_key = dlg.result
        self._update_victim_label()

    def _ask_time(self):
        dlg = TimeDialog(self.root, current=self.time_of_day)
        self.time_of_day = dlg.result

    def _change_character(self):
        self._ask_character()
        self._apply_theme()
        self._new_game()

    def _change_time(self):
        self._ask_time()
        self._apply_theme()
        self._refresh_ui()

    def _update_victim_label(self):
        ch = CHARACTERS[self.char_key]
        sym = "♀" if ch["gender"] == "f" else "♂"
        self.victim_lbl.config(
            text=f"{sym} {self.char_key}\n{ch['weight_lbs']} lbs • {ch['height_ft']}")

    # ── Game logic ─────────────────────────────────────────────────────

    def _new_game(self):
        self.word    = choose_word()
        self.guessed = set()
        self.wrong   = set()
        t = THEMES[self.time_of_day]
        for btn in self.buttons.values():
            btn.config(state=tk.NORMAL, bg=t["btn_bg"], fg=t["btn_fg"])
        self._update_victim_label()
        self._refresh_ui()

    def _on_guess(self, letter):
        if letter in self.guessed or letter in self.wrong:
            return
        if letter in self.word:
            self.guessed.add(letter)
            self.buttons[letter.upper()].config(state=tk.DISABLED, bg="#2a9d8f", fg="white")
        else:
            self.wrong.add(letter)
            self.buttons[letter.upper()].config(state=tk.DISABLED, bg="#e63946", fg="white")
        self._refresh_ui()
        self._check_end()

    def _refresh_ui(self):
        w       = len(self.wrong)
        is_dead = (w >= MAX_WRONG)
        is_win  = check_win(self.word, self.guessed)
        t       = THEMES[self.time_of_day]

        draw_scene(self.canvas, w, self.time_of_day, self.char_key, dead=is_dead)
        self.word_label.config(text=build_display(self.word, self.guessed))
        self.wrong_label.config(
            text="  ".join(sorted(self.wrong)).upper() if self.wrong else "—")

        remaining = MAX_WRONG - w
        self.lives_label.config(text="♥ " * remaining + "♡ " * w)

        if not self.wrong and not self.guessed:
            self.status_label.config(text="Guess a letter to begin!", fg=t["status_fg"])
        elif is_dead:
            self.status_label.config(text=f"💀 {self.char_key}\n    has been hanged!", fg="#e63946")
        elif is_win:
            self.status_label.config(text=f"🎉 {self.char_key}\n    escaped!", fg="#2a9d8f")
        else:
            pl = "guesses" if remaining != 1 else "guess"
            self.status_label.config(
                text=f"Keep going!\n{remaining} {pl} left.", fg=t["status_fg"])

    def _check_end(self):
        ch = CHARACTERS[self.char_key]
        if check_win(self.word, self.guessed):
            self._disable_all()
            messagebox.showinfo("🎉  Escape!",
                f"{self.char_key} lives another day!\n\nWord: {self.word.upper()}")
            self._new_game()
        elif len(self.wrong) >= MAX_WRONG:
            self._disable_all()
            messagebox.showerror("💀  Hanged!",
                f"{self.char_key} ({ch['weight_lbs']} lbs, {ch['height_ft']}) "
                f"has been hanged!\n\nWord: {self.word.upper()}")
            self._new_game()

    def _disable_all(self):
        for btn in self.buttons.values():
            btn.config(state=tk.DISABLED)


# ─────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────

def main():
    root = tk.Tk()
    HangmanApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()