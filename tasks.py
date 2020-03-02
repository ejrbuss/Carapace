from invoke import task

@task
def test(ctx):
    ctx.run("pytest --cov=carapace --cov-report html -vv")

@task
def coverage(ctx):
    ctx.run("open ./htmlcov/index.html")
