import math


def ochiai(v):
    numerator = float(v['Ncf'])
    denominator = math.sqrt(v['Nf'] * v['Nc'])
    try:
        score = numerator / denominator
    except ZeroDivisionError:
        score = 0
    return score
