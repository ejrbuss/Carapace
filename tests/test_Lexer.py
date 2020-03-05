import re
import pytest

from carapace import (ANSI, Lexer, Scanner, Data, EBNF)

def test_str_token():
    str_token = Lexer.token("test", "str_token")
    assert str_token["type"] == "test"
    assert str_token["skip"] == False
    scanner = Scanner.of("str_token_more")
    str_token["action"](scanner)
    assert Scanner.rest(scanner) == "_more"
    scanner = Scanner.of("not_str_token")
    str_token["action"](scanner)
    assert Scanner.rest(scanner) == "not_str_token"

def test_re_token():
    re_token = Lexer.token("test", re.compile(r"abc|cba"), True)
    assert re_token["type"] == "test"
    assert re_token["skip"] == True
    scanner = Scanner.of("abccba")
    re_token["action"](scanner)
    assert Scanner.rest(scanner) == "cba"
    re_token["action"](scanner)
    assert Scanner.rest(scanner) == ""
    scanner = Scanner.of("not_re_token")
    re_token["action"](scanner)
    assert Scanner.rest(scanner) == "not_re_token"

def test_token():
    token = Lexer.token("test", lambda scanner : Scanner.chomp(scanner))
    assert token["type"] == "test"
    assert token["skip"] == False
    scanner = Scanner.of("abc")
    token["action"](scanner)
    assert Scanner.rest(scanner) == "bc"
    token["action"](scanner)
    assert Scanner.rest(scanner) == "c"
    token["action"](scanner)
    assert Scanner.rest(scanner) == ""

def test_describe():
    token = dict(type="test", source="test_token")
    assert Lexer.describe(token) == "test[test_token]"

def test_lex_metrics():
    tokens = [
        Lexer.token("whitespace", re.compile(r"\s+"), skip=True),
        Lexer.token("word", re.compile(r"\w+")),
    ]
    assert Lexer.lex(tokens, " a bc\n   def ") == [
        {   
            'column': 2,
            'end': 2,
            'line': 1,
            'source': 'a',
            'start': 1,
            'type': 'word'
        },
        {   
            'column': 4,
            'end': 5,
            'line': 1,
            'source': 'bc',
            'start': 3,
            'type': 'word'
        },
        {   
            'column': 4,
            'end': 12,
            'line': 2,
            'source': 'def',
            'start': 9,
            'type': 'word'
        },
    ]

def test_lex_syntax_error():
    pytest.raises(SyntaxError, lambda : Lexer.lex([], "???"))

def test_lex():
    assert Data.subset(
        [
            dict(type="identifier"),
            dict(type="op_eq"),
            dict(type="identifier"),
            dict(type="op_alt"),
            dict(type="terminal"),
            dict(type="terminator"),
        ],
        Lexer.lex(EBNF.token_defs, '''
            identifier = identifier | 'terminal' ;
        '''),
    )

def test_syntax_error():
    pytest.raises(SyntaxError, lambda : Lexer.lex([], '+'))
    try:
        Lexer.lex(EBNF.token_defs, '''
identifier
    = identifier 
    | [ terminal ]
    ;
        ''')
    except SyntaxError as err:
        print(str(err))
        assert ANSI.escape(str(err)).strip() == '''
Unexpected character sequence!

<anonymous>:4:7
 2 | identifier
 3 |     = identifier 
 4 |     | [ terminal ]
   |       ^ I'm not sure what this is!

'''.strip()