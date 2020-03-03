import re

from carapace import (Parser, Lexer)
from carapace.Parser import (
    rule,
    sequence,
    choice,
    many,
    non_terminal,
    terminal,
)

token_defs = [
    Lexer.token("comment", re.compile(r"#.*"), skip=True),
    Lexer.token("whitespace", re.compile(r"\s+"), skip=True),
    Lexer.token("op_eq", "="),
    Lexer.token("op_alt", "|"),
    Lexer.token("op_cleft", "{"),
    Lexer.token("op_cright", "}"),
    Lexer.token("op_bleft", "["),
    Lexer.token("op_bright", "]"),
    Lexer.token("terminator", ";"),
    Lexer.token("terminal", re.compile(r"'\w+'")),
    Lexer.token("identifier", re.compile(r"\w+")),
]

# The following defines BNF in BNF
grammar_source = '''
rules
    = { rule }
    ;

rule
    = 'identifier' 'op_eq' expr 'terminator'
    ;

expr
    = { term } 'op_alt' expr
    | { term }
    ;

term
    = 'op_cleft' atom 'op_cright'
    | 'op_bleft' atom 'op_bright'
    | atom
    ;

atom
    = 'identifier'
    | 'terminal'
    ;
'''.strip()
grammar = Parser.grammar(
    rule("rules", many(non_terminal("rule"))),
    rule("rule", sequence(
        terminal("identifier"),
        terminal("op_eq"),
        non_terminal("expr"),
        terminal("terminator"),
    )),
    rule("expr", choice(
        sequence(
            many(non_terminal("term")),
            terminal("op_alt"),
            non_terminal("expr"),
        ),
        many(non_terminal("term")),
    )),
    rule("term", choice(
        sequence(
            terminal("op_cleft"),
            non_terminal("atom"),
            terminal("op_cright"),
        ),
        sequence(
            terminal("op_bleft"),
            non_terminal("atom"),
            terminal("op_bright"),
        ),
        non_terminal("atom"),
    )),
    rule("atom", choice(
        terminal("identifier"),
        terminal("terminal"),
    ))
)

def parse(source):
    tokens = Lexer.lex(token_defs, source)
    cst = Parser.parse(grammar, tokens)
    return cst