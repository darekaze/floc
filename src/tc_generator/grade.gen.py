import os
import argparse
import random
import json

grade = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']
gc = {
    'A+': 4.5,
    'A': 4.0,
    'B+': 3.5,
    'B': 3.0,
    'C+': 2.5,
    'C': 2.0,
    'D': 1.0,
    'F': 0.0
}


def generate(cases, r, fileName='sorting', dir='testCases'):
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open('{}/{}.json'.format(dir, fileName), 'w') as f:
        outputs = []
        for _ in range(cases):
            li = {'input': []}
            s = 0
            for _ in range(r):
                temp = random.choice(grade)
                li['input'].append(temp)
                s += gc[temp]
            li['result'] = float(s / len(li['input']))
            outputs.append(li)
        json.dump(outputs, f, indent=2)
    print('Done! Testcases successfully generated!\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Random test case generator for sorting algorithms',
    )
    parser.add_argument(
        '-c', '--tc',
        default=100,
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
