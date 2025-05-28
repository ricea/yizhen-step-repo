import sys


def main():
    dist_num = None
    calc = 0

    for l in sys.stdin:
        line = l.strip()
        print('Line', line, type(line))
        if line == 'end':
            break
        try:
            n = int(line)
            if calc == 0:
                dist_num = n
                calc += 1
            elif dist_num == n:
                calc += 1
            else:
                calc -= 1

        except TypeError as e:
            print("{} is not an Integer, error : {}".format(line, e))

    print('majority number: {}'.format(dist_num))


main()
