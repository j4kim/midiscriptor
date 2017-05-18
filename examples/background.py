import pygame
from threading import Thread

pygame.init()

size = 2 * [508] # = [508, 508]
screen = pygame.display.set_mode(size)

KNOBS = {}
COLOR = [0,0,0]

def color(i, v):
    global COLOR
    COLOR[i] = v

# crée un itérateur sur les fonctions
# à chaque fois que l'utilisateur touche un nouveau bouton,
# l'id du bouton sera associé à une nouvelle fonction
# une fois tous les boutons assignés, la fonction default est appelée
functions = iter([
    lambda x: color(0, x*2), # x va de 0 à 127
    lambda x: color(1, x*2),
    lambda x: color(2, x*2)
])

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


    screen.fill(COLOR)
    pygame.display.flip()
