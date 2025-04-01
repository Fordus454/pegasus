###PREREQ### pip install pythonping
###PREREQ### pip install pandas

import tkinter as tk
from tkinter import filedialog, messagebox
from pythonping import ping
import pandas as pd
import os
from typing import Optional, Union, Any, List, TextIO, Dict  # Add Dict for type annotations
from collections.abc import Mapping  # Use Mapping for type compatibility
import traceback  # Added for detailed error logging
from datetime import datetime  # Added for timestamped filenames
import tkinter.scrolledtext as scrolledtext  # Import for the display box
import sys  # Import for redirecting stdout
import threading  # Import threading for background processing
import time  # Import for adding delay

# Fix type annotations for global variables
input_file: Optional[str] = None
output_file: Optional[str] = None

class ConsoleRedirector:
    """Redirect console output to the display box and terminal."""
    def __init__(self, text_widget: scrolledtext.ScrolledText):
        self.text_widget = text_widget

    def write(self, message: str) -> None:
        """
        Writes a message to the display box and terminal.
        """
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", message)  # Append the new message with its original formatting
        self.text_widget.see("end")  # Scroll to the bottom
        self.text_widget.config(state="disabled")
        # Also print to the terminal if sys.__stdout__ is not None
        if sys.__stdout__:
            sys.__stdout__.write(message)
            sys.__stdout__.flush()

    def flush(self) -> None:
        """
        Required for compatibility with stdout.
        """
        pass

def choose_file() -> None:
    """
    Opens a file dialog for the user to select a CSV file.
    Updates the global `input_file` variable and displays the selected file path.
    """
    global input_file
    input_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if input_file:
        file_label.config(text=f"Selected File: {input_file}")
    else:
        file_label.config(text="No file selected")

def process_file() -> None:
    """
    Processes the selected CSV file to detect IP addresses, ping them, and save the results.
    Runs the processing in a separate thread to keep the GUI responsive.
    """
    global output_file
    if not input_file:
        processing_label.config(text="Error: Please select an input file first.", fg="red")
        return

    # Clear previous status and output messages
    processing_label.config(text="", fg="blue")  # Clear processing label
    output_label.config(text="Results saved to:                                                                                                                  ", fg="black")  # Reset output label
    root.update_idletasks()

    # Display "Processing..." message
    processing_label.config(text="Processing...", fg="blue")
    root.update_idletasks()

    def process_in_background():
        """
        Background thread function to process the CSV file.
        Detects the IP address column, pings the IPs, and saves the results.
        """
        try:
            # Load the input file and detect the header row
            print("Loading input file...")
            root.update_idletasks()
            header_row = None
            with open(input_file, 'r') as file:
                for i, line in enumerate(file):
                    # Look for a keyword in the header row to detect headers
                    if "IP Address" in line:
                        header_row = i
                        break

            # If no header row is found, assume the file has no headers
            if header_row is None:
                print("No header row detected. Assuming the file has no headers.")
                df: pd.DataFrame = pd.read_csv(input_file, header=None, on_bad_lines='skip')
                # Assign default column names for headerless files
                df.columns = [f"Column_{i}" for i in range(len(df.columns))]
            else:
                # Load the CSV file, skipping metadata rows
                df: pd.DataFrame = pd.read_csv(input_file, header=header_row, on_bad_lines='skip')

            print(f"Initial DataFrame shape: {df.shape}")
            root.update_idletasks()

            # Detect the column containing IP addresses
            ip_col: Optional[str] = None
            for col in df.columns:
                header_value = str(col).lower()  # Use column names directly as headers
                # Skip columns with irrelevant keywords
                if "last known" in header_value or "gateway" in header_value:
                    continue
                # Prioritize columns with "IP Address" in the header
                if "ip address" in header_value:
                    if df[col].astype(str).str.match(r'^\d{1,3}(\.\d{1,3}){3}$', na=False).any():
                        ip_col = col
                        break

            # Fallback: Check all columns if no "IP Address" header is found
            if ip_col is None:
                for col in df.columns:
                    if df[col].astype(str).str.match(r'^\d{1,3}(\.\d{1,3}){3}$', na=False).any():
                        ip_col = col
                        break

            if ip_col is None:
                # If no valid IP address column is found, display an error
                processing_label.config(text="Error: No column with valid IP addresses detected.", fg="red")
                print("Error: No column with valid IP addresses detected.")
                root.update_idletasks()
                return

            print(f"Detected IP address column: {ip_col}")
            root.update_idletasks()

            # Filter rows with valid IP addresses
            df = df[df[ip_col].astype(str).str.match(r'^\d{1,3}(\.\d{1,3}){3}$', na=False)].reset_index(drop=True)
            print(f"Filtered DataFrame shape: {df.shape}")
            root.update_idletasks()

            # Add a 'Status' column to store ping results
            print("Pinging IP addresses...")
            root.update_idletasks()
            df["Status"] = ""
            for index, row in df.iterrows():
                ip = str(row[ip_col]).strip() if pd.notna(row[ip_col]) else None
                try:
                    if ip:
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
                    # Handle errors during pinging
                    df.at[index, "Status"] = "Error: IP Offline during process"
                    print(f"Error pinging {ip}: {e}")
                    root.update_idletasks()

            # Save the results to a new CSV file
            timestamp = datetime.now().strftime("%m-%d-%Y")
            output_file = os.path.splitext(input_file)[0] + f"_{timestamp}_results.csv"
            df.to_csv(output_file, index=False)  # Save with headers
            processing_label.config(text="File processed successfully.", fg="green")
            output_label.config(text=f"Results saved to: {output_file}", fg="green")  # Update output label
        except pd.errors.EmptyDataError:
            # Handle empty or invalid input files
            processing_label.config(text="Error: The input file is empty or invalid.", fg="red")
            print("Error: The input file is empty or invalid.")
            root.update_idletasks()
        except Exception as e:
            # Handle unexpected errors
            processing_label.config(text="Error: An unexpected error occurred. Check console for details.", fg="red")
            print("An unexpected error occurred:")
            traceback.print_exc()
            root.update_idletasks()
        finally:
            root.update_idletasks()

    # Run the processing in a separate thread to keep the GUI responsive
    threading.Thread(target=process_in_background, daemon=True).start()

def download_results() -> None:
    """
    Allows the user to save the processed results to a different location.
    Opens a save dialog and moves the output file to the selected location.
    """
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













