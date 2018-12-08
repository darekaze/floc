import os
import argparse
import random
import json


def generate(cases, num, r, fileName='sorting', dir='testCases'):
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open('{}/{}.json'.format(dir, fileName), 'w') as f:
        outputs = []
        for _ in range(cases):
            li = {'input': []}
            for _ in range(num):
                li['input'].append(random.randint(0, r))
            li['result'] = sorted(li['input'])
            outputs.append(li)
        json.dump(outputs, f, indent=2)
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
        default=6,
        type=int,
        help='Number of element inside each list'
    )
    parser.add_argument(
        '-r', '--range',
        default=500,
        type=int,
        help='The range for the list (e.g. 0~1000, default=1000)'
    )
    parser.add_argument(
        '--name',
        default='sorting',
        type=str,
        help='The name of the output [].json file (default: sorting)'
    )

    args = parser.parse_args()
    generate(args.tc, args.el, args.range, args.name)
