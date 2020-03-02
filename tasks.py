from invoke import task

@task
def test(ctx):
    ctx.run("pytest --cov=carapace --cov-report html -vv")

@task
def coverage(ctx):
    ctx.run("open ./htmlcov/index.html")

@task
def graph(ctx):
    from carapace import (Parser, BNF)
    with open("graph.dot", "w") as f:
        f.write(Parser.graph(BNF.parse(BNF.grammar_source)))
    ctx.run("dot -Tpng graph.dot -o graph.png")