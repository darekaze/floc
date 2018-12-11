def mid(li):
    x, y, z = li
    m = z
    if (y < z):
        if (x < y):
            m = y
        elif (x < z):
            m = y
    else:
        if (x > y):
            m = y
        elif (x > z):
            m = x
    return m
