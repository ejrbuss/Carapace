def of(source):
    return dict(source=source, checkpoint=0)

def checkpoint(scanner):
    return scanner["checkpoint"]

def rollback(scanner, checkpoint):
    scanner["checkpoint"] = checkpoint

def current(scanner):
    if checkpoint(scanner) < len(scanner["source"]):
        return scanner["source"][checkpoint(scanner)]
    return None

def check(scanner, predicate):
    if predicate(current(scanner)):
        scanner["checkpoint"] += 1
        return True
    else:
        return False

def rest(scanner):
    return scanner["source"][checkpoint(scanner):]

def scan(scanner, start, end):
    return scanner["source"][start:end]