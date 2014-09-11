import ply.lex as lex
import ply.yacc as yacc
import re

class Parser:
    tokens = ("SYMBOL", "STRING", "LBRACE", "RBRACE", "ASSIGN")

    t_ignore    = ' \t\r'
    t_SYMBOL    = r'[a-zA-Z0-9_\.]+'
    t_STRING    = r'\"([^\\\n]|(\\.))*?\"'
    t_LBRACE    = '{'
    t_RBRACE    = '}'
    t_ASSIGN    = '='

    linepos = 0

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.linepos = t.lexpos

    def t_error(self, t):
        raise Exception("illegal character '%s'=%02XH: line = %d, column = %d" % (t.value[0], ord(t.value[0]), t.lineno, t.lexpos - self.linepos))

    def p_error(self, p):
        raise Exception("syntax error '%s': line = %d, column = %d" % (p, p.lineno(0), p.lexpos(0) - linepos))

    def p_script_rules(self, p):
        '''script : rules'''
        p[0] = MultiRules(p[1])

    def p_rules_rule(self, p):
        '''rules : rules rule
                 | '''
        if len(p) == 3:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = []

    def p_rule(self, p):
        '''rule : symbol ASSIGN value'''
        p[0] = SingleRule(p[1], p[3])

    def p_symbol(self, p):
        '''symbol : SYMBOL'''
        p[0] = p[1]

    def p_value(self, p):
        '''value : SYMBOL
                 | STRING
                 | LBRACE rules RBRACE'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = MultiRules(p[2], brace=True)

    def __init__(self):
        self.lexer = lex.lex(module=self, reflags=re.UNICODE)

    def settext(self, text):
        self.lexer.input(text)
        self.linepos = 0

    def token(self):
        return self.lexer.token()

    def parse(self, text):
        self.settext(text)
        p = yacc.yacc(module=self)
        return p.parse(lexer=self.lexer)

class SingleRule:
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def format(self, indent):
        s = ""
        for i in range(indent):
            s += "\t"
        s += str(self.key)
        s += " = "
        if type(self.val) is MultiRules:
            s += self.val.format(indent)
        else:
            s += str(self.val)
            s += "\n"
        return s

    def __str__(self):
        return self.format(0)

    def __repr__(self):
        return self.format(0)

class MultiRules:
    def __init__(self, rules=[], brace=False):
        self.rules = rules
        self.brace = brace

    def format(self, indent):
        s = ""
        if self.brace:
            s += "{\n"
            for r in self.rules:
                s += r.format(indent + 1)
            for i in range(indent):
                s += "\t"
            s += "}\n"
        else:
            for r in self.rules:
                s += r.format(indent)
        return s

    def __str__(self):
        return self.format(0)

    def __repr__(self):
        return self.format(0)

    def append(self, r):
        if type(r) is not SingleRule:
            raise Exception("invalid type append")
        self.rules.append(r)
