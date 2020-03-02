from carapace import (Lexer, Parser, BNF)

def test_check():
    tokens = Lexer.lex(BNF.token_defs, BNF.grammar_source)
    assert Parser.check(BNF.grammar, tokens)

def test_describe():
    assert Parser.describe(BNF.grammar) == BNF.grammar_source