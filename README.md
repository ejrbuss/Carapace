# Carapace

Dev dependencies:
 - pytest
 - pytest-cov
 - invoke

## Tests
```
pytest --cov=carapace --cov-report html
```

## Pipeline

```
main {
    parse_args
    if interacitve {
        if file {
            fork thread2 file
            join thread1 file
        }
        repl
    } else if file {
        if level1 cached file {
            fork thread2 parse_tree
            join thread1 parse_tree
        } else if level2 cached file {
            generated_code
        } else {
            fork thread2 file
            join thread1 file
        }
    }
    exit
}

thread1 {
    if file {
        parse
        interpret
    } else if parse_tree {
        interpret
    }
}

thread2 { # caching
    if file {
        parse
        cache parse_tree
        generate
        cache generated_code
    } else if parse_tree {
        generate
        cache generated_code
    }
}
```




```
let join = List.join

let describe_expr = { expr ->
    match expr {
        [ --rule name expr ] => 
            "${name}\n    = ${describe_expr expr}"
        [ --sequence exprs ] => 
            join (for exprs describe_expr) " "
        [ --choice alternatives ] => 
            join (for alternatives describe_expr) "\n    | "
        [ --many expr ] =>
            "{ ${describe_expr expr} }"
        [ --option expr ] =>
            "[ ${describe_expr expr} ]"
        [ --non_terminal name ] =>
            name
        [ --terminal token_type ] =>
            "'${token_type}'"
    }
}

let describe = { grammar ->
    join (for grammar.rules describe_expr) "\n\n"
}
```