import sys
import argparse
import json
from tabulate import tabulate

def writeJson(results):
    with open('resultCrosstab.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Successfully written the crosstab debugger details\n")

def printTable(results):
    print('line no\tsuspiciousness\trank')
    for line in results['coverage_matrix']:
        print('%d\t%f\t%d' % (line['_line_no'],line['suspiciousness'],line['rank']))

def start():
    rank = []
    try:
        resultsfile = 'result.json'
        with open(resultsfile) as json_data:
            results = json.load(json_data)
    except FileNotFoundError:
        print(
            'Error: Could not find {}.json in src'.format(resultsfile),
            '\n..Abort..'
        )
        sys.exit(2)

    for line in results['coverage_matrix']:
        # print(line)
        N = results['total_passes'] + results['total_fails'] # 30
        Nf = results['total_fails']
        Ns = results['total_passes']
        Nc = sum(line['n_cover']) 
        Ncf = line['n_cover'][1]# covered and failed
        Ncs = line['n_cover'][0]# covered and successful
        Nu = sum(line['n_uncover'])
        Nuf = line['n_uncover'][1]# uncovered and failed
        Nus = line['n_uncover'][0]# uncovered and successful

        Ecf = Nc*Nf/N
        Ecs = Nc*Ns/N
        Euf = Nu*Nf/N
        Eus = Nu*Ns/N

        # calculate the chi-square
        if Nc==0 or Nu==0:
            # complete independance from test result and coverage
            X_square = 0
        else:
            X_square = ((Ncf-Ecf)**2)/Ecf + ((Ncs-Ecs)**2)/Ecs + ((Nuf-Euf)**2)/Euf + ((Nus-Eus)**2)/Eus

        #calculate contingency coefficient
        M = X_square/N

        # calculate phi
        if Ncs == 0 and Ncf == 0:
            phi = 1 # coverage complete independance with result
        elif Ncs == 0 and Ncf != 0:
            phi = 2
        elif Ncs != 0 and Ncf == 0:
            phi = 0
        else:
            phi = (Ncf*Ns)/(Nf*Ncs)

        # calculate zeta, the suspiciousness of a statement
        Z = M if phi>1 else -M if phi<1 else 0

        line['suspiciousness'] = Z
        rank.append(Z)
    rank.sort(reverse=True)
    for line in results['coverage_matrix']:
        if line['suspiciousness'] == 0:
            line['rank'] = len(rank)
        else:
            line['rank'] = rank.index(line['suspiciousness']) + 1
    writeJson(results)
    printTable(results)

if __name__ == '__main__':
    start()
