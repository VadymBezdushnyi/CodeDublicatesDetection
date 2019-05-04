from antlr4 import *
from antlr4.InputStream import InputStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import TerminalNodeImpl

from Python3.Python3Lexer import Python3Lexer
from Python3.Python3Parser import Python3Parser
from CPP.CPP14Lexer import CPP14Lexer
from CPP.CPP14Parser import CPP14Parser
from Java.JavaLexer import JavaLexer
from Java.JavaParser import JavaParser
from CS.CSharpLexer import CSharpLexer
from CS.CSharpParser import CSharpParser


def printAst(parser, node, indent: int = 0):
    print(" " * indent, end="")

    if isinstance(node, TerminalNodeImpl):
        print(node.getSymbol())
    else:
        print(parser.ruleNames[node.getRuleIndex()])

    for i in range(node.getChildCount()):
        child = node.getChild(i)
        if isinstance(child, RuleContext) or True:
            printAst(parser, child, indent + 1)


class MyListener(ErrorListener):
    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        raise Exception()


def parse_python(code):
    parser = Python3Parser(CommonTokenStream(Python3Lexer(InputStream(code))))
    parser._listeners = []
    parser.addErrorListener(MyListener())
    return parser, parser.file_input()


def parse_cpp(code):
    parser = CPP14Parser(CommonTokenStream(CPP14Lexer(InputStream(code))))
    parser._listeners = []
    parser.addErrorListener(MyListener())
    return parser, parser.translationunit()


def parse_java(code):
    parser = JavaParser(CommonTokenStream(JavaLexer(InputStream(code))))
    parser._listeners = []
    parser.addErrorListener(MyListener())
    return parser, parser.compilationUnit()

def parse_sharp(code):
    parser = CSharpParser(CommonTokenStream(CSharpLexer(InputStream(code))))
    parser._listeners = []
    parser.addErrorListener(MyListener())
    return parser, parser.compilation_unit()


def parse(code):
    parsers = [parse_python, parse_java, parse_sharp, parse_cpp]
    result = None
    for parser in parsers:
        try:
            result = parser(code)
            break
        except Exception as e:
            continue
    if result is None:
        raise Exception()
    return result


if __name__ == '__main__':
    code = open('tests/test.py').read()
    printAst(*parse(code))
