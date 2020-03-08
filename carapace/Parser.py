from carapace import (Data, Scanner, Lexer, Span)

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

def many(expr):
    return dict(type="many", expr=expr)

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

    if expr["type"] == "many":
        return f"{{ {describe_expr(expr['expr'])} }}"

    if expr["type"] == "option":
        return f"[ {describe_expr(expr['expr'])} ]"

    if expr["type"] == "non_terminal":
        return expr["name"]

    if expr["type"] == "terminal":
        return "'" + expr["token_type"] + "'"

def describe(grammar):
    return "\n\n".join([ describe_expr(rule)
        for rule
        in grammar["rules"].values()
    ])

def parse(grammar, tokens):
    scanner = Scanner.of(tokens)
    rules   = grammar["rules"]

    def parse_expr(expr):
        if expr["type"] == "rule":
            (parsed, node) = parse_expr(expr["expr"])
            return (parsed, dict(type=expr["name"], children=Data.deep_append([], node)))

        if expr["type"] == "sequence":
            checkpoint = Scanner.checkpoint(scanner)
            children   = []
            for expr in expr["exprs"]:
                (parsed, node) = parse_expr(expr)
                if not parsed:
                    Scanner.rollback(scanner, checkpoint)
                    return (False, children)
                Data.deep_append(children, node)
            return (True, children)

        if expr["type"] == "choice":
            for (alt, expr) in enumerate(expr["alternatives"]):
                (parsed, node) = parse_expr(expr)
                if parsed:
                    return (True, dict(type="choice", alt=alt, children=Data.deep_append([], node)))
            return (False, [])

        if expr["type"] == "many":
            children  = []
            parsed    = True
            while parsed:
                (parsed, node) = parse_expr(expr["expr"])
                if parsed:
                    Data.deep_append(children, node)
            return (True, dict(type="many", children=children))

        if expr["type"] == "option":
            (parsed, node) = parse_expr(expr["expr"])
            if parsed:
                return (True, dict(type="option", present=True, children=Data.deep_append([], node)))
            else:
                return (True, dict(type="option", present=False, children=[]))

        if expr["type"] == "non_terminal":
            return parse_expr(rules[expr["name"]])

        if expr["type"] == "terminal":
            token = Scanner.current(scanner)
            if token is not None and token["type"] == expr["token_type"]:
                Scanner.chomp(scanner)
                return (True, [ token ])
            return (False, token)

    (parsed, cst) = parse_expr(grammar["root"])
    if not parsed or len(Scanner.rest(scanner)) > 0:
        raise SyntaxError(Scanner.furthest(scanner))
    return cst

def graph(cst, name="parse_tree"):

    edges = list()

    def add_edge(node):
        left = node
        children = node["children"]
        edges.append(f"{id(left)} [ label=\"{label_node(left)}\", shape=plaintext ] ;\n    ")
        for right in children:
            edges.append(f"{id(right)} [ label=\"{label_node(right)}\", shape=plaintext ] ;\n    ")
        edges.append(f"{id(left)} -> {{ {' '.join([ str(id(right)) for right in children ])} }} [ arrowhead=none ] ;\n    ")

    def label_node(node):
        if isinstance(node, dict):
            if "type" in node and "children" in node:
                if node["type"] == "choice":
                    return f"{node['type']}[{node['alt']}]"
                return node["type"]
            if "type" in node and "source" in node:
                return Lexer.describe(node)
        if isinstance(node, list):
            return [ label_node(node) for node in node ]
    
    def graph_node(node):
        if isinstance(node, dict):
            if "type" in node and "children" in node:
                add_edge(node)
                graph_node(node["children"])
        if isinstance(node, list):
            for node in node:
                graph_node(node)

    graph_node(cst)

    return f"""
digraph {name} {{
    ordering = out ;

    {"".join(edges)}
}}
    """.strip()
