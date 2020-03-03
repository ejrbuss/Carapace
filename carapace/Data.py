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

def dump(data):
    import json
    print(json.dumps(data))

def deep_append(unwrapped, element):
    wrapped = []
    if isinstance(element, list):
        wrapped.extend(element)
    else:
        unwrapped.append(element)
    while len(wrapped) > 0:
        element = wrapped.pop(0)
        if isinstance(element, list):
            element.extend(wrapped)
            wrapped = element
        else:
            unwrapped.append(element)
    return unwrapped
