from carapace import (ANSI, Span)

def test_contextualize():
    source = '''
#include <stdio.h>
int main() {

    int number1, number2, sum;

    printf("Enter two integers: ");
    scanf("%d %d", &number1, &number2);

    // calculating sum
    sum = number1 + number2;  

    printf("%d + %d = %d", number1, number2, sum);
    return 0;
}
'''.strip()
    
    span = Span.make("source", "test.c", source, 69, 140)
    context = Span.contextualize(span, "printing some numbers in C", 
        prev_lines          = 100, 
        underline           = '~', 
        file_style          = ANSI.foreground(100, 100, 200),
        prev_line_num_style = ANSI.foreground(200, 200, 255),
        span_line_num_style = ANSI.foreground(200, 100, 100),
        line_gutter_style   = ANSI.foreground(150, 150, 255),
        prev_style          = ANSI.foreground(200, 200, 255),
        span_style          = ANSI.foreground(200, 100, 100),
        underline_style     = ANSI.foreground(255, 100, 100),
        message_style       = ANSI.bold + ANSI.foreground(200, 50, 150),
    )
    print(context)
    assert ANSI.escape(context).strip() == '''
test.c:6:5
 1 | #include <stdio.h>
 2 | int main() {
 3 | 
 4 |     int number1, number2, sum;
 5 | 
 6 |     printf("Enter two integers: ");
 7 |     scanf("%d %d", &number1, &number2);
   |     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   |     printing some numbers in C
    '''.strip()