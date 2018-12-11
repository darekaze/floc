import os
import sys
import argparse
import json
from tabulate import tabulate

colorLint = {
    'tarantula': 0.5,
    'crosstab': 0.1,
    'dstar': 999999,
    'ochiai': 0.5,
    'barinel': 0.99,
}


def print_message_red(message):
    return ('\033[91m' + str(message) + '\033[0m')


def print_message_green(message):
    return ('\033[92m' + str(message) + '\033[0m')


def print_message_yellow(message):
    return ('\033[93m' + str(message) + '\033[0m')


def writeJson(result, tech, dir='testResults'):
    if not os.path.exists(dir):
        os.makedirs(dir)

    fileName = '{}/{}_{}.json'.format(dir, result['name'], tech)
    with open(fileName, 'w') as f:
        json.dump(result, f, indent=2)
    print('\n\nResult is outputted to {}'.format(fileName))


def readJson(resultfile):
    try:
        with open(resultfile) as json_data:
            return json.load(json_data)
    except FileNotFoundError:
        print(
            'Error: Could not open JSON result from coverage'
        )
        sys.exit(2)


def printTable(cov, tech):
    headers = ["Line Number", "Code", "Suspiciousness", "Rank"]
    table = []

    for r in cov:
        row = []
        row.append(r['_line_no'])
        row.append(r['code'])

        cof = colorLint[tech] if tech in colorLint else 100000
        if r['suspiciousness'] <= 0:
            row.append(print_message_green(r['suspiciousness']))
        elif r['suspiciousness'] <= cof:
            row.append(print_message_yellow(r['suspiciousness']))
        else:
            row.append(print_message_red(r['suspiciousness']))
        row.append(r['rank'])
        table.append(row)
    print(tabulate(table, headers, tablefmt="grid"))


def start(tech, resultfile):
    module = __import__('_{}'.format(tech))
    getSuspiciousness = getattr(module, tech)
    results = readJson(resultfile)

    rank = []
    rank_global = {}
    for line in results['coverage_matrix']:
        defins = {
            'N': results['total_passes'] + results['total_fails'],
            'Nf': results['total_fails'],
            'Ns': results['total_passes'],
            'Nc': sum(line['n_cover']),
            'Ncf': line['n_cover'][1],
            'Ncs': line['n_cover'][0],
            'Nu': sum(line['n_uncover']),
            'Nuf': line['n_uncover'][1],
            'Nus': line['n_uncover'][0],
        }

        sup = getSuspiciousness(defins)  # get Suspiciousness

        line['suspiciousness'] = sup
        rank.append(sup)

    rank.sort(reverse=True)
    for r in rank:
        if r in rank_global:
            rank_global[r] += 1
        else:
            rank_global[r] = 1
    for line in results['coverage_matrix']:
        rank_no = 0
        for d in rank_global:
            if d >= line['suspiciousness']:
                rank_no += rank_global[d]
        line['rank'] = rank_no
    writeJson(results, tech)
    printTable(results['coverage_matrix'], tech)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Fault localization tools with different techniques',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'tech',
        type=str,
        help='Name of debugging technique'
    )
    parser.add_argument(
        '--src',
        type=str,
        default='result_matrix.json',
        help='Name of the coverage matrix .json file'
    )
    args = parser.parse_args()
    start(args.tech, args.src)
