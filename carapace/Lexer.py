import re

from carapace import Scanner

def token(type, action, skip=False):

    if isinstance(action, str):
        def str_action(scanner):
            if Scanner.rest(scanner).startswith(action):
                Scanner.rollback(scanner, Scanner.checkpoint(scanner) + len(action))
        return dict(type=type, action=str_action, skip=skip)

    if isinstance(action, re.Pattern):
        def re_action(scanner):
            match = re.match(action, scanner.rest())
            if match is not None:
                Scanner.rollback(scanner, Scanner.checkpoint(scanner) + len(match[0]))
        return dict(type=type, action=re_action, skip=skip)

    return dict(type=type, action=action, skip=skip)

def lex(tokenDefs, source):
    scanner = Scanner.of(source)
    tokens  = []
    line    = 1
    column  = 1
    while Scanner.current(scanner) is not None:
        for tokenDef in tokenDefs:
            start = Scanner.checkpoint(scanner)
            tokenDef["action"](scanner)
            end = Scanner.checkpoint(scanner)
            if start == end:
                continue
            if tokenDef["skip"]:
                break
            token = dict(
                type   = tokenDef["type"],
                source = Scanner.scan(scanner, start, end),
                start  = start,
                end    = end,
                line   = line,
                column = column,
            )
            lines = token["source"].split("\n")
            if len(lines) == 1:
                column += len(token["source"])
            else:
                lines += len(lines) - 1
                column = len(lines[-1]) + 1
            break
        else:
            raise SyntaxError("Unexpected input: " + scanner.rest())
    return tokens
