import re

from carapace import (Parser, Lexer)
from carapace.Parser import (
    rule,
    sequence,
    choice,
    many,
    option,
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
    cst    = Parser.parse(grammar, tokens)
    ast    = walk(cst)
    return ast

def walk(node, flat_expr=False):

    if node["type"] == "rules":
        return Parser.grammar(*[ walk(rule)
            for rule
            in node["children"][0]["children"]
        ])

    if node["type"] == "rule":
        name = node["children"][0]["source"]
        expr = walk(node["children"][2])
        return rule(name, expr)

    if node["type"] == "expr":
        choice_node = node["children"][0]
        if choice_node["alt"] == 0:                
            seq = [ walk(term) 
                for term 
                in choice_node["children"][0]["children"]
            ]
            if len(seq) == 1:
                alt = seq[0]
            else:
                alt = sequence(*seq)
            rest = walk(choice_node["children"][2], flat_expr=True)
            if flat_expr:
                rest.insert(0, alt)
                return rest
            else:
                return choice(alt, *rest)
        if choice_node["alt"] == 1:
            seq = [ walk(term)
                for term
                in choice_node["children"][0]["children"]
            ]
            if flat_expr:
                return seq
            if len(seq) == 1:
                return seq[0]
            else:
                return sequence(*seq)

    if node["type"] == "term":
        choice_node = node["children"][0]
        if choice_node["alt"] == 0:
            return many(walk(choice_node["children"][1]))
        if choice_node["alt"] == 1:
            return option(walk(choice_node["children"][1]))
        if choice_node["alt"] == 2:
            return walk(choice_node["children"][0])

    if node["type"] == "atom":
        choice_node = node["children"][0]
        if choice_node["alt"] == 0:
            return non_terminal(choice_node["children"][0]["source"])
        if choice_node["alt"] == 1:
            return terminal(choice_node["children"][0]["source"][1:-1])

    raise Exception("Unhandled node: ", node)