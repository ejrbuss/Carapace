def of(type, source, start, end, line, column):
    return dict(
        type      = type, 
        source    = source, 
        start     = start, 
        end       = end, 
        line      = line, 
        column    = column, 
    )

def concat(*spans):
    return of(
        "concat", 
        "".join(span["source"] for span in spans),
        spans[0]["start"],
        spans[-1]["end"],
        spans[0]["line"],
        spans[0]["column"],
    )

def contextualize(span, source, message, underline="^", prev_lines=2, source_name="<anonymous>"):
    lines          = source.split("\n")
    multiline      = "\n" in span["source"]
    min_line_num   = max(span["line"] - prev_lines - 1, 0)
    max_line_num   = span["line"] + len(span["source"].split("\n")) - 1
    line_nums      = list(range(min_line_num, max_line_num))
    max_num_widths = len(str(max_line_num + 1))

    def line(line_num):
        padded_line_num = (max_num_widths - len(str(line_num + 1))) * " " + str(line_num + 1)
        line            = lines[line_num]
        return f" {padded_line_num} | {line}"

    title   = f"{source_name}:{span['line']}:{span['column']}\n"
    context = "\n".join([ line(line_num) for line_num in line_nums ])
    prefix  = (max_num_widths + 2) * " " + "| "
    if multiline:
        last_line = lines[max_line_num - 1]
        leading   = (len(last_line) - len(last_line.lstrip())) * ' '
        width     = len(last_line.strip())        
        postfix   = f"{leading}{width * underline}\n{prefix}{leading}{message}"
        pass
    else:
        postfix = (span["column"] - 1) * " " + len(span["source"]) * underline + " " + message

    return f"\n{title}{context}\n{prefix}{postfix}\n"