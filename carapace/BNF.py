import re

from carapace import (Parser, Lexer)
from carapace.Parser import (
    rule,
    sequence,
    choice,
    non_terminal,
    terminal,
)

token_defs = [
    Lexer.token("comment", re.compile(r"#.*"), skip=True),
    Lexer.token("whitespace", re.compile(r"\s+"), skip=True),
    Lexer.token("op_eq", "="),
    Lexer.token("op_alt", "|"),
    Lexer.token("terminator", ";"),
    Lexer.token("terminal", re.compile(r"'\w+'")),
    Lexer.token("identifier", re.compile(r"\w+")),
]

# The following defines BNF in BNF
grammar_source = '''
rules
    = rule
    | rule rules
    ;

rule
    = 'identifier' 'op_eq' expr 'terminator'
    ;

expr
    = term 'op_alt' expr
    | term expr
    | 
    ;

term
    = 'identifier'
    | 'terminal'
    ;
'''.strip()
grammar = Parser.grammar(
    rule("rules", choice(
        non_terminal("rule"),
        sequence(
            non_terminal("rule"),
            non_terminal("rules"),
        ),
    )),
    rule("rule", sequence(
        terminal("identifier"),
        terminal("op_eq"),
        non_terminal("expr"),
        terminal("terminator"),
    )),
    rule("expr", choice(
        sequence(
            non_terminal("term"),
            terminal("op_alt"),
            non_terminal("expr"),
        ),
        sequence(
            non_terminal("term"),
            non_terminal("expr"),
        ),
        sequence(),
    )),
    rule("term", choice(
        terminal("identifier"),
        terminal("terminal"),
    ))
)