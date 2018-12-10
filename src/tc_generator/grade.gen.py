import os
import argparse
import random
import json

grade = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']


def gpa(grades):
    ap = a = bp = b = cp = c = d = 0

    for grade in grades:
        if grade == 'A+':
            ap += 1
        elif grade == 'A':
            a += 1
        elif grade == 'B+':
            bp += 1
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

    return sum / len(grades)


def generate(cases, r, fileName='sorting', dir='testCases'):
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open('{}/{}.json'.format(dir, fileName), 'w') as f:
        outputs = []
        for _ in range(cases):
            li = {'input': []}
            for _ in range(r):
                li['input'].append(random.choice(grade))
            li['result'] = gpa(li['input'])
            outputs.append(li)
        json.dump(outputs, f, indent=2)
    print('Done! Testcases successfully generated!\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Random test case generator for sorting algorithms',
    )
    parser.add_argument(
        '-c', '--tc',
        default=50,
        type=int,
        help='Number of testcases'
    )
    parser.add_argument(
        '-n', '--el',
        default=5,
        type=int,
        help='Number of element inside each list'
    )
    parser.add_argument(
        '--name',
        default='grade',
        type=str,
        help='The name of the output [].json file (default: grade)'
    )

    args = parser.parse_args()
    generate(args.tc, args.el, args.name)
