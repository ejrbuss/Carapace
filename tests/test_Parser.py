from carapace import (Lexer, Parser, BNF, EBNF)

def test_describe():
    assert Parser.describe(BNF.grammar) == BNF.grammar_source
    assert Parser.describe(EBNF.grammar) == EBNF.grammar_source