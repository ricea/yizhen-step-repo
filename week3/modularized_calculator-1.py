#! /usr/bin/python3
import traceback
import sys

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


def read_plus(index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_multiply(index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def read_divide(index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def read_left_bracket(index):
    token = {'type': 'LEFT'}
    return token, index + 1


def read_right_bracket(index):
    token = {'type': 'RIGHT'}
    return token, index + 1


def read_abs(index):
    token = {'type': 'ABS'}
    return token, index + 3


def read_int(index):
    token = {'type': 'INT'}
    return token, index + 3


def read_round(index):
    token = {'type': 'ROUND'}
    return token, index + 5


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(index)
        elif line[index] == '-':
            (token, index) = read_minus(index)
        elif line[index] == '*':
            (token, index) = read_multiply(index)
        elif line[index] == '/':
            (token, index) = read_divide(index)
        elif line[index] == '(':
            (token, index) = read_left_bracket(index)
        elif line[index] == ')':
            (token, index) = read_right_bracket(index)
        elif line[index] == 'a':
            (token, index) = read_abs(index)
        elif line[index] == 'i':
            (token, index) = read_int(index)
        elif line[index] == 'r':
            (token, index) = read_round(index)
        else:
            raise ValueError(f'Invalid character found: {line[index]}')

        tokens.append(token)

    return tokens


# ------------------finish of initial process to convert string to numbers and operators------------------

# ------------------chunck and construct------------------

def chunkify_bracket(tokens: list, idx=0, fn=None) -> tuple[dict, int]:
    '''
    input: plain tokens list
    returns a nested dict with corresponding bracket structure
    call itself recursively
    '''
    chunk = {'type': 'CHUNK', 'tokens': [], 'fn': fn}

    while idx < len(tokens):
        if tokens[idx]['type'] == 'LEFT':
            operator = None
            if idx > 0 and tokens[idx-1]['type'] in ['ABS', 'INT', 'ROUND']:
                operator = chunk['tokens'].pop()['type']

            child, idx = chunkify_bracket(tokens, idx+1, operator
                                          )
            chunk['tokens'].append(child)
        elif tokens[idx]['type'] == 'RIGHT':
            return chunk, idx
        else:
            chunk['tokens'].append(tokens[idx])

        idx += 1
    return (chunk, idx)


# ------------------finish of chunck and construct------------------


def handle_add_substract(chunk: dict, idx=0) -> int:
    '''
    input: parent chunk
    returns the result
    call unpack and handle_multiply_divide
    recursively calculate the parent chunk
    '''
    tokens = chunk['tokens']
    res = 0
    prev_operator = 'PLUS'
    while idx < len(tokens):
        if tokens[idx]['type'] in ['PLUS', 'MINUS']:
            prev_operator = tokens[idx]['type']
            idx += 1
        elif tokens[idx]['type'] in ['NUMBER', 'CHUNK']:
            right = 0
            if idx == len(tokens)-1 or (idx < len(tokens)-1 and tokens[idx+1]['type']not in ['MULTIPLY', 'DIVIDE']):
                right = unpack(tokens[idx])
                idx += 1

            elif tokens[idx+1]['type'] in ['MULTIPLY', 'DIVIDE']:
                right, idx = handle_multiply_divide(chunk, idx)
            res += right if prev_operator == 'PLUS' else -right

    return res


def handle_multiply_divide(chunk: dict, idx: int) -> tuple[int, int]:
    '''
    input: the same chunk as handle_add_substract 
    it calculates a chain of '*' and '/' until encounters '+' or '-'
    returns result and idx of stop position
    '''
    tokens = chunk['tokens']
    res = 1
    prev_operator = 'MULTIPLY'

    while idx < len(tokens):
        if tokens[idx]['type'] in ['PLUS', 'MINUS']:
            break
        if tokens[idx]['type'] in ['MULTIPLY', 'DIVIDE']:
            prev_operator = tokens[idx]['type']

        elif tokens[idx]['type'] in ['NUMBER', 'CHUNK']:
            value = unpack(tokens[idx])
            if prev_operator == 'DIVIDE' and value == 0:
                raise ZeroDivisionError(
                    "Division by zero is not allowed.\n")
            res = res * value if prev_operator == 'MULTIPLY' else res / value
        idx += 1

    return (res, idx)


def handle_abs(num):
    return abs(num)


def handle_int(num):
    return int(num)


def handle_round(num):
    return round(num)


def unpack(chunk):
    '''
    input: chunk
    as an entry opint of each chun, it calls handle_add_substract and gets the result in 'res'
    then checks 'abs', 'int', round' and calculates them
    '''
    if chunk['type'] == 'NUMBER':
        return chunk['number']

    res = handle_add_substract(chunk)
    if chunk['fn'] in ['ABS', 'INT', 'ROUND']:
        if chunk['fn'] == 'ABS':
            res = handle_abs(res)
        elif chunk['fn'] == 'INT':
            res = handle_int(res)

        elif chunk['fn'] == 'ROUND':
            res = handle_round(res)

    return res


def evaluate(tokens):
    '''
    input: plain tokens list
    call chunkify_bracket to convert tokens into chunk, then unpack the chunk to get result
    '''
    chunk, _ = chunkify_bracket(tokens)
    res = unpack(chunk)
    return res


def test(line):
    if line == '':
        expected_answer = 0
    else:
        try:
            expected_answer = eval(line)
        except ZeroDivisionError:
            print(
                f"INFO! Cannot test '{line}' because eval() causes ZeroDivisionError.")
            traceback.print_exc()
            return
        except SyntaxError:
            print(
                f"INFO! Cannot test '{line}' because eval() causes SyntaxError.")
            traceback.print_exc()
            return

    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" %
              (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    print("\n--- Test basic operation ---")
    test('')
    test('0')
    test('-1')
    test('1+2')
    test('4-9')
    test('2*1.9')
    test('4/3')
    test('1.0+2.1-3')
    test('0.9*2.1*3')
    print('\n--- Test combinations of operation ---')
    test('1.4+2*3')
    test('10-8/2')
    test('2*3.5*9+4*5')
    test('1+2*3/6-4/2*5')
    print('\n--- Test parentheses ---')
    test('(4)')
    test('(-2)')
    test('(1-2)/1')
    test('10/(2+3)')
    test('(1+2)*3')
    test('(1+2)*3-(1-3)/2')
    test('10-(4-2)')
    test('2*(3+4)/5')
    test('((1+1)*2)*3')
    test('((3*1)*8)*3')
    print('\n--- Test advanced operations ---')
    print('\n--- Test abs ---')
    test('abs(3)')
    test('abs(-9)')
    test('abs(-3.14)')
    test('abs(0)')
    test('abs(4-91)')
    test('abs(1.5*11)')
    test('abs(-1.5)-4')
    print('\n--- Test int ---')
    test('int(2.3)')
    test('int(-10.2)')
    test('int(2/3)')
    test('int(-7/2)')
    test('-10+int(2.5)')
    test('int(4.7)/2')
    print('\n--- Test round ---')
    test('round(4.7)')
    test('round(4.23)')
    test('round(-9.3)')
    test('round(-9.5)')
    test('round(3/4)')
    test('round(-8.9/4)')
    test('10+round(4.23)')
    test('round(7.66)/4')
    print('\n--- Test combinations of advanced operations ---')

    test('abs(int(-9.9))')
    test('int(abs(-9.9))')
    test('round(abs(-8.7))')
    test('abs(round(-8.7))')
    test('int(round(10.6)/2)')
    test('abs(5-round(10.8))')
    test('(round(2.6)+int(1.1))*abs(-2)')
    test('abs(round(int(5-10.8)))')

    print('==== Test finished! ====\n')


run_test()

while True:
    '''
    accept one line input each time, tokenlize the line and calculate answer
    '''
    print('> ', end="")
    line = input().strip()
    if not line:
        print("Please enter an expression.")
        continue
    line = line.replace(' ', '')
    try:
        tokens = tokenize(line)
        answer = evaluate(tokens)
        print("answer = %f\n" % answer)
    except Exception as e:
        traceback.print_exc()
