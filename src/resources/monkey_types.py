import random

PRIMATE_TYPES = [
    # General primate types
    "Ape", "Baboon", "Bonobo", "Capuchin", "Chimpanzee", "Gibbon",
    "Gorilla", "Great Ape", "Howler", "Lemur", "Macaque", "Mandrill",
    "Marmoset", "Monkey", "Orangutan", "Primate", "Silverback", "Simian",
    "Spider Monkey", "Tamarin",

    # Fun names
    "Banana Baron", "Ooga Booga King", "Certified Monke", "Chaos Chimp",
    "Vine Vandal", "Lord of the Swing", "The Banana Whisperer", "Jungle Jester",
    "Banana Bandit", "Canopy King", "Fruit Fiend", "Jungle VIP",
    "Liana Swinger", "Tree Dweller", "The Branch Manager", "Sir Ooks-a-Lot",
    "Primate Punisher", "Simian Savage", "Banana Brawler", "Coconut Cannoneer",
    "Mango Maniac", "Liana Lunatic", "Tree-Top Terror", "The Fuzzy Fury",
    "Grand Poobah of the Jungle", "Agent OOK", "Professor Primate",

    # Old School RuneScape (OSRS) monkeys
    "Awowogei", "Demonic Gorilla", "Karamjan Monkey", "Kruk",
    "Maniacal Monkey", "Monkey Archer", "Monkey Guard", "Monkey Zombie",
    "Tortured Gorilla",
]

def get_random_monkey_type() -> str:
    """Returns a random primate type from the list (capitalized)."""
    return random.choice(PRIMATE_TYPES)

def get_plural_monkey_type(monkey_type: str) -> str:
    """Returns the plural form of a given monkey type, with basic rules."""
    lower_type = monkey_type.lower()
    if lower_type.endswith('s'):
        return monkey_type
    if lower_type.endswith('y') and lower_type[-2] not in 'aeiou':
        return monkey_type[:-1] + 'ies'
    return monkey_type + 's'
