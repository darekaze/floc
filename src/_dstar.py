import math


def dstar(v):
    numerator = float(v['Ncf'] * v['Ncf'])
    denominator = float(v['Nuf'] + v['Ncs'])
    try:
        score = numerator / denominator
    except ZeroDivisionError:
        score = math.inf
    return score
