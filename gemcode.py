To use the compiler, follow these steps:

Save the compiler code in a file named compiler.py
Create a source file with code in the simple language the compiler understands. For example, create a file test.txt with these contents:
Copyx = 10;
y = 20;
z = x + y;
print(z);
print("Hello, world!");

Run the compiler from the command line:
Copypython compiler.py test.txt output.py
This will compile your source file (test.txt) and generate a Python file (output.py).
Execute the generated code:
Copypython output.py


You can also compile without saving the output by omitting the output filename:
Copypython compiler.py test.txt
This will display the generated Python code in the terminal instead of saving it to a file.
The compiler understands:

Variable assignments using =
Basic arithmetic (+, -, *, /)
Print statements in the form print(expression);
String literals in double quotes
Integer and float numbers
Each statement must end with a semicolon (;)

If your code has syntax errors, the compiler will report them with error messages to help you identify and fix the issues.