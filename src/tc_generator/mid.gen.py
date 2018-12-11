import os
import argparse
import random
import json
from statistics import median


def generate(cases, r, fileName='mid', dir='testCases'):
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open('{}/{}.json'.format(dir, fileName), 'w') as f:
        outputs = []
        for _ in range(cases):
            li = {'input': []}
            for _ in range(3):
                li['input'].append(random.randint(0, r))
            li['result'] = median(li['input'])
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
        '-r', '--range',
        default=20,
        type=int,
        help='The range for the list (e.g. 0~1000, default=1000)'
    )

    args = parser.parse_args()
    generate(args.tc, args.range)
