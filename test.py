import sys

print("a")

try:
    raise Exception()
except:
    sys.exit()

print("b")