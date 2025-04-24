import tkinter as tk  
import xml.etree.ElementTree as ET  
import os  

# Path to the XML file containing site manager configuration
XML_FILE = r"C:\ProgramData\American Dynamics\SiteManagerConfiguration\SiteManagerConfigurationInfo.xml"  

# Path to the Victor Client executable
VICTOR_CLIENT_PATH = r"C:\Program Files\Tyco\victorClient\VEClient.exe"  

# Dictionary mapping region names to their respective store numbers
# Each store number is prefixed with "N" for consistency
regions = {  
    "NW": [  
        "N0001", "N0003", "N0004", "N0005", "N0006", "N0009", "N0010", "N0011", "N0014", "N0015", "N0016", "N0017", 
        "N0020", "N0022", "N0025", "N0027", "N0028", "N0089", "N0109", "N0111", "N0112", "N0113", "N0120", "N0125", 
        "N0130", "N0138", "N0139", "N0400", "N0401", "N0402", "N0405", "N0417", "N0420", "N0421", "N0422", "N0423", 
        "N0425", "N0428", "N0431", "N0432", "N0433", "N0434", "N0435", "N0440", "N0450", "N0470", "N0471", "N0472", 
        "N0475", "N0476", "N0477", "N0478", "N0479", "N0481", "N0482", "N0483", "N0484", "N0485", "N0490", "N0497", 
        "N0585", "N0806", "N0865"  
    ],  
    "SW": [  
        "N0032", "N0034", "N0036", "N0037", "N0071", "N0072", "N0073", "N0074", "N0110", "N0135", "N0136", "N0137", 
        "N0140", "N0148", "N0150", "N0151", "N0154", "N0155", "N0217", "N0310", "N0367", "N0373", "N0377", "N0379", 
        "N0380", "N0388", "N0389", "N0416", "N0620", "N0686", "N0688", "N0691", "N0709", "N0713", "N0715", "N0719", 
        "N0720", "N0721", "N0723", "N0724", "N0727", "N0730", "N0731", "N0732", "N0733", "N0734", "N0735", "N0736", 
        "N0738", "N0739", "N0740", "N0741", "N0744", "N0745", "N0746", "N0747", "N0748", "N0749", "N0770", "N3721", 
        "N3722", "N3761"  
    ],  
    "SCAL": [  
        "N0033", "N0045", "N0047", "N0048", "N0054", "N0160", "N0161", "N0162", "N0163", "N0164", "N0165", "N0166", 
        "N0167", "N0168", "N0320", "N0321", "N0322", "N0326", "N0328", "N0329", "N0330", "N0331", "N0332", "N0333", 
        "N0334", "N0336", "N0337", "N0338", "N0340", "N0341", "N0342", "N0345", "N0347", "N0348", "N0349", "N0350", 
        "N0351", "N0352", "N0353", "N0354", "N0356", "N0357", "N0358", "N0359", "N0360", "N0361", "N0363", "N0366", 
        "N0368", "N0369", "N0370", "N0371", "N0372", "N0374", "N0376", "N0378", "N0383", "N0384", "N0386", "N0391", 
        "N0393", "N0395", "N0396", "N0399", "N0403", "N0411", "N0413", "N0414", "N0441", "N0486", "N0488", "N0491", 
        "N0499", "N0584", "N0706", "N0879", "N0916", "N3341", "N3361", "N3362" 
    ],  
    "NE": [  
        "N0175", "N0201", "N0202", "N0209", "N0210", "N0212", "N0509", "N0515", "N0519", "N0520", "N0521", "N0523", 
        "N0524", "N0526", "N0527", "N0529", "N0531", "N0533", "N0535", "N0538", "N0539", "N0541", "N0542", "N0543", 
        "N0544", "N0545", "N0546", "N0547", "N0548", "N0550", "N0551", "N0552", "N0553", "N0554", "N0555", "N0569", 
        "N0600", "N0621", "N0622", "N0623", "N0624", "N0625", "N0627", "N0629", "N0631", "N0633", "N0634", "N0637", 
        "N0639", "N0640", "N0642", "N0643", "N0644", "N0645", "N0646", "N0647", "N0648", "N0649", "N0650", "N0651", 
        "N0652", "N0656", "N0660", "N0661", "N0670", "N0671", "N0673", "N0674", "N0675", "N0677", "N0697", "N0699", 
        "N5511", "N5521", "N5531"  
    ],  
    "MW": [  
        "N0200", "N0220", "N0221", "N0222", "N0223", "N0224", "N0225", "N0227", "N0228", "N0229", "N0230", "N0231",  
        "N0232", "N0233", "N0234", "N0235", "N0237", "N0238", "N0239", "N0240", "N0241", "N0242", "N0243", "N0244",  
        "N0245", "N0246", "N0247", "N0248", "N0249", "N0250", "N0253", "N0256", "N0260", "N0264", "N0265", "N0266",  
        "N0267", "N0268", "N0269", "N0270", "N0271", "N0272", "N0273", "N0274", "N0275", "N0276", "N0277", "N0278",  
        "N0279", "N0280", "N0281", "N0282", "N0283", "N0284", "N0285", "N0286", "N0287", "N0288", "N0289", "N0297",  
        "N0299", "N0676", "N0808", "N2221", "N2223", "N2242", "N2261", "N2262", "N2263"  
    ],  
    "SE": [  
        "N0610", "N0641", "N0658", "N0692", "N0700", "N0708", "N0711", "N0712", "N0714", "N0716", "N0717", "N0743", 
        "N0750", "N0751", "N0754", "N0755", "N0756", "N0757", "N0758", "N0759", "N0760", "N0762", "N0763", "N0764", 
        "N0765", "N0771", "N0772", "N0773", "N0774", "N0777", "N0778", "N0779", "N0781", "N0782", "N0783", "N0784", 
        "N0785", "N0786", "N0787", "N0788", "N0789", "N0791", "N0792", "N0793", "N0796", "N0797", "N0798", "N0799", 
        "N7751", "N7752", "N7753", "N7755", "N7761", "N7762" 
    ]  
} 
def get_current_default():  
    """
    Retrieve the currently selected default region from the XML file.
    Returns:
        str: The name of the currently selected default region, or None if not found.
    """
    try:  
        tree = ET.parse(XML_FILE)  
        root = tree.getroot()  
        for site_manager in root.findall("SiteManager"):  
            if site_manager.find("Default").text.lower() == "true":  
                return site_manager.find("DisplayName").text  
    except Exception as e:  
        print(f"Error reading XML file: {e}")  
    return None  

def update_default(region_name):  
    """
    Update the Default flag in the XML file to set the specified region as the default.
    Args:
        region_name (str): The name of the region to set as default.
    """
    try:  
        tree = ET.parse(XML_FILE)  
        root = tree.getroot()  

        # Reset all Default flags to false
        for site_manager in root.findall("SiteManager"):  
            site_manager.find("Default").text = "false"  

        # Set the selected region's Default flag to true
        for site_manager in root.findall("SiteManager"):  
            if site_manager.find("DisplayName").text == region_name:  
                site_manager.find("Default").text = "true"  
                break  

        # Save the changes back to the XML file
        tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)  

        # Update the status label and highlight the button
        update_status(f"Updated default to:   ", region_name, "#00ffff")  
        highlight_button(region_name)  
    except Exception as e:  
        update_status(f"Error: {e}", "", "red")  

def update_status(message, region_name, color):  
    """
    Update the status message displayed in the GUI.
    Args:
        message (str): The message to display.
        region_name (str): The name of the region to highlight in the message.
        color (str): The color of the text.
    """
    status_label.delete("1.0", tk.END)  
    status_label.insert(tk.END, message, ("normal_text",))  
    status_label.insert(tk.END, region_name, ("bold_text",))  
    status_label.tag_config("normal_text", foreground=color, font=("Arial", 12))  
    status_label.tag_config("bold_text", foreground=color, font=("Arial", 12, "bold"))  

def highlight_button(region_name):  
    """
    Highlight the button corresponding to the currently selected region.
    Args:
        region_name (str): The name of the region to highlight.
    """
    for btn in buttons:  
        if btn["text"] == region_name:  
            btn.config(bg="#007BFF", fg="white", relief="solid", borderwidth=2)  
        else:  
            btn.config(bg="#333333", fg="#dcdcdc", relief="flat", borderwidth=0)  

def launch_victor_client():  
    """
    Launch the Victor Client application.
    """
    try:  
        os.startfile(VICTOR_CLIENT_PATH)  
    except Exception as e:  
        update_status(f"Error launching Victor Client: {e}", "", "red")  

def find_region(store_number):
    """
    Find the region a store belongs to based on its store number.
    Args:
        store_number (str): The store number to search for.
    Returns:
        str: The region name if found, otherwise None.
    """
    store_number = store_number.upper().zfill(4)  # Ensure uppercase and pad with leading zeros
    if not store_number.startswith("N"):
        store_number = "N" + store_number  # Add leading "N" if missing
    for region, stores in regions.items():
        if store_number in stores:
            return region
    return None

def display_store_region():
    """
    Display the region for the entered store number in the GUI.
    """
    store_number = store_entry.get().strip()
    region = find_region(store_number)
    if region:
        store_region_label.config(
            text=f"Store {store_number} belongs to region: ",
            fg="#00ff00",  # Green text for success
            font=("Arial", 10)
        )
        store_region_value.config(
            text=region,
            fg="#00ff00",  # Green text for success
            font=("Arial", 10, "bold")  # Bold font for region
        )
    else:
        store_region_label.config(
            text=f"Store {store_number} not found in any region.",
            fg="red",  # Red text for error
            font=("Arial", 10)
        )
        store_region_value.config(text="")  # Clear the bold region value

def create_gui():  
    """
    Create the tkinter GUI for the application.
    """
    global store_entry, store_region_label, store_region_value  
    root = tk.Tk()  
    root.title("Site Manager Default Selector")  
    root.geometry("400x510")  
    root.configure(bg="#1e1e1e")  

    # Add instructions
    instructions = tk.Label(
        root,
        text="Select a region to set as the default:",
        font=("Arial", 10),
        bg="#1e1e1e",
        fg="#dcdcdc",
        anchor="w",
        padx=8
    )
    instructions.pack(pady=5, fill="x")

    # Add buttons for each region
    regions = [
        "Northwest/Canada",
        "Southern California",
        "Southwest",
        "Northeast",
        "Midwest",
        "Southeast"
    ]

    global buttons
    buttons = []
    for region in regions:
        btn = tk.Button(
            root,
            text=region,
            font=("Arial", 10),
            bg="#333333",
            fg="#dcdcdc",
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=5,
            command=lambda r=region: update_default(r)
        )
        btn.pack(pady=5, fill="x", padx=20)
        buttons.append(btn)

    # Add a status label
    global status_label
    status_label = tk.Text(
        root,
        height=2,
        bg="#1e1e1e",
        fg="#dcdcdc",
        font=("Arial", 12),
        relief="flat",
        borderwidth=0,
        wrap=tk.WORD,
        padx=8,
        pady=5
    )
    status_label.pack(pady=10, fill="x", padx=10)

    # Get the currently selected region and highlight its button
    current_default = get_current_default()
    if current_default:
        update_status("Current default:    ", current_default, "#00ffff")
        highlight_button(current_default)
    else:
        update_status("No default region set.", "", "red")

    # Add store lookup section
    store_frame = tk.Frame(root, bg="#1e1e1e")
    store_frame.pack(pady=10, fill="x", padx=20)

    store_label = tk.Label(
        store_frame,
        text="Enter store number to find its region:",
        font=("Arial", 10),
        bg="#1e1e1e",
        fg="#dcdcdc"
    )
    store_label.pack(anchor="w")

    input_frame = tk.Frame(store_frame, bg="#1e1e1e")
    input_frame.pack(fill="x", pady=5)

    store_entry = tk.Entry(
        input_frame,
        font=("Arial", 10),
        bg="#333333",
        fg="#dcdcdc",
        insertbackground="#dcdcdc",
        relief="solid",
        borderwidth=1,
        width=6
    )
    store_entry.pack(side="left", padx=(0, 5))

    store_button = tk.Button(
        input_frame,
        text="Find Region",
        font=("Arial", 10),
        bg="#007BFF",
        fg="white",
        relief="solid",
        borderwidth=2,
        command=display_store_region
    )
    store_button.pack(side="left")

    store_region_label = tk.Label(
        input_frame,
        text="",
        font=("Arial", 10),
        bg="#1e1e1e",
        fg="#dcdcdc",
        justify="left"
    )
    store_region_label.pack(side="left")

    store_region_value = tk.Label(
        input_frame,
        text="",
        font=("Arial", 10, "bold"),
        bg="#1e1e1e",
        fg="#dcdcdc",
        justify="left"
    )
    store_region_value.pack(side="left")

    # Bind Enter key to the "Find Region" button
    root.bind("<Return>", lambda event: display_store_region())

    # Launch Victor Client button
    launch_button = tk.Button(
        root,
        text="Launch Victor Client",
        font=("Arial", 12, "bold"),
        bg="#007BFF",
        fg="white",
        relief="solid",
        borderwidth=2,
        padx=10,
        pady=5,
        command=launch_victor_client
    )
    launch_button.pack(pady=5, side="bottom", fill="x", padx=20)

    root.mainloop()

# Run the GUI
create_gui()