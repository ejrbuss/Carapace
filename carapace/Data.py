def subset(part, full):
    if isinstance(part, list) and isinstance(full, list) and len(part) == len(full):
        for (part, full) in zip(part, full):
            if not subset(part, full):
                return False
        return True
    if isinstance(part, dict) and isinstance(full, dict):
        for (key, value) in part.items():
            if key not in full or not subset(value, full[key]):
                return False
        return True
    print("part:", part, "full:", full, "part == full", part == full, type(part), type(full))
    return part == full