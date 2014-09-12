# -*- coding: utf-8 -*-

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

    def t_comment(self, t):
        r'\#[^\\\n]*'

    def t_error(self, t):
        raise Exception("illegal character '%s'=%02XH: line = %d, column = %d" % (t.value[0], ord(t.value[0]), t.lineno, t.lexpos - self.linepos))

    def p_error(self, p):
        raise Exception("syntax error '%s': line = %d, column = %d" % (p, p.lineno(0), p.lexpos(0) - linepos))

    def p_script_rules(self, p):
        '''script : rules'''
        p[0] = p[1]

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
        p[0] = {}
        p[0]['key'] = p[1]
        p[0]['val'] = p[3]

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
            p[0] = p[2]

    def __init__(self):
        self.lexer = lex.lex(module=self, reflags=re.UNICODE)

    def parse(self, text):
        self.lexer.input(text)
        self.linepos = 0
        p = yacc.yacc(module=self)
        return p.parse(lexer=self.lexer)
