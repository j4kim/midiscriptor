knobs = {}

chars = "*+#.-_|/0123456789"

def next_char():
    global chars
    n=0
    while True:
        yield chars[n]
        n += 1
        n %= len(chars)

char_generator = next_char()    

while True:
    try:
        id, value = input().split(":")
    except ValueError:
        continue
    
    if id.split(";")[0] == "8":
        # on ne traite pas les signaux de relachements,
        # qui ont toujours une valeurs ä 127
        continue
    
    if id in knobs:
        print(knobs[id] * int(value))
    else:
        knobs[id] = next(char_generator)
