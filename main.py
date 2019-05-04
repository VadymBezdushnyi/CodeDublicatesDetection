import sys
from Char_based.char_based_similarity import *
from antlr4 import *
from antlr4.InputStream import InputStream

from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser

def printAst(parser:Python3Parser, node:RuleContext, indent:int = 0):
    isSimplePath = node.getChildCount() == 1
    if not isSimplePath:
        for _ in range(indent):
            print(" ", end = "")
        print(parser.ruleNames[node.getRuleIndex()])

    for i in range(node.getChildCount()):
        child = node.getChild(i)
        if isinstance(child, RuleContext):
            printAst(parser, child, indent + (0 if isSimplePath else 1))


def get_tokens(char_stream:str):
    lexer = Python3Lexer(InputStream(char_stream))
    all_tokens = lexer.getAllTokens()
    return [i.text for i in all_tokens]



if __name__ == '__main__':
    s1 = open("test_example1.py").read()
    # get_tokens(s1)

    s2 = open("test_example2.py").read()

    tokens1 = get_tokens(s1)
    tokens2 = get_tokens(s2)

    fs_char = FileSimilarity(s1, s2)
    fs_token = FileSimilarity(tokens1, tokens2)

    print(fs_char.get_similarity())
    print(fs_token.get_similarity())

    # tree = parser.expr().toStringTree()
    # print(tree)
    # printAst(parser, parser.file_input())



    # lexer = Python3Lexer(None)
    # parser.buildParseTrees = False
    # parser.memory = {}  # how to add this to generated constructor?
    #
    # line = sys.stdin.readline()
    # lineno = 1
    #
    # while line != '':
    #     line = line.strip()
    #     #print(lineno, line)
    #
    #     istream = InputStream(line + "\n")
    #     lexer = ExprLexer(istream)
    #     lexer.line = lineno
    #     lexer.column = 0
    #     token_stream = CommonTokenStream(lexer)
    #     parser.setInputStream(token_stream)
    #     parser.stat()
    #
    #     line = sys.stdin.readline()
    #     lineno += 1