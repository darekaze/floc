def crosstab(v):
    Ecf = v['Nc']*v['Nf'] / v['N']
    Ecs = v['Nc']*v['Ns'] / v['N']
    Euf = v['Nu']*v['Nf'] / v['N']
    Eus = v['Nu']*v['Ns'] / v['N']

    # calculate the chi-square
    if v['Nc'] == 0 or v['Nu'] == 0:
        # complete independence from test result and coverage
        X_square = 0
    else:
        X_square = ((v['Ncf']-Ecf)**2)/Ecf
        + ((v['Ncs']-Ecs)**2)/Ecs
        + ((v['Nuf']-Euf)**2)/Euf
        + ((v['Nus']-Eus)**2)/Eus

    # calculate contingency coefficient
    M = X_square/v['N']
    # print(Ncs, Ncf)

    # calculate phi
    if v['Ncs'] == 0 and v['Ncf'] == 0:
        phi = 1     # coverage complete independence with result
    elif v['Ncs'] == 0 and v['Ncf'] != 0:
        phi = 2
    elif v['Ncs'] != 0 and v['Ncf'] == 0:
        phi = 0
    else:
        phi = (v['Ncf'] * v['Ns']) / (v['Nf'] * v['Ncs'])

    # calculate zeta, the suspiciousness of a statement
    Z = M if phi > 1 else -M if phi < 1 else 0

    return Z
