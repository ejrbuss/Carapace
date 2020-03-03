import re

from carapace import (Span, Scanner)

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

def lex(token_defs, source, source_name="<anonymous>"):
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
            
            token = Span.of(
                token_def["type"],
                Scanner.scan(scanner, start, end),
                start,
                end,
                line,
                column,
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
            start = Scanner.checkpoint(scanner)
            token = Span.of(
                "error",
                Scanner.scan(scanner, start, start + 1),
                start,
                start + 1,
                line,
                column,
            )
            context = Span.contextualize(
                token, 
                source, 
                source_name=source_name, 
                message="I'm not sure what this is!",
            )
            raise SyntaxError(f"Unexpected character sequence!\n" + context)
    return tokens

def describe(token):
    return f"{token['type']}[{token['source']}]"