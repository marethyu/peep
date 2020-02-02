# Peep

EBNF for Peep programming language

<program> ::= <block>
<block> ::= "{" { <statement> } "}"
<statement> ::= "if" <paren_expression> <block> [ [ "else" "if" <paren_expression> <block> ] "else" <block> ] |
                "while" <paren_expression> <block> |
                "for" "(" <declare_assign> ";" <expression> ";" <assignment> | <increment> | <decrement> ")" <block> |
                "do" <block> "while" <paren_expression> ";" |
                "break" |
                "continue" |
                <block> |
                <declaration> ";" |
                <declare_assign> ";" |
                <assignment> ";" |
                <expression> ";" |
                <increment> ";" |
                <decrement> ";" |
                "print" <paren_expression> ";" |
                ";"
<assignment> ::= <identifier> "=" <expression>
<declare_assign> ::= <declaration> "=" <expression>
<declaration> ::= <builtin_type> <identifier>
<increment> ::= <identifier> "+=" <expression>
<decrement> ::= <identifier> "-=" <expression>
<paren_expression> ::= "(" <expression> ")"
<expression> ::= <or_operand> [ "||" <or_operand> ]
<or_operand> ::= <and_operand> [ "&&" <and_operand> ]
<and_operand> ::= <equality_operand> [ <equality_op> <equality_operand> ]
<equality_operand> ::= <simple_expression> [ <relational_op> <simple_expression> ]
<simple_expression> ::= <term> [ <addictive_op> <term> ]
<term> ::= <factor> [ <multiplicative_op> <factor> ]
<factor> ::= [ <unary_op> ] <int_constant> |
             [ <unary_op> ] <real_constant> |
             [ <unary_op> ] <bool_const> |
             [ <unary_op> ] <paren_expression> |
             [ <unary_op> ] <identifier> |
             <string_literal>
<identifier> ::= <alpha> [ <alpha_num> ]
<builtin_type> ::= "int" | "float" | "bool" | "string"
<equality_op> ::= "==" | "!="
<relational_op> ::= "<" | ">" | "<=" | ">="
<addictive_op> ::= "+" | "-"
<multiplicative_op> ::= "*" | "/" | "%"
<unary_op> ::= "+" | "-" | "!"
<int_constant> ::= <digit> [ <digit> ]
<real_constant> ::= <int_constant> "." <digit> [ <digit> ]
<bool_const> ::= "true" | "false"
<string_literal> ::= "\"" <character> [ <character> ] "\""
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<alpha> ::= "a" | "b" | "c" | "d" | "e" | ... | "z"
<alpha_num> ::= <digit> | <alpha>
<character> ::= <alpha_num> | "\" <escape_seq>
<escape_seq> ::= "n" | "t" | "\"" | "'" | "\" | "a" | "b" | "f" | "r" | "v"

********************************************************************************

IMPORTANT: PLEASE START SMALL!

Next steps (not necessary in order):
- Ternary operator
- Global variables
- Command line arguments
- Generalize for statement
- Functions
- Builtin functions
- Variable references
- Casting
- Arrays
- Modules
- Classes
- Make language loosenly typed (make the language feel like PHP)