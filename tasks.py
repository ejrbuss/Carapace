from invoke import task

@task
def test(ctx):
    ctx.run("pytest --cov=carapace --cov-report html -vv")

@task
def coverage(ctx):
    ctx.run("open ./htmlcov/index.html")

@task
def graph(ctx):
    from carapace import (Data, Parser, Lexer, EBNF)
    
    with open("ebnf-graph.dot", "w") as f:
        tokens = Lexer.lex(EBNF.token_defs, EBNF.grammar_source, "ebnf-graph.dot")
        cst    = Parser.parse(EBNF.grammar, tokens)
        f.write(Parser.graph(cst))
        
    ctx.run("dot -Tpng ebnf-graph.dot -o ebnf-graph.png")

@task
def check(ctx):
    from carapace import (Parser, EBNF)
    with open("carapace.ebnf", "r") as f:
        print(Parser.describe(EBNF.parse(f.read())))