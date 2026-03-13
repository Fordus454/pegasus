"""
Dungeon Master's Assistant v4.2
Unified grid layout – initiative tracker and attack columns share the same rows
as HP/Name/Init, so everything lines up visually.
"""
import random
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import os
import json

# ═══════════════════════════════════════════════════════════════════
# THEME - neutral dark grays, not purple
# ═══════════════════════════════════════════════════════════════════
BG_MAIN     = "#1a1a1a"      # Root window background
BG_FRAME    = "#242424"      # Panel background
BG_ENTRY    = "#2e2e2e"      # Entry fields
FG_TEXT     = "#d4d4d4"      # Default text
FG_HEADER   = "#e8c44a"      # Gold section headers
FG_PC       = "#5ba8e8"      # Player character names (blue)
FG_NPC      = "#5dba6e"      # NPC names (green)
FG_BBG      = "#e85b5b"      # BBG name (red)
FG_HP       = "#e06060"      # HP text
FG_SPELL    = "#bb86fc"      # Spell/ASI text (purple accent)
FG_INIT_DIM = "#555555"      # Dim initiative placeholder
FG_BTN      = "#d4d4d4"      # Button text
BG_BTN      = "#363636"      # Button background
BG_BTN_ACT  = "#d1b779"      # Button active/hover
FG_BTN_RED  = "#e85b5b"      # Destructive button text
FG_BTN_BLUE = "#5ba8e8"      # Save/load button text
BG_RESULT   = "#2a2a2a"      # Dice result backgrounds
FG_RESULT   = "#e0e0e0"      # Dice result text
BORDER_CLR  = "#3a3a3a"      # Border/separator color
BG_CHECKBOX = "#2e2e2e"      # Checkbox select color

# Initiative tier colors
INIT_HIGH = "#5ba8e8"   # >15 blue
INIT_MED  = "#5dba6e"   # >10 green
INIT_LOW  = "#e8c44a"   # >5  gold
INIT_VLOW = "#e85b5b"   # <=5 red

MAX_PCS  = 6
MAX_NPCS = 17   # index 0 = BBG, 1-16 = NPC 1..16

FONT        = ("Segoe UI", 11)
FONT_B      = ("Segoe UI", 11, "bold")
FONT_SM     = ("Segoe UI", 9)
FONT_SM_B   = ("Segoe UI", 9, "bold")
FONT_SM_I   = ("Segoe UI", 9, "italic")
FONT_XS     = ("Segoe UI", 8)
FONT_XS_B   = ("Segoe UI", 8, "bold")
FONT_XS_I   = ("Segoe UI", 8, "italic")
FONT_HEAD   = ("Segoe UI", 11, "bold underline")
FONT_DICE   = ("Segoe UI", 10, "bold")
FONT_MONO   = ("Consolas", 11, "bold")

SAVES_DIR = "Saves"

# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════
def safe_int(value, default=0):
    try:
        if isinstance(value, str) and value.strip() in ("", "-0-", "nan"):
            return default
        if pd.isna(value):
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default

def entry_set(entry, value):
    entry.delete(0, tk.END)
    entry.insert(0, str(value))

def init_color(total):
    if total > 15: return INIT_HIGH
    if total > 10: return INIT_MED
    if total > 5:  return INIT_LOW
    return INIT_VLOW


# ═══════════════════════════════════════════════════════════════════
# MAIN CLASS
# ═══════════════════════════════════════════════════════════════════
class DungeonMasterAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon Master's Assistant  v4.3")
        self.root.configure(bg=BG_MAIN)
        os.makedirs(SAVES_DIR, exist_ok=True)

        # Widget storage
        self.pc_names = [];  self.pc_inits = [];  self.pc_hp = []
        self.npc_names = []; self.npc_inits = []; self.npc_hp = []
        self.npc_atk1 = [];  self.npc_atk2 = []
        self.init_labels = []
        self.spell_entries = []
        self.spell_slot_vars = []
        self.lair_entries = []
        self.legendary_vars = []
        self.asi_entries = {}
        self.asi_total_labels = {}
        self.prof_vars = {}

        # Will be set during build
        self.dice_mod = None
        self.npc_atk_mod = None
        self.npc_init_mod = None
        self.prof_entry = None
        self.prof_level_lbl = None
        self.dice_mults = {}
        self.dice_results = {}

        self._build()
        self._auto_resize()

    # ───────────────────────────────────────────────────────────────
    # Widget factories
    # ───────────────────────────────────────────────────────────────
    def _entry(self, parent, width=5, font=FONT, fg=FG_TEXT, bg=BG_ENTRY, **kw):
        return tk.Entry(parent, width=width, font=font, fg=fg, bg=bg,
                        insertbackground=fg, bd=1, relief="sunken",
                        selectbackground="#4a4a4a", selectforeground="#ffffff", **kw)

    def _label(self, parent, text="", font=FONT, fg=FG_TEXT, bg=None, **kw):
        return tk.Label(parent, text=text, font=font, fg=fg,
                        bg=bg or parent.cget("bg"), **kw)

    def _button(self, parent, text, cmd, fg=FG_BTN, width=14, font=FONT, **kw):
        return tk.Button(parent, text=text, command=cmd, font=font, width=width,
                         fg=fg, bg=BG_BTN, activebackground=BG_BTN_ACT,
                         activeforeground="#1a1a1a", bd=2, relief="raised",
                         cursor="hand2", **kw)

    # ───────────────────────────────────────────────────────────────
    # MASTER LAYOUT
    #
    # TOP ROW:   [Modifiers] [Dice]                        [Spells/ASI]
    # BOTTOM:    [HP|Name|Init | Initiative | Atk1 | Atk2] [Spells cont]
    #
    # The key change: combatant rows, initiative labels, and attack
    # labels all live in ONE grid so rows are guaranteed to align.
    # ───────────────────────────────────────────────────────────────
    def _build(self):
        # ── Bottom buttons – pack FIRST so they're never clipped ──
        btn_bar = tk.Frame(self.root, bg=BG_FRAME, bd=1, relief="groove")
        btn_bar.pack(side="bottom", fill="x", padx=4, pady=4)
        self._build_buttons(btn_bar)

        content = tk.Frame(self.root, bg=BG_MAIN)
        content.pack(fill="both", expand=True, padx=4, pady=(4, 0))

        # ── Left side: modifiers+dice on top, unified grid below ──
        left = tk.Frame(content, bg=BG_MAIN)
        left.pack(side="left", fill="both", expand=True)

        top_row = tk.Frame(left, bg=BG_MAIN)
        top_row.pack(fill="x", pady=(0, 2))

        self._build_modifiers(top_row)
        self._build_dice(top_row)

        # ── Unified combatant grid (HP/Name/Init + Initiative + Attacks) ──
        self._build_unified_grid(left)

        # ── Right side: Spells & ASI ──
        col_right = tk.Frame(content, bg=BG_FRAME, bd=1, relief="groove",
                             highlightbackground=BORDER_CLR, highlightthickness=1)
        col_right.pack(side="left", fill="y", padx=(2, 0))
        self._build_spells_asi(col_right)

    # ───────────────────────────────────────────────────────────────
    # TOP LEFT: Modifiers
    # ───────────────────────────────────────────────────────────────
    def _build_modifiers(self, parent):
        frame = tk.Frame(parent, bg=BG_FRAME, bd=1, relief="groove",
                         highlightbackground=BORDER_CLR, highlightthickness=1)
        frame.pack(side="left", fill="y", padx=(0, 2))

        self._label(frame, "  Modifiers  ", font=FONT_HEAD, fg=FG_HEADER).grid(
            row=0, column=0, columnspan=2, pady=(0, 4))

        labels = ["Dice Modifier:", "NPC HP & Attack Mod:", "NPC Initiative Modifier:"]
        defaults = ["0", "4", "2"]
        entries = []
        for i, (txt, dflt) in enumerate(zip(labels, defaults)):
            self._label(frame, txt, font=FONT_SM).grid(row=i+1, column=0, sticky="e", padx=(8, 4), pady=2)
            e = self._entry(frame, width=4, font=FONT)
            e.grid(row=i+1, column=1, sticky="w", padx=(0, 8), pady=2)
            entry_set(e, dflt)
            entries.append(e)
        self.dice_mod, self.npc_atk_mod, self.npc_init_mod = entries

        self._button(frame, "Set HP", self.set_npc_hp, fg=FG_BTN_BLUE,
                     width=8, font=FONT_SM_B).grid(row=4, column=0, columnspan=2, pady=(4, 6))

    # ───────────────────────────────────────────────────────────────
    # TOP LEFT: Dice Rollers
    # ───────────────────────────────────────────────────────────────
    def _build_dice(self, parent):
        frame = tk.Frame(parent, bg=BG_FRAME, bd=1, relief="groove",
                         highlightbackground=BORDER_CLR, highlightthickness=1)
        frame.pack(side="left", fill="y", padx=2)

        # D20 rows
        for i, txt in enumerate(["Roll 1st D20", "Roll 2nd D20"]):
            key = f"d20_{i+1}"
            self._button(frame, txt, lambda k=key: self._roll_d20(k),
                         width=13, font=FONT_DICE).grid(row=i, column=0, sticky="e", padx=(4, 2), pady=2)
            lbl = self._label(frame, "", font=FONT_MONO, fg=FG_RESULT, bg=BG_RESULT, width=12, anchor="w")
            lbl.grid(row=i, column=1, columnspan=3, sticky="w", padx=(2, 4), pady=2)
            self.dice_results[key] = lbl

        # D100
        self._button(frame, "Roll D100", self._roll_d100,
                     width=13, font=FONT_DICE).grid(row=2, column=0, sticky="e", padx=(4, 2), pady=2)
        lbl = self._label(frame, "", font=FONT_MONO, fg=FG_RESULT, bg=BG_RESULT, width=12, anchor="w")
        lbl.grid(row=2, column=1, columnspan=3, sticky="w", padx=(2, 4), pady=2)
        self.dice_results["d100"] = lbl

        # Multi-dice: D4, D6, D8, D10, D12
        for idx, sides in enumerate([4, 6, 8, 10, 12]):
            r = idx + 3
            key = f"d{sides}"
            mult = self._entry(frame, width=3, font=FONT_DICE)
            mult.grid(row=r, column=0, sticky="e", padx=(8, 0), pady=2); entry_set(mult, "1")
            self.dice_mults[key] = mult
            self._label(frame, "x", font=FONT_DICE).grid(row=r, column=1, padx=2)
            self._button(frame, f"D{sides}", lambda s=sides, k=key: self._roll_multi(s, k),
                         width=5, font=FONT_DICE).grid(row=r, column=2, padx=(0, 2), pady=2)
            lbl = self._label(frame, "", font=FONT_MONO, fg=FG_RESULT, bg=BG_RESULT, width=12, anchor="w")
            lbl.grid(row=r, column=3, sticky="w", padx=(2, 4), pady=2)
            self.dice_results[key] = lbl

    # ───────────────────────────────────────────────────────────────
    # UNIFIED GRID: Initiative + Combatants + Attacks in one frame
    #
    # Columns: 0=Initiative  1=Init  2=Name  3=HP  |  4=Atk1  5=Atk2
    # Row 0: Headers
    # Rows 1-6: PCs (attacks columns blank for PCs)
    # Rows 7-23: NPCs (all columns active)
    # ───────────────────────────────────────────────────────────────
    def _build_unified_grid(self, parent):
        frame = tk.Frame(parent, bg=BG_FRAME, bd=1, relief="groove",
                         highlightbackground=BORDER_CLR, highlightthickness=1)
        frame.pack(fill="both", expand=True, padx=0, pady=0)
        self._grid_frame = frame

        # Column config: Name column stretches, initiative stays compact
        frame.columnconfigure(2, weight=1)  # Name

        # ── Row 0: Headers ──
        headers = [
            (0, "Initiative",     22),
            (1, "Init",           5),
            (2, "Name",           18),
            (3, "HP",             6),
            (4, "First Attack",   14),
            (5, "Second Attack",  14),
        ]
        for col, txt, _ in headers:
            self._label(frame, txt, font=FONT_HEAD, fg=FG_HEADER).grid(
                row=0, column=col, padx=3, pady=(2, 2))

        # ── PC rows (rows 1..MAX_PCS) ──
        for i in range(MAX_PCS):
            r = i + 1

            # Initiative label (col 0)
            lbl = self._label(frame, "- initiative -", font=FONT_SM, fg=FG_INIT_DIM,
                              anchor="w", width=15)
            lbl.grid(row=r, column=0, sticky="w", padx=6, pady=0)
            self.init_labels.append(lbl)

            # Init entry (col 1)
            ini = self._entry(frame, width=5, font=FONT)
            ini.grid(row=r, column=1, padx=3, pady=1, sticky="ew")
            entry_set(ini, "0")
            self.pc_inits.append(ini)

            # Name entry (col 2)
            nm = self._entry(frame, width=18, font=FONT_B, fg=FG_PC)
            nm.grid(row=r, column=2, padx=3, pady=1, sticky="ew")
            entry_set(nm, f"Player {i+1}")
            self.pc_names.append(nm)

            # HP entry (col 3)
            hp = self._entry(frame, width=5, font=FONT_B, fg=FG_HP, bg="#2a2020")
            hp.grid(row=r, column=3, padx=3, pady=1, sticky="ew")
            entry_set(hp, "-0-")
            self.pc_hp.append(hp)

            # PCs don't have attack columns – leave blank

        # ── NPC rows (rows MAX_PCS+1 .. MAX_PCS+MAX_NPCS) ──
        npc_start = MAX_PCS + 1
        for i in range(MAX_NPCS):
            r = npc_start + i

            # Initiative label (col 0)
            lbl = self._label(frame, "- initiative -", font=FONT_SM, fg=FG_INIT_DIM,
                              anchor="w", width=15)
            lbl.grid(row=r, column=0, sticky="w", padx=6, pady=0)
            self.init_labels.append(lbl)

            # Init entry (col 1)
            ini = self._entry(frame, width=5, font=FONT)
            ini.grid(row=r, column=1, padx=3, pady=1, sticky="ew")
            self.npc_inits.append(ini)

            # Name entry (col 2)
            dflt = "BBG" if i == 0 else f"NPC {i}"
            clr = FG_BBG if i == 0 else FG_NPC
            nm = self._entry(frame, width=18, font=FONT_B, fg=clr)
            nm.grid(row=r, column=2, padx=3, pady=1, sticky="ew")
            entry_set(nm, dflt)
            self.npc_names.append(nm)

            # HP entry (col 3)
            hp = self._entry(frame, width=5, font=FONT_B, fg=FG_HP, bg="#202a20")
            hp.grid(row=r, column=3, padx=3, pady=1, sticky="ew")
            entry_set(hp, "0")
            self.npc_hp.append(hp)

            # Attack labels (cols 4-5) – aligned to the same row
            a1 = self._label(frame, "", font=FONT_MONO, fg=FG_RESULT, bg=BG_RESULT,
                             width=14, anchor="w")
            a1.grid(row=r, column=4, padx=3, pady=1)
            self.npc_atk1.append(a1)

            a2 = self._label(frame, "", font=FONT_MONO, fg=FG_RESULT, bg=BG_RESULT,
                             width=14, anchor="w")
            a2.grid(row=r, column=5, padx=3, pady=1)
            self.npc_atk2.append(a2)

    # ───────────────────────────────────────────────────────────────
    # Auto-resize window height based on visible NPC rows
    # ───────────────────────────────────────────────────────────────
    def _auto_resize(self):
        """Resize window to fit content naturally using actual widget measurements."""
        self.root.update_idletasks()
        # Ask tkinter what height the root actually needs
        needed = self.root.winfo_reqheight()
        # Add a small buffer (~2 rows worth)
        h = needed + 52
        w = max(1060, self.root.winfo_reqwidth())
        self.root.geometry(f"{w}x{h}")
        self.root.minsize(w, 500)

    # ───────────────────────────────────────────────────────────────
    # COL RIGHT: Spells & ASI (unchanged from v4.1)
    # ───────────────────────────────────────────────────────────────
    def _build_spells_asi(self, parent):
        # ── TOP: Spells header + ASI controls + prof ──
        top = tk.Frame(parent, bg=BG_FRAME)
        top.pack(fill="x", padx=4, pady=(4, 0))

        self._label(top, "Spells", font=FONT_HEAD, fg=FG_HEADER).grid(
            row=0, column=0, columnspan=3, sticky="w")

        self._button(top, "ASI reset", self.reset_asi, width=7, font=FONT_XS).grid(
            row=0, column=3, padx=2)
        self._button(top, "prof", self.calc_asi, width=4, font=FONT_XS).grid(
            row=0, column=4, padx=1)
        self._label(top, "prof:", font=FONT_XS_I).grid(row=0, column=5, padx=(4, 1))
        self.prof_entry = self._entry(top, width=2, font=FONT_XS)
        self.prof_entry.grid(row=0, column=6, padx=(0, 4))
        entry_set(self.prof_entry, "2")

        # ── ASI stat rows alongside cantrips (6 rows) ──
        mid = tk.Frame(parent, bg=BG_FRAME)
        mid.pack(fill="x", padx=4, pady=0)

        stats = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        for i in range(6):
            sp = self._entry(mid, width=10, font=FONT_XS_I, fg=FG_SPELL)
            sp.grid(row=i, column=0, sticky="e", padx=(0, 4), pady=1)
            entry_set(sp, "Cantrip")
            self.spell_entries.append(sp)

            stat = stats[i]
            self._label(mid, f"{stat}:", font=FONT_XS_B, fg=FG_SPELL).grid(
                row=i, column=1, sticky="e", padx=2)
            e = self._entry(mid, width=3, font=FONT_XS, fg=FG_SPELL)
            e.grid(row=i, column=2, padx=1, pady=1); entry_set(e, "10")
            self.asi_entries[stat] = e

            var = tk.IntVar()
            tk.Checkbutton(mid, variable=var, bg=BG_FRAME, activebackground=BG_FRAME,
                           selectcolor=BG_CHECKBOX, fg=FG_SPELL, bd=0).grid(
                row=i, column=3, padx=1)
            self.prof_vars[stat] = var

            tot = self._label(mid, "-click 'prof'-", font=FONT_XS_I, fg="#666666")
            tot.grid(row=i, column=4, sticky="w", padx=2)
            self.asi_total_labels[stat] = tot

        self.prof_level_lbl = self._label(mid, "", font=FONT_XS_I, fg=FG_NPC)
        self.prof_level_lbl.grid(row=6, column=1, columnspan=4, sticky="w", padx=4, pady=(2, 0))

        # ── Leveled spells with slot checkboxes ──
        sp_frame = tk.Frame(parent, bg=BG_FRAME)
        sp_frame.pack(fill="x", padx=4, pady=0)

        slot_counts = [4, 3, 3, 3, 2, 2, 2, 2, 2]

        for lvl_idx in range(9):
            r = lvl_idx
            sp = self._entry(sp_frame, width=10, font=FONT_XS_I, fg=FG_SPELL)
            sp.grid(row=r, column=0, sticky="e", padx=(0, 2), pady=1)
            entry_set(sp, "Spell")
            self.spell_entries.append(sp)

            self._label(sp_frame, f"Lvl {lvl_idx+1}", font=FONT_XS_B, fg=FG_SPELL).grid(
                row=r, column=1, sticky="e", padx=2)

            for s in range(slot_counts[lvl_idx]):
                var = tk.IntVar()
                tk.Checkbutton(sp_frame, variable=var, bg=BG_FRAME,
                               activebackground=BG_FRAME, selectcolor=BG_CHECKBOX,
                               fg=FG_SPELL, bd=0).grid(row=r, column=2+s, padx=0)
                self.spell_slot_vars.append(var)

        # ── Additional spell slots (below Lvl 9, no checkboxes) ──
        extra_frame = tk.Frame(parent, bg=BG_FRAME)
        extra_frame.pack(fill="x", padx=4, pady=0)

        for i in range(8):
            sp = self._entry(extra_frame, width=10, font=FONT_XS_I, fg=FG_SPELL)
            sp.grid(row=i, column=0, sticky="e", padx=(0, 4), pady=1)
            entry_set(sp, "Spell")
            self.spell_entries.append(sp)

        # ── Lair Actions ──
        lair_frame = tk.Frame(parent, bg=BG_FRAME)
        lair_frame.pack(fill="x", padx=4, pady=(4, 0))

        for i in range(3):
            self._label(lair_frame, "Lair Action Init", font=FONT_XS_B, fg=FG_NPC).grid(
                row=i, column=0, sticky="e", padx=2, pady=1)
            e = self._entry(lair_frame, width=4, font=FONT_XS, fg=FG_NPC)
            e.grid(row=i, column=1, sticky="w", padx=2, pady=1)
            self.lair_entries.append(e)

        # ── Legendary Resistance ──
        lr_frame = tk.Frame(parent, bg=BG_FRAME)
        lr_frame.pack(fill="x", padx=4, pady=(4, 8))
        self._label(lr_frame, "Legendary Resistance:", font=FONT_XS_B, fg=FG_NPC).grid(
            row=0, column=0, sticky="e", padx=2)
        for i in range(3):
            var = tk.IntVar()
            tk.Checkbutton(lr_frame, variable=var, bg=BG_FRAME,
                           activebackground=BG_FRAME, selectcolor=BG_CHECKBOX,
                           fg=FG_NPC, bd=0).grid(row=0, column=1+i, padx=1)
            self.legendary_vars.append(var)

    # ───────────────────────────────────────────────────────────────
    # BOTTOM: Action Buttons
    # ───────────────────────────────────────────────────────────────
    def _build_buttons(self, parent):
        buttons = [
            ("Reset NPC Rolls", self.clear_npc_rolls,  FG_BTN_RED,  14),
            ("Roll NPC Initiative", self.roll_all_init, FG_BTN,      16),
            ("Re-Sort",         self.sort_initiative,   FG_BTN,      8),
            ("Roll 1st Attack", self.roll_atk1,         FG_BTN,      12),
            ("Roll 2nd Attack", self.roll_atk2,         FG_BTN,      12),
            ("Clear HP",        self.clear_npc_hp,      FG_BTN_RED,  8),
            ("Add NPC",         self.add_npc,           FG_BTN,      8),
            ("Remove NPC",      self.remove_npc,        FG_BTN_RED,  10),
            ("Save",            self.save_data,         FG_BTN_BLUE, 8),
            ("Load",            self.load_data,         FG_BTN_BLUE, 8),
        ]
        for i, (txt, cmd, fg, w) in enumerate(buttons):
            b = self._button(parent, txt, cmd, fg=fg, width=w, font=FONT_SM_B)
            b.grid(row=0, column=i, padx=3, pady=4)

    # ═══════════════════════════════════════════════════════════════
    # DICE FUNCTIONS
    # ═══════════════════════════════════════════════════════════════
    def _get_mod(self):
        return safe_int(self.dice_mod.get(), 0)

    def _roll_d20(self, key):
        mod = self._get_mod()
        roll = random.randint(1, 20)
        total = roll + mod
        self.dice_results[key].config(text=f" {roll}+{mod} = {total}")

    def _roll_d100(self):
        self.dice_results["d100"].config(text=f" {random.randint(1, 100)}")

    def _roll_multi(self, sides, key):
        mod = self._get_mod()
        mult = max(1, safe_int(self.dice_mults[key].get(), 1))
        roll_sum = sum(random.randint(1, sides) for _ in range(mult))
        total = roll_sum + mod
        self.dice_results[key].config(text=f" {roll_sum}+{mod} = {total}")

    # ═══════════════════════════════════════════════════════════════
    # INITIATIVE
    # ═══════════════════════════════════════════════════════════════
    def roll_all_init(self):
        mod = safe_int(self.npc_init_mod.get(), 0)
        for i in range(MAX_NPCS):
            if self.npc_names[i].get().strip():
                roll = random.randint(1, 20)
                total = roll + mod
                entry_set(self.npc_inits[i], total)
                self.npc_inits[i].config(fg=init_color(total))
        self.sort_initiative()

    def sort_initiative(self):
        items = []
        for i in range(MAX_PCS):
            name = self.pc_names[i].get().strip()
            if name:
                items.append((name, safe_int(self.pc_inits[i].get()), "pc"))
        for i in range(MAX_NPCS):
            name = self.npc_names[i].get().strip()
            if name:
                items.append((name, safe_int(self.npc_inits[i].get()), "npc"))

        items.sort(key=lambda x: x[1], reverse=True)

        for i, lbl in enumerate(self.init_labels):
            if i < len(items):
                name, val, kind = items[i]
                fg = FG_PC if kind == "pc" else init_color(val)
                lbl.config(text=f"{name} - {val}", fg=fg)
            else:
                lbl.config(text="- initiative -", fg=FG_INIT_DIM)

    # ═══════════════════════════════════════════════════════════════
    # ATTACKS
    # ═══════════════════════════════════════════════════════════════
    def _roll_atk_generic(self, labels):
        mod = safe_int(self.npc_atk_mod.get(), 0)
        for i in range(MAX_NPCS):
            if self.npc_names[i].get().strip():
                roll = random.randint(1, 20)
                labels[i].config(text=f" {roll}+{mod} = {roll+mod}")
            else:
                labels[i].config(text="")

    def roll_atk1(self): self._roll_atk_generic(self.npc_atk1)
    def roll_atk2(self): self._roll_atk_generic(self.npc_atk2)

    # ═══════════════════════════════════════════════════════════════
    # NPC MANAGEMENT
    # ═══════════════════════════════════════════════════════════════
    def add_npc(self):
        for i in range(1, MAX_NPCS):
            if not self.npc_names[i].get().strip():
                entry_set(self.npc_names[i], f"NPC {i}")
                self._auto_resize()
                return

    def remove_npc(self):
        for i in range(MAX_NPCS - 1, 0, -1):
            if self.npc_names[i].get().strip():
                entry_set(self.npc_names[i], "")
                entry_set(self.npc_inits[i], "")
                entry_set(self.npc_hp[i], "0")
                self.npc_atk1[i].config(text="")
                self.npc_atk2[i].config(text="")
                self._auto_resize()
                return

    def clear_npc_rolls(self):
        for i in range(MAX_PCS):
            entry_set(self.pc_inits[i], "0")
        for i in range(MAX_NPCS):
            entry_set(self.npc_inits[i], "")
            entry_set(self.npc_names[i], "BBG" if i == 0 else f"NPC {i}")
            self.npc_inits[i].config(fg=FG_TEXT)
            self.npc_atk1[i].config(text="")
            self.npc_atk2[i].config(text="")
        for lbl in self.init_labels:
            lbl.config(text="- initiative -", fg=FG_INIT_DIM)

    def clear_npc_hp(self):
        for hp in self.npc_hp:
            entry_set(hp, "0")

    def set_npc_hp(self):
        val = self.npc_atk_mod.get()
        for hp in self.npc_hp:
            entry_set(hp, val)

    # ═══════════════════════════════════════════════════════════════
    # ASI
    # ═══════════════════════════════════════════════════════════════
    def reset_asi(self):
        for e in self.asi_entries.values():
            entry_set(e, "10")
        for lbl in self.asi_total_labels.values():
            lbl.config(text="-click 'prof'-", fg="#666666")

    def calc_asi(self):
        prof = safe_int(self.prof_entry.get(), 2)
        lvl_map = {2: "Lvl 1-4", 3: "Lvl 5-8", 4: "Lvl 9-12", 5: "Lvl 13-16",
                   6: "Lvl 17-20", 7: "Lvl 21-24", 8: "Lvl 25-29"}
        if prof > 8:
            self.prof_level_lbl.config(text="Lvl 30+", fg=INIT_VLOW)
        else:
            self.prof_level_lbl.config(text=lvl_map.get(prof, "---"), fg=FG_NPC)

        for stat in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
            score = safe_int(self.asi_entries[stat].get(), 10)
            base = (score - 10) // 2 if score >= 10 else -((11 - score) // 2)
            has_prof = self.prof_vars[stat].get() == 1
            total = base + prof if has_prof else base
            sign = "+" if total >= 0 else ""
            self.asi_total_labels[stat].config(
                text=f"Mod: {sign}{total}", fg=FG_SPELL)

    # ═══════════════════════════════════════════════════════════════
    # SAVE / LOAD
    # ═══════════════════════════════════════════════════════════════
    def save_data(self):
        data = {
            "pc_names":  [e.get() for e in self.pc_names],
            "pc_inits":  [e.get() for e in self.pc_inits],
            "pc_hp":     [e.get() for e in self.pc_hp],
            "npc_names": [e.get() for e in self.npc_names],
            "npc_inits": [e.get() for e in self.npc_inits],
            "npc_hp":    [e.get() for e in self.npc_hp],
            "mods": {"dice": self.dice_mod.get(),
                     "npc_atk": self.npc_atk_mod.get(),
                     "npc_init": self.npc_init_mod.get()},
            "spells":    [e.get() for e in self.spell_entries],
            "lair":      [e.get() for e in self.lair_entries],
            "asi":       {s: e.get() for s, e in self.asi_entries.items()},
            "prof":      self.prof_entry.get(),
            "prof_chk":  {s: v.get() for s, v in self.prof_vars.items()},
        }
        ts = datetime.now().strftime("saveDMA_%m-%d-%Y_%H-%M-%S")
        with open(os.path.join(SAVES_DIR, f"{ts}.json"), "w") as f:
            json.dump(data, f, indent=2)

        # CSV backwards compat
        self._save_csv(data, ts)

    def _save_csv(self, data, ts):
        try:
            cd = {
                'PC_names': data["pc_names"],
                'PC_inits': data["pc_inits"],
                'NPC_names': data["npc_names"],
                'NPC_inits': data["npc_inits"],
                'Mod_entries': [data["mods"]["dice"], data["mods"]["npc_atk"], data["mods"]["npc_init"]],
                'PC_HP_labels': data["pc_hp"],
                'NPC_HP_labels': data["npc_hp"],
                'Spell_labels': data["spells"],
                'Lair_actions': data["lair"],
                'ASI_entries': [data["asi"].get(s, "10") for s in ["STR","DEX","CON","INT","WIS","CHA"]],
                'Prof_entries': [data["prof"]] + [str(data["prof_chk"].get(s, 0))
                                                   for s in ["STR","DEX","CON","INT","WIS","CHA"]],
            }
            mx = max(len(v) for v in cd.values())
            for k in cd: cd[k] += [''] * (mx - len(cd[k]))
            pd.DataFrame(cd).to_csv(os.path.join(SAVES_DIR, f"{ts}.csv"), index=False)
        except Exception:
            pass

    def load_data(self):
        files = os.listdir(SAVES_DIR)
        jsons = sorted([f for f in files if f.endswith(".json")],
                       key=lambda x: os.path.getmtime(os.path.join(SAVES_DIR, x)), reverse=True)
        csvs = sorted([f for f in files if f.endswith(".csv")],
                      key=lambda x: os.path.getmtime(os.path.join(SAVES_DIR, x)), reverse=True)

        if jsons:
            self._load_json(os.path.join(SAVES_DIR, jsons[0]))
        elif csvs:
            self._load_csv(os.path.join(SAVES_DIR, csvs[0]))
        else:
            messagebox.showinfo("Load", "No save files found.")

    def _load_json(self, path):
        with open(path) as f:
            d = json.load(f)
        for i, v in enumerate(d.get("pc_names", [])):
            if i < MAX_PCS: entry_set(self.pc_names[i], v or "")
        for i, v in enumerate(d.get("pc_inits", [])):
            if i < MAX_PCS: entry_set(self.pc_inits[i], v or "0")
        for i, v in enumerate(d.get("pc_hp", [])):
            if i < MAX_PCS: entry_set(self.pc_hp[i], v or "-0-")
        for i, v in enumerate(d.get("npc_names", [])):
            if i < MAX_NPCS: entry_set(self.npc_names[i], v or "")
        for i, v in enumerate(d.get("npc_inits", [])):
            if i < MAX_NPCS: entry_set(self.npc_inits[i], v or "")
        for i, v in enumerate(d.get("npc_hp", [])):
            if i < MAX_NPCS: entry_set(self.npc_hp[i], v or "0")
        m = d.get("mods", {})
        entry_set(self.dice_mod, m.get("dice", "0"))
        entry_set(self.npc_atk_mod, m.get("npc_atk", "0"))
        entry_set(self.npc_init_mod, m.get("npc_init", "0"))
        for i, v in enumerate(d.get("spells", [])):
            if i < len(self.spell_entries): entry_set(self.spell_entries[i], v or "")
        for i, v in enumerate(d.get("lair", [])):
            if i < len(self.lair_entries): entry_set(self.lair_entries[i], v or "")
        for s, v in d.get("asi", {}).items():
            if s in self.asi_entries: entry_set(self.asi_entries[s], v or "10")
        entry_set(self.prof_entry, d.get("prof", "2"))
        for s, v in d.get("prof_chk", {}).items():
            if s in self.prof_vars: self.prof_vars[s].set(int(v))
        self.calc_asi()
        self.sort_initiative()

    def _load_csv(self, path):
        try:
            df = pd.read_csv(path)
        except Exception as e:
            messagebox.showerror("Load Error", str(e)); return

        for i, v in enumerate(df.get("PC_names", [])):
            if i < MAX_PCS: entry_set(self.pc_names[i], v if not pd.isna(v) else "")
        for i, v in enumerate(df.get("PC_inits", [])):
            if i < MAX_PCS: entry_set(self.pc_inits[i], str(safe_int(v)))
        for i, v in enumerate(df.get("NPC_names", [])):
            if i < MAX_NPCS: entry_set(self.npc_names[i], v if not pd.isna(v) else "")
        for i, v in enumerate(df.get("NPC_inits", [])):
            if i < MAX_NPCS: entry_set(self.npc_inits[i], str(safe_int(v)))
        mods = df.get("Mod_entries", [])
        if len(mods) >= 3:
            entry_set(self.dice_mod, safe_int(mods.iloc[0]))
            entry_set(self.npc_atk_mod, safe_int(mods.iloc[1]))
            entry_set(self.npc_init_mod, safe_int(mods.iloc[2]))
        for i, v in enumerate(df.get("PC_HP_labels", [])):
            if i < MAX_PCS: entry_set(self.pc_hp[i], str(safe_int(v)) if not pd.isna(v) else "-0-")
        for i, v in enumerate(df.get("NPC_HP_labels", [])):
            if i < MAX_NPCS: entry_set(self.npc_hp[i], str(safe_int(v)))
        for i, v in enumerate(df.get("Spell_labels", [])):
            if i < len(self.spell_entries): entry_set(self.spell_entries[i], v if not pd.isna(v) else "")
        for i, v in enumerate(df.get("Lair_actions", [])):
            if i < len(self.lair_entries): entry_set(self.lair_entries[i], str(safe_int(v)))
        stats = ["STR","DEX","CON","INT","WIS","CHA"]
        for i, v in enumerate(df.get("ASI_entries", [])):
            if i < 6: entry_set(self.asi_entries[stats[i]], str(safe_int(v, 10)))
        pe = df.get("Prof_entries", [])
        if len(pe) >= 1: entry_set(self.prof_entry, str(safe_int(pe.iloc[0], 2)))
        for i in range(1, min(7, len(pe))):
            self.prof_vars[stats[i-1]].set(safe_int(pe.iloc[i]))
        self.calc_asi()
        self.sort_initiative()


# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = DungeonMasterAssistant(root)
    root.mainloop()
