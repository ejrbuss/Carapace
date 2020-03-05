from carapace import (Data, Lexer, Parser, EBNF)

def test_describe():
    assert Parser.describe(EBNF.grammar) == EBNF.grammar_source

def test_parse():
    assert EBNF.parse(EBNF.grammar_source) == EBNF.grammar