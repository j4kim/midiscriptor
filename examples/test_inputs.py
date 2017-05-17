import time,sys

# python test_inputs.py | python background.py

for i in range(127,0,-10):
    time.sleep(0.1)
    print("a:{}".format(i))
    sys.stdout.flush()

for i in range(0,127,10):
    time.sleep(0.1)
    print("b:{}".format(i))
    sys.stdout.flush()

for i in range(0,127,10):
    time.sleep(0.1)
    print("c:{}".format(i))
    sys.stdout.flush()

for i in range(127,0,-10):
    time.sleep(0.1)
    print("d:{}".format(i))
    sys.stdout.flush()