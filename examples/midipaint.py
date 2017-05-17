import pygame
from threading import Thread

pygame.init()

SIZE_FACTOR = 4
size = 2 * [127 * SIZE_FACTOR] # = [508, 508]
screen = pygame.display.set_mode(size)

KNOBS = {}
COLOR = [255,255,255]
POS = [0,0]
SIZE = 6

def color(idx, value):
    COLOR[idx] = value

def pos(idx, value):
    POS[idx] = value

def size(value):
    global SIZE
    SIZE = value

# crée un itérateur sur les fonctions
# à chaque fois que l'utilisateur touche un nouveau bouton,
# l'id du bouton sera associé à une nouvelle fonction
functions = iter([
    lambda x: pos(0, x*SIZE_FACTOR),
    lambda y: pos(1, y*SIZE_FACTOR),
    lambda d: size(d*2),
    lambda r: color(0, r*2),
    lambda g: color(1, g*2),
    lambda b: color(2, b*2)
])

# une fois tous les boutons assignés, la fonction default est appelée
default = lambda x: print("Received value: %d" % x)

while True:
    try:
        id, value = input().split(":")
    except ValueError: continue # l'input n'a pas le format id:value, pas grave on le traite pas
    except EOFError: break # fin du fichier -> il n'y aura plus d'input

    if id in KNOBS:
        f = KNOBS[id]
    else:
        f = KNOBS[id] = next(functions, default)

    f(int(value))

    pygame.draw.circle(screen, COLOR, POS, SIZE)
    pygame.display.flip()
