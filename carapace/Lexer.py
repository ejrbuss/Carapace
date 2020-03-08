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

def lex(token_defs, source, file):
    scanner = Scanner.of(source)
    tokens  = []
    while Scanner.current(scanner) is not None:
        for token_def in token_defs:
            start = Scanner.checkpoint(scanner)
            token_def["action"](scanner)
            end = Scanner.checkpoint(scanner)
            if start == end:
                continue
            
            token = Span.make(
                type   = token_def["type"],
                source = source,
                file   = file,
                start  = start,
                end    = end,
            )
            if not token_def["skip"]:
                tokens.append(token)
            break
        else:
            start = Scanner.checkpoint(scanner)
            span = Span.make(
                type   = "error",
                source = source,
                file   = file,
                start  = start,
                end    = start + 1,
            )
            context = Span.contextualize(span, message="I'm not sure what this is!")
            raise SyntaxError(f"Unexpected character sequence!\n" + context)
    return tokens

def describe(token):
    return f"{token['type']}[{token['value']}]"