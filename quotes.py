import random

quotes = [
    "🎵 Music gives a soul to the universe, wings to the mind, flight to the imagination and life to everything. – Plato",
    "🎶 Where words fail, music speaks. – Hans Christian Andersen",
    "🎧 One good thing about music, when it hits you, you feel no pain. – Bob Marley",
    "🎼 Music can change the world because it can change people. – Bono",
    "🎹 Music is the shorthand of emotion. – Leo Tolstoy",
    "🎤 Music is life itself. – Louis Armstrong",
    "🎸 Without music, life would be a mistake. – Friedrich Nietzsche"
]

def get_random_quote():
    return random.choice(quotes)
