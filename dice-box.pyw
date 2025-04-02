import tkinter as tk
from tkinter import Text  # Import for type annotation
from typing import Callable, Any  # Import for type annotation
import random  

# Store the last roll details for recalculation
last_roll_details = {"results": [], "dice_sides": 0, "modifier": 0, "num_dice": 0}

# Define dark mode colors
DARK_BG = "#2e2e2e"
DARK_FG = "#ffffff"
DARK_ENTRY_BG = "#3e3e3e"
DARK_ENTRY_FG = "#ffffff"
DARK_BUTTON_BG = "#4e4e4e"
DARK_BUTTON_FG = "#ffffff"
DARK_OUTPUT_BG = "#1e1e1e"
DARK_OUTPUT_FG = "#ffffff"
DARK_HIGHLIGHT = "#25bf17"
DARK_ERROR = "#ff4d4d"

# Define button colors for better contrast
DARKER_BUTTON_BG = "#3a3a3a"
DARKER_HIGHLIGHT = "#1e8f13"
DARKER_ERROR = "#b22222"
DARKER_AMBER = "#cc9900"

# Default color for the ReCalc button
recalc_button_default_color = DARKER_BUTTON_BG

def roll_dice(dice_sides, dice_entry, modifier_entry, output_box):  
    """
    Perform the initial dice roll and store the results.
    Handles advantage, disadvantage, and regular rolls.
    """
    recalc_button.configure(bg=recalc_button_default_color)
    try:  
        num_dice = int(dice_entry.get())  
        modifier = int(modifier_entry.get())  
    except ValueError:  
        add_to_output(output_box, "Error: Enter valid integers for the number of dice and modifier.", "red")  
        return  
  
    if num_dice < 1:  
        add_to_output(output_box, "Error: The number of dice must be at least 1.", "red")  
        return  
  
    results = []
    detailed_rolls = []  
    nat_20 = False  
    for _ in range(num_dice):
        roll1 = random.randint(1, dice_sides)
        roll2 = random.randint(1, dice_sides)
        if advantage_state.get():
            kept = max(roll1, roll2)
            results.append((roll1, roll2))
            detailed_rolls.append(f"{roll1}, {roll2}  (kept: {kept})")
            if dice_sides == 20 and kept == 20:
                nat_20 = True
        elif disadvantage_state.get():
            kept = min(roll1, roll2)
            results.append((roll1, roll2))
            detailed_rolls.append(f"{roll1}, {roll2}  (kept: {kept})")
            if dice_sides == 20 and kept == 20:
                nat_20 = True
        else:
            results.append(roll1)
            detailed_rolls.append(f"{roll1}")
            if dice_sides == 20 and roll1 == 20:
                nat_20 = True

    last_roll_details.update({
        "results": results,
        "dice_sides": dice_sides,
        "modifier": modifier,
        "num_dice": num_dice
    })

    total = sum([max(roll) if isinstance(roll, tuple) else roll for roll in results]) + modifier
    output = (  
        f"Rolling {num_dice}d{dice_sides} + {modifier}\n"  
        f" Roll:  {', '.join(detailed_rolls)}\n"  
        f" Total:  {total}"  
    )
    if nat_20:
        output += "  ★ Nat 20!"
  
    add_to_output(output_box, output)  

def add_to_output(output_box, text, color=DARK_FG):  
    """
    Add text to the output box with the current roll at the top.
    Styles the text based on its type (current roll, old roll, etc.).
    """
    output_box.tag_configure("current", foreground=color, font=("TkDefaultFont", 10, "bold"))  
    output_box.tag_configure("current-rolling", foreground=DARK_HIGHLIGHT, font=("TkDefaultFont", 10))  
    output_box.tag_configure("current-unbold", foreground=DARK_FG, font=("TkDefaultFont", 10))  
    output_box.tag_configure("old", foreground="#aaaaaa", font=("TkDefaultFont", 8, "italic"))  
  
    lines = text.split("\n")
    new_roll = (
        lines[0] + "\n",  
        lines[1] + "\n",  
        lines[2] + "\n",  
        "-"*32 + "\n"     
    )
  
    output_box.insert("1.0", new_roll[3], "current")  
    output_box.insert("1.0", new_roll[2], "current")  
    output_box.insert("1.0", new_roll[1], "current-unbold")  
    output_box.insert("1.0", new_roll[0], "current-rolling")  
  
    total_lines = int(output_box.index(tk.END).split(".")[0])  
    for i in range(5, total_lines):  
        start_line = f"{i}.0"  
        end_line = f"{i}.end"  
        output_box.tag_remove("current", start_line, end_line)  
        output_box.tag_add("old", start_line, end_line)  
  
    output_box.see("1.0")
  
def configure_output_tags(output_box):
    """
    Configure text tags for the output box.
    Defines styles for current rolls, old rolls, and other text.
    """
    output_box.tag_configure("current", foreground=DARK_FG, font=("TkDefaultFont", 10, "bold"))
    output_box.tag_configure("current-rolling", foreground=DARK_HIGHLIGHT, font=("TkDefaultFont", 10))
    output_box.tag_configure("current-unbold", foreground=DARK_FG, font=("TkDefaultFont", 10)) 
    output_box.tag_configure("old", foreground="#aaaaaa", font=("TkDefaultFont", 8, "italic"))

def toggle_advantage():
    """
    Toggle the Advantage button and ensure mutual exclusivity with Disadvantage.
    """
    if advantage_state.get():
        advantage_button.config(bg=DARKER_BUTTON_BG)
        advantage_state.set(False)
    else:
        advantage_button.config(bg=DARKER_HIGHLIGHT)
        disadvantage_button.config(bg=DARKER_BUTTON_BG)
        advantage_state.set(True)
        disadvantage_state.set(False)

def toggle_disadvantage():
    """
    Toggle the Disadvantage button and ensure mutual exclusivity with Advantage.
    """
    if disadvantage_state.get():
        disadvantage_button.config(bg=DARKER_BUTTON_BG)
        disadvantage_state.set(False)
    else:
        disadvantage_button.config(bg=DARKER_ERROR)
        advantage_button.config(bg=DARKER_BUTTON_BG)
        disadvantage_state.set(True)
        advantage_state.set(False)

def recalculate_with_modifier():
    """
    Recalculate the total using the last roll's dice values and the updated modifier.
    Adjusts for advantage/disadvantage and retains or generates second rolls as needed.
    """
    if not last_roll_details["results"]:
        add_to_output(output_box, "Error: No previous roll to recalculate.", "red")
        return

    try:
        new_modifier = int(modifier_entry.get())
    except ValueError:
        add_to_output(output_box, "Error: Enter a valid integer for the modifier.", "red")
        return

    adjusted_results = []
    detailed_rolls = []
    nat_20 = False  
    for roll in last_roll_details["results"]:
        if isinstance(roll, tuple):  
            if advantage_state.get():
                kept = max(roll)
                adjusted_results.append(kept)
                detailed_rolls.append(f"{roll[0]}, {roll[1]}  (kept: {kept})")
                if last_roll_details["dice_sides"] == 20 and kept == 20:
                    nat_20 = True
            elif disadvantage_state.get():
                kept = min(roll)
                adjusted_results.append(kept)
                detailed_rolls.append(f"{roll[0]}, {roll[1]}  (kept: {kept})")
                if last_roll_details["dice_sides"] == 20 and kept == 20:
                    nat_20 = True
            else:
                adjusted_results.append(roll[0])
                detailed_rolls.append(f"{roll[0]}  (dropped: {roll[1]})")
                if last_roll_details["dice_sides"] == 20 and roll[0] == 20:
                    nat_20 = True
        else:  
            if advantage_state.get() or disadvantage_state.get():
                if "second_rolls" not in last_roll_details:
                    last_roll_details["second_rolls"] = {}

                if roll in last_roll_details["second_rolls"]:
                    new_roll = last_roll_details["second_rolls"][roll]
                else:
                    new_roll = random.randint(1, last_roll_details["dice_sides"])
                    last_roll_details["second_rolls"][roll] = new_roll

                if advantage_state.get():
                    kept = max(roll, new_roll)
                    adjusted_results.append(kept)
                    detailed_rolls.append(f"{roll}, {new_roll}  (kept: {kept})")
                    if last_roll_details["dice_sides"] == 20 and kept == 20:
                        nat_20 = True
                elif disadvantage_state.get():
                    kept = min(roll, new_roll)
                    adjusted_results.append(kept)
                    detailed_rolls.append(f"{roll}, {new_roll}  (kept: {kept})")
                    if last_roll_details["dice_sides"] == 20 and kept == 20:
                        nat_20 = True
            else:
                adjusted_results.append(roll)
                detailed_rolls.append(f"{roll}")
                if last_roll_details["dice_sides"] == 20 and roll == 20:
                    nat_20 = True

    total = sum(adjusted_results) + new_modifier
    output = (
        f"Recalculating {last_roll_details['num_dice']}d{last_roll_details['dice_sides']} + {new_modifier}\n"
        f" Roll:  {', '.join(detailed_rolls)}\n"
        f" Total:  {total}"
    )
    if nat_20:
        output += "  ★ Nat 20!"

    add_to_output(output_box, output)
    recalc_button.configure(bg=DARKER_AMBER)

root = tk.Tk()  
root.title("Dice Roller")  
root.configure(bg=DARK_BG)
  
main_frame = tk.Frame(root, padx=10, pady=10)  
main_frame.pack()  
main_frame.configure(bg=DARK_BG)
  
modifier_label = tk.Label(main_frame, text="Modifier:", font=("TkDefaultFont", 9, "bold"))  
modifier_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")  
modifier_label.configure(bg=DARK_BG, fg=DARK_FG)
  
modifier_entry = tk.Entry(main_frame, width=4)  
modifier_entry.grid(row=0, column=1, padx=5, pady=5)  
modifier_entry.insert(0, "0")  
modifier_entry.configure(bg=DARK_ENTRY_BG, fg=DARK_ENTRY_FG, insertbackground=DARK_FG, justify="center")

advantage_state = tk.BooleanVar(value=False)
disadvantage_state = tk.BooleanVar(value=False)

recalc_button = tk.Button(
    main_frame,
    text="ReCalc",
    bg=DARKER_BUTTON_BG,
    fg=DARK_BUTTON_FG,
    font=("TkDefaultFont", 9, "bold"),
    width=8,
    command=recalculate_with_modifier
)
recalc_button.grid(row=0, column=2, padx=(2, 2), pady=5, sticky="w")

advantage_button = tk.Button(
    main_frame,
    text="Advantage",
    bg=DARKER_BUTTON_BG,
    fg=DARK_BUTTON_FG,
    font=("TkDefaultFont", 9, "bold"),
    width=12,
    command=toggle_advantage
)
advantage_button.grid(row=0, column=3, padx=(2, 2), pady=5, sticky="e")

disadvantage_button = tk.Button(
    main_frame,
    text="Disadvantage",
    bg=DARKER_BUTTON_BG,
    fg=DARK_BUTTON_FG,
    font=("TkDefaultFont", 9, "bold"),
    width=12,
    command=toggle_disadvantage
)
disadvantage_button.grid(row=0, column=4, padx=(2, 5), pady=5, sticky="w")

dice_types = [4, 6, 8, 10, 12, 20, 100]  
row_counter = 1  
  
for dice in dice_types:  
    dice_frame = tk.Frame(main_frame)
    dice_frame.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    dice_frame.configure(bg=DARK_BG)

    dice_entry = tk.Entry(dice_frame, width=5)  
    dice_entry.pack(side="left", padx=(0, 2))  
    dice_entry.insert(0, "1")  
    dice_entry.configure(bg=DARK_ENTRY_BG, fg=DARK_ENTRY_FG, insertbackground=DARK_FG, justify="center")

    x_label = tk.Label(dice_frame, text="x")
    x_label.pack(side="left")
    x_label.configure(bg=DARK_BG, fg=DARK_FG)

    def create_roll_command(d: int, e: tk.Entry, m: tk.Entry) -> Callable[[], Any]:
        return lambda: roll_dice(d, e, m, output_box)
  
    roll_button = tk.Button(  
        main_frame,  
        text=f"d{dice}",
        width=4,
        bg=DARK_BUTTON_BG,
        fg=DARK_BUTTON_FG,
        font=("TkDefaultFont", 9, "bold"),  
        command=create_roll_command(dice, dice_entry, modifier_entry)
    )  
    roll_button.grid(row=row_counter, column=1, padx=(2, 5), pady=5, sticky="w")  
  
    row_counter += 1  

for widget in main_frame.winfo_children():
    if isinstance(widget, tk.Entry):
        widget.configure(bg=DARK_ENTRY_BG, fg=DARK_ENTRY_FG, insertbackground=DARK_FG, justify="center")

output_box: Text = tk.Text(main_frame, width=40, height=20, wrap="word", borderwidth=2, relief="solid")  
output_box.grid(row=1, column=2, rowspan=row_counter, columnspan=3, padx=5, pady=5)
output_box.configure(bg=DARK_OUTPUT_BG, fg=DARK_OUTPUT_FG, insertbackground=DARK_FG)
configure_output_tags(output_box)

root.mainloop()
