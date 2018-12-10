import sys
import argparse
import json
from tabulate import tabulate


def print_message_red(message):
    return ('\033[91m' + str(message) + '\033[0m')


def print_message_green(message):
    return ('\033[92m' + str(message) + '\033[0m')


def print_message_yellow(message):
    return ('\033[93m' + str(message) + '\033[0m')


def writeJson(result, modName):
    with open('result{}.json'.format(modName.capitalize()), 'w') as f:
        json.dump(result, f, indent=2)
    print('Successfully written the {} debugger results'.format(modName))


def readJson():
    try:
        with open('result.json') as json_data:
            return json.load(json_data)
    except FileNotFoundError:
        print(
            'Error: Could not open JSON result from coverage'
        )
        sys.exit(2)


def printTable(cov):
    headers = ["Line Number", "Code", "Suspiciousness", "Rank"]
    table = []

    for r in cov:
        row = []
        row.append(r['_line_no'])
        row.append(r['code'])

        if r['suspiciousness'] <= 0:
            row.append(print_message_green(r['suspiciousness']))
        elif r['suspiciousness'] <= 0.5:
            row.append(print_message_yellow(r['suspiciousness']))
        else:
            row.append(print_message_red(r['suspiciousness']))
        row.append(r['rank'])
        table.append(row)
    print(tabulate(table, headers, tablefmt="grid"))


def start(tech, resultfile):
    module = __import__('_{}'.format(tech))
    getSuspiciousness = getattr(module, tech)
    results = readJson()

    rank = []
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
    for line in results['coverage_matrix']:
        if line['suspiciousness'] <= 0:
            line['rank'] = len(rank)
        else:
            line['rank'] = rank.index(line['suspiciousness']) + 1
    writeJson(results, tech)
    printTable(results['coverage_matrix'])


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
        default='result.json',
        help='Name of the coverage matrix .json file'
    )
    args = parser.parse_args()
    start(args.tech, args.src)
