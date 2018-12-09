def barinel(v):
    Ncs = float(v['Ncs'])
    Ncf = float(v['Ncf'])
    try:
        score = float(1 - (Ncs / (Ncs + Ncf)))
    except ZeroDivisionError:
        score = 0
    return score
