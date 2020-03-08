# Peep

![](https://img.shields.io/badge/pypi-1.1.2-blue)
![](https://img.shields.io/badge/version-v1.1.2-blue)

## Overview

Peep is a toy programming language with small practical applications. This project helps me to learn more about complier and interpreter design and implementation. Peep's syntax is mostly based off C, with some minor modifications.

This repository consists of a complete compiler frontend (lexical analyzer, syntax analyzer, and semantic analyzer) and a working tree-walk interpreter.

## Getting Started (for Windows users)

This project is built with Python 3.6.0 so make sure you have [Python](https://www.python.org/downloads/) installed in your system with version 3.6.0 or greater. Also Python must be added in PATH environment variable.

After you satisfy the Python requirement, open a command prompt and type the following command to install Peep:
```markdown
pip install thepeep
```

Then type ```peep```, have fun!

## Basic Usage

To run the Peep program, save the code in a file with .peep extension and then type the following command in the prompt (replace ____ with your file name):
```markdown
peep -i ____.peep
```

To view the Peep program's abstract syntax tree (AST), run the following command:
```markdown
peep -p ____.peep
```
It will generate a seperate file with .ast.xml extension. You can use your favourite text editor to view AST in the generated file.

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

Generated .xml file for the program above
```markdown
<?xml version="1.0" encoding="UTF-8"?>
<Program>
  <Block>
    <Block>
    </Block>
    <Print>
      <Constant type="Type.STRING" value="Hello World!"></Constant>
    </Print>
  </Block>
</Program>
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

## Technical Details

[TODO]

## Changes
- 03/7/2020: Added new operators: *=, /=, %=
- 03/7/2020: For technical reasons, do-while loop is removed from the language's grammar
- 02/08/2020: Organized files; Packaged this repository to PyPI

## Things to Add for Next Version (not necessary in order)
- Ternary operator
- Multiple assignment
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

## Contributing

I appreciate any kind of contributions. It can be bug fixes, code improvements, recommendations, and etc...

## License

GNU General Public License v3.0

## Bugs or Feature Request?

Please [email](mailto:codingexpert123@gmail.com) me or you can open a new issue for this repository.