def op2(v):
    Ncf = float(v['Ncf'])
    Ncs = float(v['Ncs'])
    Ns = float(v['Ns'])
    return Ncf - (Ncs / (Ns + 1))
