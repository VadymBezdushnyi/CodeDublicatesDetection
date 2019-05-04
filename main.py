import sys
from antlr4 import *
from antlr4.InputStream import InputStream

from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser

def printAst(parser:Python3Parser, node:RuleContext, indent:int = 0):
    isSimplePath = node.getChildCount() == 1 and node.getChild(0).getChildCount() != 1
    if not isSimplePath:
        for _ in range(indent):
            print(" ", end = "")
        print(parser.ruleNames[node.getRuleIndex()])

    for i in range(node.getChildCount()):
        child = node.getChild(i)
        if isinstance(child, RuleContext):
            printAst(parser, child, indent + (0 if isSimplePath else 1))



if __name__ == '__main__':
    s = open("test_example.py").read()
    lexer = Python3Lexer(InputStream(s))
    # all_tokens = lexer.getAllTokens()
    # print([i.text for i in all_tokens])

    token_stream = CommonTokenStream(lexer)
    parser = Python3Parser(token_stream)
    # print([i.text for i in lexer.getAllTokens()])
    # tree = parser.expr().toStringTree()
    # print(tree)
    printAst(parser, parser.file_input())



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