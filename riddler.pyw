import tkinter as tk  
from tkinter import ttk  
import random  
  
  
class RiddlerApp:  
    def __init__(self, root):  
        self.root = root  
        self.root.title("The Riddler")  
  
        # Dark Theme Colors  
        self.bg_color = "#2b2b2b"  
        self.fg_color = "#ffffff"  
        self.button_color = "#444444"  
        self.highlight_color = "#666666"  
        self.listbox_bg = "#3d3d3d"  
        self.listbox_fg = "#a9a9a9"  
  
        # Dictionary of riddles and answers (you can add your riddles here later)  
        self.riddles = {  
            "Riddle: I have towns but no houses, forests but no trees, and rivers but no water. What am I?": "Answer: A map",  
            "Riddle: The more you take, the more you leave behind. What am I?": "Answer: Footsteps",  
            "Riddle: I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?": "Answer: An echo",  
            "Riddle: I am always hungry, I must always be fed. The finger I touch will soon turn red. What am I?": "Answer: Fire",  
            "Riddle: I have keys but no locks. I have space but no room. You can enter, but you can’t go outside. What am I?": "Answer: A keyboard",  
            "Riddle: What has roots as nobody sees, is taller than trees, up, up it goes, and yet it never grows?": "Answer: A mountain",  
            "Riddle: What can travel the world while staying in the same corner?": "Answer: A stamp",  
            "Riddle: The more you take away, the bigger I get. What am I?": "Answer: A hole",  
            "Riddle: I am light as a feather, yet the strongest warrior can’t hold me for long. What am I?": "Answer: Breath",  
            "Riddle: I fly without wings, I cry without eyes. Whenever I go, darkness flies. What am I?": "Answer: Clouds",  
            "Riddle: What has an eye but cannot see?": "Answer: A needle",  
            "Riddle: What has a head, a tail, is brown, and has no legs?": "Answer: A coin",  
            "Riddle: I have no life, but I can die. What am I?": "Answer: A battery",  
            "Riddle: What has four legs in the morning, two legs at noon, and three legs in the evening?": "Answer: A human (life stages: crawling, walking, using a cane)",  
            "Riddle: What has many hearts but no other organs?": "Answer: A deck of cards",  
            "Riddle: The more you have of me, the less you see. What am I?": "Answer: Darkness",  
            "Riddle: I am invisible, weigh nothing, and if you put me in a barrel, it will make the barrel lighter. What am I?": "Answer: A hole",  
            "Riddle: I am found in the sky, but am not alive. I am bright, but I do not burn. What am I?": "Answer: Stars",  
            "Riddle: What has a ring but no fingers?": "Answer: A bell",  
            "Riddle: What can you catch but not throw?": "Answer: A cold",  
            "Riddle: What has no beginning, end, or middle?": "Answer: A circle",  
            "Riddle: I am always in front of you, but you cannot see me. What am I?": "Answer: The future",  
            "Riddle: I am harder to catch the faster you run. What am I?": "Answer: Your breath",  
            "Riddle: The more you feed me, the smaller I become. What am I?": "Answer: A candle",  
            "Riddle: What has hands but cannot clap?": "Answer: A clock",  
            "Riddle: What comes down but never goes up?": "Answer: Rain",  
            "Riddle: What is always in motion but never moves?": "Answer: Time",  
            "Riddle: What has no bones but is strong enough to hold a castle?": "Answer: Water",  
            "Riddle: What gets sharper the more you use it?": "Answer: Your mind",  
            "Riddle: What must be broken before you can use it?": "Answer: An egg",  
            "Riddle: What is so fragile that saying its name breaks it?": "Answer: Silence",  
            "Riddle: What can fill a room but takes up no space?": "Answer: Light",  
            "Riddle: I am the beginning of the end, and the end of time and space. I am essential to creation and surround every place. What am I?": "Answer: The letter 'E'",  
            "Riddle: I am taken from a mine and shut inside a wooden case, from which I am never released, yet I am used by almost everyone. What am I?": "Answer: A pencil",  
            "Riddle: What has teeth but cannot bite?": "Answer: A comb",  
            "Riddle: I am always near you, but you can never see me. What am I?": "Answer: The air",  
            "Riddle: I am a word. I begin with the letter 'E' and only contain one letter. What am I?": "Answer: An envelope",  
            "Riddle: What comes once in a minute, twice in a moment, but never in a thousand years?": "Answer: The letter 'M'",  
            "Riddle: What has an endless supply but is always used up?": "Answer: Time",  
            "Riddle: What has a neck but no head, arms, or legs?": "Answer: A bottle",  
            "Riddle: I am the companion of kings and the maker of history. What am I?": "Answer: A pen",  
            "Riddle: I am a castle wall that cannot fall, yet I am not made of stone. What am I?": "Answer: A shadow",  
            "Riddle: I can be cracked, made, told, and played. What am I?": "Answer: A joke",  
            "Riddle: What is black when clean and white when dirty?": "Answer: A chalkboard",  
            "Riddle: What has an end but no beginning, a home but no family?": "Answer: A road",  
            "Riddle: I’m tall when I’m young, and I’m short when I’m old. What am I?": "Answer: A candle",  
            "Riddle: What has legs but doesn’t walk?": "Answer: A table",  
            "Riddle: What belongs to you but other people use it more than you do?": "Answer: Your name",  
            "Riddle: What gets wetter the more it dries?": "Answer: A towel",  
            "Riddle: What has a spine but no bones?": "Answer: A book",  
            "Riddle: I am always moving forward but can never turn back. What am I?": "Answer: Time",  
            "Riddle: I am a path between high places, yet I never move. What am I?": "Answer: A bridge",  
            "Riddle: What has a thousand needles but cannot sew?": "Answer: A porcupine",  
            "Riddle: I go up but never come down. What am I?": "Answer: Your age",  
            "Riddle: I am alive without breath, as cold as death. I am never thirsty but always drinking. What am I?": "Answer: A fish",  
            "Riddle: I have no wings, but I can fly. What am I?": "Answer: A kite",  
            "Riddle: What has four fingers and a thumb but is not alive?": "Answer: A glove",  
            "Riddle: What has wheels and flies but is not alive?": "Answer: A garbage truck",  
            "Riddle: What is full of holes but still holds water?": "Answer: A sponge",  
            "Riddle: I am not a bird, but I can fly through the air and have feathers. What am I?": "Answer: An arrow",  
            "Riddle: What cannot be burned in fire or drowned in water?": "Answer: Ice",  
            "Riddle: What has a golden head, a golden tail, but no body?": "Answer: A gold coin",  
            "Riddle: I am at the beginning of time and part of every ending. What am I?": "Answer: The letter 'T'",  
            "Riddle: What runs around a house but doesn’t move?": "Answer: A fence",  
            "Riddle: What has feet but no legs?": "Answer: A ruler",  
            "Riddle: What can you break, even if you never pick it up or touch it?": "Answer: A promise",  
            "Riddle: What has a heart that doesn’t beat?": "Answer: An artichoke",  
            "Riddle: I am a king without a crown. What am I?": "Answer: A chess king",  
            "Riddle: I am a weapon forged in fire but never thrown. What am I?": "Answer: A sword",  
            "Riddle: What has a throat but no mouth, and sings without a voice?": "Answer: A bell",  
            "Riddle: I am the father of all knowledge but have no children. What am I?": "Answer: A book",  
            "Riddle: I wear a crown but am no king. I can be broken but am not alive. What am I?": "Answer: A tooth",  
            "Riddle: You can hold me in your hands, but you can never throw me away. What am I?": "Answer: Time",  
            "Riddle: I am the beginning of sorrow and the end of sickness. You cannot express happiness without me, yet I am always in misery. What am I?": "Answer: The letter 'S'",  
            "Riddle: What has a bark but no bite?": "Answer: A tree",  
            "Riddle: What can pierce armor but has no blade?": "Answer: A word",  
            "Riddle: I am small as a grain but can fill the skies. What am I?": "Answer: A star",  
            "Riddle: What has no body but can haunt your dreams?": "Answer: A ghost",  
            "Riddle: What can be opened but is never closed?": "Answer: A secret",  
            "Riddle: I can change color but never move. What am I?": "Answer: A chameleon",  
            "Riddle: What has no mouth yet whispers to you?": "Answer: The wind",  
            "Riddle: What can fill an ocean but fit in the palm of your hand?": "Answer: A raindrop",  
            "Riddle: What has no eyes but watches, no ears but listens, and no mouth but speaks?": "Answer: A mirror",  
            "Riddle: What breaks but never falls, and falls but never breaks?": "Answer: Day and night",  
            "Riddle: What has one head, one foot, and four legs?": "Answer: A bed",  
            "Riddle: I am not alive, but I bring life. What am I?": "Answer: Water",  
            "Riddle: I am a seed that spreads across the land, yet I cannot grow. What am I?": "Answer: Sand",  
            "Riddle: I am a cloak that covers the world but cannot be felt. What am I?": "Answer: Darkness",  
            "Riddle: I can cut through steel but am not sharp. What am I?": "Answer: Rust",  
            "Riddle: What has no end but circles forever?": "Answer: A ring",  
            "Riddle: I am the key to knowledge but can also lock you away. What am I?": "Answer: A book",  
            "Riddle: I can be hot or cold, hard or soft, and I shape the world. What am I?": "Answer: Stone",  
            "Riddle: What has no weight but can hold the world?": "Answer: A thought",  
            "Riddle: What has no substance but can break your heart?": "Answer: A promise",  
            "Riddle: What has no tongue but can whisper secrets?": "Answer: Paper",  
            "Riddle: I am a shield that cannot break, yet I am invisible. What am I?": "Answer: Courage",  
            "Riddle: What can run faster than any horse but has no legs?": "Answer: The wind",  
            "Riddle: I am a bridge that spans the world but cannot be crossed. What am I?": "Answer: A rainbow",  
            "Riddle: I am a tale that cannot be told, yet I am written in every stone. What am I?": "Answer: History",  
            "Riddle: What has no hands but can catch anything?": "Answer: A net",  
            "Riddle: I am a traveler that leaves no footprints. What am I?": "Answer: Light",  
            "Riddle: What has no roots but is taller than trees and touches the sky?": "Answer: A mountain",  
            "Riddle: What can make a king bow and a peasant rise?": "Answer: Gold",  
            "Riddle: I am a prison with no walls, a treasure with no key. What am I?": "Answer: A memory",  
            "Riddle: What can hold fire and ice but never melt or burn?": "Answer: A cauldron",  
            "Riddle: I am soft as silk but can break like glass. What am I?": "Answer: Trust",  
            "Riddle: I am a hunter that stalks the night but cannot kill. What am I?": "Answer: The moon",  
            "Riddle: What has no wings, yet can lift you to the skies?": "Answer: A balloon",  
            "Riddle: I am a weapon that can kill but cannot be held. What am I?": "Answer: Words",  
            "Riddle: I am a servant to kings and a companion to thieves. What am I?": "Answer: Gold",  
            "Riddle: What has no shape but can fill a room?": "Answer: Light",  
            "Riddle: I am a flame that cannot burn. What am I?": "Answer: A shadow",  
            "Riddle: What has no hands but can move mountains?": "Answer: Time",  
            "Riddle: I am a melody that can be heard but never sung. What am I?": "Answer: The wind",  
            "Riddle: What can rise without wings and fall without a sound?": "Answer: Smoke",  
            "Riddle: I am a keeper of secrets but have no lock. What am I?": "Answer: A diary",  
            "Riddle: I am a vessel that cannot sail and a treasure that cannot be spent. What am I?": "Answer: A memory",  
            "Riddle: What has no voice but can call you to action?": "Answer: A bell",  
            "Riddle: I am a mirror that never lies but cannot show your face. What am I?": "Answer: The truth",  
            "Riddle: What has no feet but can dance?": "Answer: Flames",  
            "Riddle: I am a whisper that cannot be heard. What am I?": "Answer: Thought",  
            "Riddle: What has no breath but gives life?": "Answer: Water",  
            "Riddle: What has no hands but can open any door?": "Answer: A key",  
            "Riddle: I am a shadow that has no master. What am I?": "Answer: The night",  
            "Riddle: I am the thread that binds the world together, yet I am invisible. What am I?": "Answer: Fate",  
            "Riddle: What has no eyes but sees the future clearly?": "Answer: A prophecy",  
            "Riddle: I am a flame that never burns out. What am I?": "Answer: Hope",  
            "Riddle: What can be divided endlessly but remains whole?": "Answer: Infinity",  
            "Riddle: What is always present but never seen?": "Answer: Time",  
            "Riddle: I am the sound of silence. What am I?": "Answer: Stillness",  
            "Riddle: I am an echo of the past and a glimpse of the future. What am I?": "Answer: Memory",  
            "Riddle: I am a clock with no hands, yet I keep perfect time. What am I?": "Answer: A sundial",  
            "Riddle: I am the boundary between the living and the dead. What am I?": "Answer: The horizon",  
            "Riddle: What can bind the strongest warrior but is made of nothing?": "Answer: A promise",  
        }  
  
        # Initialize Variables  
        self.current_riddle = None  
        self.history = []  
  
        # Configure the root window  
        self.root.configure(bg=self.bg_color)  
  
        # Layout  
        self.create_widgets()  
  
    def create_widgets(self):  
        # Left Frame for Buttons  
        button_frame = tk.Frame(self.root, bg=self.bg_color)  
        button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)  
  
        # Button: Display Riddle  
        self.riddle_button = tk.Button(  
            button_frame,  
            text="Riddle",  
            bg=self.button_color,  
            fg=self.fg_color,  
            activebackground=self.highlight_color,  
            command=self.display_riddle,  
            width=15,  
        )  
        self.riddle_button.pack(pady=5)  
  
        # Button: Display Answer  
        self.answer_button = tk.Button(  
            button_frame,  
            text="Answer",  
            bg=self.button_color,  
            fg=self.fg_color,  
            activebackground=self.highlight_color,  
            command=self.display_answer,  
            state=tk.DISABLED,  # Initially disabled  
            width=15,  
        )  
        self.answer_button.pack(pady=5)  
  
        # Button: Clear History (moved to the bottom)  
        self.clear_button = tk.Button(  
            button_frame,  
            text="Clear History",  
            bg=self.button_color,  
            fg=self.fg_color,  
            activebackground=self.highlight_color,  
            command=self.clear_history,  
            width=15,  
        )  
        self.clear_button.pack(side=tk.BOTTOM, pady=10)  
  
        # Right Frame for Display and History  
        display_frame = tk.Frame(self.root, bg=self.bg_color)  
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)  
  
        # Label: Riddle Display  
        self.riddle_label = tk.Label(  
            display_frame,  
            text="Riddle: ",  
            bg=self.bg_color,  
            fg=self.fg_color,  
            anchor="w",  
            wraplength=600,
            justify="left", 
            font=("Helvetica", 12),  
        )  
        self.riddle_label.pack(fill=tk.X, pady=5)  
  
        # Label: Answer Display  
        self.answer_label = tk.Label(  
            display_frame,  
            text="Answer: ",  
            bg=self.bg_color,  
            fg=self.fg_color,  
            anchor="w",  
            wraplength=600,  
            font=("Helvetica", 12),  
        )  
        self.answer_label.pack(fill=tk.X, pady=5)  
  
        # Listbox: History  
        self.history_listbox = tk.Listbox(  
            display_frame,  
            bg=self.listbox_bg,  
            fg=self.listbox_fg,  
            selectbackground=self.highlight_color,  
            height=15,  
            font=("Helvetica", 10, "italic"),  
        )  
        self.history_listbox.pack(fill=tk.BOTH, expand=True, pady=5)  
  
    def display_riddle(self):  
        # Display a random riddle  
        if self.riddles:  
            self.current_riddle = random.choice(list(self.riddles.keys()))  
            self.riddle_label.config(text=self.current_riddle)  
            self.answer_label.config(text="Answer: ")  # Clear previous answer  
            self.answer_button.config(state=tk.NORMAL)  # Enable the answer button  
  
    def display_answer(self):  
        # Display the answer to the current riddle  
        if self.current_riddle:  
            answer = self.riddles[self.current_riddle]  
            self.answer_label.config(text=answer)  
            self.history.append((self.current_riddle, answer))  
            self.update_history()  
            self.answer_button.config(state=tk.DISABLED)  # Disable answer button  
  
    def clear_history(self):  
        # Clear the history listbox  
        self.history = []  
        self.update_history()  
        self.riddle_label.config(text="Riddle: ")  
        self.answer_label.config(text="Answer: ")  
  
    def update_history(self):  
        # Update the listbox with the history  
        self.history_listbox.delete(0, tk.END)  
        for riddle, answer in self.history:  
            self.history_listbox.insert(tk.END, riddle)  
            self.history_listbox.insert(tk.END, answer)  
  
  
# Run the App  
if __name__ == "__main__":  
    root = tk.Tk()  
    root.geometry("760x450")  # Width: 760px, Height: 450px   
    app = RiddlerApp(root)  
    root.mainloop()  