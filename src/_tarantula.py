def tarantula(v):
    try:
        numerator = float(v['Ncf'] / v['Nf'])
        denominator = float(v['Ncs'] / v['Ns']) + float(numerator)
        score = numerator / denominator
    except ZeroDivisionError:
        score = 0
    return score
