import sys
import argparse
import json
import tarantula as ttl
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
                'n_cover': [0, 0],
                'n_uncover': [0, 0],
                'coverage': [],
                # 'fl': {}
                'suspiciousness': 0
            })
    return i + 1


def makeCovMatrix(res, totalLine, passed, failed, totalPF):
    for t in testCovLines.values():
        r = t['result']
        for i in range(totalLine):
            stat = 'O'
            if i+1 in t['coverlines']:
                if r == 0:
                    stat = 'P'
                    passed[i] += 1
                else:
                    stat = 'F'
                    failed[i] += 1
                                
                res[i]['n_cover'][r] += 1
            else:
                res[i]['n_uncover'][r] += 1
            res[i]['coverage'].append(stat)
    #Tarantula
    for i in range(totalLine):
        if passed[i] > 0 or failed[i] > 0:
            lineSuspiciousness = ttl.suspiciousness(passed[i], failed[i], totalPF[0], totalPF[1])
            res[i]['suspiciousness'] = lineSuspiciousness


def outputCovMatrix(res, pf):
    resJson = {
        'total_passes': pf[0],
        'total_fails': pf[1],
        'coverage_matrix': res
    }
    with open('result.json', 'w') as f:
        json.dump(resJson, f, indent=2)


def start(modName, funcName, testcases):
    global current
    res = []
    totalLine = initCovMatrix(res, modName)
    #For Tarantula
    passed = [0  for i in range(totalLine)]
    failed = [0  for i in range(totalLine)]
    
    module = __import__('tmods.{}'.format(modName))
    func = getattr(getattr(module, modName), funcName)
    try:
        with open(testcases) as json_data:
            tests = json.load(json_data)
    except FileNotFoundError:
        print(
            'Error: Could not find {}.json in /testCases'.format(testcases),
            '\n..Abort..'
        )
        sys.exit(2)

    totalPF = [0, 0]
    for test in tests:
        current = tuple(test['input'])
        if current not in testCovLines:
            testCovLines[current] = {'coverlines': set()}

            sys.settrace(traceLine)
            output = func(test['input'])
            sys.settrace(None)

            temp = int(not(output == test['result']))
            totalPF[temp] += 1
            testCovLines[current]['result'] = temp
    makeCovMatrix(res, totalLine, passed, failed, totalPF)
    outputCovMatrix(res, totalPF)
    print('Done! The Coverage Matrix Data is outputted to result.json')


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