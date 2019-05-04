from antlr4 import Lexer, Token


class JavaScriptBaseLexer(Lexer):
    def __init__(self, input, output):
        super().__init__(input, output)
        self.scopeStrictModes = []
        self.lastToken = None
        self.useStrictDefault = True
        self.useStrictCurrent = True

    def getStrictDefault(self):
        return self.useStrictDefault

    def setUseStrictDefault(self, val):
        self.useStrictDefault = val
        self.useStrictCurrent = val

    def IsSrictMode(self):
        return self.useStrictCurrent

    def nextToken(self):
        next = super().nextToken()

        if next.channel == Token.DEFAULT_CHANNEL:
            self.lastToken = next

        return next

    def ProcessOpenBrace(self):
        self.useStrictDefault = True if len(self.scopeStrictModes) > 0 and \
                                        self.scopeStrictModes[-1] else self.useStrictDefault
        self.scopeStrictModes.append(self.useStrictCurrent)

    def ProcessCloseBrace(self):
        self.useStrictCurrent = self.scopeStrictModes.pop() if len(self.scopeStrictModes) > 0 else \
            self.useStrictDefault

    def ProcessStringLiteral(self):
        if self.lastToken == None or self.lastToken.type == 8: #JavaScriptLexer.OpenBrace
            text = self.getText()
            if text.equals("\"use strict\"") or text.equals("'use strict'"):
                if len(self.scopeStrictModes) > 0:
                    self.scopeStrictModes.pop()
                    self.useStrictCurrent = True
                self.scopeStrictModes.append(self.useStrictCurrent)