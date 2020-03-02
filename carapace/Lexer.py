import re

from carapace import Scanner

def token(type, action=None, skip=False):

    if isinstance(action, str):
        def str_action(scanner):
            if Scanner.rest(scanner).startswith(action):
                Scanner.consume(scanner, len(action))
        return dict(type=type, action=str_action, skip=skip)

    if isinstance(action, re.Pattern):
        def re_action(scanner):
            match = re.match(action, Scanner.rest(scanner))
            if match is not None:
                Scanner.consume(scanner, len(match[0]))
        return dict(type=type, action=re_action, skip=skip)

    return dict(type=type, action=action, skip=skip)

def lex(token_defs, source):
    scanner = Scanner.of(source)
    tokens  = []
    line    = 1
    column  = 1
    while Scanner.current(scanner) is not None:
        for token_def in token_defs:
            start = Scanner.checkpoint(scanner)
            token_def["action"](scanner)
            end = Scanner.checkpoint(scanner)
            if start == end:
                continue
            
            token = dict(
                type   = token_def["type"],
                source = Scanner.scan(scanner, start, end),
                start  = start,
                end    = end,
                line   = line,
                column = column,
            )
            if not token_def["skip"]:
                tokens.append(token)
            lines = token["source"].split("\n")
            if len(lines) == 1:
                column += len(token["source"])
            else:
                line  += len(lines) - 1
                column = len(lines[-1]) + 1
            break
        else:
            raise SyntaxError("Unexpected input: " + Scanner.rest(scanner))
    return tokens

def describe(token):
    return f"{token['type']}[{token['source']}]"