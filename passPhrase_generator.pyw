import tkinter as tk  
from tkinter import ttk, messagebox  
import random  
import string  

# Predefined extended word list for passphrase generation  
WORD_LIST = [  
    # Fruits  
    "apple", "banana", "cherry", "mango", "strawberry", "blueberry", "peach", "pear", "kiwi", "grapes", "orange",  
    "pineapple", "watermelon", "plum", "papaya", "fig", "coconut",
    "lychee", "mulberry", "persimmon", "tamarind", "guava", "durian", "jackfruit", "passionfruit", "rambutan",   
    "jabuticaba", "soursop", "longan", "sapodilla", "cherimoya", "pitaya", "camu", "acerola", "salak",   
    "marang", "pawpaw", "feijoa", "gooseberry", "boysenberry", "loganberry", "cloudberry", "huckleberry",   
    "cranberry", "elderberry", "currant", "calamansi", "kumquat", "yuzu", "bergamot",  

    # Vegetables  
    "carrot", "broccoli", "spinach", "pepper", "onion", "potato", "tomato", "cucumber", "lettuce", "zucchini",  
    "pumpkin", "celery", "radish", "beet", "asparagus",
    "parsnip", "rutabaga", "kohlrabi", "jicama", "artichoke", "fennel", "bokchoy", "mustardgreens",   
    "swisschard", "collards", "watercress", "endive", "radicchio", "turnip", "beetroot", "horseradish",   
    "daikon", "chayote", "okra", "cress", "celtuce", "tatsoi", "malunggay", "nopales", "gobo", "kangkong",   
    "amaranth", "tindora", "wingedbean", "bittermelon", "yardlongbean", "broccolini", "romanesco",    

    # Nuts       
    "almond", "walnut", "peanut", "cashew", "pecan", "hazelnut", "pistachio", "macadamia",    
    "chestnut", "brazilnut", "pine", "acorn", "betelnut", "candlenut", "ginkgo", "hickory",    
    "kukui", "baruka", "marcona", "tigernut",
    "hempseed", "chia", "poppyseed", "flaxseed", "sesame", "pumpkinseed", "sunflowerseed", "watermelonseed",   
    "pinon", "sacha", "pequi", "casimiroa", "karuka",   
    "nuts", "catalinaalmond", "egusi", "junipernut", "breadnut", "canariumnut", "chileanpine",   
    "salmonberry", "peanutbutter", "butternut", 

    # NATO Phonetic Alphabet  
    "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india",  
    "juliet", "kilo", "lima", "mike", "november", "oscar", "papa", "quebec", "romeo",  
    "sierra", "tango", "uniform", "victor", "whiskey", "xray", "yankee", "zulu",  

    # DND  
    "dragon", "beholder", "goblin", "orc", "troll", "kobold", "giant", "wyvern", "basilisk", "lich",  
    "mindflayer", "vampire", "zombie", "skeleton", "werewolf", "hydra", "chimera", "griffon", "owlbear",  
    "gnoll", "medusa", "succubus", "mimic", "elemental", "hag", "wraith", "shadow", "golem", "doppelganger",  
    "wizard", "fighter", "rogue", "cleric", "paladin", "ranger", "bard", "barbarian", "druid", "warlock", "monk",  
    "sorcerer",  

    # Animals  
    "lion", "tiger", "elephant", "wolf", "bear", "giraffe", "zebra", "cheetah", "panther", "leopard", "crocodile",  
    "kangaroo", "fox", "rabbit", "eagle", "hawk", "falcon", "owl", "penguin", "dolphin", "whale",  
    "cow", "pig", "chicken", "horse", "sheep", "goat", "duck", "goose", "donkey", "rooster", "turkey",  
    "salmon", "trout", "bass", "tuna", "halibut", "cod", "snapper", "mackerel", "swordfish", "catfish", "anchovy",  
    "herring", "flounder", "barracuda", "eel", "shark", "pike",
    "dog", "cat", "fish", "bird", "anteater", "axolotl", "capybara", "echidna", "pangolin", "quokka", "ibex", "wolverine", "ocelot",   
    "caracal", "saola", "numbat", "dikdik", "aardwolf", "cassowary", "kudu", "quetzal", "tamarin",   
    "dugong", "narwhal", "manatee", "platypus", "coati", "uakari", "binturong", "peccary", "tapir",   
    "arowana", "goby", "mudskipper", "lamprey", "sturgeon", "alligatorgar",  

    # Colors
    "red", "blue", "green", "yellow", "orange", "purple", "violet", "indigo", "pink", "teal", "brown", "beige", 
    "silver", "gold", "cyan", "azure", "maroon", "magenta", "scarlet", "emerald", "coral", "peach", "apricot", 
    "mustard", "navy", "amber", "lavender", "plum", "ivory", "salmon", "bronze", "ochre", "mint", "fuchsia", 
    "jade", "lime", "olive", "tan", "pearl", "charcoal", "ruby", "sapphire", "topaz", "orchid", "cream", "clay", 
    "lilac", "ash", "sand", "rose", "cobalt", "denim", "taupe", "slate", "umber", "seafoam", 
    "cerulean", "chartreuse", "vermillion", "periwinkle", "burgundy", "amethyst", "crimson", "saffron",   
    "sepia", "terracotta", "viridian", "eggshell", "mocha", "mahogany", "cinnamon",   
    "turquoise", "pewter", "agate", "ebony", "garnet", "opal", "onyx", "peachpuff",   
    "rubyred", "smokey", "topazblue", "midnight", "carmine",  

    # Tools
    "hammer", "wrench", "pliers", "screwdriver", "chisel", "drill", "saw", "level", "measure", "ladder",  
    "shovel", "axe", "hoe", "rake", "trowel", "spade", "mallet", "vise", "clamp", "socket set", "crowbar",  
    "pickaxe", "chainsaw", "file", "grinder", "sander", "welder", "torch", "anvil", "wheelbarrow", "toolbox",  
    "stud finder", "wire stripper", "pipe cutter", "caulking gun", "roller", "ratchet",  
    "square", "goggles", "gloves", "ear plugs", "work boots", "flashlight",
    
    # Car Brands
    "Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "Hyundai", "Kia", "Volkswagen", "Subaru", "Mazda",  
    "BMW", "Mercedes", "Audi", "Lexus", "Jeep", "Dodge", "Ram", "Porsche", "Tesla", "Volvo", "Jaguar",  
    "Buick", "Cadillac", "Acura", "Infiniti", "Mini", "Fiat", "AlfaRomeo", "Suzuki", "Mitsubishi", "Peugeot",  
    "Renault", "Citroen", "Skoda", "Seat", "Saab", "Opel", "Chrysler", "Lincoln", "Genesis", "Isuzu",   
    "LandRover", "Bentley", "Ferrari", "Lamborghini", "Maserati", "RollsRoyce", "Bugatti", "McLaren",   
    "Pagani", "Koenigsegg", "Rivian",

    # Calendar  
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",  
    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",  
    "christmas", "thanksgiving", "halloween", "easter", "newyear", "valentine", "hanukkah", "diwali", "eid", "ramadan",  

    # US States
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",   
    "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",   
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",   
    "Nevada", "NewHampshire", "NewJersey", "NewMexico", "NewYork", "NorthCarolina", "NorthDakota", "Ohio",   
    "Oklahoma", "Oregon", "Pennsylvania", "RhodeIsland", "SouthCarolina", "SouthDakota", "Tennessee", "Texas",   
    "Utah", "Vermont", "Virginia", "Washington", "WestVirginia", "Wisconsin", "Wyoming",
    
    # Countries
    "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Armenia", "Australia", "Austria",   
    "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",   
    "Botswana", "Brazil", "Brunei", "Bulgaria", "Burundi", "Cambodia", "Cameroon", "Canada", "Chad", "Chile",   
    "China", "Colombia", "Comoros", "Croatia", "Cuba", "Cyprus", "Denmark", "Djibouti", "Dominica", "Ecuador",   
    "Egypt", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia",   
    "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guyana", "Haiti", "Honduras", "Hungary",   
    "Iceland", "India", "Indonesia", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",   
    "Kenya", "Kiribati", "Kosovo", "Laos", "Suriname", "Tajikistan", "Mauritania", "Malawi", "Lesotho",   
    "Vanuatu", "Tuvalu", "TimorLeste", "SanMarino", "Monaco", "Liechtenstein", "Seychelles", "Palau",   
    "Maldives", "Barbuda", "Micronesia", "Tonga", "Nauru", "MarshallIslands",   

    # Cities
    "NewYork", "LosAngeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "SanAntonio", "SanDiego",   
    "Dallas", "SanJose", "Austin", "Jacksonville", "FortWorth", "Columbus", "Charlotte", "Indianapolis",   
    "SanFrancisco", "Seattle", "Denver", "Washington", "Boston", "ElPaso", "Nashville", "Detroit", "OklahomaCity",   
    "Portland", "LasVegas", "Memphis", "Louisville", "Baltimore", "Milwaukee", "Albuquerque", "Tucson",   
    "Fresno", "Sacramento", "Mesa", "KansasCity", "Atlanta", "Omaha", "ColoradoSprings", "Raleigh", "Miami",   
    "LongBeach", "VirginiaBeach", "Oakland", "Minneapolis", "Tulsa", "Arlington", "Tampa", "NewOrleans",   
    "Wichita", "Cleveland", "Bakersfield", "Aurora", "Anaheim", "Honolulu", "SantaAna", "Riverside", "CorpusChristi",   
    "Lexington", "Stockton", "Henderson", "SaintPaul", "StLouis", "Cincinnati", "Pittsburgh", "Greensboro",   
    "Anchorage", "Plano", "Lincoln", "Orlando", "Irvine", "Newark", "Durham", "ChulaVista", "Toledo", "FortWayne",   
    "StPetersburg", "Laredo", "JerseyCity", "Chandler", "Madison", "Lubbock", "Scottsdale", "Reno", "Buffalo",   
    "Gilbert", "Glendale", "NorthLasVegas", "WinstonSalem", "Chesapeake", "Norfolk", "Fremont", "Garland",
    "Kyoto", "Osaka", "Cairo", "Istanbul", "Mumbai", "Jakarta", "Dubai", "Lagos", "Karachi",   
    "Manila", "Seoul", "Bangkok", "Athens", "Dublin", "Reykjavik", "Helsinki", "Oslo",   
    "Zurich", "Geneva", "Brussels", "Vienna", "Milan", "Lisbon", "Prague", "Budapest",   
    "Bucharest", "Belgrade", "Sofia", "Tallinn", "Riga", "Vilnius",  

    # Clothing
    "Nike", "Adidas", "Puma", "Reebok", "UnderArmour", "Levi's", "Gap", "H&M", "Zara", "Uniqlo", "Gucci",   
    "Prada", "Chanel", "Versace", "Fendi", "Burberry", "Armani", "RalphLauren", "TommyHilfiger", "Lacoste",   
    "CalvinKlein", "Diesel", "Guess", "Dior", "Hermes", "Balenciaga", "Supreme", "OffWhite", "Balmain",   
    "Bershka", "Mango" "Forever21", "Abercrombie", "Hollister", "OldNavy", "Topshop",   
    "ASOS", "AllSaints", "TedBaker", "Roxy", "Billabong", "Quiksilver", "Patagonia", "Columbia", "TheNorthFace",   
    "Lululemon", "Champion", "Converse", "Vans", "Dockers", "Wrangler", "Carhartt", "Timberland", "Pendleton",   
    "Stussy", "Bape", "Kappa", "Fila", "HugoBoss", "Moschino", "Kenzo", "Moncler",  
    "YSL", "MichaelKors", "ToryBurch", "KateSpade", "Coach", "MarcJacobs", "J.Crew", "BananaRepublic",   
    "FreePeople", "Madewell", "Anthropologie", "Aritzia", "OutdoorVoices", "Express", "NewBalance", "Crocs",   
    "Skechers", "DrMartens", "Birkenstock", "VeraWang", "DKNY", "EddieBauer", "BrooksBrothers", "Lands'End",   
    "Everlane", "Celine", "Etro", "Ganni", "MiuMiu", "PaulSmith", "FredPerry", "LeSportsac",   
    "Barbour", "Belstaff", "Orvis", "Arcteryx", "StoneIsland", "Gant", "Seafolly", "RipCurl", "Rains",   
    "Filson", "Blundstone", "Woolrich", "Danner", "Frye", "Hunter",   
    "Arcade", "ToadandCo", "Kuhl", "Obermeyer", "Prana", "Icebreaker", "Smartwool", "Fjallraven",   
    "MountainHardwear", "Cotopaxi", "OutdoorResearch", "Marmot", "Sportswear",  

    # Conjunctions  
    "and", "or", "but", "nor", "so", "yet", "for", "although", "because", "since",   
    "unless", "until", "while", "if", "though", "even", "than", "where", "whether",  
    "after", "before", "once", "as", "when",  

    # Maritime
    "Atlantic", "Pacific", "Indian", "Arctic", "Southern", "Mediterranean", "Caribbean", "Baltic",   
    "NorthSea", "BlackSea", "RedSea", "Caspian", "Arabian", "Adriatic", "Aegean", "SouthChina",   
    "EastChina", "YellowSea", "Tasman", "CoralSea", "Bering", "Barents", "Beaufort", "Laptev",   
    "Greenland", "Norwegian", "Chukchi", "Okhotsk", "Marmara", "Sargasso", "Andaman", "Timor",   
    "Philippine", "Java", "Celebes", "RossSea", "Amundsen", "Weddell", "Scotia", "Labrador",   
    "HudsonBay", "BayOfBengal", "PersianGulf", "GulfOfMexico", "SeaOfJapan", "Ionian", "Tyrrhenian",   
    "BandaSea", "Arafura", "Mozambique", "SomaliSea", "SuluSea", "Bismarck", "Solomon",
    "Anchor", "Buoy", "Stern", "Bow", "Port", "Starboard", "Deck", "Hull", "Keel", "Mast", "Rigging",   
    "Sail", "Rudder", "Helm", "Bridge", "Cabin", "Galley", "Hatch", "Berth", "Fender", "Tiller",   
    "Gangway", "Winch", "Mooring", "Crow'sNest", "Lifeboat", "Compass", "Chronometer", "Chart",   
    "Logbook", "Radar", "Sonar", "Fathom", "Knot", "Buoyage", "Scupper", "Bilge", "Bulkhead",   
    "Windlass", "Cleat", "Davits", "Fo'c'sle", "Jib", "Spinnaker", "Boom", "Bowsprit", "Capstan",   
    "Halyard", "Leeward", "Windward", "Overboard", "Plimsoll", "Helmsman", "Quarterdeck", "Seacock",   
    "Shipyard", "Trawler", "Catamaran", "Frigate", "Galleon", "Yacht", "Dinghy", "Caravel",   
    "Barque", "Schooner", "Brig", "Barge", "Flotilla", "Convoy", "Buoyancy", "Mariner", "Seafarer",   
    "Admiral", "Bosun", "Deckhand", "Shipwright", "Navigator", "Helmsperson", "Seamanship", "Wharf",   
    "Dockyard", "Slipway", "Quay", "Jetty", "Harbor", "Breakwater", "Lighthouse", "Crowsnest",
    
    # Star Trek  
    "enterprise", "kirk", "spock", "picard", "data", "worf", "riker", "sulu", "uhura", "janeway", "seven", "voyager",  
    "defiant", "ds9", "borg", "romulan", "klingon", "ferengi", "cardassian", "q", "tribble",  

    # Star Wars  
    "luke", "leia", "yoda", "vader", "han", "chewbacca", "jedi", "sith", "deathstar", "tatooine", "coruscant", "lightsaber",  
    "palpatine", "stormtrooper", "kylo", "rey", "grogu", "mandalorian", "ahsoka", "grievous", "droid", "padme", "obiwan",  

    # Sports Teams  
    "yankees", "redsox", "dodgers", "lakers", "warriors", "patriots", "cowboys", "packers", "steelers", "eagles",  
    "broncos", "bears", "bulls", "heat", "knicks", "mets", "giants", "ravens", "chiefs", "seahawks"  

    # Space
    "quasar", "nebula", "galaxy", "comet", "asteroid", "supernova", "blackhole", "wormhole",   
    "pulsar", "singularity", "exoplanet", "satellite", "telescope", "observatory", "cosmos",   
    "photon", "neutron", "proton", "quark", "boson", "entropy", "gravity", "relativity",   
    "quantum", "darkmatter", "higgs", "spacetime", "eventhorizon", "multiverse", 
    "asteroid", "comet", "meteor", "meteoroid", "meteorite", "planet", "dwarfplanet", "exoplanet", "moon",   
    "satellite", "star", "supergiant", "redgiant", "whitedwarf", "neutronstar", "pulsar", "quasar",   
    "blackhole", "singularity", "eventhorizon", "galaxy", "nebula", "supernova", "hypernova", "protostar",   
    "stellarcore", "cosmicdust", "darkmatter", "darkenergy", "globularcluster", "opencluster",   
    "interstellar", "intergalactic", "magellaniccloud", "andromeda", "milkyway", "orion", "pleiades",   
    "betelgeuse", "sirius", "vega", "aldebaran", "polaris", "proxima", "rigel", "canopus", "arcturus",   
    "altair", "deneb", "capella", "spica", "regulus", "antares", "castor", "pollux",
    "aurora", "eclipse", "solarflare", "coronalhole", "coronalmass", "radiationbelt", "cosmicray",   
    "gamma-rayburst", "x-rayburst", "tidalforce", "gravitationalwave", "redshift", "blueshift",   
    "orbit", "perihelion", "aphelion", "perigee", "apogee", "synodic", "ecliptic", "transit",   
    "conjunction", "opposition", "occultation", "supermoon", "bloodmoon",
    "spacesuit", "rocket", "shuttle", "lander", "rover", "probe", "orbiter", "launchpad",   
    "spacecraft", "capsule", "module", "saturnv", "falcon", "starship", "booster", "thruster",   
    "heatshield", "payload", "spacewalk", "extravehicular", "dockingsystem", "commandmodule",   
    "servicebay", "spaceport", "launchvehicle", "crewdragon", "orioncapsule", "iss", "hubble",   
    "voyager", "cassini", "jameswebb", "newhorizons",
    "nasa", "spacex", "blueorigin", "roscosmos", "esa", "isro", "cnsa", "jaxa", "apollo",   
    "artemis", "gemini", "mercury", "vostok", "soyuz", "salyut", "mir", "skylab", "mariner",   
    "pioneer", "pathfinder", "curiosity", "perseverance", "ingenuity", "opportunity",   
    "spirit", "galileo", "kepler", "tess",
    "spacetime", "wormhole", "multiverse", "bigbang", "inflation", "cosmicmicrowave",   
    "fasterthanlight", "lightspeed", "relativity", "specialrelativity", "generalrelativity",   
    "quantummechanics", "higgsboson", "entropy", "singularity", "hawkingradiation", "antimatter",   
    "darkflow", "tachyon", "energyfield", "graviton", "stringtheory", "brane", "dimension",   
    "hyperdimension", "quantumfoam", "vacuumdecay", "cosmology", "chrononaut", "timeparadox",   
    "timewarp", "spatialanomaly", "chroniton", "subspace", "tachyonbeam", "photon", 

    # Zelda       
    "link", "zelda", "ganondorf", "hyrule", "epona", "sheik", "goron", "zora", "kokiri",    
    "gerudo", "deku", "hylian", "master", "triforce", "midna", "fi", "navi", "tatl",    
    "malon", "saria", "ruto", "darunia", "impaz", "ravio", "twinrova", "ghirahim",    
    "volvagia", "vaati", "minish", "faron", "eldin", "lanayru", "arbiter", "agahnim",    
    "skullkid", "termia", "majora", "ganon", "demise", "hyrulewar", "calamity",    
    "korok", "beedle", "tingle", "rupee", "cucco", "bombchu", "bokoblin", "moblin",    
    "revali", "mipha", "urbosa", "daruk", "yiga", "ravio", "maple", "oracle",    
    "din", "nayru", "farore", "bellum", "linebeck", "stalfos", "poe", "darklink",    
    "ganonsork", "hylia", "ancient", "wizzrobe", "lynel", "molduga", "blight", "sheikah",    
    "divines", "hateno", "lorule", "holodrum", "labrynna", "windfish", "fiercedeity",    
    "hyrulking", "greatfair", "helmasaur", "manhandla", "phantom", "armos", "gohma",    
    "moldorm", "lanmolas", "vire", "zant", "byrne", "yeto",  

    # Foods  
    "burger", "hotdog", "chili", "pancakes", "waffles", "grilled", "crabcakes", "gumbo", "jambalaya",   
    "sloppyjoe", "ribs", "taco", "burrito", "tamale", "quesadilla", "nachos", "salsa", "mole", "tostada",   
    "dumpling", "friedrice", "noodles", "ramen", "sushi", "tempura", "miso", "teriyaki", "naan", "biryani",   
    "roti", "vindaloo", "samosa", "pakora", "pizza", "pasta", "paella", "fondue", "bratwurst", "pierogi",   
    "jerkchicken", "oxtail", "plantains", "conch",
    "ceviche", "empanada", "arepas", "pupusas", "tamales", "yuca", "tostones", "fufu", "egusi", "shakshuka",  
    "falafel", "hummus", "tabbouleh", "shawarma", "kabsa", "kebab", "baba ghanouj", "manakeesh", "fattoush",   
    "baklava", "maqluba", "harira", "tajine", "couscous", "koshari",    
    "risotto", "gnocchi", "lasagna", "calzone", "bruschetta", "frittata", "carbonara", "puttanesca", "cioppino",    
    "caponata", "ratatouille", "bouillabaisse", "cassoulet", "tartiflette", "croissant", "beignets", "galette",    
    "crepes", "quiche", "brioche", "raclette", "escargot", "coqauvin", "chowder", "lobsterroll", "crabcakes",    
    "clamchowder", "biscotti", "gelato", "sorbetto", "sushiroll", "wasabi",
    "abalone", "aioli", "alfredo", "anchovy", "applesauce", "arugula", "avocado", "bacon",   
    "bagel", "basil", "bisque", "bologna", "bouillon", "broth", "brownie", "butter",   
    "cactus", "cannoli", "caramel", "caviar", "cheddar", "cheese", "cherries", "chickpea",   
    "chili", "chorizo", "chowmein", "chutney", "clafoutis", "coleslaw", "coriander", "crackers",   
    "cream", "croquette", "crouton", "cupcake", "currants", "custard", "dates", "doughnut",   
    "durian", "edamame", "eel", "eggnog", "emmental", "farro", "fig", "flan", "flatbread",   
    "focaccia", "fritters", "galangal", "garbanzo", "garlic", "gazpacho", "ghee", "ginger",   
    "gouda", "granola", "greens", "grits", "guacamole", "haddock", "halva", "ham", "honey",   
    "jalapeno", "jelly", "lamb", "lasagna", "lentils", "macaroon", "marmalade", "marzipan",   
    "mascarpone", "mousse", "muffin", "mushroom", "nutmeg", "octopus", "olive", "omelet",   
    "orzo", "oyster", "parmesan", "pickle", "popcorn", "pork", "praline", "pretzel", "prosciutto",   
    "pudding", "quinoa", "raisin", "ravioli", "relish", "ricotta", "risotto", "roquefort",   
    "rye", "salami", "sardine", "satsuma", "scallop", "shallot", "sherbet", "shrimp", "snapper",   
    "sorbet", "souffle", "soybean", "steak", "stilton", "stringbean", "sugar", "sundriedtomato",   
    "tamarind", "tapioca", "tilapia", "tofu", "truffle", "vanilla", "veal", "venison", "wasabi",   
    "watercress", "wheat", "yam", "yogurt", "ziti",

    # Beverages   
    "espresso", "americano", "latte", "cappuccino", "macchiato", "mocha", "cortado", "ristretto", "flatwhite",    
    "affogato", "doppio", "breve", "redeye", "lungo", "frappe", "icedlatte", "nitrobrew", "coldbrew",    
    "piccolo", "turkhjava", "green", "matcha", "sencha", "jasmine", "oolong", "pu-erh", "darjeeling",    
    "assam", "masala", "chai", "earlgrey", "rooibos", "camomile", "peppermint", "hibiscus", "white",    
    "lapsang", "yerba", "mate", "kombucha",
    
    # Emperors    
    "augustus", "tiberius", "caligula", "claudius", "nero", "galba", "otho", "vitellius",    
    "vespasian", "titus", "domitian", "nerva", "trajan", "hadrian", "antoninus", "marcus",    
    "commodus", "pertinax", "julianus", "septimius", "caracalla", "geta", "macrinus",    
    "elagabalus", "alexander", "maximinus", "gordian", "philippus", "decimus", "valerian",    
    "gallienus", "claudius", "aurelian", "probus", "carus", "numerian", "diocletian",    
    "maximian", "galerius", "constantine", "licinius", "julian", "jovian", "valentinian",    
    "valens", "theodosius", "arcadius", "honorius", "constantius", "justinian", "heraclius",    
    "phocas", "leo", "zeno", "romulus", "majorian", "anthemius", "avitus", "nepos",    
    "julius", "domitianus", "magnentius", "gratian", "theodoric", "eugenius", "marcellus",    
    "tacitus", "florianus", "carinus", "licinianus", "maxentius", "maximus", "valentinus",    
    "jovinus", "athalaric", "glycerius", "zeno", "leoiv", "basiliscus", "constantii",    
    "theophilus", "anastasius", "arcadius", "theodora", "marcianus", "augustulus", "domitius"  

    # Mythology     
    "zeus", "hera", "poseidon", "hades", "demeter", "athena", "apollo", "artemis",   
    "ares", "aphrodite", "hermes", "hephaestus", "hestia", "dionysus", "persephone",   
    "chronos", "gaia", "uranus", "nyx", "erebus", "helios", "selene", "eos",   
    "pan", "nike", "tyche", "nemesis", "eris", "thanatos", "hypnos", "morpheus",   
    "janus", "jupiter", "juno", "neptune", "pluto", "ceres", "minerva", "venus",   
    "mars", "mercury", "vulcan", "vesta", "bacchus", "proserpina", "saturn", "ops",   
    "sol", "luna", "aurora", "fortuna", "victoria", "discordia", "orcus", "terminus",   
    "odin", "frigg", "thor", "loki", "balder", "freyja", "frey", "tyr",   
    "heimdall", "hodr", "vidar", "vali", "bragi", "idunn", "skadi", "njord",   
    "ran", "aegir", "hel", "fenrir", "jormungandr", "surtur", "ymir", "mimir",   
    "ullr", "forseti", "eir", "sigyn", "hati", "skoll", "verdandi", "urd", "skuld",   
    "nanna", "modi", "magni", "sif", "kvasir", "gullveig", "hecate", "eros",   
    "rhea", "typhon", "medusa", "pandora", "achilles", "hercules", "odysseus",   
    "perseus", "theseus", "jason", "orpheus", "pegasus", "cerberus", "minotaur",   
    "chimera", "sphinx", "hydra", "phoenix", "griffin", "centaur", "satyr",   
    "cyclops", "titans", "nymphs", "dryads", "sirens", "furies", "erinyes",   
    "muses", "fates", "asgard", "yggdrasil", "ragnarok", "valhalla", "mjolnir",   
    "valkyrie", "nidhogg", "surt", "vili", "ve", "bifrost", "ginnungagap",   
    "midgard", "niflheim", "muspelheim", "jotunheim", "alfheim", "svartalfheim",   
    "vanaheim", "Achilles", "Cerberus", "Prometheus", "Argus", "Atalanta", "Echidna", "Hestia", "Hecate",   
    "Charybdis", "Scylla", "Antaeus", "Pegasus", "Panacea", "Erebus", "Phobos", "Deimos",   
    "Calliope", "Clio", "Thalia", "Euterpe", "Polyhymnia", "Terpsichore", "Urania", "Melpomene",   
    "Orion", "Clytemnestra", "Icarus", "Daedalus", "Tantalus", "Sisyphus",    

    # Companies   
    "apple", "amazon", "alphabet", "microsoft", "exxonmobil", "berkshire", "chevron", "meta",    
    "pfizer", "pepsico", "citi", "oracle", "intel", "comcast", "verizon", "walmart",    
    "at&t", "disney", "boeing", "tesla", "ford", "target", "adobe", "dell",    
    "fedex", "ups", "costco", "amgen", "merck", "paypal", "qualcomm", "3m",    
    "ibm", "nike", "honeywell", "netflix", "caterpillar", "texasinst", "micron",    
    "gilead", "biogen", "autozone", "snap", "kraft", "wellsfargo", "goldman", "tdbank",    
    "raytheon", "lockheed", "cvshealth", "abbvie", "allstate", "aetna", "ameren", "anthem",    
    "avangrid", "baxter", "biogen", "centene", "citrix", "corning", "dominion", "dow",    
    "dupont", "edison", "genpact", "hallibur", "humana", "intuit", "keycorp", "kimberly",    
    "kraft", "lennar", "marathon", "marriott", "navistar", "netapp", "norfolk", "nucor",    
    "nvidia", "paccar", "parsons", "prologis", "progress", "prudential", "publicsvc",    
    "quanta", "regions", "roku", "seaworld", "snap", "southern", "spirit", "stanley",    
    "tenet", "textron", "thermo", "united", "valero", "veritiv", "vistaprint", "walgreens",    
    "whirlpool", "xerox", "zillow", "zoom", 

    # Miscellaneous
    "abyss", "acorn", "amber", "anthem", "arcade", "arctic", "aster", "badge", "banjo",   
    "beacon", "beetle", "bison", "blade", "blaze", "blimp", "bliss", "bluff", "bongo",   
    "booth", "breeze", "bronco", "brush", "bugle", "cabin", "camel", "candy", "caper",   
    "cargo", "cello", "chalk", "charm", "chess", "cliff", "cloak", "clown", "cobra",   
    "comet", "coral", "crane", "creek", "crest", "crypt", "cupid", "daisy", "delta",   
    "disco", "diver", "dodge", "dome", "donut", "dream", "drift", "drone", "ember",   
    "epic", "falcon", "ferry", "fjord", "flame", "flute", "forge", "frost", "fungus",   
    "fuzzy", "gale", "gecko", "gemini", "ghost", "glide", "globe", "gnome", "grape",   
    "grove", "guest", "gusto", "gypsy", "harp", "hatch", "haven", "hazel", "hedge",   
    "helix", "honey", "horn", "hound", "hurry", "icicle", "iguana", "ionic", "ivory",   
    "jewel", "jolly", "jumbo", "karat", "karma", "kayak", "kudos", "lager", "laser",   
    "latch", "lilac", "lodge", "lotus", "lunar", "lynx", "magic", "magma", "mango",   
    "maple", "meadow", "melon", "mist", "mixer", "mohawk", "mossy", "mural", "muse",   
    "myth", "nymph", "oasis", "onion", "opera", "orbit", "otter", "oxbow", "panda",   
    "peony", "petal", "pilot", "pixel", "plaza", "plume", "polar", "prism", "pulse",   
    "pyre", "quail", "quartz", "quill", "quiet", "quilt", "radar", "raven", "rhyme",   
    "ridge", "river", "robin", "rogue", "rook", "ruble", "rugby", "saber", "salvo",   
    "samba", "satyr", "scarf", "scout", "serif", "shade", "shard", "shark", "sheep",   
    "shell", "shrub", "silk", "siren", "skate", "slate", "sloth", "smelt", "smith",   
    "solar", "sonar", "spade", "spark", "spear", "spice", "spine", "spire", "spore",   
    "squid", "stake", "stall", "stone", "storm", "swell", "swift", "swoop", "talon",   
    "terra", "thief", "thorn", "thrum", "tiara", "tiger", "titan", "toast", "torch",   
    "totem", "tower", "trace", "trail", "trawl", "truce", "trump", "tulip", "twine",   
    "union", "vapor", "vault", "vivid", "vixen", "vogue", "waltz", "whisk", "whisker",   
    "wisp", "witty", "wombat", "woven", "wrath", "wreath", "xenon", "xerox", "yacht",   
    "yodel", "youth", "zenith", "zipper", "zodiac", "zonal", "zoom",
    "abyssal", "acetone", "acrylic", "admiral", "aerobic", "alchemy", "almanac", "ammonia", "android",   
    "anemone", "angst", "anvil", "aquatic", "archive", "armory", "arsenic", "artwork", "ashore",   
    "asphalt", "astral", "atlas", "atrium", "auricle", "aviator", "awning", "azimuth", "baboon",   
    "badger", "bagpipe", "bamboo", "bandit", "banshee", "banyan", "barbell", "bargain", "barista",   
    "barrage", "bastion", "bathtub", "bazooka", "beet", "beetle", "bellhop", "biceps", "bifrost",   
    "bigfoot", "bilge", "biology", "biplane", "birch", "bizarre", "blaster", "blender", "blizzard",   
    "blubber", "boarder", "bogey", "boiler", "bonfire", "bonsai", "boomer", "boulder", "bowline",   
    "bramble", "brandy", "bravado", "brimstone", "bronzed", "brunette", "buckeye", "buckler", "buffalo",   
    "buffet", "bulwark", "bunting", "burlap", "butane", "butcher", "buttery", "buzzard", "cabana",   
    "caboose", "cactus", "cairn", "calcite", "caldera", "caliber", "camphor", "canopy", "canyon",   
    "capsize", "capstan", "carbine", "caribou", "carousel", "carving", "cascade", "cashmere", "cassava",   
    "catapult", "catfish", "cattail", "cauldron", "cavalry", "caveman", "cedar", "celadon", "centaur",   
    "chamber", "chateau", "chisel", "chiton", "chopper", "chorus", "cinder", "clapper", "cloister",   
    "coal", "coastal", "cobalt", "cobbler", "coconut", "coffer", "colony", "compass", "concord",   
    "condor", "confetti", "conifer", "corsair", "corset", "cotton", "cougar", "cowbell", "cowhide",   
    "coyote", "crackle", "craft", "cranial", "crawdad", "crescent", "crimson", "crinkle", "critter",   
    "croaker", "crossbow", "crowbar", "crusade", "cumulus", "curtain", "cyclone", "dagger", "dahlia",   
    "dashing", "dauntless", "daybreak", "decanter", "decibel", "decoy", "defrost", "deluge", "demigod",   
    "density", "descent", "desert", "desire", "detour", "diamond", "diorama", "docking", "dolphin",   
    "domino", "donkey", "downhill", "drizzle", "droplet", "drummer", "drywall", "duchess", "duplex",   
    "dwarven", "dynamo", "earthen", "ebony", "echidna", "eclipse", "elegant", "emerald", "enclave",   
    "endless", "engine", "engrave", "entwine", "epitome", "erosion", "esoteric", "eternal", "ether",   
    "ethos", "evermore", "exalted", "exodus", "eyelash", "eyewear", "faction", "fanfare", "fantasy",   
    "farrier", "fateful", "faucet", "feather", "fervor", "festival", "fiddle", "figment", "firefly",   
    "fireman", "fissure", "flannel", "flask", "flaxen", "fleece", "floater", "flotsam", "flycatcher",   
    "flywheel", "fogbank", "foreman", "forever", "forge", "fountain", "foxhole", "fracture", "freight",   
    "fresco", "frigate", "fulcrum", "furnace", "futon", "gadget", "gaffer", "galaxy", "galleon",   
    "gambit", "gander", "garland", "garment", "garrison", "gazelle", "geology", "gilded", "gingham",   
    "glacier", "glamour", "gleaming", "gliding", "glisten", "glitter", "gnarled", "goblin", "goldenrod",   
    "gondola", "gorilla", "gossamer", "granite", "grapnel", "gravitas", "grotto", "gullet", "gunmetal",   
    "gyroscope", "habitat", "halberd", "halcyon", "hallway", "handy", "harpoon", "harvest", "hatchet",   
    "hazard", "headway", "heather", "helical", "heroine", "hexagon", "highway", "hinter", "hoarder",   
    "horizon", "hullabaloo", "hurdle", "hurricane", "icelandic", "igneous", "illusion", "imbibe",   
    "immortal", "impulse", "infamy", "infinity", "inkling", "innate", "inquiry", "insight", "instinct",   
    "intrepid", "invasion", "isotope", "jackal", "jasmine", "jaybird", "jigsaw", "jogger", "jubilee",   
    "jungler", "justice", "karate", "keystone", "kindred", "kingdom", "kitchen", "knapsack", "knighthood",   
    "labyrinth", "lacquer", "landmark", "lantern", "latitude", "lavender", "leather", "legend",   
    "lighthouse", "limestone", "limpid", "lioness", "lithium", "locust", "lodestone", "logbook",   
    "longship", "lottery", "lumber", "luminous", "luster", "lyric", "maelstrom", "magnet", "magnolia",   
    "majesty", "malachite", "mammoth", "mandolin", "manifest", "mantle", "mariner", "marriage",   
    "marsh", "masquerade", "mastodon", "matador", "matter", "meadow", "melody", "memory", "meteorite",   
    "metronome", "midsummer", "milestone", "millstone", "minaret", "minnow", "mirage", "mission",   
    "monsoon", "monument", "moonbeam", "moonscape", "morning", "mosaic", "mountain", "movement",   
    "mystic", "narrative", "narwhal", "nebula", "nectar", "neptune", "nightfall", "nightmare",   
    "nomad", "northern", "novice", "nymph", "obelisk", "obsidian", "oceanic", "octagonal", "octopus",   
    "odyssey", "omen", "opaline", "opinion", "oracle", "orchid", "oregano", "orifice", "ornament",   
    "orphan", "outlaw", "outpost", "overcast", "oxygen", "ozone", "paisley", "palette", "pandemonium",   
    "paradox", "parasol", "parchment", "parlor", "parsnip", "pasture", "pavilion", "peacock", "pebble",   
    "pendulum", "penguin", "pergola", "perilous", "periwinkle", "phantom", "phoenix", "piano",   
    "pinnacle", "pirate", "pistol", "pixie", "plankton", "platinum", "plummet", "polaris", "ponder",   
    "poplar", "portico", "prairie", "precious", "predator", "prelude", "primrose", "pristine",   
    "prodigy", "prologue", "prophet", "prospect", "proton", "pyramid",
    "abacus", "abandon", "abbey", "abdomen", "abolish", "absorb", "abyssal", "academy", "acclaim", "acorned",  
    "acoustic", "acrobat", "actress", "adaptor", "admiral", "adorable", "advocate", "aeronaut", "affinity",  
    "airborne", "alchemist", "algebra", "alliance", "alluvial", "almanac", "alpenglow", "alphabet", "altitude",  
    "amaranth", "amethyst", "amoeba", "amplify", "anchored", "anemone", "angelic", "angler", "animated", "animism",  
    "annex", "annulus", "antelope", "antenna", "antique", "antonym", "anvil", "aperture", "aphelion", "apogee",  
    "apricot", "aqueduct", "aquifer", "arachnid", "archway", "artisan", "artistry", "ashwood", "aspen", "asteroid",  
    "atlas", "atomizer", "atrium", "aurora", "autonomy", "aviation", "avocado", "backdrop", "backpack", "bacteria",  
    "baggage", "ballista", "ballet", "balloon", "baluster", "bandage", "bandana", "banditry", "banker", "banner",  
    "baritone", "barracks", "barrier", "basilisk", "bastille", "battles", "bazooka", "beaconry", "bedrock", "beechnut",  
    "beetroot", "bellows", "beret", "beryl", "bestiary", "bifrost", "bigfoot", "bilberry", "bilge", "biology",  
    "birchwood", "birdbath", "birdsong", "bitters", "blizzard", "blossom", "bluejay", "blueprint", "bogwood",  
    "bohemian", "boiler", "bolster", "bonanza", "bonfire", "bonsai", "booster", "boulder", "boundary", "bracelet",  
    "bramble", "brass", "brawler", "breadth", "breakage", "breakout", "briar", "brigade", "brisket", "brocade",  
    "bromine", "brother", "brunette", "buckeye", "buckler", "buffet", "bulldog", "bullfrog", "bullion", "bullseye",  
    "bullwhip", "bungalow", "bunting", "butcher", "cabinet", "caboose", "cadence", "calcite", "caliber", "calypso",  
    "camellia", "campfire", "canyon", "caprice", "capsule", "captain", "caravan", "carbine", "carcass", "carillon",  
    "carpenter", "carriage", "carve", "cashew", "cassette", "catapult", "cathedral", "cavalier", "cavern", "cedarwood",  
    "ceramics", "chalet", "chamber", "chandler", "chapel", "charger", "chatroom", "cheetah", "chessboard", "chimera",  
    "chipmunk", "chivalry", "chloride", "choir", "chopper", "chrysalis", "cinnamon", "cirrus", "citadel", "citrine",  
    "cladding", "clarinet", "claymore", "cleanup", "cleaver", "climber", "clockwork", "clover", "clubhouse", "cluster",  
    "coalesce", "coastal", "cobalt", "cobweb", "coconut", "codex", "coffer", "colander", "collar", "colossus",  
    "compass", "comrade", "concord", "condor", "conifer", "conquest", "consul", "coraline", "cordial", "corral",  
    "corsair", "corset", "cottonwood", "countess", "courier", "crater", "crimson", "crockery", "crossbeam",  
    "crossfire", "crowfoot", "crusader", "crystals", "cumulus", "curator", "currant", "cutlass", "cyclone", "cygnet",  
    "dagger", "dahlia", "daffodil", "dandelion", "dashing", "daybreak", "decanter", "decibel", "defender", "delirium",  
    "dendrite", "density", "dentist", "derelict", "deserted", "designee", "detonate", "diadem", "diary", "diecast",  
    "dignity", "diorama", "diplomat", "disarray", "disguise", "dividend", "dockside", "dolphin", "dominion", "dovetail",  
    "downpour", "drainage", "driftwood", "drizzle", "drywall", "duality", "duchess", "duplex", "dwarven", "dynamo",  
    "earthen", "ebonwood", "eclipse", "elegance", "elephant", "emerald", "empire", "enclave", "endless", "engraved",  
    "entangle", "epilogue", "epitome", "epoch", "erosion", "eternal", "ethereal", "euphoria", "evergreen", "evermore",  
    "exalted", "excelsior", "exodus", "eyelash", "fable", "fabled", "fabrics", "faience", "fairway", "falchion",  
    "fanfare", "fantasy", "farmland", "farthest", "faucet", "feathers", "felicity", "fencer", "festival", "fiddler",  
    "fireball", "firefly", "firmament", "fissure", "flamingo", "flannel", "flaxen", "fletcher", "flintlock",  
    "flotation", "flowchart", "flurry", "forestry", "foretold", "foreword", "forging", "fortify", "fortress",  
    "fossil", "fountain", "foxhole", "fracture", "fragrance", "freedom", "freefall", "freezer", "fresco", "frigate",  
    "frosting", "fulcrum", "furnace", "galactic", "galleon", "galleys", "galvanic", "gardener", "garments", "garuda",  
    "gazebo", "geology", "geometry", "germinal", "gilded", "ginger", "gladiator", "glamour", "gleaming", "gliding",  
    "glimmer", "glisten", "glitter", "globule", "glorious", "gnarled", "goblet", "goldfish", "gondola", "gopher",  
    "gossamer", "graceful", "granite", "grapnel", "grassland", "gravitas", "greenery", "gridlock", "griffin", "grizzly",  
    "grotto", "guardian", "gunmetal", "gyroscope", "habitat", "halberd", "halcyon", "hallmark", "hallway", "hamlet",  
    "harbinger", "harpoon", "harvest", "hatchery", "hatchling", "headgear", "heirloom", "helipad", "helmsman",  
    "hemlock", "highland", "hightail", "hinter", "hoarder", "hollow", "horizon", "hullabaloo", "hurricane", "igneous",  
    "illusion", "imbibe", "immortal", "impulse", "infinity", "innkeeper", "insignia", "intrepid", "isotopes",  
    "jackal", "jasmine", "jaybird", "jeweller", "jigsaw", "jubilee", "jungler", "keystone", "kindred", "kingdom",  
    "kitchen", "knighthood", "lacquer", "landmark", "lantern", "latitude", "lavender", "leathery", "legendary",  
    "lightbox", "limestone", "lioness", "lodestone", "logistics", "longship", "luminous", "lyrical", "maelstrom",  
    "magnetic", "magnolia", "majesty", "malachite", "mandolin", "manifest", "mantis", "mariner", "marriage",  
    "masquerade", "memento", "meteorite", "midsummer", "milestone", "millstone", "minaret", "mirage", "mission",  
    "monsoon", "monument", "moonbeam", "moonscape", "morning", "mosaic", "mountain", "movement", "mystic",  
    "narrative", "nectarine", "nightfall", "nightmare", "obelisk", "obsidian", "octagon", "octopus", "odyssey",  
    "omen", "opaline", "oracle", "ornament", "outpost", "overcast", "oxygen", "paisley", "palette", "pandemonium",  
    "paradox", "parchment", "pavilion", "peacock", "pendulum", "pergola", "phantom", "phoenix", "pinnacle",  
    "pirate", "pixie", "plankton", "platinum", "plummet", "poinsettia", "ponder", "portico", "prairie", "pristine",  
    "prodigy", "prologue", "quarry", "quasar", "quintet", "radiance", "rainbow", "ravenous", "redwood", "rendezvous",  
    "reverie", "rhodium", "rippling", "riverbank", "roadway", "rooftop", "rosewood", "runestone", "saffron",  
    "sapphire", "scarlet", "scimitar", "seascape", "shipyard", "silhouette", "skyline", "slalom", "snowfall",  
    "snowflake", "solstice", "sonata", "spectral", "squall", "stallion", "starburst", "starlight", "stargaze",  
    "stormcloud", "submarine", "sunburst", "sunflower", "sunrise", "sunset", "sunstone", "symphony", "talisman",  
    "tapestry", "tarmac", "teleport", "thunder", "tidalwave", "timeless", "tornado", "treetop", "trident",  
    "tundra", "turquoise", "umbra", "valiant", "valkyrie", "vanguard", "verdant", "vortex", "wanderer", "warlock",  
    "wayfinder", "whirlpool", "wildfire", "windward", "wisp", "wizardry", "zephyr"

]  

# Allowed symbols  
ALLOWED_SYMBOLS = "!@#$%&():;_"  

# Function to generate a passphrase  
def generate_passphrase():  
    excluded_word = "Nord"  
    try:  
        # Convert the selected length from string to integer  
        selected_length = int(length_selector.get())  
        passphrase = ""  
        current_length = 0  

        # Randomly start with a symbol, number, or letter  
        start_char = random.choice([  
            random.choice(ALLOWED_SYMBOLS),  
            random.choice(string.digits),  
            random.choice(string.ascii_letters)  
        ])  
        passphrase += start_char  
        current_length += len(start_char)  

        while current_length < selected_length:  
            # Randomly select a word from the word list  
            word = random.choice(WORD_LIST)  

            # Capitalize or modify the word  
            if random.random() > 0.5:  
                word = word.capitalize()  
            else:  
                word += random.choice(string.ascii_lowercase)  

            # Add a random symbol and number  
            symbol = random.choice(ALLOWED_SYMBOLS)  
            number = random.choice(string.digits)  
            word += symbol + number  

            # Check if adding this word exceeds the length  
            if current_length + len(word) > selected_length:  
                # Fill the remaining space with random characters  
                remaining_space = selected_length - current_length  
                filler = ''.join(random.choices(string.ascii_letters + string.digits + ALLOWED_SYMBOLS, k=remaining_space))  
                passphrase += filler  
                break  

            # Add the word to the passphrase  
            passphrase += word  
            current_length += len(word)  

        # Ensure the passphrase contains at least one number and one symbol  
        if not any(char.isdigit() for char in passphrase):  
            passphrase = passphrase[:-1] + random.choice(string.digits)  
        if not any(char in ALLOWED_SYMBOLS for char in passphrase):  
            passphrase = passphrase[:-1] + random.choice(ALLOWED_SYMBOLS)  

        # Display the passphrase in the output entry box  
        output_entry.delete(0, tk.END)  
        output_entry.insert(0, passphrase)  
    except ValueError:  
        messagebox.showerror("Error", "Invalid length selected!")  

# Function to copy the passphrase to the clipboard  
def copy_to_clipboard():  
    passphrase = output_entry.get()  
    if passphrase:  
        root.clipboard_clear()  
        root.clipboard_append(passphrase)  
        root.update()  

        # Show temporary "Copied to Clipboard" notification  
        copied_label.config(text="Copied to Clipboard!", fg="#00ff00")  
        root.after(1500, lambda: copied_label.config(text=""))  # Clear message after 1.5 seconds  
    else:  
        copied_label.config(text="No passphrase to copy!", fg="#ff0000")  
        root.after(1500, lambda: copied_label.config(text=""))  # Clear message after 1.5 seconds  

# Create the main application window  
root = tk.Tk()  
root.title("EAS Passphrase Generator")  
root.geometry("700x350")  # Make the window wide enough for 32 characters  
root.resizable(False, False)  
root.config(bg="#2b2b2b")  # Dark background for a modern look  

# Create and place widgets  
title_label = tk.Label(  
    root, text="Passphrase Generator", font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#2b2b2b"  
)  
title_label.pack(pady=10)  

desc_label = tk.Label(  
    root, text="Set the desired passphrase length and click 'Generate'", font=("Helvetica", 10), fg="#aaaaaa", bg="#2b2b2b"  
)  
desc_label.pack()  

output_frame = tk.Frame(root, bg="#2b2b2b")  
output_frame.pack(pady=20)  

output_label = tk.Label(output_frame, text="Your Passphrase:", font=("Helvetica", 10), fg="#ffffff", bg="#2b2b2b")  
output_label.grid(row=0, column=0, sticky="w")  

output_entry = tk.Entry(output_frame, font=("Courier", 12), width=50, fg="#2b2b2b", bg="#ffffff", borderwidth=2)  
output_entry.grid(row=0, column=1, padx=10)  

# Dropdown for passphrase length  
length_frame = tk.Frame(root, bg="#2b2b2b")  
length_frame.pack(pady=10)  

length_label = tk.Label(length_frame, text="Select Length:", font=("Helvetica", 10), fg="#ffffff", bg="#2b2b2b")  
length_label.grid(row=0, column=0, padx=5)  

# Ensure combobox values are strings  
length_selector = ttk.Combobox(length_frame, values=["16", "20", "24", "32"], font=("Helvetica", 10), state="readonly", width=5)  
length_selector.grid(row=0, column=1, padx=5)  
length_selector.set("16")  # Default value  

generate_button = tk.Button(  
    root, text="Generate", command=generate_passphrase, font=("Helvetica", 12), bg="#4caf50", fg="#ffffff", relief="flat"  
)  
generate_button.pack(pady=10)  

copy_button = tk.Button(  
    root, text="Copy to Clipboard", command=copy_to_clipboard, font=("Helvetica", 12), bg="#2196f3", fg="#ffffff", relief="flat"  
)  
copy_button.pack()  

# Temporary "Copied to Clipboard" notification  
copied_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#2b2b2b")  
copied_label.pack()  

footer_label = tk.Label(  
    root, text="©2025 EAS Passphrase Generator", font=("Helvetica", 8), fg="#555555", bg="#2b2b2b"  
)  
footer_label.pack(side="bottom", pady=10)  

# Run the application  
root.mainloop()  
word_count = len(WORD_LIST)  
print(f"Total number of words in WORD_LIST: {word_count}")