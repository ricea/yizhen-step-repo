#! /usr/bin/python3
'''
assume there's no invalid input:
    multiple operators in a row like +-, /*, unclosed round bracket, divide 0
TODO: handle divide 0
'''

# ------------------initial process to convert string to numbers and operators------------------


def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def read_left_bracket(line, index):
    token = {'type': 'LEFT'}
    return token, index + 1


def read_right_bracket(line, index):
    token = {'type': 'RIGHT'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_left_bracket(line, index)
        elif line[index] == ')':
            (token, index) = read_right_bracket(line, index)

        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)

    return tokens


# ------------------finish of initial process to convert string to numbers and operators------------------

# ------------------chunck and construct------------------

def chunkify_bracket(tokens, idx=0):
    chunk = {'type': 'CHUNK', 'tokens': []}

    while idx < len(tokens):
        if tokens[idx]['type'] == 'LEFT':
            child, idx = chunkify_bracket(tokens, idx+1)
            chunk['tokens'].append(child)
        elif tokens[idx]['type'] == 'RIGHT':
            return chunk, idx
        else:
            chunk['tokens'].append(tokens[idx])

        idx += 1
    return (chunk, idx)


def chunkify_multiply_divide(chunk, idx=0):
    '''
    check * and /, put them in chunks
    '''
    tokens = chunk['tokens']
    if tokens[0]['type'] != 'MINUS':
        chunk['tokens'].append({'type': 'PLUS'})

    while idx < len(tokens):

        if tokens[idx]['type'] in ['MULTIPLY', 'DIVIDE']:
            chunk['tokens'].pop()
            child = {'type': 'CHUNK', 'tokens': []}
            child['tokens'].append({'type': 'MULTIPLY'})
            child['tokens'].append(tokens[idx-1])

            while idx < len(tokens) and (tokens[idx]['type'] not in ['PLUS', 'MINUS']):
                child['tokens'].append(tokens[idx])
                idx += 1
            chunk['tokens'].append(child)

        else:
            chunk['tokens'].append(tokens[idx])
            idx += 1

    return chunk


# ------------------finish of chunck and construct------------------


def handle_add_substract(chunk):
    '''
    '''
    tokens = chunk['tokens']
    res = 0
    idx = 0
    while idx < len(tokens)-1:
        operator = tokens[idx]
        next = tokens[idx+1]
        next_value = 0
        if next['type'] == 'CHUNK':
            next_value = handle_multiply_divide(next)
        else:
            next_value = next['number']
        res += next_value if operator['type'] == 'PLUS' else - \
            next_value
        idx += 2
    return res


def handle_multiply_divide(chunk):
    '''
    '''
    tokens = chunk['tokens']
    res = 1
    idx = 0
    while idx < len(tokens)-1:
        operator = tokens[idx]
        next = tokens[idx+1]
        res = res * next['number'] if operator['type'] == 'MULTIPLY' else res / \
            tokens[idx+1]['number']
        idx += 2
    return res


def evaluate(tokens):
    '''
    this function assumes there's no space or invalid inputs, and each number is coming after a operator
    '''
    chunk, _ = chunkify_bracket(tokens)
    print(chunk)
    return 0
    chunk = chunkify_multiply_divide(tokens)
    print(chunk)
    ans = handle_add_substract(chunk)
    print(ans)
    return ans


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" %
              (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    # test("1+2*3")
    test("1+2")
    test("1.0+2.1-3")
    print("==== Test finished! ====\n")


# run_test()

while True:
    '''
    accept one line input each time, tokenlize the line and calculate answer
    '''
    print('> ', end="")
    line = input().strip()
    tokens = tokenize(line)

    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
