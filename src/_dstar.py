def dstar(v):
    star = 8
    numerator = float(v['Ncf'] ^ star)
    denominator = float(v['Nuf'] + v['Ncs'])
    try:
        score = numerator / denominator
    except ZeroDivisionError:
        score = 0
    return score
