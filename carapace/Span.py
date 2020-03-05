from carapace import (ANSI)

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

def contextualize(span, source, message, 
    underline           = "^", 
    prev_lines          = 2, 
    source_name         = "<anonymous>",
    # Styles
    source_name_style   = '',
    prev_line_num_style = '',
    span_line_num_style = '',
    line_gutter_style   = '',
    prev_style          = '',
    span_style          = '',
    underline_style     = '',
    message_style       = '',
):
    lines          = source.split("\n")
    multiline      = "\n" in span["source"]
    min_line_num   = max(span["line"] - prev_lines - 1, 0)
    max_line_num   = span["line"] + len(span["source"].split("\n")) - 1
    prev_line_nums = list(range(min_line_num, span["line"] - 1))
    span_line_nums = list(range(span["line"] - 1, max_line_num))
    max_num_widths = len(str(max_line_num + 1))

    def line(line_num, line_num_style, line_style):
        padded_line_num = (max_num_widths - len(str(line_num + 1))) * " " + f"{line_num_style}{line_num + 1}{ANSI.reset}"
        line            = lines[line_num]
        return f" {padded_line_num} {line_gutter_style}|{ANSI.reset} {line_style}{line}{ANSI.reset}"

    title      = f"{source_name_style}{source_name}:{span['line']}:{span['column']}{ANSI.reset}\n"
    prev_lines = "\n".join([ line(line_num, prev_line_num_style, prev_style) for line_num in prev_line_nums ])
    span_lines = "\n".join([ line(line_num, span_line_num_style, span_style) for line_num in span_line_nums ])
    prefix     = f"{(max_num_widths + 2) * ' '}{line_gutter_style}|{ANSI.reset} "
    if len(prev_line_nums) > 0:
        prev_lines += "\n"
    if multiline:
        last_line = lines[max_line_num - 1]
        leading   = (len(last_line) - len(last_line.lstrip())) * ' '
        width     = len(last_line.strip())        
        postfix   = f"{leading}{underline_style}{width * underline}{ANSI.reset}\n{prefix}{leading}{message_style}{message}{ANSI.reset}"
        pass
    else:
        postfix = f"{(span['column'] - 1) * ' '}{underline_style}{len(span['source']) * underline}{ANSI.reset} {message_style}{message}{ANSI.reset}"

    return f"\n{title}{prev_lines}{span_lines}\n{prefix}{postfix}\n"