import re
import Scanner

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

def terminal(pattern):
    return dict(type="terminal", pattern=pattern)

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
        return "'" + expr["pattern"] + "'"

def describe(grammar):
    return "\n\n".join([ describe_expr(rule)
        for rule
        in grammar["rules"].values()
    ])

def check(grammar, source):
    scanner = Scanner.new(source)
    rules   = grammar["rules"]

    def check_expr(expr, tab):
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
            return Scanner.check(scanner, lambda token : token == expr["pattern"])

    return check_expr(grammar["root"], "")

def parse(grammar, input):
    pass