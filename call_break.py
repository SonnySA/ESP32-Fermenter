import sys


def c_break():
    print("================================================")
    print("Get into 'shell' ...... Press 'C' to continue...")
    while True:
        key = sys.stdin.read(1)
        if key.upper() == "C":
            break
    print("Continuing program...")
    print("================================================")
