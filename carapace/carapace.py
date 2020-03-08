import re

from carapace import (Parser, Lexer, Data, EBNF)

token_defs = [
    Lexer.token("ml_doc_comment", re.compile(r"#--[.\s]*?#--")),
    Lexer.token("sl_doc_comment", re.compile(r"#-.*")),
    Lexer.token("comment",        re.compile(r"#.*"), skip=True),
    Lexer.token("seperator",      ";"),
    Lexer.token("nl_seperator",   re.compile(r"\n\s*")),
    Lexer.token("whitespace",     re.compile("\s+"), skip=True),
    Lexer.token("lbracket",       "{"),
    Lexer.token("rbracket",       "}"),
    Lexer.token("lparen",         "("),
    Lexer.token("rparen",         ")"),
    Lexer.token("lbrace",         "["),
    Lexer.token("rbrace",         "]"),
    Lexer.token("s_flag_literal", re.compile(r"-[^\s\d]")),
    Lexer.token("l_flag_literal", re.compile(r"--[^\s\d][^\s]*")),
    Lexer.token("int_literal",    re.compile(r"-?\d+")),
    Lexer.token("dec_literal",    re.compile(r"-?\d*\.\d+")),
    Lexer.token("sci_literal",    re.compile(r"-?\d+[eE]\d+")),
    Lexer.token("bin_literal",    re.compile(r"-?0[bB][01]+")),
    Lexer.token("oct_literal",    re.compile(r"-?0[oO][01234567]+")),
    Lexer.token("hex_literal",    re.compile(r"-?0[xX][\da-fA-F]+")),
]

grammar_source = """
prog
    = { stmt }
    ;

stmt
    = expr 'seperator'
    ;

expr
    = term { term }
    ;

term
    = map_expr
    | sub_expr
    | list_expr
    | atom
    ;

map_expr
    = 'rbracket' { stmt } 'rbracket'
    ;

sub_expr
    = 'lparen' expr 'rparen'
    ;

list_expr
    = 'lbrace' { term } 'rbrace'
    ;

atom
    = string
    | number
    | 'identifier'
    | 's_flag_literal'
    | 'l_flag_literal'
    ;

string
    = 'string_literal'
    | 'string_start' expr { string_middle } 'string_end'
    ;

string_middle
    = 'string_join' expr
    ;

number
    = 'int_literal'
    | 'dec_literal'
    | 'sci_literal'
    | 'bin_literal'
    | 'oct_literal'
    | 'hex_literal'
    ;
"""

gramamr = EBNF.parse(grammar_source, "carapace.ebnf")