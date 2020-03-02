def of(source):
    return dict(source=source, checkpoint=0, furthest=0)

def checkpoint(scanner):
    return scanner["checkpoint"]

def furthest(scanner):
    return scanner["furthest"]

def rollback(scanner, checkpoint):
    scanner["checkpoint"] = checkpoint

def current(scanner):
    if checkpoint(scanner) < len(scanner["source"]):
        return scanner["source"][checkpoint(scanner)]
    return None

def chomp(scanner):
    consume(scanner, 1)

def consume(scanner, n):
    scanner["checkpoint"] += n
    scanner["furthest"] = max(scanner["furthest"], scanner["checkpoint"])

def rest(scanner):
    return scanner["source"][checkpoint(scanner):]

def scan(scanner, start, end):
    return scanner["source"][start:end]