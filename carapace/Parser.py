import re

from carapace import (Scanner, Lexer)

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

def repetition(expr):
    return dict(type="repetition", expr=expr)

def option(expr):
    return dict(type="option", expr=expr)

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

    def check_expr(expr):
        if expr["type"] == "rule":
            return check_expr(expr["expr"])

        if expr["type"] == "sequence":
            checkpoint = Scanner.checkpoint(scanner)
            for expr in expr["exprs"]:
                if not check_expr(expr):
                    Scanner.rollback(scanner, checkpoint)
                    return False
            return True

        if expr["type"] == "choice":
            for alt in expr["alternatives"]:
                if check_expr(alt):
                    return True
            return False

        if expr["type"] == "non_terminal":
            return check_expr(rules[expr["name"]])

        if expr["type"] == "terminal":
            token = Scanner.current(scanner)
            if token is not None and token["type"] == expr["token_type"]:
                Scanner.chomp(scanner)
                return True
            return False

    return check_expr(grammar["root"])

def parse(grammar, tokens):
    scanner = Scanner.of(tokens)
    rules   = grammar["rules"]

    def parse_expr(expr):
        if expr["type"] == "rule":
            (parsed, node) = parse_expr(expr["expr"])
            return (parsed, dict(type=expr["name"], value=node))

        if expr["type"] == "sequence":
            checkpoint = Scanner.checkpoint(scanner)
            nodes      = []
            for expr in expr["exprs"]:
                (parsed, node) = parse_expr(expr)
                if not parsed:
                    Scanner.rollback(scanner, checkpoint)
                    return (False, nodes)
                nodes.append(node)
            return (True, nodes)

        if expr["type"] == "choice":
            for (alt, expr) in enumerate(expr["alternatives"]):
                (parsed, node) = parse_expr(expr)
                if parsed:
                    return (True, node)
            return (False, None)

        if expr["type"] == "non_terminal":
            return parse_expr(rules[expr["name"]])

        if expr["type"] == "terminal":
            token = Scanner.current(scanner)
            if token is not None and token["type"] == expr["token_type"]:
                Scanner.chomp(scanner)
                return (True, token)
            return (False, token)

    return parse_expr(grammar["root"])

def graph(cst, name="parse_tree"):

    edges = set()

    def add_edge(left, right):
        edges.add(f"{id(left)} [ label=\"{label_node(left)}\" ] ;")
        if isinstance(right, list):
            edges.add(f"{id(left)} -> {{{' '.join([ str(id(right)) for right in right ])}}} ;")
            for right in right:
                edges.add(f"{id(right)} [ label=\"{label_node(right)}\" ] ;")
        else:
            edges.add(f"{id(left)} -> {id(right)} ;")
            edges.add(f"{id(right)} [ label=\"{label_node(right)}\" ] ;")

    def label_node(node):
        if isinstance(node, dict):
            if "type" in node and "value" in node:
                return node["type"]
            if "type" in node and "source" in node:
                return Lexer.describe(node)
        if isinstance(node, list):
            return [ label_node(node) for node in node ]
    
    def graph_node(node):
        if isinstance(node, dict):
            if "type" in node and "value" in node:
                add_edge(node, node["value"])
                graph_node(node["value"])
        if isinstance(node, list):
            for node in node:
                graph_node(node)

    graph_node(cst)

    return f"""
        digraph {name} {{
            ordering = out ;
            {"".join(edges)}
        }}
    """
