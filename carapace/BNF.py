from Parser import (
    grammar,
    rule,
    sequence,
    choice,
    non_terminal,
    terminal,
    describe,
    check,
)

'''
We use a hand rolled BNF parser to bootstrap the parser. Our BNF has the following token types

    IDENT
    LITERAL
    EQUAL
    TERMINATOR

And the following grammar

rules
    = rule
    | rule rules
    ;

rule
    = 'IDENT' 'EQUAL' expr 'TERMINATOR'
    ;

expr
    = term
    | term expr
    ;

term
    = 'IDENT'
    | 'LITERAL'
    ;
'''

bnf = grammar(
    rule("rules", choice(
        non_terminal("rule"),
        sequence(
            non_terminal("rule"),
            non_terminal("rules"),
        ),
    )),
    rule("rule", sequence(
        terminal("IDENT"),
        terminal("EQUAL"),
        non_terminal("expr"),
        terminal("TERMINATOR"),
    )),
    rule("expr", choice(
        sequence(
            non_terminal("term"),
            terminal("ALT"),
            non_terminal("expr"),
        ),
        sequence(
            non_terminal("term"),
            non_terminal("expr"),
        ),
        sequence(),
    )),
    rule("term", choice(
        terminal("IDENT"),
        terminal("LITERAL"),
    ))
)

print(describe(bnf))
print(check(bnf, [
    "IDENT", "EQUAL", "IDENT", "TERMINATOR"
]))