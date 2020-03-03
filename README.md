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