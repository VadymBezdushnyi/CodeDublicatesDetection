from parse_ast import *
import numpy as np


def get_name(parser, root):
    if isinstance(root, TerminalNodeImpl):
        return root.getText()
    else:
        return parser.ruleNames[root.getRuleIndex()]


def get_size(root):
    size = 1
    for i in range(root.getChildCount()):
        child = root.getChild(i)
        size += get_size(child)
    return size


memory = {}


def get_min_diff(matrix):
    diff = 0
    matrix = np.array(matrix)
    rows = list(range(matrix.shape[0]))
    cols = list(range(matrix.shape[1]))
    while len(matrix) > 0 and len(matrix[0]) > 0:
        row, col = np.unravel_index(matrix.argmin(), matrix.shape)
        diff += matrix[row, col]
        matrix = np.delete(matrix, row, axis=0)
        matrix = np.delete(matrix, col, axis=1)
        cols = np.delete(cols, col, axis=0)
        rows = np.delete(rows, row, axis=0)
    return diff, rows, cols


def tree_diff(parser_left, parser_right, root_left, root_right):
    if (root_left, root_right) in memory:
        return memory[(root_left, root_right)]
    if get_name(parser_left, root_left) != get_name(parser_right, root_right):
        memory[(root_left, root_right)] = get_size(root_left) + get_size(root_right)
        return memory[(root_left, root_right)]

    if root_left.getChildCount() == 1 and root_right.getChildCount() == 1:
        memory[(root_left, root_right)] = tree_diff(parser_left, parser_right, root_left.getChild(0), root_right.getChild(0))
        return memory[(root_left, root_right)]

    matrix = np.zeros((root_left.getChildCount(), root_right.getChildCount()))
    for i in range(root_left.getChildCount()):
        for j in range(root_right.getChildCount()):
            matrix[i, j] = tree_diff(parser_left, parser_right, root_left.getChild(i), root_right.getChild(j))
    diff, rows, cols = get_min_diff(matrix)
    memory[(root_left, root_right)] = diff + \
                                      sum([get_size(root_left.getChild(i)) for i in rows])+\
                                      sum([get_size(root_right.getChild(i)) for i in cols])
    return memory[(root_left, root_right)]
