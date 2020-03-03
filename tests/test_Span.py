from carapace import Span

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
    
    span = Span.of(
        "source",
        "printf(\"Enter two integers: \");\nnscanf(\"%d %d\", &number1, &number2);  ",
        70, 41, 6, 5,
    )

    context = Span.contextualize(span, source, "printing some numbers in C", 
        prev_lines  = 0, 
        underline   = '-', 
        source_name = "test.c",
    )

    assert context.strip() == '''
test.c:6:5
 6 |     printf("Enter two integers: ");
 7 |     scanf("%d %d", &number1, &number2);
   |     -----------------------------------
   |     printing some numbers in C
    '''.strip()