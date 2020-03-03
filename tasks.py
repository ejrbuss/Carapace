from invoke import task

@task
def test(ctx):
    ctx.run("pytest --cov=carapace --cov-report html -vv")

@task
def coverage(ctx):
    ctx.run("open ./htmlcov/index.html")

@task
def graph(ctx):
    from carapace import (Data, Parser, BNF, EBNF)
    with open("bnf-graph.dot", "w") as f:
        f.write(Parser.graph(BNF.parse(BNF.grammar_source)))
    with open("ebnf-graph.dot", "w") as f:
        f.write(Parser.graph(EBNF.parse(EBNF.grammar_source)))
    # Data.dump(BNF.parse(BNF.grammar_source))
    # Data.dump(EBNF.parse(EBNF.grammar_source))
    ctx.run("dot -Tpng bnf-graph.dot -o bnf-graph.png")
    ctx.run("dot -Tpng ebnf-graph.dot -o ebnf-graph.png")