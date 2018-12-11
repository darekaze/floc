def gpa(grades):
    ap = a = bp = b = cp = c = d = 0

    for grade in grades:
        if grade == 'A+':
            ap += 2
        elif grade == 'A':
            a += 1
        elif grade == 'B+':
            bp += 2
        elif grade == 'B':
            b += 1
        elif grade == 'C+':
            cp += 1
        elif grade == 'C':
            c += 1
        elif grade == 'D':
            d += 1

    sum = float(ap * 4.5 + a * 4.0 + bp * 3.5 + b * 3.0
                + cp * 2.5 + c * 2.0 + d * 1.0)

    return sum / len(grades)    # gpa
