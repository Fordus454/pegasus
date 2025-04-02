import tkinter as tk
from tkinter import Text  # Import for type annotation
from typing import Callable, Any  # Import for type annotation
import random  
  
# Function to roll the dice  
def roll_dice(dice_sides, dice_entry, modifier_entry, output_box):  
    try:  
        num_dice = int(dice_entry.get())  
        modifier = int(modifier_entry.get())  
    except ValueError:  
        add_to_output(output_box, "Error: Enter valid integers for the number of dice and modifier.", "red")  
        return  
  
    if num_dice < 1:  
        add_to_output(output_box, "Error: The number of dice must be at least 1.", "red")  
        return  
  
    # Perform the dice rolls  
    results = []
    detailed_rolls = []  # To store all rolls for output
    for _ in range(num_dice):
        roll1 = random.randint(1, dice_sides)
        roll2 = random.randint(1, dice_sides)
        if advantage_state.get():
            kept = max(roll1, roll2)
            results.append(kept)
            detailed_rolls.append(f"{roll1}, {roll2}  (kept: {kept})")
        elif disadvantage_state.get():
            kept = min(roll1, roll2)
            results.append(kept)
            detailed_rolls.append(f"{roll1}, {roll2}  (kept: {kept})")
        else:
            results.append(roll1)  # Regular roll
            detailed_rolls.append(f"{roll1}")

    total = sum(results) + modifier
    output = (  
        f"Rolling {num_dice}d{dice_sides} + {modifier}\n"  
        f" Roll:  {', '.join(detailed_rolls)}\n"  
        f" Total:  {total}"  
    )  
  
    # Add the result to the output box  
    add_to_output(output_box, output)  

def add_to_output(output_box, text, color="black"):  
    """Add text to the output box without removing old lines."""  
    # Configure tags  
    output_box.tag_configure("current", foreground=color, font=("TkDefaultFont", 10, "bold"))  # Bold new lines 
    output_box.tag_configure("current-unbold", foreground="#044a18", font=("TkDefaultFont", 10))  # Unbold new lines
    output_box.tag_configure("current-2", foreground="black", font=("TkDefaultFont", 10))  # unbold new lines with black font
    output_box.tag_configure("old", foreground="gray", font=("TkDefaultFont", 8, "italic"))  # Italic and smaller font for old lines  
  
    # Split the text into lines  
    lines = text.split("\n")
  
    # Add the new roll (3 lines: description, results, total)  
    output_box.insert(tk.END, lines[0] + "\n", "current-unbold")  # First line (bold "Rolling")  
    output_box.insert(tk.END, lines[1] + "\n", "current-2")  # Second line (bold "Results")  
    output_box.insert(tk.END, lines[2] + "\n", "current")  # Third line (bold "Total")  
    output_box.insert(tk.END, "-"*32 + "\n", "current")  # Separator  
  
    # Apply the "old" style to all lines except the last 4 lines (new roll)  
    total_lines = int(output_box.index(tk.END).split(".")[0])  # Total number of lines in the output box  
    old_lines_limit = total_lines - 5  # Adjust to exclude the last 4 lines + 1 for index (new roll)
    for i in range(1, old_lines_limit):  # Exclude the last 4 lines (new roll)  
        start_line = f"{i}.0"  
        end_line = f"{i}.end"  
        output_box.tag_remove("current", start_line, end_line)  # Remove "current" tag  
        output_box.tag_add("old", start_line, end_line)  # Add "old" tag  
  
    # Ensure the last 4 lines (new roll) are tagged as "current"
    for i in range(old_lines_limit, total_lines):  
        start_line = f"{i}.0"  
        end_line = f"{i}.end"  
        output_box.tag_remove("old", start_line, end_line)  # Remove "old" tag  
        output_box.tag_add("current", start_line, end_line)  # Add "current" tag  
  
    # Scroll to the bottom of the output box  
    output_box.see(tk.END)  
  
# Ensure tags are configured for bold and unbold text
def configure_output_tags(output_box):
    output_box.tag_configure("current", foreground="black", font=("TkDefaultFont", 10, "bold"))
    output_box.tag_configure("current-unbold", foreground="black", font=("TkDefaultFont", 10))
    output_box.tag_configure("current-2", foreground="black", font=("TkDefaultFont", 10)) 
    output_box.tag_configure("old", foreground="gray", font=("TkDefaultFont", 8, "italic"))

# Create the main application window  
root = tk.Tk()  
root.title("Dice Roller")  
  
# Main frame  
main_frame = tk.Frame(root, padx=10, pady=10)  
main_frame.pack()  
  
# Modifier entry  
modifier_label = tk.Label(main_frame, text="Modifier:", font=("TkDefaultFont", 9, "bold"))  
modifier_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")  
  
modifier_entry = tk.Entry(main_frame, width=4)  
modifier_entry.grid(row=0, column=1, padx=5, pady=5)  
modifier_entry.insert(0, "0")  

# Add Advantage and Disadvantage buttons with mutual exclusivity and state tracking
advantage_state = tk.BooleanVar(value=False)
disadvantage_state = tk.BooleanVar(value=False)

def toggle_advantage():
    """Toggle Advantage button and ensure mutual exclusivity."""
    if advantage_state.get():
        advantage_button.config(bg="SystemButtonFace")
        advantage_state.set(False)
    else:
        advantage_button.config(bg="#25bf17")
        disadvantage_button.config(bg="SystemButtonFace")
        advantage_state.set(True)
        disadvantage_state.set(False)

def toggle_disadvantage():
    """Toggle Disadvantage button and ensure mutual exclusivity."""
    if disadvantage_state.get():
        disadvantage_button.config(bg="SystemButtonFace")
        disadvantage_state.set(False)
    else:
        disadvantage_button.config(bg="red")
        advantage_button.config(bg="SystemButtonFace")
        disadvantage_state.set(True)
        advantage_state.set(False)

advantage_button = tk.Button(
    main_frame,
    text="Advantage",
    bg="SystemButtonFace",
    font=("TkDefaultFont", 9, "bold"),
    width=12,
    command=toggle_advantage
)
advantage_button.grid(row=0, column=2, padx=(0, 2), pady=5, sticky="e")  # Adjust padding for closer alignment

disadvantage_button = tk.Button(
    main_frame,
    text="Disadvantage",
    bg="SystemButtonFace",
    font=("TkDefaultFont", 9, "bold"),
    width=12,
    command=toggle_disadvantage
)
disadvantage_button.grid(row=0, column=3, padx=(2, 5), pady=5, sticky="w")  # Adjust padding for closer alignment

# Dice options  
dice_types = [4, 6, 8, 10, 12, 20, 100]  
row_counter = 1  
  
for dice in dice_types:  
    # Frame to group entry and "x" label
    dice_frame = tk.Frame(main_frame)
    dice_frame.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")

    # Entry for number of dice  
    dice_entry = tk.Entry(dice_frame, width=5)  
    dice_entry.pack(side="left", padx=(0, 2))  
    dice_entry.insert(0, "1")  

    # Add "x" label
    x_label = tk.Label(dice_frame, text="x")
    x_label.pack(side="left")

    # Button to roll the dice  
    def create_roll_command(d: int, e: tk.Entry, m: tk.Entry) -> Callable[[], Any]:
        return lambda: roll_dice(d, e, m, output_box)
  
    roll_button = tk.Button(  
        main_frame,  
        text=f"d{dice}",
        width=4,
        bg="#f2f2f2",
        font=("TkDefaultFont", 9, "bold"),  
        command=create_roll_command(dice, dice_entry, modifier_entry)  # Use the helper function
    )  
    roll_button.grid(row=row_counter, column=1, padx=(2, 5), pady=5, sticky="w")  
  
    row_counter += 1  
  
# Output box for displaying results  
output_box: Text = tk.Text(main_frame, width=40, height=20, wrap="word", borderwidth=2, relief="solid")  
output_box.grid(row=1, column=2, rowspan=row_counter, columnspan=2, padx=5, pady=5)
configure_output_tags(output_box)

# Start the Tkinter event loop  
root.mainloop()