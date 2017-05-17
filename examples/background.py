import pygame
from threading import Thread

pygame.init()
size = width, height = 508, 508
screen = pygame.display.set_mode(size)

KNOBS = {}
COLOR = [0,0,0]
QUIT = False

def bg(r=None, g=None, b=None):
    for i,v in enumerate([r,g,b]):
        if v: COLOR[i] = v*2 # v va de 0 à 127
    screen.fill(COLOR)
    pygame.display.flip()

# crée un itérateur sur les fonctions
# à chaque fois que l'utilisateur touche un nouveau bouton,
# l'id du bouton sera associé à une nouvelle fonction
# une fois tous les boutons assignés, la fonction default est appelée
functions = iter([
    lambda x: bg(r=x),
    lambda x: bg(g=x),
    lambda x: bg(b=x)
])

default = lambda x: print("No more functions to call. Received value: %d" % x)

def listen_input():
    while not QUIT:
        try:
            id, value = input().split(":")
        except ValueError: continue # l'input n'a pas le format id:value, pas grave on le traite pas
        except EOFError: break # fin du fichier -> il n'y aura plus d'input

        if id in KNOBS:
            f = KNOBS[id]
        else:
            f = KNOBS[id] = next(functions, default)

        f(int(value))

Thread(target = listen_input).start()

while not QUIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            QUIT = True

    pygame.display.flip()
