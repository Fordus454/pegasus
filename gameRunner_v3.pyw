import random
import tkinter as tk
import pandas as pd  
from datetime import datetime  
import os  

frame = tk.Tk()
frame.title("Dungeon Master's Assistant")
frame.config(
    borderwidth=2, 
    relief= "groove")
frame.geometry("1045x905")



################################    Saves    #################################  
# Ensure 'Saves' directory exists  
if not os.path.exists('Saves'):  
    os.makedirs('Saves')  
  
def pad_list(lst, length):  
    """Pad a list with empty strings to match the desired length."""  
    return lst + [''] * (length - len(lst))  
  
def save_data(Event=None):  
    data = {  
        'PC_names': [  
            PC1_name_Label.get(), PC2_name_Label.get(), PC3_name_Label.get(),   
            PC4_name_Label.get(), PC5_name_Label.get(), PC6_name_Label.get()  
        ],  
        'PC_inits': [  
            pc1_Ientry.get(), pc2_Ientry.get(), pc3_Ientry.get(),   
            pc4_Ientry.get(), pc5_Ientry.get(), pc6_Ientry.get()  
        ],  
        'NPC_names': [  
            NPC0_name_Label.get(), NPC1_name_Label.get(), NPC2_name_Label.get(),   
            NPC3_name_Label.get(), NPC4_name_Label.get(), NPC5_name_Label.get(),                          
            NPC6_name_Label.get(), NPC7_name_Label.get(), NPC8_name_Label.get(),   
            NPC9_name_Label.get(), NPC10_name_Label.get(), NPC11_name_Label.get(),                          
            NPC12_name_Label.get(), NPC13_name_Label.get(), NPC14_name_Label.get(),   
            NPC15_name_Label.get(), NPC16_name_Label.get()  
        ],  
        'NPC_inits': [  
            npc1_Ientry.get(), npc2_Ientry.get(), npc3_Ientry.get(),   
            npc4_Ientry.get(), npc5_Ientry.get(), npc6_Ientry.get(), npc7_Ientry.get(),                          
            npc8_Ientry.get(), npc9_Ientry.get(), npc10_Ientry.get(),   
            npc11_Ientry.get(), npc12_Ientry.get(), npc13_Ientry.get(), npc14_Ientry.get(),                          
            npc15_Ientry.get(), npc16_Ientry.get(), npc17_Ientry.get()  
        ],  
        'Mod_entries': [  
            modentry.get(), NPCAmodentry.get(), NPCImodentry.get()  
        ],  
        'PC_HP_labels': [hp_label.get() for hp_label in hp_labels1],  
        'NPC_HP_labels': [hp_label.get() for hp_label in hp_labels],  
        'Spell_labels': [spell_label.get() for spell_label in spell_label_entries],  
        'Lair_actions': [lair_box1.get(), lair_box2.get(), lair_box3.get()],  
        'ASI_entries': [  
            ASIstr_Entry.get(), ASIdex_Entry.get(), ASIcon_Entry.get(),   
            ASIint_Entry.get(), ASIwis_Entry.get(), ASIcha_Entry.get()  
        ],  
        'Prof_entries': [  
            prof_entry.get(), prof_str_var.get(), prof_dex_var.get(),   
            prof_con_var.get(), prof_int_var.get(), prof_wis_var.get(),   
            prof_cha_var.get()  
        ]  
    }  
  
    # Find the maximum length of the lists  
    max_length = max(len(lst) for lst in data.values())  
  
    # Pad all lists to the same length  
    for key in data:  
        data[key] = pad_list(data[key], max_length)  
  
    df = pd.DataFrame(data)  
    timestamp = datetime.now().strftime("saveDMA_%m-%d-%Y_%H-%M-%S")  
    save_path = os.path.join('Saves', f"{timestamp}.csv")  
    df.to_csv(save_path, index=False)  
    print(f"Data saved to {save_path}")  
  
def load_data(Event=None):  
    file_list = os.listdir('Saves')  
    csv_files = [file for file in file_list if file.endswith('.csv')]  
  
    if not csv_files:  
        print("No saved files found.")  
        return  
  
    # Load the latest save file  
    latest_file = max(csv_files, key=lambda x: os.path.getmtime(os.path.join('Saves', x)))  
    load_path = os.path.join('Saves', latest_file)  
    df = pd.read_csv(load_path)  
  
    pc_labels = [  
        PC1_name_Label, PC2_name_Label, PC3_name_Label,   
        PC4_name_Label, PC5_name_Label, PC6_name_Label  
    ]  
    pc_entries = [  
        pc1_Ientry, pc2_Ientry, pc3_Ientry,   
        pc4_Ientry, pc5_Ientry, pc6_Ientry  
    ]  
    npc_labels = [  
        NPC0_name_Label, NPC1_name_Label, NPC2_name_Label,   
        NPC3_name_Label, NPC4_name_Label, NPC5_name_Label,                      
        NPC6_name_Label, NPC7_name_Label, NPC8_name_Label,   
        NPC9_name_Label, NPC10_name_Label, NPC11_name_Label,                      
        NPC12_name_Label, NPC13_name_Label, NPC14_name_Label,   
        NPC15_name_Label, NPC16_name_Label  
    ]  
    npc_entries = [  
        npc1_Ientry, npc2_Ientry, npc3_Ientry,   
        npc4_Ientry, npc5_Ientry, npc6_Ientry, npc7_Ientry,                      
        npc8_Ientry, npc9_Ientry, npc10_Ientry,   
        npc11_Ientry, npc12_Ientry, npc13_Ientry, npc14_Ientry,                      
        npc15_Ientry, npc16_Ientry, npc17_Ientry  
    ]  
  
    for i, name in enumerate(df['PC_names']):  
        if i < len(pc_labels):  
            pc_labels[i].delete(0, tk.END)  
            pc_labels[i].insert(0, name)  
  
    for i, init in enumerate(df['PC_inits']):  
        if i < len(pc_entries):  
            pc_entries[i].delete(0, tk.END)  
            if pd.isna(init) or init == '':  
                pc_entries[i].insert(0, '')  
            else:  
                pc_entries[i].insert(0, str(int(float(init))))  
  
    for i, name in enumerate(df['NPC_names']):  
        if i < len(npc_labels):  
            npc_labels[i].delete(0, tk.END)  
            npc_labels[i].insert(0, name if not pd.isna(name) else "N/A")  
  
    for i, init in enumerate(df['NPC_inits']):  
        if i < len(npc_entries):  
            npc_entries[i].delete(0, tk.END)  
            if pd.isna(init) or init == '':  
                npc_entries[i].insert(0, '')  
            else:  
                npc_entries[i].insert(0, str(int(float(init))))  
  
    modentry.delete(0, tk.END)  
    modentry.insert(0, str(int(float(df['Mod_entries'][0]))) if not pd.isna(df['Mod_entries'][0]) and df['Mod_entries'][0] != '' else '')  
  
    NPCAmodentry.delete(0, tk.END)  
    NPCAmodentry.insert(0, str(int(float(df['Mod_entries'][1]))) if not pd.isna(df['Mod_entries'][1]) and df['Mod_entries'][1] != '' else '')  
  
    NPCImodentry.delete(0, tk.END)  
    NPCImodentry.insert(0, str(int(float(df['Mod_entries'][2]))) if not pd.isna(df['Mod_entries'][2]) and df['Mod_entries'][2] != '' else '')  
  
    for i, hp in enumerate(df['PC_HP_labels']):  
        if i < len(hp_labels1):  
            hp_labels1[i].delete(0, tk.END)  
            if pd.isna(hp) or hp == '' or hp == '-0-':  
                hp_labels1[i].insert(0, '-0-')  
            else:  
                hp_labels1[i].insert(0, str(int(float(hp))))  
  
    for i, hp in enumerate(df['NPC_HP_labels']):  
        if i < len(hp_labels):  
            hp_labels[i].delete(0, tk.END)  
            if pd.isna(hp) or hp == '' or hp == '-0-':  
                hp_labels[i].insert(0, '0')  
            else:  
                hp_labels[i].insert(0, str(int(float(hp))))  
  
    for i, spell in enumerate(df['Spell_labels']):  
        if i < len(spell_label_entries):  
            spell_label_entries[i].delete(0, tk.END)  
            spell_label_entries[i].insert(0, spell)  
  
    lair_boxes = [lair_box1, lair_box2, lair_box3]  
    for i, lair_action in enumerate(df['Lair_actions']):  
        if i < len(lair_boxes):  
            lair_boxes[i].delete(0, tk.END)  
            if pd.isna(lair_action) or lair_action == '':  
                lair_boxes[i].insert(0, "N/A")  
            else:  
                lair_boxes[i].insert(0, str(int(float(lair_action))))  
  
    asi_entries = [  
        ASIstr_Entry, ASIdex_Entry, ASIcon_Entry,   
        ASIint_Entry, ASIwis_Entry, ASIcha_Entry  
    ]  
    for i, asi in enumerate(df['ASI_entries']):  
        if i < len(asi_entries):  
            asi_entries[i].delete(0, tk.END)  
            asi_entries[i].insert(0, str(int(float(asi))) if not pd.isna(asi) and asi != '' else '0')  
  
    prof_entry.delete(0, tk.END)  
    prof_entry.insert(0, str(int(float(df['Prof_entries'][0]))) if not pd.isna(df['Prof_entries'][0]) and df['Prof_entries'][0] != '' else '0')  
  
    prof_vars = [  
        prof_str_var, prof_dex_var, prof_con_var,   
        prof_int_var, prof_wis_var, prof_cha_var  
    ]  
    for i, prof in enumerate(df['Prof_entries'][1:]):  
        if i < len(prof_vars):  
            prof_vars[i].set(int(prof))  
  
    print(f"Data loaded from {load_path}")
    calc_asi()
    sort_init()  


# Adding Save and Load buttons  
save_button = tk.Button(  
    frame,  
    width=11,  
    borderwidth=3,  
    relief="raised",  
    activebackground="#d1b779",  
    text="Save",
    fg="Blue",  
    font="Ariel 11",  
    command=save_data  
)  
save_button.grid(column=4, row=31, sticky="W", pady=3, padx=3)  
  
load_button = tk.Button(  
    frame,  
    width=11,  
    borderwidth=3,  
    relief="raised",  
    activebackground="#d1b779",  
    text="Load",
    fg="Blue",  
    font="Ariel 11",  
    command=load_data  
)  
load_button.grid(column=5, row=31, sticky="W", pady=3, padx=3)  






######################
def rollD20 (Event=None):
    userInput_modifier = modentry.get()
    rolled_result = random.randint(1,20)
    total = (int(userInput_modifier) + rolled_result)
    d20label.config(text = str(rolled_result) + "+" + userInput_modifier + " = " + str(total))
    
def rollD202 (Event=None):
    userInput_modifier = modentry.get()
    rolled_result = random.randint(1,20)
    total = (int(userInput_modifier) + rolled_result)
    d202label.config(text = str(rolled_result) + "+" + userInput_modifier + " = " + str(total))

def rollD100 (Event=None):
    rolled_result = random.randint(1,100)
    d100label.config(text = str(rolled_result))

def rollD4 (Event=None):
    userInput_modifier = modentry.get()
    mult = d4mult.get()
    intmult = int(mult)
    multroll = 0
    for _ in range(intmult):
        multroll += random.randint(1,4)
    total = (int(userInput_modifier) + multroll)
    d4label.config(text = str(multroll)+ "+" + userInput_modifier + " = " + str(total))

def rollD6 (Event=None):
    userInput_modifier = modentry.get()
    mult = d6mult.get()
    intmult = int(mult)
    multroll = 0
    for _ in range(intmult):
        multroll += random.randint(1,6)
    total = (int(userInput_modifier) + multroll)
    d6label.config(text = str(multroll)+ "+" + userInput_modifier + " = " + str(total))
    
def rollD8 (Event=None):
    userInput_modifier = modentry.get()
    mult = d8mult.get()
    intmult = int(mult)
    multroll = 0
    for _ in range(intmult):
        multroll += random.randint(1,8)
    total = (int(userInput_modifier) + multroll)
    d8label.config(text = str(multroll)+ "+" + userInput_modifier + " = " + str(total))
    
def rollD10 (Event=None):
    userInput_modifier = modentry.get()
    mult = d10mult.get()
    intmult = int(mult)
    multroll = 0
    for _ in range(intmult):
        multroll += random.randint(1,10)
    total = (int(userInput_modifier) + multroll)
    d10label.config(text = str(multroll)+ "+" + userInput_modifier + " = " + str(total))
    
def rollD12 (Event=None):
    userInput_modifier = modentry.get()
    mult = d12mult.get()
    intmult = int(mult)
    multroll = 0
    for _ in range(intmult):
        multroll += random.randint(1,12)
    total = (int(userInput_modifier) + multroll)
    d12label.config(text = str(multroll)+ "+" + userInput_modifier + " = " + str(total))

def roll_init (Event=None):
    initiative_dictionary = {}
    DMInput_modifier = NPCImodentry.get()

    npc1_Ientry.delete(0, tk.END)
    npc2_Ientry.delete(0, tk.END)
    npc3_Ientry.delete(0, tk.END)
    npc4_Ientry.delete(0, tk.END)
    npc5_Ientry.delete(0, tk.END)
    npc6_Ientry.delete(0, tk.END)
    npc7_Ientry.delete(0, tk.END)
    npc8_Ientry.delete(0, tk.END)
    npc9_Ientry.delete(0, tk.END)
    npc10_Ientry.delete(0, tk.END)
    npc11_Ientry.delete(0, tk.END)
    npc12_Ientry.delete(0, tk.END)
    npc13_Ientry.delete(0, tk.END)
    npc14_Ientry.delete(0, tk.END)
    npc15_Ientry.delete(0, tk.END)
    npc16_Ientry.delete(0, tk.END)
    npc17_Ientry.delete(0, tk.END)

    if PC1_name_Label.get() != "":
        initiative_dictionary[PC1_name_Label.get()] = int(pc1_Ientry.get())
    if PC2_name_Label.get() != "":
        initiative_dictionary[PC2_name_Label.get()] = int(pc2_Ientry.get())
    if PC3_name_Label.get() != "":
        initiative_dictionary[PC3_name_Label.get()] = int(pc3_Ientry.get())
    if PC4_name_Label.get() != "":
        initiative_dictionary[PC4_name_Label.get()] = int(pc4_Ientry.get())
    if PC5_name_Label.get() != "":
        initiative_dictionary[PC5_name_Label.get()] = int(pc5_Ientry.get())
    if PC6_name_Label.get() != "":
        initiative_dictionary[PC6_name_Label.get()] = int(pc6_Ientry.get())

    koolaid = NPC0_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc1_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc1_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc1_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc1_Ientry.config(fg="#944747", font="arial 11 bold")
        npc1_Ientry.insert(0, str(total))
        initiative_dictionary[NPC0_name_Label.get()] = int(npc1_Ientry.get())

    koolaid = NPC1_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc2_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc2_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc2_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc2_Ientry.config(fg="#944747", font="arial 11 bold")
        npc2_Ientry.insert(0, str(total))
        initiative_dictionary[NPC1_name_Label.get()] = int(npc2_Ientry.get())

    koolaid = NPC2_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc3_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc3_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc3_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc3_Ientry.config(fg="#944747", font="arial 11 bold")
        npc3_Ientry.insert(0, str(total))
        initiative_dictionary[NPC2_name_Label.get()] = int(npc3_Ientry.get())

    koolaid = NPC3_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc4_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc4_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc4_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc4_Ientry.config(fg="#944747", font="arial 11 bold")
        npc4_Ientry.insert(0, str(total))
        initiative_dictionary[NPC3_name_Label.get()] = int(npc4_Ientry.get())

    koolaid = NPC4_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc5_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc5_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc5_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc5_Ientry.config(fg="#944747", font="arial 11 bold")
        npc5_Ientry.insert(0, str(total))
        initiative_dictionary[NPC4_name_Label.get()] = int(npc5_Ientry.get())

    koolaid = NPC5_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc6_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc6_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc6_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc6_Ientry.config(fg="#944747", font="arial 11 bold")
        npc6_Ientry.insert(0, str(total))
        initiative_dictionary[NPC5_name_Label.get()] = int(npc6_Ientry.get())

    koolaid = NPC6_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc7_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc7_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc7_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc7_Ientry.config(fg="#944747", font="arial 11 bold")
        npc7_Ientry.insert(0, str(total))
        initiative_dictionary[NPC6_name_Label.get()] = int(npc7_Ientry.get())

    koolaid = NPC7_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc8_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc8_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc8_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc8_Ientry.config(fg="#944747", font="arial 11 bold")
        npc8_Ientry.insert(0, str(total))
        initiative_dictionary[NPC7_name_Label.get()] = int(npc8_Ientry.get())

    koolaid = NPC8_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc9_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc9_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc9_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc9_Ientry.config(fg="#944747", font="arial 11 bold")
        npc9_Ientry.insert(0, str(total))
        initiative_dictionary[NPC8_name_Label.get()] = int(npc9_Ientry.get())

    koolaid = NPC9_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc10_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc10_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc10_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc10_Ientry.config(fg="#944747", font="arial 11 bold")
        npc10_Ientry.insert(0, str(total))
        initiative_dictionary[NPC9_name_Label.get()] = int(npc10_Ientry.get())

    koolaid = NPC10_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc11_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc11_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc11_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc11_Ientry.config(fg="#944747", font="arial 11 bold")
        npc11_Ientry.insert(0, str(total))
        initiative_dictionary[NPC10_name_Label.get()] = int(npc11_Ientry.get())

    koolaid = NPC11_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc12_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc12_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc12_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc12_Ientry.config(fg="#944747", font="arial 11 bold")
        npc12_Ientry.insert(0, str(total))
        initiative_dictionary[NPC11_name_Label.get()] = int(npc12_Ientry.get())

    koolaid = NPC12_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc13_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc13_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc13_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc13_Ientry.config(fg="#944747", font="arial 11 bold")
        npc13_Ientry.insert(0, str(total))
        initiative_dictionary[NPC12_name_Label.get()] = int(npc13_Ientry.get())

    koolaid = NPC13_name_Label.get()
    if koolaid != "":  
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc14_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc14_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc14_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc14_Ientry.config(fg="#944747", font="arial 11 bold")
        npc14_Ientry.insert(0, str(total))
        initiative_dictionary[NPC13_name_Label.get()] = int(npc14_Ientry.get())

    koolaid = (NPC14_name_Label).get()
    if koolaid != "":    
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc15_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc15_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc15_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc15_Ientry.config(fg="#944747", font="arial 11 bold")
        npc15_Ientry.insert(0, str(total))
        initiative_dictionary[NPC14_name_Label.get()] = int(npc15_Ientry.get())

    koolaid = NPC15_name_Label.get()
    if koolaid != "":
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc16_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc16_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc16_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc16_Ientry.config(fg="#944747", font="arial 11 bold")
        npc16_Ientry.insert(0, str(total))
        initiative_dictionary[NPC15_name_Label.get()] = int(npc16_Ientry.get())

    koolaid = NPC16_name_Label.get()
    if koolaid != "":
        rolled_result = random.randint(1,20)
        total = (int(DMInput_modifier) + rolled_result)
        if total > 15:
            npc17_Ientry.config(fg="#012075", font="arial 11 bold")
        elif total > 10:
            npc17_Ientry.config(fg="#336643", font="arial 11 bold")
        elif total > 5:
            npc17_Ientry.config(fg="#948247", font="arial 11 bold")
        else:
            npc17_Ientry.config(fg="#944747", font="arial 11 bold")
        npc17_Ientry.insert(0, str(total))
        initiative_dictionary[NPC16_name_Label.get()] = int(npc17_Ientry.get())

    sorty = sorted(initiative_dictionary.items(), key=lambda x:x[1], reverse=True)
    Init_track0.config(text=sorty[0])
    try:
        Init_track1.config(text=sorty[1])
    except:
        Init_track1.config(text="n/a")
    try:
        Init_track2.config(text=sorty[2])
    except:
        Init_track2.config(text="n/a")
    try:
        Init_track3.config(text=sorty[3])
    except:
        Init_track3.config(text="n/a")
    try:  
        Init_track4.config(text=sorty[4])
    except:
        Init_track4.config(text="n/a")
    try:  
        Init_track5.config(text=sorty[5])
    except:
        Init_track5.config(text="n/a")
    try:  
        Init_track6.config(text=sorty[6])
    except:
        Init_track6.config(text="n/a")
    try:  
        Init_track7.config(text=sorty[7])
    except:
        Init_track7.config(text="n/a")
    try:  
        Init_track8.config(text=sorty[8])
    except:
        Init_track8.config(text="n/a")
    try:  
        Init_track9.config(text=sorty[9])
    except:
        Init_track9.config(text="n/a")
    try:  
        Init_track10.config(text=sorty[10])
    except:
        Init_track10.config(text="n/a")
    try:  
        Init_track11.config(text=sorty[11])
    except:
        Init_track11.config(text="n/a")
    try:  
        Init_track12.config(text=sorty[12])
    except:
        Init_track12.config(text="n/a")
    try:  
        Init_track13.config(text=sorty[13])
    except:
        Init_track13.config(text="n/a")
    try:  
        Init_track14.config(text=sorty[14])
    except:
        Init_track14.config(text="n/a")
    try:  
        Init_track15.config(text=sorty[15])
    except:
        Init_track15.config(text="n/a")
    try: 
        Init_track16.config(text=sorty[16])
    except:
        Init_track16.config(text="n/a")
    try:
        Init_track17.config(text=sorty[17])
    except:
        Init_track17.config(text="n/a")
    try:
        Init_track18.config(text=sorty[18])
    except:
        Init_track18.config(text="n/a")
    try:
        Init_track19.config(text=sorty[19])
    except:
        Init_track19.config(text="n/a")
    try:
        Init_track20.config(text=sorty[20])
    except:
        Init_track20.config(text="n/a")
    try:
        Init_track21.config(text=sorty[21])
    except:
        Init_track21.config(text="n/a")
    try:
        Init_track22.config(text=sorty[22])
    except:
        Init_track22.config(text="n/a")
    
def sort_init():  
    initiative_dictionary = {}  
    pc_labels = [  
        PC1_name_Label, PC2_name_Label, PC3_name_Label,  
        PC4_name_Label, PC5_name_Label, PC6_name_Label  
    ]  
  
    pc_entries = [  
        pc1_Ientry, pc2_Ientry, pc3_Ientry,  
        pc4_Ientry, pc5_Ientry, pc6_Ientry  
    ]  
  
    npc_labels = [  
        NPC0_name_Label, NPC1_name_Label, NPC2_name_Label,  
        NPC3_name_Label, NPC4_name_Label, NPC5_name_Label,  
        NPC6_name_Label, NPC7_name_Label, NPC8_name_Label,  
        NPC9_name_Label, NPC10_name_Label, NPC11_name_Label,  
        NPC12_name_Label, NPC13_name_Label, NPC14_name_Label,  
        NPC15_name_Label, NPC16_name_Label  
    ]  
  
    npc_entries = [  
        npc1_Ientry, npc2_Ientry, npc3_Ientry,  
        npc4_Ientry, npc5_Ientry, npc6_Ientry, npc7_Ientry,  
        npc8_Ientry, npc9_Ientry, npc10_Ientry,  
        npc11_Ientry, npc12_Ientry, npc13_Ientry, npc14_Ientry,  
        npc15_Ientry, npc16_Ientry, npc17_Ientry  
    ]  
  
    # Add PCs to the initiative dictionary  
    for i, label in enumerate(pc_labels):  
        name = label.get()  
        if name:  
            try:  
                initiative = int(pc_entries[i].get())  
                initiative_dictionary[name] = initiative  
            except ValueError:  
                continue  
  
    # Add NPCs to the initiative dictionary  
    for i, label in enumerate(npc_labels):  
        name = label.get()  
        if name:  
            try:  
                initiative = int(npc_entries[i].get())  
                initiative_dictionary[name] = initiative  
            except ValueError:  
                continue  
  
    # Sort the dictionary by initiative values  
    sorted_initiatives = sorted(initiative_dictionary.items(), key=lambda x: x[1], reverse=True)  
  
    # Update the initiative display labels and apply color scheme  
    for i, (name, initiative) in enumerate(sorted_initiatives):  
        if i < 23:  # Ensure we don't exceed the number of initiative display labels  
            eval(f'Init_track{i}.config(text="{name} - {initiative}")')  
            if name in [label.get() for label in npc_labels]:  # Check if the name is an NPC  
                npc_index = [label.get() for label in npc_labels].index(name)  
                npc_entry = npc_entries[npc_index]  
                if initiative > 15:  
                    npc_entry.config(fg="#012075", font="arial 11 bold")  
                elif initiative > 10:  
                    npc_entry.config(fg="#336643", font="arial 11 bold")  
                elif initiative > 5:  
                    npc_entry.config(fg="#948247", font="arial 11 bold")  
                else:  
                    npc_entry.config(fg="#944747", font="arial 11 bold")  
  
    # Clear any remaining initiative display labels  
    for i in range(len(sorted_initiatives), 23):  
        eval(f'Init_track{i}.config(text="- initiative -")')  

def drop_npc (Event=None):
    if NPC16_name_Label.get() != "":  
        NPC16_name_Label.delete(0, tk.END)
    elif NPC15_name_Label.get() != "":
        NPC15_name_Label.delete(0, tk.END)
    elif NPC15_name_Label.get() != "":
        NPC15_name_Label.delete(0, tk.END)
    elif NPC14_name_Label.get() != "":
        NPC14_name_Label.delete(0, tk.END)
    elif NPC13_name_Label.get() != "":
        NPC13_name_Label.delete(0, tk.END)
    elif NPC12_name_Label.get() != "":
        NPC12_name_Label.delete(0, tk.END)
    elif NPC11_name_Label.get() != "":
        NPC11_name_Label.delete(0, tk.END)
    elif NPC10_name_Label.get() != "":
        NPC10_name_Label.delete(0, tk.END)
    elif NPC9_name_Label.get() != "":
        NPC9_name_Label.delete(0, tk.END)
    elif NPC8_name_Label.get() != "":
        NPC8_name_Label.delete(0, tk.END)
    elif NPC7_name_Label.get() != "":
        NPC7_name_Label.delete(0, tk.END)
    elif NPC6_name_Label.get() != "":
        NPC6_name_Label.delete(0, tk.END)
    elif NPC5_name_Label.get() != "":
        NPC5_name_Label.delete(0, tk.END)
    elif NPC4_name_Label.get() != "":
        NPC4_name_Label.delete(0, tk.END)
    elif NPC3_name_Label.get() != "":
        NPC3_name_Label.delete(0, tk.END)
    elif NPC2_name_Label.get() != "":
        NPC2_name_Label.delete(0, tk.END)
    elif NPC1_name_Label.get() != "":
        NPC1_name_Label.delete(0, tk.END)



def add_npc (Event=None):
    if NPC1_name_Label.get() == "":  
        NPC1_name_Label.insert(0, "NPC 1")
    elif NPC2_name_Label.get() == "":
        NPC2_name_Label.insert(0, "NPC 2")
    elif NPC3_name_Label.get() == "":
        NPC3_name_Label.insert(0, "NPC 3")
    elif NPC4_name_Label.get() == "":
        NPC4_name_Label.insert(0, "NPC 4")
    elif NPC5_name_Label.get() == "":
        NPC5_name_Label.insert(0, "NPC 5")
    elif NPC6_name_Label.get() == "":
        NPC6_name_Label.insert(0, "NPC 6")
    elif NPC7_name_Label.get() == "":
        NPC7_name_Label.insert(0, "NPC 7")
    elif NPC8_name_Label.get() == "":
        NPC8_name_Label.insert(0, "NPC 8")
    elif NPC9_name_Label.get() == "":
        NPC9_name_Label.insert(0, "NPC 9")
    elif NPC10_name_Label.get() == "":
        NPC10_name_Label.insert(0, "NPC 10")
    elif NPC11_name_Label.get() == "":
        NPC11_name_Label.insert(0, "NPC 11")
    elif NPC12_name_Label.get() == "":
        NPC12_name_Label.insert(0, "NPC 12")
    elif NPC13_name_Label.get() == "":
        NPC13_name_Label.insert(0, "NPC 13")
    elif NPC14_name_Label.get() == "":
        NPC14_name_Label.insert(0, "NPC 14")
    elif NPC15_name_Label.get() == "":
        NPC15_name_Label.insert(0, "NPC 15")
    elif NPC16_name_Label.get() == "":
        NPC16_name_Label.insert(0, "NPC 16") 

        
def roll_attacks (Event=None):
    npc1_Alabel.config(text= "")
    npc2_Alabel.config(text= "")
    npc3_Alabel.config(text= "")
    npc4_Alabel.config(text= "")
    npc5_Alabel.config(text= "")
    npc6_Alabel.config(text= "")
    npc7_Alabel.config(text= "")
    npc8_Alabel.config(text= "")
    npc9_Alabel.config(text= "")
    npc10_Alabel.config(text= "")
    npc11_Alabel.config(text= "")
    npc12_Alabel.config(text= "")
    npc13_Alabel.config(text= "")
    npc14_Alabel.config(text= "")
    npc15_Alabel.config(text= "")
    npc16_Alabel.config(text= "")
    npc17_Alabel.config(text= "")

    DMatt_mod = NPCAmodentry.get()
    koolaid = NPC0_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc1_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC1_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc2_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC2_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc3_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC3_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc4_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC4_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc5_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC5_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc6_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC6_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc7_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC7_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc8_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC8_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc9_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC9_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc10_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC10_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc11_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC11_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc12_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC12_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc13_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC13_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc14_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC14_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc15_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC15_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc16_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    koolaid = NPC16_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc17_Alabel.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " + str(total))
    
def roll_attacks2 (Event=None):
    npc1_A2label.config(text= "")
    npc2_A2label.config(text= "")
    npc3_A2label.config(text= "")
    npc4_A2label.config(text= "")
    npc5_A2label.config(text= "")
    npc6_A2label.config(text= "")
    npc7_A2label.config(text= "")
    npc8_A2label.config(text= "")
    npc9_A2label.config(text= "")
    npc10_A2label.config(text= "")
    npc11_A2label.config(text= "")
    npc12_A2label.config(text= "")
    npc13_A2label.config(text= "")
    npc14_A2label.config(text= "")
    npc15_A2label.config(text= "")
    npc16_A2label.config(text= "")
    npc17_A2label.config(text= "")

    DMatt_mod = NPCAmodentry.get()
    koolaid = NPC0_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc1_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC1_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc2_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC2_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc3_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC3_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc4_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC4_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc5_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC5_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc6_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC6_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc7_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC7_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc8_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC8_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc9_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC9_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc10_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC10_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc11_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC11_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc12_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC12_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc13_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC13_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc14_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC14_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc15_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC15_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc16_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))
    koolaid = NPC16_name_Label.get()
    if koolaid != "":     
        rolled_result = random.randint(1,20)
        total = (int(DMatt_mod) + rolled_result)
        npc17_A2label.config(text= " " + str(rolled_result) + "+" + DMatt_mod + " = " +str(total))

def clear_npc_rolls(Event=None):
    pc1_Ientry.delete(0, tk.END)
    pc1_Ientry.insert(0, "0")
    pc2_Ientry.delete(0, tk.END)
    pc2_Ientry.insert(0, "0")
    pc3_Ientry.delete(0, tk.END)
    pc3_Ientry.insert(0, "0")
    pc4_Ientry.delete(0, tk.END)
    pc4_Ientry.insert(0, "0")
    pc5_Ientry.delete(0, tk.END)
    pc5_Ientry.insert(0, "0")
    pc6_Ientry.delete(0, tk.END)
    pc6_Ientry.insert(0, "0")

    npc1_Ientry.delete(0, tk.END)
    NPC0_name_Label.delete(0, tk.END)
    NPC0_name_Label.insert(0, "BBG")
    npc2_Ientry.delete(0, tk.END)
    NPC1_name_Label.delete(0, tk.END)
    NPC1_name_Label.insert(0, "NPC 1")
    npc3_Ientry.delete(0, tk.END)
    NPC2_name_Label.delete(0, tk.END)
    NPC2_name_Label.insert(0, "NPC 2")
    npc4_Ientry.delete(0, tk.END)
    NPC3_name_Label.delete(0, tk.END)
    NPC3_name_Label.insert(0, "NPC 3")
    npc5_Ientry.delete(0, tk.END)
    NPC4_name_Label.delete(0, tk.END)
    NPC4_name_Label.insert(0, "NPC 4")
    npc6_Ientry.delete(0, tk.END)
    NPC5_name_Label.delete(0, tk.END)
    NPC5_name_Label.insert(0, "NPC 5")
    npc7_Ientry.delete(0, tk.END)
    NPC6_name_Label.delete(0, tk.END)
    NPC6_name_Label.insert(0, "NPC 6")
    npc8_Ientry.delete(0, tk.END)
    NPC7_name_Label.delete(0, tk.END)
    NPC7_name_Label.insert(0, "NPC 7")
    npc9_Ientry.delete(0, tk.END)
    NPC8_name_Label.delete(0, tk.END)
    NPC8_name_Label.insert(0, "NPC 8")
    npc10_Ientry.delete(0, tk.END)
    NPC9_name_Label.delete(0, tk.END)
    NPC9_name_Label.insert(0, "NPC 9")
    npc11_Ientry.delete(0, tk.END)
    NPC10_name_Label.delete(0, tk.END)
    NPC10_name_Label.insert(0, "NPC 10")
    npc12_Ientry.delete(0, tk.END)
    NPC11_name_Label.delete(0, tk.END)
    NPC11_name_Label.insert(0, "NPC 11")
    npc13_Ientry.delete(0, tk.END)
    NPC12_name_Label.delete(0, tk.END)
    NPC12_name_Label.insert(0, "NPC 12")
    npc14_Ientry.delete(0, tk.END)
    NPC13_name_Label.delete(0, tk.END)
    NPC13_name_Label.insert(0, "NPC 13")
    npc15_Ientry.delete(0, tk.END)
    NPC14_name_Label.delete(0, tk.END)
    NPC14_name_Label.insert(0, "NPC 14")
    npc16_Ientry.delete(0, tk.END)
    NPC15_name_Label.delete(0, tk.END)
    NPC15_name_Label.insert(0, "NPC 15")
    npc17_Ientry.delete(0, tk.END)
    NPC16_name_Label.delete(0, tk.END)
    NPC16_name_Label.insert(0, "NPC 16")

    npc1_Alabel.config(text= "")
    npc2_Alabel.config(text= "")
    npc3_Alabel.config(text= "")
    npc4_Alabel.config(text= "")
    npc5_Alabel.config(text= "")
    npc6_Alabel.config(text= "")
    npc7_Alabel.config(text= "")
    npc8_Alabel.config(text= "")
    npc9_Alabel.config(text= "")
    npc10_Alabel.config(text= "")
    npc11_Alabel.config(text= "")
    npc12_Alabel.config(text= "")
    npc13_Alabel.config(text= "")
    npc14_Alabel.config(text= "")
    npc15_Alabel.config(text= "")
    npc16_Alabel.config(text= "")
    npc17_Alabel.config(text= "")

    npc1_A2label.config(text= "")
    npc2_A2label.config(text= "")
    npc3_A2label.config(text= "")
    npc4_A2label.config(text= "")
    npc5_A2label.config(text= "")
    npc6_A2label.config(text= "")
    npc7_A2label.config(text= "")
    npc8_A2label.config(text= "")
    npc9_A2label.config(text= "")
    npc10_A2label.config(text= "")
    npc11_A2label.config(text= "")
    npc12_A2label.config(text= "")
    npc13_A2label.config(text= "")
    npc14_A2label.config(text= "")
    npc15_A2label.config(text= "")
    npc16_A2label.config(text= "")
    npc17_A2label.config(text= "")


def clear_npc_hp(Event=None):  
    for hp_label in hp_labels:  
        hp_label.delete(0, tk.END)  
        hp_label.insert(0, "0")  

def set_npc_hp(Event=None):  
    npc_attack_modifier = NPCAmodentry.get()  # Get current NPC attack modifier value  
    for hp_label in hp_labels:  # Loop through X HP labels  
        hp_label.delete(0, tk.END)  
        hp_label.insert(0, npc_attack_modifier)  




###################################################################
#### NORTH DICE ###################################################
###################################################################
button20 = tk.Button(
    frame,
    width = 11,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "Roll 1st D20",
    font = "Ariel 10 bold",
    command = rollD20)
button20.grid(column=4, row=1, sticky="E",pady=(1,0), padx=(7,3))
d20label = tk.Label(
    text = "",
    width = 11,
    bg = "Snow",
    font = "Ariel 11 bold")
d20label.grid(column=5, row=1, sticky="W",pady=(1,0), padx=3)
button202 = tk.Button(
    frame,
    width = 11,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "Roll 2nd D20",
    font = "Ariel 10 bold",
    command = rollD202)
button202.grid(column=4, row=2, sticky="E",pady=(1,0), padx=(7,3))
d202label = tk.Label(
    text = "",
    width = 11,
    bg = "Snow",
    font = "Ariel 11 bold")
d202label.grid(column=5, row=2, sticky="W",pady=(1,0), padx=3)

button100 = tk.Button(
    frame,
    width = 11,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "Roll D100",
    font = "Ariel 10 bold",
    command = rollD100)
button100.grid(column=4, row=3, sticky="E",pady=(1,0), padx=(7,3))
d100label = tk.Label(
    text = "",
    width = 11,
    bg = "Snow",
    font = "Ariel 11 bold")
d100label.grid(column=5, row=3, sticky="W",pady=(1,0), padx=3)

button4 = tk.Button(
    frame,
    width = 5,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "D4",
    font = "Ariel 8 bold",
    command = rollD4)
button4.grid(column=4, row=4, sticky="E",pady=(1,0), padx=3)
d4label = tk.Label(
    text = "",
    width = 12,
    bg = "Snow",
    font = "Ariel 10 bold")
d4label.grid(column=5, row=4, sticky="W",pady=(1,0), padx=3)
d4mult = tk.Entry(frame, width = 3, bg = "Snow", font = "Ariel 10 bold")
d4mult.insert(0, "1")
d4mult.grid(column=4, row=4, sticky="W",pady=(1,0), padx=(30,0))
d4X = tk.Label(
    text = "x",
    width = 1,
    font = "Ariel 10 bold")
d4X.grid(column=4, row=4,pady=(1,0))

button6 = tk.Button(
    frame,
    width = 5,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "D6",
    font = "Ariel 8 bold",
    command = rollD6)
button6.grid(column=4, row=5, sticky="E",pady=(1,0), padx=3)
d6label = tk.Label(
    text = "",
    width = 12,
    bg = "Snow",
    font = "Ariel 10 bold")
d6label.grid(column=5, row=5, sticky="W",pady=(1,0), padx=3)
d6mult = tk.Entry(frame, width = 3, bg = "Snow", font = "Ariel 10 bold")
d6mult.insert(0, "1")
d6mult.grid(column=4, row=5, sticky="W",pady=(1,0), padx=(30,0))
d6X = tk.Label(
    text = "x",
    width = 1,
    font = "Ariel 10 bold")
d6X.grid(column=4, row=5,pady=(1,0))

button8 = tk.Button(
    frame,
    width = 5,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "D8",
    font = "Ariel 8 bold",
    command = rollD8)
button8.grid(column=4, row=6, sticky="E",pady=(1,0), padx=3)
d8label = tk.Label(
    text = "",
    width = 12,
    bg = "Snow",
    font = "Ariel 10 bold")
d8label.grid(column=5, row=6, sticky="W",pady=(1,0), padx=3)
d8mult = tk.Entry(frame, width = 3, bg = "Snow", font = "Ariel 10 bold")
d8mult.insert(0, "1")
d8mult.grid(column=4, row=6, sticky="W",pady=(1,0), padx=(30,0))
d8X = tk.Label(
    text = "x",
    width = 1,
    font = "Ariel 10 bold")
d8X.grid(column=4, row=6,pady=(1,0))

button10 = tk.Button(
    frame,
    width = 5,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "D10",
    font = "Ariel 8 bold",
    command = rollD10)
button10.grid(column=4, row=7, sticky="E",pady=(1,0), padx=3)
d10label = tk.Label(
    text = "",
    width = 12,
    bg = "Snow",
    font = "Ariel 10 bold")
d10label.grid(column=5, row=7, sticky="W",pady=(1,0), padx=3)
d10mult = tk.Entry(frame, width = 3, bg = "Snow", font = "Ariel 10 bold")
d10mult.insert(0, "1")
d10mult.grid(column=4, row=7, sticky="W",pady=(1,0), padx=(30,0))
d10X = tk.Label(
    text = "x",
    width = 1,
    font = "Ariel 10 bold")
d10X.grid(column=4, row=7,pady=(1,0))

button12 = tk.Button(
    frame,
    width = 5,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "D12",
    font = "Ariel 8 bold",
    command = rollD12)
button12.grid(column=4, row=8, sticky="E",pady=(1,0), padx=3)
d12label = tk.Label(
    text = "",
    width = 12,
    bg = "Snow",
    font = "Ariel 10 bold")
d12label.grid(column=5, row=8, sticky="W",pady=(1,0), padx=3)
d12mult = tk.Entry(frame, width = 3, bg = "Snow", font = "Ariel 10 bold")
d12mult.insert(0, "1")
d12mult.grid(column=4, row=8, sticky="W",pady=(1,0), padx=(30,0))
d12X = tk.Label(
    text = "x",
    width = 1,
    font = "Ariel 10 bold")
d12X.grid(column=4, row=8,pady=(1,0))


setHP_button = tk.Button(  
    frame,  
    width=6,  
    borderwidth=3,  
    relief="raised",  
    activebackground="#d1b779",  
    text="Set HP",  
    font="Ariel 11",  
    fg="blue",  
    command=set_npc_hp)  
setHP_button.grid(column=0, row=4, sticky="W", pady=(1, 0), padx=3)  




#### MODIFIERS ####
modlabel = tk.Label(
    text = "Dice Modifier:",
    font = "Ariel 10")
modlabel.grid(column=0, columnspan=2, row=1, pady=3, padx=(36,0))
modentry =  tk.Entry(frame, width = 4, font = "Ariel 12", borderwidth = 1, relief = "sunken")
modentry.insert(0, "0")
modentry.grid(column=1, row=1, sticky="E",pady=3, padx=3)

NPCAmodlabel = tk.Label(
    text = "NPC HP & Attack Mod:",
    font = "Ariel 10")
NPCAmodlabel.grid(column=0, columnspan=2, row=2, pady=3, padx=(26,0))
NPCAmodentry =  tk.Entry(frame, width = 4, font = "Ariel 12", borderwidth = 1, relief = "sunken")
NPCAmodentry.insert(0, "0")
NPCAmodentry.grid(column=1, row=2, sticky="E",pady=3, padx=3)

NPCImodlabel = tk.Label(
    text = "NPC Initiative Modifier:",
    anchor="e",
    font = "Ariel 10")
NPCImodlabel.grid(column=0, columnspan=2, row=3, pady=3, padx=(20,0))
NPCImodentry =  tk.Entry(frame, width = 4, font = "Ariel 12", borderwidth = 1, relief = "sunken")
NPCImodentry.insert(0, "0")
NPCImodentry.grid(column=1, row=3, sticky="E",pady=3, padx=3)


#### HEADER LABELS ####
headlabel_modify = tk.Label(
    text = "    Modifiers    ",
    font = "Ariel 11 bold underline")
headlabel_modify.grid(column=1, sticky="S", row=0, pady=3, padx=7)

headlabel_hp = tk.Label(
    text = " HP ",
    font = "Ariel 11 bold underline")
headlabel_hp.grid(column=0, row=5, sticky="SE", pady=3, padx=3)

headlabel_name = tk.Label(
    text = " Name ",
    font = "Ariel 11 bold underline")
headlabel_name.grid(column=1, row=5, sticky="S", pady=3, padx=3)

headlabel_init = tk.Label(
    text = " Init",
    anchor="e",
    font = "Ariel 11 bold underline")
headlabel_init.grid(column=2, columnspan=2, row=5, sticky="SW",pady=3, padx=3)

headlabel_firstattack = tk.Label(
    text = "First Attack",
    font = "Ariel 11 bold underline")
headlabel_firstattack.grid(column=4, row=11, sticky="SW", padx=7)

headlabel_secondattack = tk.Label(
    text = "Second Attack",
    font = "Ariel 11 bold underline")
headlabel_secondattack.grid(column=5, row=11, sticky="SW", padx=7)

headlabel_spells = tk.Label(text = "  Spells  ", font = "Ariel 11 bold underline").grid(column=6, row=0, sticky="S")




##### PC ENTRY ####
#PC1
pc1_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", borderwidth = 1, relief = "sunken")
pc1_Ientry.insert(0, "0")
pc1_Ientry.grid(column=2, row=6, sticky="W",pady=(0,3), padx=3)
PC1_name_Label=tk.Entry(frame, bg='white', fg="dark blue", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
PC1_name_Label.grid(column=1, row=6, pady=(0,3), padx=3)
PC1_name_Label.insert(0,"PC 1")

#PC2
pc2_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", borderwidth = 1, relief = "sunken")
pc2_Ientry.insert(0, "0")
pc2_Ientry.grid(column=2, row=7, sticky="W",pady=(0,3), padx=3)
PC2_name_Label=tk.Entry(frame, bg='white', fg="dark blue", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
PC2_name_Label.grid(column=1, row=7, pady=(0,3), padx=3)
PC2_name_Label.insert(0,"PC 2")

#pc3
pc3_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", borderwidth = 1, relief = "sunken")
pc3_Ientry.insert(0, "0")
pc3_Ientry.grid(column=2, row=8, sticky="W",pady=(0,3), padx=3)
PC3_name_Label=tk.Entry(frame, bg='white', fg="dark blue", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
PC3_name_Label.grid(column=1, row=8, pady=(0,3), padx=3)
PC3_name_Label.insert(0,"PC 3")

#PC4
pc4_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", borderwidth = 1, relief = "sunken")
pc4_Ientry.insert(0, "0")
pc4_Ientry.grid(column=2, row=9, sticky="W",pady=(0,3), padx=3)
PC4_name_Label=tk.Entry(frame, bg='white', fg="dark blue", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
PC4_name_Label.grid(column=1, row=9, pady=(0,3), padx=3)
PC4_name_Label.insert(0,"PC 4")

#PC5
pc5_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", borderwidth = 1, relief = "sunken")
pc5_Ientry.insert(0, "0")
pc5_Ientry.grid(column=2, row=10, sticky="W",pady=(0,3), padx=3)
PC5_name_Label=tk.Entry(frame, bg='white', fg="dark blue", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
PC5_name_Label.grid(column=1, row=10, pady=(0,3), padx=3)
PC5_name_Label.insert(0,"PC 5")

#PC6
pc6_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", borderwidth = 1, relief = "sunken")
pc6_Ientry.insert(0, "0")
pc6_Ientry.grid(column=2, row=11, sticky="W",pady=(0,3), padx=3)
PC6_name_Label=tk.Entry(frame, bg='white', fg="dark blue", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
PC6_name_Label.grid(column=1, row=11, pady=(0,3), padx=3)
PC6_name_Label.insert(0,"PC 6")



#### NPC ENTRY ####
#NPC1
npc1_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc1_Ientry.grid(column=2, row=12, sticky="W",pady=(0,3), padx=3)

npc1_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc1_Alabel.grid(column=4, row=12, sticky="W",pady=(0,3), padx=3)

npc1_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc1_A2label.grid(column=5, row=12, sticky="W",pady=(0,3), padx=3)

NPC0_name_Label=tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC0_name_Label.grid(column=1, row=12, pady=(0,3), padx=3)
NPC0_name_Label.insert(0,"BBG")

#NPC2
npc2_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc2_Ientry.grid(column=2, row=13, sticky="W",pady=(0,3), padx=3)

npc2_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc2_Alabel.grid(column=4, row=13, sticky="W",pady=(0,3), padx=3)

npc2_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc2_A2label.grid(column=5, row=13, sticky="W",pady=(0,3), padx=3)

NPC1_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC1_name_Label.grid(column=1, row=13, pady=(0,3), padx=3)
NPC1_name_Label.insert(0, "NPC 1")

#NPC3
npc3_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc3_Ientry.grid(column=2, row=14, sticky="W",pady=(0,3), padx=3)

npc3_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc3_Alabel.grid(column=4, row=14, sticky="W",pady=(0,3), padx=3)

npc3_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc3_A2label.grid(column=5, row=14, sticky="W",pady=(0,3), padx=3)

NPC2_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC2_name_Label.grid(column=1, row=14, pady=(0,3), padx=3)
NPC2_name_Label.insert(0, "NPC 2")

#NPC4
npc4_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc4_Ientry.grid(column=2, row=15, sticky="W",pady=(0,3), padx=3)

npc4_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc4_Alabel.grid(column=4, row=15, sticky="W",pady=(0,3), padx=3)

npc4_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc4_A2label.grid(column=5, row=15, sticky="W",pady=(0,3), padx=3)

NPC3_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC3_name_Label.grid(column=1, row=15, pady=(0,3), padx=3)
NPC3_name_Label.insert(0, "NPC 3")

#NPC5
npc5_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc5_Ientry.grid(column=2, row=16, sticky="W",pady=(0,3), padx=3)

npc5_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc5_Alabel.grid(column=4, row=16, sticky="W",pady=(0,3), padx=3)

npc5_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc5_A2label.grid(column=5, row=16, sticky="W",pady=(0,3), padx=3)

NPC4_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC4_name_Label.grid(column=1, row=16, pady=(0,3), padx=3)
NPC4_name_Label.insert(0, "NPC 4")

#NPC6
npc6_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc6_Ientry.grid(column=2, row=17, sticky="W",pady=(0,3), padx=3)

npc6_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc6_Alabel.grid(column=4, row=17, sticky="W",pady=(0,3), padx=3)

npc6_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc6_A2label.grid(column=5, row=17, sticky="W",pady=(0,3), padx=3)

NPC5_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC5_name_Label.grid(column=1, row=17, pady=(0,3), padx=3)
NPC5_name_Label.insert(0, "NPC 5")

#NPC7
npc7_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc7_Ientry.grid(column=2, row=18, sticky="W",pady=(0,3), padx=3)

npc7_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc7_Alabel.grid(column=4, row=18, sticky="W",pady=(0,3), padx=3)

npc7_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc7_A2label.grid(column=5, row=18, sticky="W",pady=(0,3), padx=3)

NPC6_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC6_name_Label.grid(column=1, row=18, pady=(0,3), padx=3)
NPC6_name_Label.insert(0, "NPC 6")

#NPC8
npc8_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc8_Ientry.grid(column=2, row=19, sticky="W",pady=(0,3), padx=3)

npc8_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc8_Alabel.grid(column=4, row=19, sticky="W",pady=(0,3), padx=3)

npc8_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc8_A2label.grid(column=5, row=19, sticky="W",pady=(0,3), padx=3)

NPC7_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC7_name_Label.grid(column=1, row=19, pady=(0,3), padx=3)
NPC7_name_Label.insert(0, "NPC 7")

#NPC9
npc9_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc9_Ientry.grid(column=2, row=20, sticky="W",pady=(0,3), padx=3)

npc9_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc9_Alabel.grid(column=4, row=20, sticky="W",pady=(0,3), padx=3)

npc9_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc9_A2label.grid(column=5, row=20, sticky="W",pady=(0,3), padx=3)

NPC8_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC8_name_Label.grid(column=1, row=20, pady=(0,3), padx=3)
NPC8_name_Label.insert(0, "NPC 8")

#NPC10
npc10_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc10_Ientry.grid(column=2, row=21, sticky="W",pady=(0,3), padx=3)

npc10_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc10_Alabel.grid(column=4, row=21, sticky="W",pady=(0,3), padx=3)

npc10_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc10_A2label.grid(column=5, row=21, sticky="W",pady=(0,3), padx=3)

NPC9_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC9_name_Label.grid(column=1, row=21, pady=(0,3), padx=3)
NPC9_name_Label.insert(0, "NPC 9")

#NPC11
npc11_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc11_Ientry.grid(column=2, row=22, sticky="W",pady=(0,3), padx=3)

npc11_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc11_Alabel.grid(column=4, row=22, sticky="W",pady=(0,3), padx=3)

npc11_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc11_A2label.grid(column=5, row=22, sticky="W",pady=(0,3), padx=3)

NPC10_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC10_name_Label.grid(column=1, row=22, pady=(0,3), padx=3)
NPC10_name_Label.insert(0, "NPC 10")

#NPC12
npc12_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc12_Ientry.grid(column=2, row=23, sticky="W",pady=(0,3), padx=3)

npc12_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc12_Alabel.grid(column=4, row=23, sticky="W",pady=(0,3), padx=3)

npc12_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc12_A2label.grid(column=5, row=23, sticky="W",pady=(0,3), padx=3)

NPC11_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC11_name_Label.grid(column=1, row=23, pady=(0,3), padx=3)
NPC11_name_Label.insert(0, "NPC 11")

#NPC13
npc13_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc13_Ientry.grid(column=2, row=24, sticky="W",pady=(0,3), padx=3)

npc13_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc13_Alabel.grid(column=4, row=24, sticky="W",pady=(0,3), padx=3)

npc13_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc13_A2label.grid(column=5, row=24, sticky="W",pady=(0,3), padx=3)

NPC12_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC12_name_Label.grid(column=1, row=24, pady=(0,3), padx=3)
NPC12_name_Label.insert(0, "NPC 12")

#NPC14
npc14_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc14_Ientry.grid(column=2, row=25, sticky="W",pady=(0,3), padx=3)

npc14_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc14_Alabel.grid(column=4, row=25, sticky="W",pady=(0,3), padx=3)

npc14_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc14_A2label.grid(column=5, row=25, sticky="W",pady=(0,3), padx=3)

NPC13_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC13_name_Label.grid(column=1, row=25, pady=(0,3), padx=3)
NPC13_name_Label.insert(0, "NPC 13")

#NPC15
npc15_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc15_Ientry.grid(column=2, row=26, sticky="W",pady=(0,3), padx=3)

npc15_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc15_Alabel.grid(column=4, row=26, sticky="W",pady=(0,3), padx=3)

npc15_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc15_A2label.grid(column=5, row=26, sticky="W",pady=(0,3), padx=3)

NPC14_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC14_name_Label.grid(column=1, row=26, pady=(0,3), padx=3)
NPC14_name_Label.insert(0, "NPC 14")

#NPC16
npc16_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc16_Ientry.grid(column=2, row=27, sticky="W",pady=(0,3), padx=3)

npc16_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc16_Alabel.grid(column=4, row=27, sticky="W",pady=(0,3), padx=3)

npc16_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc16_A2label.grid(column=5, row=27, sticky="W",pady=(0,3), padx=3)

NPC15_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC15_name_Label.grid(column=1, row=27, pady=(0,3), padx=3)
NPC15_name_Label.insert(0, "NPC 15")

#NPC17 (technically 'NPC 16', but npc1 is reserved for the BBG)
npc17_Ientry =  tk.Entry(frame, width = 5, font = "Ariel 11", bg= "white smoke", borderwidth = 1, relief = "sunken")
npc17_Ientry.grid(column=2, row=28, sticky="W",pady=(0,3), padx=3)

npc17_Alabel = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc17_Alabel.grid(column=4, row=28, sticky="W",pady=(0,3), padx=3)

npc17_A2label = tk.Label(
    text = "",
    width=14,
    anchor="w",
    font = "Ariel 11 bold")
npc17_A2label.grid(column=5, row=28, sticky="W",pady=(0,3), padx=3)

NPC16_name_Label = tk.Entry(frame, bg='white smoke', fg="dark green", font = "Ariel 11 bold", width=22, borderwidth=1, relief='sunken')
NPC16_name_Label.grid(column=1, row=28, pady=(0,3), padx=3)
NPC16_name_Label.insert(0, "NPC 16")

########################
Init_track0 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track0.grid(column=3, row=6)
Init_track1 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track1.grid(column=3, row=7)
Init_track2 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track2.grid(column=3, row=8)
Init_track3 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track3.grid(column=3, row=9)
Init_track4 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track4.grid(column=3, row=10)
Init_track5 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track5.grid(column=3, row=11)
Init_track6 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track6.grid(column=3, row=12)
Init_track7 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track7.grid(column=3, row=13)
Init_track8 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track8.grid(column=3, row=14)
Init_track9 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track9.grid(column=3, row=15)
Init_track10 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track10.grid(column=3, row=16)
Init_track11 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track11.grid(column=3, row=17)
Init_track12 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track12.grid(column=3, row=18)
Init_track13 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track13.grid(column=3, row=19)
Init_track14 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track14.grid(column=3, row=20)
Init_track15 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track15.grid(column=3, row=21)
Init_track16 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track16.grid(column=3, row=22)
Init_track17 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track17.grid(column=3, row=23)
Init_track18 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track18.grid(column=3, row=24)
Init_track19 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track19.grid(column=3, row=25)
Init_track20 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track20.grid(column=3, row=26)
Init_track21 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track21.grid(column=3, row=27)
Init_track22 = tk.Label(frame, fg="dark gray", text="  - initiative -  ")
Init_track22.grid(column=3, row=28)



#### REPEATED ENTRY #### 
# List to store HP_Label entries  
hp_labels1 = []
hp_labels = []  
  
# PC HP Labels  
for i in range(6, 12):  
    HP_Label1 = tk.Entry(frame, bg='#fcdcf2', fg="maroon", font="Ariel 11 bold", width=5, borderwidth=1, relief='sunken')  
    HP_Label1.grid(column=0, row=i, sticky="E", pady=(0, 3), padx=(9, 3))  
    HP_Label1.insert(0, "-0-")  
    hp_labels1.append(HP_Label1)  # Add to list  
  
# NPC HP Labels  
for i in range(12, 29):  # This should create 17 labels (index 0 to 16)  
    HP_Label = tk.Entry(frame, bg='#fcdcf2', fg="maroon", font="Ariel 11 bold", width=5, borderwidth=1, relief='sunken')  
    HP_Label.grid(column=0, row=i, sticky="E", pady=(0, 3), padx=(9, 3))  
    HP_Label.insert(0, "0")  
    hp_labels.append(HP_Label)  # Add to list   


# Initialize the list for spell labels  
spell_label_entries = []  
  
#### SPELLS ####  
for i in range(1, 7):  
    spell_label = tk.Entry(frame, bg='snow', fg="#8c53b0", font="Ariel 8 italic", width=12, borderwidth=1, relief='sunken')  
    spell_label.grid(column=6, row=i, sticky="E")  
    spell_label.insert(0, " Cantrip")  
    spell_label_entries.append(spell_label)  
  
for i in range(8, 25):  
    spell_label = tk.Entry(frame, bg='snow', fg="#441163", font="Ariel 8 italic", width=14, borderwidth=1, relief='sunken')  
    spell_label.grid(column=6, row=i, sticky="E")  
    spell_label.insert(0, " Spell")  
    spell_label_entries.append(spell_label)  
  
Slot_lvl = tk.Label(frame, text="Lvl 1", fg="#3c0161", font="Ariel 10 bold").grid(column=7, row=8, sticky="E", pady=(0, 3), padx=1)  
Slot_lvl = tk.Label(frame, text="Lvl 2", fg="#3c0161", font="Ariel 10 bold").grid(column=7, row=9, sticky="E", pady=(0, 3), padx=1)  
Slot_lvl = tk.Label(frame, text="Lvl 3", fg="#3c0161", font="Ariel 10 bold").grid(column=7, row=10, sticky="E", pady=(0, 3), padx=1)  
Slot_lvl = tk.Label(frame, text="Lvl 4", fg="#3c0161", font="Ariel 10 bold").grid(column=7, row=11, sticky="E", pady=(0, 3), padx=1)  
Slot_lvl = tk.Label(frame, text="Lvl 5", fg="#3c0161", font="Ariel 10 bold").grid(column=7, row=12, sticky="E", pady=(0, 3), padx=1)  
Slot_lvl = tk.Label(frame, text="Lvl 6", fg="#3c0161", font="Ariel 10 bold").grid(column=7, row=13, sticky="E", pady=(0, 3), padx=1)  
Slot_lvl = tk.Label(frame, text="Lvl 7", fg="#3c0161", font="Ariel 10 bold").grid(column=7, row=14, sticky="E", pady=(0, 3), padx=1)  
Slot_lvl = tk.Label(frame, text="Lvl 8", fg="#3c0161", font="Ariel 10 bold").grid(column=7, row=15, sticky="E", pady=(0, 3), padx=1)  
Slot_lvl = tk.Label(frame, text="Lvl 9", fg="#3c0161", font="Ariel 10 bold").grid(column=7, row=16, sticky="E", pady=(0, 3), padx=1)  
  
lair_slot = tk.Label(frame, text="Lair Action Init", fg="dark green", font="Ariel 8 bold").grid(column=6, columnspan=1, row=25, sticky="w", pady=(6, 0))  
lair_box1 = tk.Entry(frame, fg="dark green", font="Ariel 8 bold", width=5)  
lair_box1.grid(column=7, columnspan=1, row=25, pady=(6, 0))  
lair_slot = tk.Label(frame, text="Lair Action Init", fg="dark green", font="Ariel 8 bold").grid(column=6, columnspan=1, row=26, sticky="w", pady=(6, 0))  
lair_box2 = tk.Entry(frame, fg="dark green", font="Ariel 8 bold", width=5)  
lair_box2.grid(column=7, columnspan=1, row=26, pady=(6, 0))  
lair_slot = tk.Label(frame, text="Lair Action Init", fg="dark green", font="Ariel 8 bold").grid(column=6, columnspan=1, row=27, sticky="w", pady=(6, 0))  
lair_box3 = tk.Entry(frame, fg="dark green", font="Ariel 8 bold", width=5)  
lair_box3.grid(column=7, columnspan=1, row=27, pady=(6, 0))  
  
res_slot = tk.Label(frame, text="Legendary Resistance:", fg="dark green", font="Ariel 8 bold").grid(column=6, columnspan=2, row=28, sticky="e", pady=(3, 0))  
res_box = tk.Checkbutton(frame).grid(column=8, row=28, pady=(3, 0))  
res_box = tk.Checkbutton(frame).grid(column=9, row=28, pady=(3, 0))  
res_box = tk.Checkbutton(frame).grid(column=10, row=28, pady=(3, 0))  
  
for i in range(8, 17):  
    Slot_box = tk.Checkbutton(frame).grid(column=8, row=i, pady=(0, 3))  
for i in range(8, 15):  
    Slot_box = tk.Checkbutton(frame).grid(column=9, row=i, pady=(0, 3))  
for i in range(8, 13):  
    Slot_box = tk.Checkbutton(frame).grid(column=10, row=i, pady=(0, 3))  
lvl1_last_Slot_box = tk.Checkbutton(frame).grid(column=11, row=8, pady=(0, 3))  




##############################################
###########     ASI modifiers    #############
##############################################

def reset_asi(Event=None):
    ASIstr_Entry.delete(0, tk.END)
    ASIstr_Entry.insert(0, "10")
    ASIdex_Entry.delete(0, tk.END)
    ASIdex_Entry.insert(0, "10")  
    ASIcon_Entry.delete(0, tk.END)
    ASIcon_Entry.insert(0, "10")  
    ASIint_Entry.delete(0, tk.END)
    ASIint_Entry.insert(0, "10")  
    ASIwis_Entry.delete(0, tk.END)
    ASIwis_Entry.insert(0, "10")  
    ASIcha_Entry.delete(0, tk.END)
    ASIcha_Entry.insert(0, "10")      


def calc_asi(Event=None):

    prof_mod = int(prof_entry.get())
    if prof_mod == 2:
        prof_level.config(text="lvl 1-4",fg="#336643")
    elif prof_mod == 3:
        prof_level.config(text="lvl 5-8",fg="#336643")
    elif prof_mod == 4:
        prof_level.config(text="lvl 9-12",fg="#3c0161")
    elif prof_mod == 5:
        prof_level.config(text="lvl 13-16",fg="#3c0161")
    elif prof_mod == 6:
        prof_level.config(text="lvl 17-20",fg="#3c0161")
    elif prof_mod == 7:
        prof_level.config(text="lvl 20-24",fg="#948247")
    elif prof_mod == 8:
        prof_level.config(text="lvl 25-29",fg="#948247")
    elif prof_mod > 8:
        prof_level.config(text="lvl 30+",fg="Red")
    else: prof_level.config(text="---")

    # Strength
    asi_mod = (int(ASIstr_Entry.get()))
    asi_mod = round(((asi_mod - 10.1)/2))
    asi_modP = (asi_mod + prof_mod)
    if (prof_str_var.get() == 1 ): j=prof_mod
    if (prof_str_var.get() == 1 ): asi_mod=asi_modP
    else: j=0
    ASIstr_Mod=tk.Label(frame, text="+"+str(j), fg="#3c0161", font = "Ariel 8 bold", width=4, borderwidth=1)
    ASIstr_Mod.grid(column=9,columnspan=2, row=1, sticky="W")
    ASIstr_total_label.config(text="Mod: +"+str(asi_mod))

    # DEXTERITY  
    asi_mod = (int(ASIdex_Entry.get()))  
    asi_mod = round(((asi_mod - 10.1) / 2))  
    asi_modP = (asi_mod + prof_mod)  
    if prof_dex_var.get() == 1:  
        j = prof_mod  
        asi_mod = asi_modP  
    else:  
        j = 0  
    ASIdex_Mod = tk.Label(frame, text="+" + str(j), fg="#3c0161", font="Ariel 8 bold", width=4, borderwidth=1)  
    ASIdex_Mod.grid(column=9, columnspan=2, row=2, sticky="W")  
    ASIdex_total_label.config(text="Mod: +" + str(asi_mod))  
  
    # CONSTITUTION  
    asi_mod = (int(ASIcon_Entry.get()))  
    asi_mod = round(((asi_mod - 10.1) / 2))  
    asi_modP = (asi_mod + prof_mod)  
    if prof_con_var.get() == 1:  
        j = prof_mod  
        asi_mod = asi_modP  
    else:  
        j = 0  
    ASIcon_Mod = tk.Label(frame, text="+" + str(j), fg="#3c0161", font="Ariel 8 bold", width=4, borderwidth=1)  
    ASIcon_Mod.grid(column=9, columnspan=2, row=3, sticky="W")  
    ASIcon_total_label.config(text="Mod: +" + str(asi_mod))  
  
    # INTELLIGENCE  
    asi_mod = (int(ASIint_Entry.get()))  
    asi_mod = round(((asi_mod - 10.1) / 2))  
    asi_modP = (asi_mod + prof_mod)  
    if prof_int_var.get() == 1:  
        j = prof_mod  
        asi_mod = asi_modP  
    else:  
        j = 0  
    ASIint_Mod = tk.Label(frame, text="+" + str(j), fg="#3c0161", font="Ariel 8 bold", width=4, borderwidth=1)  
    ASIint_Mod.grid(column=9, columnspan=2, row=4, sticky="W")  
    ASIint_total_label.config(text="Mod: +" + str(asi_mod))  
  
    # WISDOM  
    asi_mod = (int(ASIwis_Entry.get()))  
    asi_mod = round(((asi_mod - 10.1) / 2))  
    asi_modP = (asi_mod + prof_mod)  
    if prof_wis_var.get() == 1:  
        j = prof_mod  
        asi_mod = asi_modP  
    else:  
        j = 0  
    ASIwis_Mod = tk.Label(frame, text="+" + str(j), fg="#3c0161", font="Ariel 8 bold", width=4, borderwidth=1)  
    ASIwis_Mod.grid(column=9, columnspan=2, row=5, sticky="W")  
    ASIwis_total_label.config(text="Mod: +" + str(asi_mod))  
    
    # CHARISMA  
    asi_mod = (int(ASIcha_Entry.get()))  
    asi_mod = round(((asi_mod - 10.1) / 2))  
    asi_modP = (asi_mod + prof_mod)  
    if prof_cha_var.get() == 1:  
        j = prof_mod  
        asi_mod = asi_modP  
    else:  
        j = 0  
    ASIcha_Mod = tk.Label(frame, text="+" + str(j), fg="#3c0161", font="Ariel 8 bold", width=4, borderwidth=1)  
    ASIcha_Mod.grid(column=9, columnspan=2, row=6, sticky="W")  
    ASIcha_total_label.config(text="Mod: +" + str(asi_mod))  
  


ASIstr_Label=tk.Label(frame, text="STR:", fg="#3c0161", font = "Ariel 8 bold", width=4, borderwidth=1)
ASIstr_Label.grid(column=7, row=1, sticky="E")
ASIstr_Entry=tk.Entry(frame, bg='snow', fg="#8c53b0", font = "Ariel 8", width=3, borderwidth=1, relief='sunken')
ASIstr_Entry.grid(column=8, columnspan=2, row=1, sticky="W")
ASIstr_Entry.insert(0,"10")
ASIstr_total_label = tk.Label(frame, text="-click 'prof'-", font="arial 8 italic")  
ASIstr_total_label.grid(column=12, columnspan=2, row=1, sticky="W") 

ASIdex_Label=tk.Label(frame, text="DEX:", fg="#3c0161", font = "Ariel 8 bold", width=4, borderwidth=1)
ASIdex_Label.grid(column=7, row=2, sticky="E")
ASIdex_Entry=tk.Entry(frame, bg='snow', fg="#8c53b0", font = "Ariel 8", width=3, borderwidth=1, relief='sunken')
ASIdex_Entry.grid(column=8, columnspan=2, row=2, sticky="W")
ASIdex_Entry.insert(0,"10")
ASIdex_total_label = tk.Label(frame, text="-click 'prof'-", font="arial 8 italic")  
ASIdex_total_label.grid(column=12, columnspan=2, row=2, sticky="W") 

ASIcon_Label=tk.Label(frame, text="CON:", fg="#3c0161", font = "Ariel 8 bold", width=4, borderwidth=1)
ASIcon_Label.grid(column=7, row=3, sticky="E")
ASIcon_Entry=tk.Entry(frame, bg='snow', fg="#8c53b0", font = "Ariel 8", width=3, borderwidth=1, relief='sunken')
ASIcon_Entry.grid(column=8, columnspan=2, row=3, sticky="W")
ASIcon_Entry.insert(0,"10")
ASIcon_total_label = tk.Label(frame, text="-click 'prof'-", font="arial 8 italic")  
ASIcon_total_label.grid(column=12, columnspan=2, row=3, sticky="W") 

ASIint_Label=tk.Label(frame, text="INT:", fg="#3c0161", font = "Ariel 8 bold", width=4, borderwidth=1)
ASIint_Label.grid(column=7, row=4, sticky="E")
ASIint_Entry=tk.Entry(frame, bg='snow', fg="#8c53b0", font = "Ariel 8", width=3, borderwidth=1, relief='sunken')
ASIint_Entry.grid(column=8, columnspan=2, row=4, sticky="W")
ASIint_Entry.insert(0,"10")
ASIint_total_label = tk.Label(frame, text="-click 'prof'-", font="arial 8 italic")  
ASIint_total_label.grid(column=12, columnspan=2, row=4, sticky="W") 

ASIwis_Label=tk.Label(frame, text="WIS:", fg="#3c0161", font = "Ariel 8 bold", width=4, borderwidth=1)
ASIwis_Label.grid(column=7, row=5, sticky="E")
ASIwis_Entry=tk.Entry(frame, bg='snow', fg="#8c53b0", font = "Ariel 8", width=3, borderwidth=1, relief='sunken')
ASIwis_Entry.grid(column=8, columnspan=2, row=5, sticky="W")
ASIwis_Entry.insert(0,"10")
ASIwis_total_label = tk.Label(frame, text="-click 'prof'-", font="arial 8 italic")  
ASIwis_total_label.grid(column=12, columnspan=2, row=5, sticky="W") 

ASIcha_Label=tk.Label(frame, text="CHA:", fg="#3c0161", font = "Ariel 8 bold", width=4, borderwidth=1)
ASIcha_Label.grid(column=7, row=6, sticky="E")
ASIcha_Entry=tk.Entry(frame, bg='snow', fg="#8c53b0", font = "Ariel 8", width=3, borderwidth=1, relief='sunken')
ASIcha_Entry.grid(column=8, columnspan=2, row=6, sticky="W")
ASIcha_Entry.insert(0,"10")
ASIcha_total_label = tk.Label(frame, text="-click 'prof'-", font="arial 8 italic")  
ASIcha_total_label.grid(column=12, columnspan=2, row=6, sticky="W") 




asi_reset_button = tk.Button(frame, text="ASI reset", font="Arial 7", relief="raised", command=reset_asi)
asi_reset_button.grid(column=7,columnspan=2,row=0,sticky="E", padx=(0,3), pady=(7,0))

asi_calc_button = tk.Button(frame, text="prof", font="Arial 7", relief="raised", command=calc_asi)
asi_calc_button.grid(column=9,columnspan=1,row=0,sticky="W",pady=(7,0))




prof_head = tk.Label(frame, text="  prof:", font="arial 8 italic")
prof_head.grid(column=10, columnspan=1,row=0,sticky="SE", pady=(0,3))

prof_entry = tk.Entry(frame, font="arial 8", width=2)
prof_entry.grid(column=11, columnspan=1,row=0,sticky="W")
prof_entry.insert(0,"2")

prof_level = tk.Label(frame,text="",font="arial 8 italic")
prof_level.grid(column=12, columnspan=2,row=0,sticky="W")


prof_str_var = tk.IntVar()
prof_str_box = tk.Checkbutton(frame, variable=prof_str_var, onvalue=1, offvalue=0).grid(column=10, columnspan=1,row=1,sticky="E")

prof_dex_var = tk.IntVar()
prof_sex_box = tk.Checkbutton(frame, variable=prof_dex_var, onvalue=1, offvalue=0).grid(column=10, columnspan=1,row=2,sticky="E")

prof_con_var = tk.IntVar()
prof_con_box = tk.Checkbutton(frame, variable=prof_con_var, onvalue=1, offvalue=0).grid(column=10, columnspan=1,row=3,sticky="E")

prof_int_var = tk.IntVar()
prof_int_box = tk.Checkbutton(frame, variable=prof_int_var, onvalue=1, offvalue=0).grid(column=10, columnspan=1,row=4,sticky="E")

prof_wis_var = tk.IntVar()
prof_wis_box = tk.Checkbutton(frame, variable=prof_wis_var, onvalue=1, offvalue=0).grid(column=10, columnspan=1,row=5,sticky="E")

prof_cha_var = tk.IntVar()
prof_cha_box = tk.Checkbutton(frame, variable=prof_cha_var, onvalue=1, offvalue=0).grid(column=10, columnspan=1,row=6,sticky="E")








###################################################################
#### South Buttons ###################################################
###################################################################
Add_NPC_button = tk.Button(
    frame,
    width =14,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "Add NPC",
    font = "Ariel 11",
    command = add_npc)
Add_NPC_button.grid(column=1, columnspan=2, row=31, sticky="E", pady=3, padx=3)

Drop_NPC_button = tk.Button(
    frame,
    width =14,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "Remove NPC",
    fg= "red",
    font = "Ariel 11",
    command = drop_npc)
Drop_NPC_button.grid(column=0, columnspan=2, row=31, sticky="W", pady=3, padx=3)


roll_Ibutton = tk.Button(
    frame,
    width = 14,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "Roll NPC Initiative",
    font = "Ariel 11",
    command = roll_init)
roll_Ibutton.grid(column=1, columnspan=2, row=30, sticky="E", pady=3, padx=3)

clearInit_button = tk.Button(
    frame,
    width = 14,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "Reset NPC Rolls",
    font = "Ariel 11",
    fg= "red",
    command = clear_npc_rolls)
clearInit_button.grid(column=0, columnspan=2, row=30, sticky="W", pady=3, padx=3)


sortIbutton = tk.Button(  
    frame,  
    width=8,  
    borderwidth=3,  
    relief="raised",  
    activebackground="#d1b779",  
    text="Re-Sort",  
    font="Ariel 10 italic",  
    command=sort_init)  
sortIbutton.grid(column=3, row=30, pady=3, padx=8)  

clearHP_button = tk.Button(  
    frame,  
    width=8,  
    borderwidth=3,  
    relief="raised",  
    activebackground="#d1b779",  
    text="Clear HP",  
    font="Ariel 10 italic",  
    fg="red",  
    command=clear_npc_hp)  
clearHP_button.grid(column=3, row=31, pady=3, padx=8)  


roll_Abutton = tk.Button(
    frame,
    width = 11,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "Roll 1st Attack",
    font = "Ariel 11",
    command = roll_attacks)
roll_Abutton.grid(column=4, row=30, sticky="W", pady=3, padx=3)

roll_A2button = tk.Button(
    frame,
    width = 11,
    borderwidth = 3,
    relief = "raised",
    activebackground= "#d1b779",
    text = "Roll 2nd Attack",
    font = "Ariel 11",
    command = roll_attacks2)
roll_A2button.grid(column=5, row=30, sticky="W", pady=3, padx=3)



#### END FRAME ####
frame.mainloop()