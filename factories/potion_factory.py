import random

from item import HealthPotion, StatPotion, Elixir


def get(potion_type, size):
    if potion_type == 'health':
        heal_amount = {'small': 25, 'medium': 50, 'large': 100}
        potion = HealthPotion(heal_amount[size])
        potion.name = 'Health Potion'
        potion.description = f'{size.capitalize()} (Restores {potion.heal_amount} hp)'
    elif potion_type == 'elixir':
        potion = Elixir()
        potion.name = "Elixir"
        potion.description = f'Restores 50% of the user\'s missing hp'
    else:
        boost_amount = {'small': 2, 'medium': 4, 'large': 8}
        potion = StatPotion(boost_amount[size], potion_type)
        potion.name = f'{potion_type.capitalize()} potion'
        potion.description = f'{size.capitalize()} (Boosts user\'s {potion_type.capitalize()} by {potion.boost_amount} levels in battle)'
    return potion


def get_random(size):
    potion_types = ['health', 'strength', 'dexterity', 'defense', 'special_defense', 'speed', 'elixir']
    potion_type = random.choice(potion_types)
    return get(potion_type, size)
