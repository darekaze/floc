import sys
import argparse
import json

current = []
testCovLines, lineCov = {}, {}


def traceLine(frame, event, arg):
    if event == 'line':
        lineno = frame.f_lineno
        testCovLines[current].add(lineno)
        if lineno in list(lineCov.keys()):
            lineCov[lineno].add(str(current))
        else:
            lineCov[lineno] = set([str(current)])
    return traceLine


def makeResult(res, a, b):
    print(current, a, b)
    obj = {
        'test': str(current),
        'coverlines': list(testCovLines[current]),
        'result': int(not(a == b))
    }
    res.append(obj)


def start(modName, funcName, testcases):
    global current
    module = __import__('tmods.{}'.format(modName))
    func = getattr(getattr(module, modName), funcName)
    with open(testcases) as json_data:
        tests = json.load(json_data)
    res = []

    for test in tests:
        current = tuple(test['input'][:])
        testCovLines[current] = set()

        sys.settrace(traceLine)
        output = func(test['input'])
        sys.settrace(None)

        makeResult(res, output, test['result'])

    print(res)

    with open('result.json', 'w') as f:
        json.dump(res, f, indent=2)
    # with open('AA.json', 'w') as f:
    #     json.dump(testCovLines, f, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate coverage matrix from testcase json file',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'module',
        type=str,
        help='Name of the test module file (without .py) in /tmods'
    )
    parser.add_argument(
        'func',
        type=str,
        help='Name of the entry function'
    )
    parser.add_argument(
        'src',
        type=str,
        help='Name of the testcase (.json) in /testCases'
    )

    args = parser.parse_args()
    start(
        args.module,
        args.func,
        '../testCases/{}'.format(args.src)
    )
