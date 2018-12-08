import random
import os
import argparse
import json


def generate(cases, num, r, dir='testCases'):
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open('{}/sorting.json'.format(dir), 'w') as f:
        outputs = []
        for _ in range(cases):
            li = []
            for _ in range(num):
                li.append(random.randint(0, r + 1))
            outputs.append(li)
        json.dump(outputs, f)
    print('Done!\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Random test case generator for sorting algorithms',
    )
    parser.add_argument(
        '-c', '--tc',
        default=30,
        type=int,
        help='Number of testcases'
    )
    parser.add_argument(
        '-n', '--el',
        default=8,
        type=int,
        help='Number of element inside each list'
    )
    parser.add_argument(
        '-r', '--range',
        default=1000,
        type=int,
        help='The range for the list (e.g. 0~1000, default=1000)'
    )

    args = parser.parse_args()
    generate(args.tc, args.el, args.range)
