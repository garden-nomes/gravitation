from math import sqrt

sqrts = []

def load_squares():
    for i in range(0, 2883600):
        sqrts.append(sqrt(i))

load_squares()