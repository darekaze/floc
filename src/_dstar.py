from math import inf, pow


def dstar(v, star=2):
    numerator = pow(v['Ncf'], star)
    denominator = float(v['Nuf'] + v['Ncs'])
    try:
        score = numerator / denominator
    except ZeroDivisionError:
        score = inf
    return score
