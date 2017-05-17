knobs = {}

chars = "*+#.-_|/0123456789"

char_generator = iter(chars)

while True:
    try:
        id, value = input().split(":")
    except ValueError:
        continue
    
    if id.split(";")[0] == "8":
        # on ne traite pas les signaux de relachements,
        # qui ont toujours une valeurs à 127
        continue
    
    if id in knobs:
        char = knobs[id]
    else:
        char = knobs[id] = next(char_generator, "^")
        
    print(char * int(value))
