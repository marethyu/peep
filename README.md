# Peep

## Overview

Peep is a toy programming language with small practical applications. This project helps me to learn more about complier and interpreter design and implementation. Peep's syntax is mostly based off C, with some minor modifications.

This repository consists of a complete compiler frontend (lexical analyzer, syntax analyzer, and semantic analyzer) and a working interpreter.

## Getting Started (for Windows users)

This project is built with Python 3.6.0 so make sure you have [Python](https://www.python.org/downloads/) installed in your system with version 3.6.0 or greater. Also Python must be added in PATH environment variable.

After you satisfy the Python requirement, open a command prompt and type the following command to install Peep:
```markdown
pip install thepeep
```

Then type ```peep```, have fun!

## Language Overview

Peep is derived from C based on its syntax. It's similar to C in most ways except that the Peep programs' entry point is a block (a code enclosed in curly braces {...}) whereas C programs have a main function as its entry point.

### Built-in variable types and literals

- **int** An unbounded number (ie. ```1```, ```-35```, ```134```)

- **float** An unbounded number with a decimal point (ie. ```3.14```, ```2.71```)

- **bool** It's allowed to take either ```true``` or ```false```.

- **string** A sequence of characters enclosed with double quotes (ie. ```"foobarbaz"```, ```"#@$*"```, ```"123456"```)

[TODO]

See Grammar file for a complete description of Peep.

## Example Programs

Hello world program
```markdown
{
    print("Hello World!");
}
```

Program to input and print your name
```markdown
{
    string name;

    print("Enter your name:");
    scan(name);
    print("Hello...\t" + name + "!");
}
```

Program to calculate lowest commom multiple of two numbers
```markdown
{
    int a;
    int b;
    int maxn;
    
    print("Input two numbers:");
    scan(a); scan(b);
    
    if (a > b) {
        maxn = a;
    } else {
        maxn = b;
    }
    
    int lcm = maxn;
    
    while (true) {
        if (lcm % a == 0 && lcm % b == 0) {
            break;
        }
        
        lcm += maxn;
    }
    
    print("Lowest commom multiple of two numbers are:");
    print(lcm);
}
```

To run one of the programs above, save the code in a file with .peep extension and then type the following command in the prompt (replace ____ with your file name):
```markdown
python peep.py -i ____.peep
```

## Technical Details

[TODO]

## Changes

- 02/08/2020: Organized files; Packaged this repository to PyPI

## Things to Add for Next Version (not necessary in order)
- Ternary operator
- Global variables
- Command line arguments
- Option to customize IO
- Functions
- More built-in functions
- Variable references
- Explicit type casting
- Arrays
- Modules
- Classes
- Debugger
- Interactive mode
- Code generation
- Code optimization

## License

GNU General Public License v3.0

## Bugs?

Please [email](mailto:codingexpert123@gmail.com) me if you find any.