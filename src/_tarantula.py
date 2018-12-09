def tarantula(v):
    numerator = float(v['Ncf'] / v['Nf'])
    denominator = float(v['Ncs'] / v['Ns']) + float(numerator)
    try:
        score = numerator / denominator
    except ZeroDivisionError:
        score = 0
    return score
