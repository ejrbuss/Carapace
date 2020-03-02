from carapace import (Lexer, Parser, BNF)

def test_describe():
    assert Parser.describe(BNF.grammar) == BNF.grammar_source

def test_check():
    tokens = Lexer.lex(BNF.token_defs, BNF.grammar_source)
    assert Parser.check(BNF.grammar, tokens)

def test_parse():
    import json
    tokens = Lexer.lex(BNF.token_defs, BNF.grammar_source)
    (parsed, cst) = Parser.parse(BNF.grammar, tokens)
    # print(json.dumps(Parser.parse(BNF.grammar, tokens)[1], indent=2))
    print(Parser.graph(cst))
    assert False