import random
import tkinter as tk
from tkinter import Button, Listbox  # Import types for type annotations

frame = tk.Tk()
frame.title("Random Encounter Generator")
frame.config(
    borderwidth=2, 
    relief= "groove")
frame.geometry("920x450")

# Add a StringVar to store the selected encounter type
encounter_type_var = tk.StringVar(value="")

root_frame = tk.Frame(frame)
root_frame.pack(pady=20)

# Adjust the layout by creating three frames: left for biomes, center-left for buttons, and right for the display box
biome_frame = tk.Frame(root_frame, width=200)
biome_frame.pack(side="left", fill="y", padx=10)

button_frame = tk.Frame(root_frame, width=200)
button_frame.pack(side="left", fill="y", padx=10)

right_frame = tk.Frame(root_frame, width=600)
right_frame.pack(side="right", fill="both", expand=True, padx=10)

# Move biome checkboxes to the biome_frame
biomes = [
    "Temperate", "Boreal", "Hills", "Grassland", "River", "Swamp", "Lake",
    "Mountain", "Ocean", "Arctic", "Volcanic", "Desert", "Badlands", "Road", "Forest"
]

selected_biomes = {biome: tk.BooleanVar(value=False) for biome in biomes}
for biome, var in selected_biomes.items():
    tk.Checkbutton(biome_frame, text=biome, variable=var).pack(anchor="w")

# Update the generate_encounter function to filter by selected biomes
def generate_encounter():
    encounter_type = encounter_type_var.get()
    if encounter_type not in Biome_Encounters:
        append_to_display("Please select an encounter type.")
        return

    # Get selected biomes
    active_biomes = [biome for biome, var in selected_biomes.items() if var.get()]
    if not active_biomes:
        append_to_display("Please select at least one biome.")
        return

    # Filter encounters by selected biomes
    possible_encounters = []
    for biome in active_biomes:
        possible_encounters.extend(Biome_Encounters[encounter_type].get(biome, []))

    if possible_encounters:
        encounter = random.choice(possible_encounters)
    else:
        encounter = "No encounters available for the selected biomes and type."

    append_to_display(encounter)

# Move buttons to the button_frame
peaceful_button: Button = tk.Button(
    button_frame, 
    text="Peaceful", 
    command=lambda: set_encounter_type("Peaceful", peaceful_button)
)
peaceful_button.pack(pady=5, fill="x")

combat_button: Button = tk.Button(
    button_frame, 
    text="Combat", 
    command=lambda: set_encounter_type("Combat", combat_button)
)
combat_button.pack(pady=5, fill="x")

exploration_button: Button = tk.Button(
    button_frame, 
    text="Exploration", 
    command=lambda: set_encounter_type("Exploration", exploration_button)
)
exploration_button.pack(pady=5, fill="x")

# Remove special handling for the generate button
generate_button = tk.Button(
    button_frame, 
    text="Generate Encounter", 
    command=generate_encounter
)
generate_button.pack(pady=20, fill="x")

# Bind the Enter key to the generate_encounter function
frame.bind("<Return>", lambda event: generate_encounter())

# Move the display box to the right_frame with added padding
display_box: Listbox = tk.Listbox(right_frame, height=16, width=100)
display_box.pack(fill="both", expand=True, padx=(5, 0))  # Add 5px padding to the left only

# Ensure buttons are created before being referenced in `update_button_styles`
def update_button_styles(selected_button):
    for button in [peaceful_button, combat_button, exploration_button]:
        button.config(relief="raised", bg="SystemButtonFace")
    selected_button.config(relief="sunken", bg="lightblue")

# Function to set encounter type, update button styles, and underline the generate button text
def set_encounter_type(encounter_type, button):
    encounter_type_var.set(encounter_type)
    update_button_styles(button)

# Function to append encounter to the display box with a leading space for padding
def append_to_display(encounter):
    display_box.insert(0, f" {encounter}")  # Add a leading space to simulate left padding
    if display_box.size() > 22:  # Limit to 22 entries
        display_box.delete(22)

# Update Biome_Encounters with at least three options per biome for each encounter type
Biome_Encounters = {
    ### Peaceful Encounters ###
    "Peaceful": {
        "Temperate": [  
            "Bird songs fill the air, and a squirrel scurries up a nearby tree.",  
            "You find a small stream with clear water, its banks adorned with vibrant wildflowers.",  
            "You come across a grove of fruit-bearing trees, their sweet aroma filling the air.",  
            "A deer grazes nearby, unperturbed by your presence, occasionally glancing your way.",  
            "You spot a patch of mushrooms growing in the shade of a large oak tree.",  
            "A butterfly flits lazily from flower to flower in the morning sun."  
        ],  
        "Boreal": [  
            "The crisp air carries the scent of pine needles and distant wood smoke.",  
            "You spot a family of rabbits hopping through the snow, their tracks weaving across the ground.",  
            "A patch of frost-covered berries gleams in the sunlight, sparkling like tiny jewels.",  
            "You hear the faint howl of a distant wolf, but the sound feels more melancholy than threatening.",  
            "A curious fox watches you from a safe distance before darting into the trees.",  
            "The snow crunches softly beneath your feet, and you notice the intricate patterns of frost on nearby branches."  
        ],  
        "Hills": [  
            "You come across a hilltop with a breathtaking view of the surrounding valleys.",  
            "A gentle breeze carries the scent of wildflowers and fresh grass.",  
            "You spot a group of grazing sheep in the distance, their soft bleats adding to the peaceful atmosphere.",  
            "A small burrow reveals a family of harmless critters, their tiny eyes peeking out at you.",  
            "A hawk circles above, riding the thermals in the clear blue sky.",  
            "You find a patch of clover, dotted with bees busily collecting nectar."  
        ],  
        "Grassland": [  
            "You find a patch of wildflowers swaying in the breeze, their colors vibrant against the green grass.",  
            "A herd of deer can be seen grazing peacefully, their ears occasionally twitching at distant sounds.",  
            "You spot a lone tree providing shade under the open sky, its branches swaying gently.",  
            "The wind carries the sound of chirping crickets and the occasional call of a meadowlark.",  
            "A pair of hares darts through the tall grass, their sudden movement startling you.",  
            "You notice a distant rainbow shimmering faintly after a brief drizzle."  
        ],  
        "River": [  
            "You find a shallow river crossing with smooth stones, perfect for skipping.",  
            "A group of fish swims upstream, their silvery bodies flashing in the sunlight.",  
            "You see ducks paddling in the water, quacking softly as they dive for food.",  
            "The sound of rushing water is calming and serene, with dragonflies darting over the surface.",  
            "A kingfisher perches on a branch, its bright plumage catching your eye before it dives into the water.",  
            "You spot a small otter sliding playfully into the river from a muddy bank."  
        ],  
        "Swamp": [  
            "The swamp is oddly quiet, save for the occasional frog croak and the buzz of insects.",  
            "You find a patch of moss-covered ground that feels springy underfoot and smells earthy.",  
            "You spot a group of fireflies lighting up the area, their glow creating an enchanting scene.",  
            "A heron stands motionless, hunting in the shallow water with graceful precision.",  
            "You notice a turtle basking on a log, lazily stretching its legs in the warm sunlight.",  
            "The murky water glimmers faintly, revealing the slow movement of fish beneath the surface."  
        ],  
        "Lake": [  
            "You find a serene lakeside spot perfect for resting, its edge dotted with cattails.",  
            "You see fish jumping out of the water playfully, creating ripples that shimmer in the sunlight.",  
            "A gentle breeze ripples across the lake's surface, carrying the faint scent of wet earth.",  
            "You spot a pair of swans gliding gracefully across the water, their reflections perfect.",  
            "A frog leaps from a lily pad into the water, sending tiny ripples outward.",  
            "You notice a trail of animal tracks in the mud leading to the water's edge."  
        ],  
        "Mountain": [  
            "You find a peaceful mountain meadow filled with colorful wildflowers and buzzing bees.",  
            "You hear the distant sound of a waterfall, its echo mingling with the mountain breeze.",  
            "You spot a rare flower growing on a rocky ledge, its vibrant petals standing out against the stone.",  
            "You come across a rock formation resembling a natural sculpture, shaped by years of erosion.",  
            "An eagle soars high above, its piercing cry echoing across the mountain range.",  
            "You see a small stream cascading down the rocks, forming a crystal-clear pool below."  
        ],  
        "Ocean": [  
            "You hear the soothing sound of waves crashing against the shore, mingling with the cries of seagulls.",  
            "You spot a pod of dolphins swimming playfully in the distance, their fins cutting through the waves.",  
            "A colorful seashell catches your eye in the sand, its intricate patterns mesmerizing.",  
            "The salty breeze carries the scent of the ocean, refreshing and invigorating.",  
            "A crab scuttles sideways across the sand before disappearing into a tiny burrow.",  
            "You notice the vibrant hues of a tidepool filled with small sea creatures and blooming algae."  
        ],  
        "Arctic": [  
            "The snow sparkles under the bright sunlight, creating a dazzling landscape of white and blue.",  
            "You see a group of penguins waddling along the ice, their calls echoing in the still air.",  
            "A seal lounges lazily on a nearby ice floe, occasionally shifting its weight with a contented grunt.",  
            "The stillness of the icy landscape feels peaceful and untouched, broken only by the distant crack of ice.",  
            "You notice a polar fox blending into the snowy background, its fur pristine and white.",  
            "You spot the faint green shimmer of the aurora borealis beginning to form on the horizon."  
        ],  
        "Volcanic": [  
            "You find a patch of hardened lava that looks like frozen waves, its texture smooth and intricate.",  
            "The air carries a faint warmth, but it’s not uncomfortable, and the ground radiates gentle heat.",  
            "You spot a cluster of glowing minerals embedded in the rocks, their colors shifting subtly.",  
            "A plume of steam rises harmlessly from a fissure nearby, mingling with the sulfur-scented air.",  
            "You notice small, hardy plants growing in cracks where the lava has cooled.",  
            "You hear the distant rumble of the volcano, a reminder of the land’s raw power."  
        ],  
        "Desert": [  
            "You find a patch of shade under a rock formation, offering respite from the sun.",  
            "A cactus blooms with vibrant flowers, its colors standing out against the barren landscape.",  
            "You spot a small lizard sunning itself on a rock, darting away as you approach.",  
            "The desert sands shimmer in the heat, creating mirage-like patterns that dance in the distance.",  
            "A gentle breeze carries the faint scent of dry earth and distant rain.",  
            "You notice a hawk circling high above, scanning the land for prey."  
        ],  
        "Badlands": [  
            "You come across colorful sedimentary rock formations, their layers telling stories of ancient times.",  
            "The dry air carries the sound of rustling tumbleweed and the occasional distant bird call.",  
            "You spot a family of prairie dogs popping in and out of their burrows, chittering softly.",  
            "The evening sky casts dramatic shadows over the rugged terrain, painting the land in warm hues.",  
            "You find a patch of hardy shrubs growing amidst the rocks, their leaves covered in fine dust.",  
            "You notice a trickle of water carving a path through the cracked earth, a rare sight in this arid land."  
        ],  
        "Road": [  
            "You encounter a friendly traveler who shares stories and offers you a piece of dried fruit.",  
            "You find a roadside shrine with offerings, its carvings worn smooth by time and weather.",  
            "A merchant caravan passes by, offering goods and news from distant lands.",  
            "A bard walking along the road plays a cheerful tune on their lute, lifting your spirits.",  
            "You spot a milestone marking the distance to the next town, its surface adorned with moss.",  
            "A pair of farmers stroll by with a cart full of fresh produce, greeting you warmly."  
        ],  
        "Forest": [  
            "You discover a hidden glade with beautiful scenery, its floor covered in soft moss.",  
            "You come across a small animal that seems unafraid of you, watching you curiously.",  
            "You find a tree with vibrant, colorful leaves that seem to shimmer in the sunlight.",  
            "The sound of rustling leaves and chirping birds fills the air, creating a tranquil ambiance.",  
            "You notice a cluster of mushrooms growing in a ring, their caps glistening with dew.",  
            "A deer and its fawn cross your path, pausing briefly to look at you before continuing on."  
        ]  
    },
    
    
    ### Combat Encounters ###
    "Combat": {
        "Temperate": [  
            "A group of goblins emerges from the underbrush, their crude weapons at the ready.",  
            "A swarm of aggressive wasps descends from a nearby tree, buzzing angrily.",  
            "A pack of wild dogs circles you, their growls growing louder as they close in.",  
            "An angry bear charges at you, defending its territory with a thunderous roar.",  
            "A band of hostile kobolds ambushes you from hidden burrows, armed with slings and spears.",  
            "A giant boar barrels toward you, its tusks gleaming as it snorts in fury."  
        ],  
        "Boreal": [  
            "A snow leopard leaps from the shadows of a pine tree, its teeth bared and claws extended.",  
            "A pack of wolves surrounds you, their glowing eyes fixed on you as they growl menacingly.",  
            "An ice mephit cackles, flinging shards of frost as it emerges from a cold mist.",  
            "A frost giant's pet polar bear charges at you, its fur bristling with icy frost.",  
            "A white dragon wyrmling swoops down, snapping its jaws and blasting icy breath.",  
            "A group of yetis emerges from the snow, their howls echoing in the frigid air."  
        ],  
        "Hills": [  
            "A group of bandits hides among the hills, ready to strike with crossbows drawn.",  
            "A territorial griffon screeches as it swoops down from the sky, talons outstretched.",  
            "A burrow collapses, revealing a group of angry giant badgers snarling at you.",  
            "A hill giant lumbers toward you, swinging a tree trunk like a massive club.",  
            "A gang of hobgoblins appears, barking commands as they charge with military precision.",  
            "A wyvern descends from the clouds, its venomous tail poised to strike."  
        ],  
        "Grassland": [  
            "A stampede of wild animals barrels toward you, their eyes wide with panic and fear.",  
            "A group of gnolls emerges from the tall grass, their hyena-like laughter chilling your spine.",  
            "A lion stalks you, growling low in its throat before leaping into a fierce attack.",  
            "A swarm of locusts engulfs you, their biting mandibles relentless and overwhelming.",  
            "A group of velociraptors bursts from the brush, their claws slashing as they dart around.",  
            "A dire wolf lunges at you from the tall grass, its massive form nearly invisible in the field."  
        ],  
        "River": [  
            "A giant crocodile lunges at you from the water, its jaws snapping shut with incredible force.",  
            "A group of lizardfolk emerges from the riverbank, armed with crude weapons and shields.",  
            "A swarm of aggressive fish surrounds you in the shallows, biting viciously at exposed skin.",  
            "A water elemental rises from the river, its swirling form blocking your path with violent intent.",  
            "A giant snake slides silently through the water, striking with venomous fangs.",  
            "A group of sahuagin warriors leaps from the water, their tridents gleaming menacingly."  
        ],  
        "Swamp": [  
            "A giant crocodile ambushes you from the murky water, snapping its powerful jaws.",  
            "A bullywug hunting party surrounds you, their spears raised and croaks threatening.",  
            "A swarm of biting insects forces you to defend yourself as they attack relentlessly.",  
            "A shambling mound lumbers toward you, its mass of vegetation writhing and grasping.",  
            "A will-o'-wisp flickers in the mist, luring you into a trap before attacking with a surge of energy.",  
            "A black dragon wyrmling bursts from the swamp, its acidic breath searing the air around you."  
        ],  
        "Lake": [  
            "A giant octopus rises from the lake’s depths, its tentacles reaching out to ensnare you.",  
            "A group of kuo-toa crawls out of the water, their bulbous eyes fixed on you with malice.",  
            "A flock of harpies descends upon you from the nearby cliffs, their song disorienting and dangerous.",  
            "A merfolk warrior emerges from the water, brandishing a trident and shouting in an unknown tongue.",  
            "A giant snapping turtle lunges from the water, its jaws closing with a loud crack.",  
            "A water weird forms from the lake, its liquid body striking with surprising force."  
        ],  
        "Mountain": [  
            "A territorial wyvern screeches as it swoops down from the cliffs above, claws extended.",  
            "A mountain troll barrels toward you, roaring in anger and swinging its massive fists.",  
            "A rockslide reveals a nest of aggressive giant scorpions, their stingers raised to strike.",  
            "A gargoyle detaches from the rock face, its stone wings beating as it attacks with ferocity.",  
            "A pack of dire goats charges at you, their horns gleaming in the mountain sunlight.",  
            "A roc flies overhead, suddenly diving toward you with talons outstretched."  
        ],  
        "Ocean": [  
            "A group of sahuagin warriors emerges from the waves, their weapons gleaming as they attack.",  
            "A giant shark circles you menacingly, its dorsal fin cutting through the water.",  
            "A sea hag rises from the surf, cackling as she casts spells to ensnare and harm you.",  
            "A kraken tentacle lashes out from the depths, its immense size threatening to crush you.",  
            "A swarm of jellyfish surrounds you, their stings painfully numbing your limbs.",  
            "A pirate crew rows ashore, swords drawn and demanding your surrender."  
        ],  
        "Arctic": [  
            "A pack of winter wolves surrounds you, their breath visible in the cold air as they growl.",  
            "A frost giant approaches, its massive footsteps shaking the ground as it readies its weapon.",  
            "A remorhaz bursts out from under the snow, its steaming body radiating heat and menace.",  
            "An ice troll charges at you, its roar echoing across the frozen tundra as it swings a massive club.",  
            "A group of ice mephits flutters around you, their frost breath chilling you to the bone.",  
            "A white dragon wyrmling appears, its icy breath freezing the ground around it."  
        ],  
        "Volcanic": [  
            "A fire elemental bursts forth from a nearby fissure, its blazing form crackling with heat.",  
            "A magma mephit cackles as it flies toward you, hurling fiery projectiles in your direction.",  
            "A group of fire snakes slithers out from the molten rock, their scales glowing with heat.",  
            "An angry salamander emerges from the lava, brandishing a fiery spear and hissing menacingly.",  
            "A group of cultists worshipping the volcano attacks you, summoning fiery magic.",  
            "A lava drake crawls out of a pool of molten rock, its molten body radiating intense heat."  
        ],  
        "Desert": [  
            "A giant scorpion bursts from the sand, its pincers snapping and stinger poised to strike.",  
            "A group of jackalweres surrounds you, their eyes glinting maliciously as they draw weapons.",  
            "A purple worm erupts from the dunes, its massive jaws opening to swallow anything in its path.",  
            "A sandstorm clears, revealing a hostile group of desert nomads armed with curved swords.",  
            "A pack of hyenas begins circling you, their laughter echoing eerily across the dunes.",  
            "A blue dragon wyrmling lands in front of you, its crackling lightning breath arcing dangerously."  
        ],  
        "Badlands": [  
            "A group of bandits appears from behind the rocky outcroppings, weapons drawn and ready.",  
            "A bulette bursts from the ground, its armored body shaking the earth as it charges.",  
            "A chimera flies overhead, then dives toward you with a terrifying roar.",  
            "A pack of snarling hyenas rushes toward you, their eyes glinting with hunger.",  
            "A gorgon charges from the shadows, its metal body gleaming and nostrils steaming.",  
            "A group of hobgoblins sets up an ambush, their archers already taking aim."  
        ],  
        "Road": [  
            "A group of highwaymen steps onto the road, demanding your valuables with drawn blades.",  
            "A rogue knight blocks your path, challenging you to a duel with their gleaming sword.",  
            "A pack of dire wolves emerges from the nearby forest, their fangs bared and snarling.",  
            "A carrion crawler slithers out from beneath a bridge, its tentacles reaching hungrily for you.",  
            "A band of marauding orcs charges down the road, their war cries echoing in the distance.",  
            "A group of cultists blocks your path, chanting ominously and preparing to attack."  
        ],  
        "Forest": [  
            "You are ambushed by a group of bandits hiding in the trees, their arrows already flying.",  
            "A pack of wolves emerges from the shadows, growling menacingly as they close in.",  
            "A giant spider descends from its web, its many eyes fixed on you as it attacks.",  
            "A corrupted treant swings its massive limbs at you, its branches cracking like thunder.",  
            "A swarm of bats erupts from a hollow tree, biting and clawing as they surround you.",  
            "A group of ettercaps emerges from the underbrush, their webbing already tangling your path."  
        ]  
    },
    
    
    ### Exploration Encounters ###
    "Exploration": {
        "Temperate": [  
            "You find an abandoned cabin with signs of past inhabitants, including a dusty journal on the table.",  
            "You stumble upon a hidden trail leading deeper into the wilderness, flanked by ancient trees.",  
            "You discover a patch of rare herbs useful for alchemy, their distinct scent filling the air.",  
            "You find a circle of ancient standing stones inscribed with runes that glow faintly in the moonlight.",  
            "You notice a hollow log hiding a stash of small trinkets left by someone long ago.",  
            "A rusted sword sticks out from the earth near a tree, its blade etched with an unfamiliar crest."  
        ],  
        "Boreal": [  
            "You find a frozen lake with something glinting beneath the ice, hinting at treasure below.",  
            "You discover a long-forgotten hunter's camp buried under the snow, its tools still intact.",  
            "You spot a distant light flickering at the top of a snowy ridge, like a beacon calling you.",  
            "You uncover an animal skeleton with strange, unnatural markings carved into the bones.",  
            "You notice a narrow crevasse leading to an icy cave filled with shimmering stalactites.",  
            "A cluster of frost-covered arrows lies half-buried in the snow, their tips still sharp."  
        ],  
        "Hills": [  
            "You discover a hidden cave entrance beneath a rocky overhang, its interior dark and inviting.",  
            "You find an ancient cairn with offerings left by travelers long ago, including a small idol.",  
            "You stumble upon a strange rock formation that looks man-made, possibly a forgotten monument.",  
            "You find the remnants of an old battlefield, with rusted weapons and broken shields scattered around.",  
            "A faint trail of smoke rises from a distant hilltop, hinting at someone’s presence.",  
            "An abandoned watchtower stands atop a hill, its walls weathered but still sturdy."  
        ],  
        "Grassland": [  
            "You come across a circle of stones covered in moss and lichen, arranged with deliberate purpose.",  
            "You find a field of tall grass that hides a hidden burrow, possibly a den of local wildlife.",  
            "You discover the ruins of a small stone structure, possibly a watchtower or outpost.",  
            "You spot the remnants of an old wagon, its contents scattered across the plain, including faded maps.",  
            "A shallow depression in the ground reveals broken pottery and tools from an ancient settlement.",  
            "You notice a flock of birds circling above, leading you to a patch of exposed earth with bones."  
        ],  
        "River": [  
            "You discover a natural bridge of stones crossing the river, worn smooth by centuries of water flow.",  
            "You find a washed-up chest on the riverbank with its contents intact, including gold coins and trinkets.",  
            "You notice unusual carvings in the rocks along the river's edge, depicting scenes of an ancient ritual.",  
            "You stumble upon the remains of an ancient fishing village, its wooden structures now decayed.",  
            "A small whirlpool in the river reveals a glimpse of something glittering beneath the surface.",  
            "An old wooden pier juts into the river, its planks creaking underfoot but holding steady."  
        ],  
        "Swamp": [  
            "You find an old wooden boat half-submerged in the muck, its hull still sturdy despite the decay.",  
            "You discover a stone altar covered in moss and vines, with remnants of offerings scattered around.",  
            "You notice strange glowing mushrooms clustered around a tree stump, their light pulsing faintly.",  
            "You uncover the skeleton of a long-dead adventurer, still clutching a rusted sword and a torn map.",  
            "A series of stepping stones leads deeper into the swamp, each marked with strange glyphs.",  
            "An abandoned hut sits precariously on stilts above the muck, its door ajar and inviting exploration."  
        ],  
        "Lake": [  
            "You discover a small island in the center of the lake with ruins on it, accessible by a rowboat nearby.",  
            "You find an underwater cave entrance near the shoreline, partially hidden by reeds and rocks.",  
            "You spot an unusual ripple in the water, as if something large swam beneath the surface.",  
            "You uncover an old fishing net filled with strange, unidentifiable bones and rusted hooks.",  
            "A sunken statue lies partially visible at the bottom of the lake, its face worn smooth by the water.",  
            "You notice a series of shallow pools nearby, each filled with shimmering minerals."  
        ],  
        "Mountain": [  
            "You stumble upon a hidden mountain pass that isn't on any map, its path winding sharply upward.",  
            "You find a cave entrance with strange markings around it, suggesting it was once inhabited.",  
            "You discover an abandoned mining cart filled with unrefined ore and broken tools.",  
            "You spot an eagle's nest high on a cliff with an unusual shiny object inside, glinting in the sunlight.",  
            "A small shrine sits at the edge of a cliff, its offerings untouched and its carvings intricate.",  
            "You notice a faint glow emanating from a crevice, hinting at crystals or magical energy below."  
        ],  
        "Ocean": [  
            "You find a message in a bottle washed up on the shore, its contents cryptic and intriguing.",  
            "You spot the wreck of a ship partially visible beneath the waves, its hull split but treasures glinting inside.",  
            "You discover tidal pools filled with strange, colorful sea creatures that move in fascinating ways.",  
            "You notice a set of footprints leading from the water and into the sand, abruptly disappearing.",  
            "A cluster of barnacle-covered crates lies wedged between rocks, their contents still sealed.",  
            "An ancient stone arch rises from the shallows, its carvings worn but still legible."  
        ],  
        "Arctic": [  
            "You find an ice cave with walls that shimmer like glass, its interior reflecting the dim light eerily.",  
            "You discover a set of tracks in the snow leading to an unknown destination, possibly an animal lair.",  
            "You come across the frozen remains of an ancient explorer, their gear still partially intact.",  
            "You uncover a strange artifact encased in a block of ice, its origins unknown and mysterious.",  
            "A glacier reveals a fissure, exposing ancient fossils embedded within the icy walls.",  
            "A distant peak glows faintly, suggesting magical activity or a hidden landmark."  
        ],  
        "Volcanic": [  
            "You find a lava tube leading deep underground, its walls glowing faintly with residual heat.",  
            "You discover ancient carvings etched into the volcanic rock, depicting rituals and sacrifices.",  
            "You notice strange glowing crystals embedded in the cooled lava, their light pulsing faintly.",  
            "You stumble upon the charred remnants of an old campsite, its ashes still warm.",  
            "A bubbling hot spring sits nearby, its waters strangely soothing despite the harsh environment.",  
            "You see a petrified tree standing amidst the cooled lava, its form frozen in time."  
        ],  
        "Desert": [  
            "You find a buried obelisk poking out of the sand, its carvings hinting at a forgotten civilization.",  
            "You uncover a hidden oasis surrounded by palm trees, its water sparkling invitingly.",  
            "You discover the skeletal remains of a caravan with scattered treasures and rusted weapons.",  
            "You spot strange symbols carved into the side of a sand dune, their meanings unclear but intriguing.",  
            "A shallow depression reveals an ancient clay pot, its surface painted with faded designs.",  
            "A distant mirage leads you to a half-buried structure, its walls crumbling yet fascinating."  
        ],  
        "Badlands": [  
            "You discover a narrow canyon with walls carved by wind and water, its curves mesmerizing.",  
            "You find a fossilized skeleton of a massive creature, its bones jutting dramatically from the earth.",  
            "You stumble upon the ruins of an ancient settlement, long abandoned but still holding secrets.",  
            "You uncover a hidden stash of supplies buried beneath the dirt, including food and tools.",  
            "A petrified forest sprawls before you, its ancient trees frozen in time and stone.",  
            "You notice a distant spire jutting from the rocky horizon, glowing faintly in the setting sun."  
        ],  
        "Road": [  
            "You find an old milestone with strange symbols etched into it, marking an unknown destination.",  
            "You come across a partially collapsed bridge over a small ravine, its structure still passable with caution.",  
            "You discover a hidden trail branching off from the main road, overgrown but clearly once traveled.",  
            "You stumble upon an abandoned wagon, its contents still intact, including tools and a torn map.",  
            "A small roadside shrine sits nearby, its candles still burning faintly despite the wind.",  
            "You spot a tattered signpost pointing to a long-forgotten village, its letters barely legible."  
        ],  
        "Forest": [  
            "You find a tree with carvings of an ancient language on its bark, their meanings lost to time.",  
            "You discover an overgrown ruin hidden among the trees, its stone walls crumbling but intriguing.",  
            "You notice a faint trail of glowing mushrooms leading deeper into the forest, their light pulsating faintly.",  
            "You uncover a hidden cache of supplies buried at the base of a tree, including rope and dried rations.",  
            "A hollow tree reveals a small stash of coins and trinkets, likely left by a traveler long ago.",  
            "You stumble upon a forgotten grave marked by a moss-covered headstone, its inscription barely readable."  
        ]  
    }
}

#### END FRAME ####
frame.mainloop()