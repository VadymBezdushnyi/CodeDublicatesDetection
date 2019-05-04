from parse_ast import *
from tree_diff import *
import timeit

def get_diff(code1, code2):
    parser, root = parse(code1)
    parser1, root1 = parse(code2)
    return tree_diff(parser, parser1, root, root1) / (get_size(root) + get_size(root1))


def work():
    code = open('tests/f3.cpp').read()
    code1 = open('tests/f4.cpp').read()
    print(get_diff(code, code1))


if __name__ == '__main__':
    print(timeit.timeit(work, number=1))