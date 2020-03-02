import re

from carapace import (Scanner)

### Gramamr ###

def grammar(root, *rules):
    return dict(type="grammar", root=root, rules={ rule["name"]: rule 
        for rule
        in [root, *rules]
    })

def rule(name, expr):
    return dict(type="rule", name=name, expr=expr)

def sequence(*exprs):
    return dict(type="sequence", exprs=list(exprs))

def choice(*alternatives):
    return dict(type="choice", alternatives=list(alternatives))

def non_terminal(name):
    return dict(type="non_terminal", name=name)

def terminal(token_type):
    return dict(type="terminal", token_type=token_type)

### Utility ###

def describe_expr(expr):

    if expr["type"] == "rule":
        return f"{expr['name']}\n    = {describe_expr(expr['expr'])}\n    ;"

    if expr["type"] == "sequence":
        return " ".join([ describe_expr(expr) 
            for expr
            in expr["exprs"]
        ])

    if expr["type"] == "choice":
        return f"\n    | ".join([ describe_expr(alt)
            for alt
            in expr["alternatives"]
        ])

    if expr["type"] == "non_terminal":
        return expr["name"]

    if expr["type"] == "terminal":
        return "'" + expr["token_type"] + "'"

def describe(grammar):
    return "\n\n".join([ describe_expr(rule)
        for rule
        in grammar["rules"].values()
    ])

def check(grammar, tokens):
    scanner = Scanner.of(tokens)
    rules   = grammar["rules"]

    def check_expr(expr, tab, debug=False):
        if debug:
            print(tab, Scanner.rest(scanner), '=>', re.sub(r"\s+", " ", describe_expr(expr)))

        if expr["type"] == "rule":
            return check_expr(expr["expr"], tab + " ")

        if expr["type"] == "sequence":
            checkpoint = Scanner.checkpoint(scanner)
            for expr in expr["exprs"]:
                if not check_expr(expr, tab + " "):
                    Scanner.rollback(scanner, checkpoint)
                    return False
            return True

        if expr["type"] == "choice":

            for alt in expr["alternatives"]:
                if check_expr(alt, tab + " "):
                    return True
            return False

        if expr["type"] == "non_terminal":
            return check_expr(rules[expr["name"]], tab + " ")

        if expr["type"] == "terminal":
            if Scanner.current(scanner)["type"] == expr["token_type"]:
                Scanner.chomp(scanner)
                return True
            return False

    return check_expr(grammar["root"], "")

def parse(grammar, tokens):
    scanner = Scanner.of(tokens)

    pass