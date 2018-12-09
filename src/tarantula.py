import json
import sys
from tabulate import tabulate


def print_message_red(message):
    return ('\033[91m' + str(message) + '\033[0m')

def print_message_green(message):
    return ('\033[92m' + str(message) + '\033[0m')

def print_message_yellow(message):
    return ('\033[93m' + str(message) + '\033[0m')

def suspiciousness(passed, failed, numberPassed, numberFailed):
    numerator = failed / numberFailed
    denominator = passed / numberPassed + numerator
    return numerator / denominator
def getJson():
    try:
        with open('result.json') as json_data:
            result = json.load(json_data)
        return result
    except FileNotFoundError:
        print(
            'Error: Could not open JSON result from coverage'
        )
    sys.exit(2)
def countLines(result):
    return len(result['coverage_matrix'])

def writeJson(result):
    with open('resultTarantula.json', 'w') as f:
        json.dump(result, f, indent=2)
    print("Successfully written the tarantula debugger details")

def printJsonToTable(result,totalLine):
    headers = ["Line Number", "Code", "Suspiciousness", "Rank"]
    table = []
    for i in range(totalLine):
        row = []
        row.append(result["coverage_matrix"][i]['_line_no'])
        row.append(result["coverage_matrix"][i]['code'])
        if result["coverage_matrix"][i]['suspiciousness'] == 0:
            row.append(print_message_green(result["coverage_matrix"][i]['suspiciousness']))
        elif result["coverage_matrix"][i]['suspiciousness'] <= 0.5:
            row.append(print_message_yellow(result["coverage_matrix"][i]['suspiciousness']))
        else:
            row.append(print_message_red(result["coverage_matrix"][i]['suspiciousness']))
        row.append(result["coverage_matrix"][i]['rank'])
        table.append(row)
    print(tabulate(table, headers, tablefmt="grid"))
def start():
    result = getJson()
    totalLine = countLines(result)
    passed = [0  for i in range(totalLine)]
    failed = [0  for i in range(totalLine)]
    totalPassed = result['total_passes']
    totalFailed = result['total_fails']
    coverage_matrix = result['coverage_matrix']
    rank = []
    for item in coverage_matrix:
        for PF in item["coverage"]:
            if(PF == "P"):
                passed[item["_line_no"]-1] += 1
            if(PF == "F"):
                failed[item["_line_no"]-1] += 1

    for i in range(totalLine):
        result["coverage_matrix"][i]['suspiciousness'] = 0
        if passed[i] > 0 or failed[i] > 0:
            lineSuspiciousness = suspiciousness(passed[i], failed[i], totalPassed, totalFailed)
            rank.append(lineSuspiciousness)
            result["coverage_matrix"][i]['suspiciousness'] = lineSuspiciousness
    rank.sort(reverse=True)
    for i in range(totalLine):
        if result["coverage_matrix"][i]['suspiciousness'] == 0:
            result["coverage_matrix"][i]['rank'] = len(rank)
        else:
            result["coverage_matrix"][i]['rank'] = rank.index(result["coverage_matrix"][i]['suspiciousness']) + 1
    writeJson(result)
    printJsonToTable(result,totalLine)
if __name__ == "__main__":
    start()