import re

from carapace import (Lexer, Scanner)

def test_str_token():
    str_token = Lexer.token("test", "str_token")
    assert str_token["type"] == "test"
    assert str_token["skip"] == False
    scanner = Scanner.of("str_token")
    str_token["action"](scanner)
    assert Scanner.rest(scanner) == ""
    scanner = Scanner.of("not_str_token")
    str_token["action"](scanner)
    assert Scanner.rest(scanner) == "not_str_token"

def test_re_token():
    re_token = Lexer.token("test", re.compile(r"abc|cba"))
