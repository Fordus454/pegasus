###PREREQ### pip install pythonping
###PREREQ### pip install pandas

import tkinter as tk
from tkinter import filedialog, messagebox
from pythonping import ping
import pandas as pd
import os
from typing import Optional, Union, Any, List, TextIO  # Ensure TextIO is imported for type annotations
from collections.abc import Mapping  # Use Mapping for type compatibility
import traceback  # Added for detailed error logging
from datetime import datetime  # Added for timestamped filenames
import tkinter.scrolledtext as scrolledtext  # Import for the display box
import sys  # Import for redirecting stdout
import time  # Import for adding delay

# Fix type annotations for global variables
input_file: Optional[str] = None
output_file: Optional[str] = None

class ConsoleRedirector:
    """Redirect console output to the display box and terminal."""
    def __init__(self, text_widget: scrolledtext.ScrolledText):
        self.text_widget = text_widget

    def write(self, message: str) -> None:
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", message)  # Append the new message with its original formatting
        self.text_widget.see("end")  # Scroll to the bottom
        self.text_widget.config(state="disabled")
        # Also print to the terminal if sys.__stdout__ is not None
        if sys.__stdout__:
            sys.__stdout__.write(message)
            sys.__stdout__.flush()

    def flush(self) -> None:
        pass  # Required for compatibility with stdout

def choose_file() -> None:
    global input_file
    input_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if input_file:
        file_label.config(text=f"Selected File: {input_file}")
    else:
        file_label.config(text="No file selected")

def process_file() -> None:
    global output_file
    if not input_file:
        processing_label.config(text="Error: Please select an input file first.", fg="red")
        return

    # Clear previous status and output messages
    processing_label.config(text="", fg="blue")  # Clear processing label
    output_label.config(text="Results saved to:                                                                                                                  ", fg="black")  # Reset output label
    root.update_idletasks()

    # Display "Processing..." message
    processing_label.config(text="Processing...                                                                           ", fg="blue")
    root.update_idletasks()

    # Add a 1-second delay before starting processing
    time.sleep(1)

    try:
        # Load the input file
        print("Loading input file...")
        root.update_idletasks()  # Ensure the display box updates immediately
        df: pd.DataFrame = pd.read_csv(input_file, header=None)  # Load without assuming headers
        print(f"Initial DataFrame shape: {df.shape}")
        root.update_idletasks()

        # Detect the column containing IP addresses based on the '10.' prefix
        ip_col: Optional[int] = None
        header_row: int = -1  # Default to no header
        for col in df.columns:
            for i, value in enumerate(df[col].astype(str)):
                if value.startswith("10."):  # Check if the value starts with "10."
                    ip_col = col
                    header_row = i - 1  # The row above the first valid IP is the header
                    break
            if ip_col is not None:
                break

        if ip_col is None:
            processing_label.config(text="Error: No column with valid IP addresses detected.", fg="red")
            print("Error: No column with valid IP addresses detected.")
            root.update_idletasks()
            return

        print(f"Detected IP address column: {ip_col}")
        print(f"Header row detected at: {header_row}")
        root.update_idletasks()

        # Adjust the DataFrame to remove leading rows and set the header
        headerless: bool = header_row < 0
        if not headerless:
            df = pd.read_csv(input_file, header=header_row)  # Reload with the correct header row
            print("Re-loaded file with headers.")
        else:
            # For headerless files, process all rows as data without skipping the first row
            df.columns = [str(col) for col in df.columns]  # Use default integer-based column names
            print("Processed file without headers.")

        # Ensure all rows after the starting row are processed
        df = df.reset_index(drop=True)  # Reset index to ensure proper row processing
        print(f"DataFrame shape after resetting index: {df.shape}")
        root.update_idletasks()

        # Add a 'Status' column
        print("Pinging IP addresses...")
        root.update_idletasks()
        df["Status"] = ""
        for index, row in df.iterrows():
            ip = str(row[ip_col]).strip() if pd.notna(row[ip_col]) else None
            try:
                if ip and ip.startswith("10."):
                    print(f"Pinging {ip}...")
                    root.update_idletasks()
                    avg_ping = ping(ip, count=3).rtt_avg_ms
                    if avg_ping < 2000:
                        df.at[index, "Status"] = f"Online at {avg_ping:.2f} avg ms ping"
                        print(f"{ip} is Online at {avg_ping:.2f} avg ms")
                    else:
                        df.at[index, "Status"] = "Error: IP Offline during process"
                        print(f"{ip} is Offline (timeout)")
                else:
                    df.at[index, "Status"] = "Error: Invalid or missing IP address"
                    print(f"Row {index} has an invalid or missing IP address.")
                root.update_idletasks()
            except Exception as e:
                df.at[index, "Status"] = "Error: IP Offline during process"
                print(f"Error pinging {ip}: {e}")
                root.update_idletasks()

        # Save the results
        timestamp = datetime.now().strftime("%m-%d-%Y")
        output_file = os.path.splitext(input_file)[0] + f"_{timestamp}_results.csv"
        if headerless:
            df.to_csv(output_file, index=False, header=False)  # Exclude headers for headerless files
        else:
            df.to_csv(output_file, index=False, header=True)  # Include headers for files with headers
        processing_label.config(text="File processed successfully.", fg="green")
        output_label.config(text=f"Results saved to: {output_file}", fg="green")  # Update output label
    except pd.errors.EmptyDataError:
        processing_label.config(text="Error: The input file is empty or invalid.", fg="red")
        print("Error: The input file is empty or invalid.")
        root.update_idletasks()
    except Exception as e:
        processing_label.config(text="Error: An unexpected error occurred. Check console for details.", fg="red")
        print("An unexpected error occurred:")
        traceback.print_exc()
        root.update_idletasks()
    finally:
        root.update_idletasks()

def download_results() -> None:
    global output_file
    if not output_file:
        processing_label.config(text="Error: No processed file available to download.", fg="red")
        return

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%m-%d-%Y")
    default_filename = f"{timestamp}_output.csv"

    # Open save dialog with the default filename
    save_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )
    if save_path:
        try:
            # Move the output file to the selected location
            os.rename(output_file, save_path)
            output_label.config(text=f"Results saved to: {save_path}", fg="green")
        except Exception as e:
            output_label.config(text=f"Error: Failed to save the file: {e}", fg="red")
            print(f"Error saving file: {e}")

# Initialize the GUI
root = tk.Tk()
root.title("Any CSV - IP Address Pinger")
root.config(borderwidth=2, relief="groove", bg="#f0f0f0")  # Light gray background
root.geometry("780x400")  # Adjust height to accommodate the display box

# GUI Elements
frame = tk.Frame(root, bg="#f0f0f0")  # Match background color
frame.pack(pady=10, padx=10, fill="both", expand=True)

# Configure grid layout
frame.columnconfigure(0, minsize=150)  # Set fixed width for buttons column
frame.columnconfigure(1, weight=1)  # Labels column expands as needed

# Fix button configuration type
button_style: Mapping[str, Any] = {
    "padx": 10,
    "pady": 5,
    "width": 20,
    "relief": "raised",
    "bg": "#d9d9d9",  # Light gray button background
    "activebackground": "#c0c0c0",  # Slightly darker gray when active
    "fg": "black"  # Black text for buttons
}

choose_button = tk.Button(frame, text="Choose File", command=choose_file, **button_style)
choose_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)

process_button = tk.Button(frame, text="Process File", command=process_file, **button_style)
process_button.grid(row=1, column=0, sticky="e", padx=5, pady=5)

download_button = tk.Button(frame, text="Save Results Elsewhere", command=download_results, **button_style)
download_button.grid(row=2, column=0, sticky="e", padx=5, pady=5)

# Labels
file_label = tk.Label(frame, text="No file selected", wraplength=400, anchor="w", justify="left", bg="#f0f0f0", fg="black")
file_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)

processing_label = tk.Label(frame, text="", fg="blue", anchor="w", justify="left", bg="#f0f0f0")
processing_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)

output_label = tk.Label(frame, text="Results saved to: ", fg="black", anchor="w", justify="left", bg="#f0f0f0")
output_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)

# Display box for console output
console_box = scrolledtext.ScrolledText(frame, height=10, state="disabled", wrap="word", bg="#ffffff", fg="black")
console_box.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

# Redirect stdout to the display box
console_redirector = ConsoleRedirector(console_box)
sys.stdout = console_redirector

# Run the GUI
root.mainloop()













