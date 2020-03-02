from carapace import (Scanner)

def test_furthest():
    scanner = Scanner.of("test")
    Scanner.chomp(scanner)
    checkpoint = Scanner.checkpoint(scanner)
    Scanner.consume(scanner, 2)
    furthest = Scanner.checkpoint(scanner)
    Scanner.rollback(scanner, checkpoint)
    assert Scanner.checkpoint(scanner) == checkpoint
    assert Scanner.furthest(scanner) == furthest

def test_rollback():
    scanner = Scanner.of("test")
    checkpoint = Scanner.checkpoint(scanner)
    Scanner.chomp(scanner)
    assert Scanner.rest(scanner) == "est"
    Scanner.rollback(scanner, checkpoint)
    assert Scanner.rest(scanner) == "test"

def test_current():
    scanner = Scanner.of("test")
    assert Scanner.current(scanner) == "t"
    Scanner.chomp(scanner)
    assert Scanner.current(scanner) == "e"
    Scanner.consume(scanner, 3)
    assert Scanner.current(scanner) == None

def test_scan():
    scanner = Scanner.of("test")
    assert Scanner.scan(scanner, 1, 3) == "test"[1:3]