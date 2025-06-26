import random

PRIMATE_TYPES = [
    "Ape", "Monkey", "Gorilla", "Chimpanzee", "Orangutan", "Baboon",
    "Simian", "Primate", "Bonobo", "Gibbon", "Macaque", "Mandrill",
    "Howler", "Spider Monkey", "Capuchin", "Lemur", "Tamarin",
    "Marmoset", "Silverback", "Jungle VIP", "Tree Dweller", "Fruit Fiend",
    "Canopy King", "Liana Swinger", "Banana Bandit", "Great Ape"
]

def get_random_monkey_type() -> str:
    """Returns a random primate type from the list (capitalized)."""
    return random.choice(PRIMATE_TYPES)

def get_plural_monkey_type(monkey_type: str) -> str:
    """Returns the plural form of a given monkey type."""
    return monkey_type + 's' if not monkey_type.lower().endswith('s') else monkey_type
