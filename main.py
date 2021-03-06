import sys
from Char_based.char_based_similarity import *
import ml
from scipy import spatial
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
        print(node.getSymbol().type)
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

def get_tokens(char_stream:str):
    lexer = Python3Lexer(InputStream(char_stream))
    all_tokens = lexer.getAllTokens()
    return [i.text for i in all_tokens]


def generete_embeddings(code):
    # printAst(*parse(code))
    parser_res = parse(code)
    emb = ml.run(parser_res)
    return emb



if __name__ == '__main__':

    s1 = open("test_example1.py").read()
    s2 = open("test_example2.py").read()

    tokens1 = get_tokens(s1)
    tokens2 = get_tokens(s2)

    fs_token = FileSimilarity(tokens1, tokens2)
    print("Difflib similarity: ", difflib.SequenceMatcher(None, s1, s2).ratio())
    print("Token similarity: ", fs_token.get_similarity())

    emb1 = generete_embeddings(s1)
    emb2 = generete_embeddings(s2)

    print("Root embeddings similarity: ", 1 - spatial.distance.cosine(emb1, emb2))

