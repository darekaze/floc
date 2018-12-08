import sys
import argparse
import json

current = []
testCovLines = {}


def traceLine(frame, event, arg):
    if event == 'line':
        lineno = frame.f_lineno
        testCovLines[current]['coverlines'].add(lineno)
    return traceLine


def initCovMatrix(res, modName):
    with open('./tmods/{}.py'.format(modName)) as f:
        for i, line in enumerate(f):
            res.append({
                '_line_no': i+1,
                'code': line,
                'coverage': [],
                'fl': {}
            })
    return i + 1


def makeCovMatrix(res, totalLine):
    for t in testCovLines.values():
        for i in range(totalLine):
            stat = 'O'
            if i+1 in t['coverlines']:
                if t['result'] == 0:
                    stat = 'P'
                else:
                    stat = 'F'
            res[i]['coverage'].append(stat)


def start(modName, funcName, testcases):
    global current
    module = __import__('tmods.{}'.format(modName))
    func = getattr(getattr(module, modName), funcName)
    with open(testcases) as json_data:
        tests = json.load(json_data)

    for test in tests:
        current = tuple(test['input'])
        testCovLines[current] = {'coverlines': set()}

        sys.settrace(traceLine)
        output = func(test['input'])
        sys.settrace(None)

        testCovLines[current]['result'] = int(not(output == test['result']))

    res = []
    totalLine = initCovMatrix(res, modName)
    makeCovMatrix(res, totalLine)
    with open('result.json', 'w') as f:
        json.dump(res, f, indent=2)


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
