def suspiciousness(passed, failed, numberPassed, numberFailed):
    numerator = failed / numberFailed
    denominator = passed / numberPassed + numerator
    return numerator / denominator

def print_message_red(message):
    print('\033[91m' + message + '\033[0m')

def print_message_green(message):
    print('\033[92m' + message + '\033[0m')

def print_message_yellow(message):
    print('\033[93m' + message + '\033[0m')
