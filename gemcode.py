import sys
import re
import os

class Lexer:
    """
    A lexical analyzer that converts source code into tokens.
    """
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[0] if self.source_code else None
        self.keywords = {'print', 'if', 'else', 'while', 'for', 'return', 'int', 'float', 'string'}
        
    def advance(self):
        """Move to the next character in the source code."""
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def get_identifier(self):
        """Get an identifier or keyword."""
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        if result in self.keywords:
            return ('KEYWORD', result)
        else:
            return ('IDENTIFIER', result)
    
    def get_number(self):
        """Get a numeric literal."""
        result = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        
        if '.' in result:
            return ('FLOAT', float(result))
        else:
            return ('INTEGER', int(result))
    
    def get_string(self):
        """Get a string literal."""
        result = ''
        # Skip the opening quote
        self.advance()
        
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        
        # Skip the closing quote
        if self.current_char == '"':
            self.advance()
        
        return ('STRING', result)
    
    def tokenize(self):
        """Convert the source code into a list of tokens."""
        tokens = []
        
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.get_identifier())
                continue
            
            if self.current_char.isdigit():
                tokens.append(self.get_number())
                continue
            
            if self.current_char == '"':
                tokens.append(self.get_string())
                continue
            
            if self.current_char == '+':
                tokens.append(('OPERATOR', '+'))
                self.advance()
                continue
            
            if self.current_char == '-':
                tokens.append(('OPERATOR', '-'))
                self.advance()
                continue
            
            if self.current_char == '*':
                tokens.append(('OPERATOR', '*'))
                self.advance()
                continue
            
            if self.current_char == '/':
                tokens.append(('OPERATOR', '/'))
                self.advance()
                continue
            
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    tokens.append(('OPERATOR', '=='))
                    self.advance()
                else:
                    tokens.append(('ASSIGN', '='))
                continue
            
            if self.current_char == ';':
                tokens.append(('SEMICOLON', ';'))
                self.advance()
                continue
            
            if self.current_char == '(':
                tokens.append(('LPAREN', '('))
                self.advance()
                continue
            
            if self.current_char == ')':
                tokens.append(('RPAREN', ')'))
                self.advance()
                continue
            
            if self.current_char == '{':
                tokens.append(('LBRACE', '{'))
                self.advance()
                continue
            
            if self.current_char == '}':
                tokens.append(('RBRACE', '}'))
                self.advance()
                continue
            
            # If we get here, we have an unrecognized character
            raise ValueError(f"Unrecognized character: {self.current_char}")
        
        tokens.append(('EOF', None))
        return tokens

class Parser:
    """
    A parser that converts tokens into an abstract syntax tree (AST).
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0]
    
    def advance(self):
        """Move to the next token."""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def eat(self, token_type):
        """Consume a token of the expected type."""
        if self.current_token[0] == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token[0]}")
    
    def parse(self):
        """Parse the tokens into an AST."""
        return self.program()
    
    def program(self):
        """Program -> Statement*"""
        statements = []
        
        while self.current_token[0] != 'EOF':
            statements.append(self.statement())
        
        return {'type': 'Program', 'body': statements}
    
    def statement(self):
        """Statement -> PrintStatement | AssignmentStatement | Block"""
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'print':
            return self.print_statement()
        elif self.current_token[0] == 'IDENTIFIER':
            return self.assignment_statement()
        elif self.current_token[0] == 'LBRACE':
            return self.block()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
    
    def print_statement(self):
        """PrintStatement -> 'print' Expression ';'"""
        self.eat('KEYWORD')  # Consume 'print'
        self.eat('LPAREN')
        expr = self.expression()
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        
        return {'type': 'PrintStatement', 'expression': expr}
    
    def assignment_statement(self):
        """AssignmentStatement -> Identifier '=' Expression ';'"""
        identifier = self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        expr = self.expression()
        self.eat('SEMICOLON')
        
        return {'type': 'AssignmentStatement', 'name': identifier[1], 'value': expr}
    
    def block(self):
        """Block -> '{' Statement* '}'"""
        self.eat('LBRACE')
        statements = []
        
        while self.current_token[0] != 'RBRACE':
            statements.append(self.statement())
        
        self.eat('RBRACE')
        
        return {'type': 'Block', 'body': statements}
    
    def expression(self):
        """Expression -> Term (('+' | '-') Term)*"""
        node = self.term()
        
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('+', '-'):
            op = self.eat('OPERATOR')
            right = self.term()
            node = {'type': 'BinaryExpression', 'operator': op[1], 'left': node, 'right': right}
        
        return node
    
    def term(self):
        """Term -> Factor (('*' | '/') Factor)*"""
        node = self.factor()
        
        while self.current_token[0] == 'OPERATOR' and self.current_token[1] in ('*', '/'):
            op = self.eat('OPERATOR')
            right = self.factor()
            node = {'type': 'BinaryExpression', 'operator': op[1], 'left': node, 'right': right}
        
        return node
    
    def factor(self):
        """Factor -> INTEGER | FLOAT | STRING | IDENTIFIER | '(' Expression ')'"""
        token = self.current_token
        
        if token[0] == 'INTEGER':
            self.eat('INTEGER')
            return {'type': 'Literal', 'value': token[1], 'dataType': 'int'}
        
        elif token[0] == 'FLOAT':
            self.eat('FLOAT')
            return {'type': 'Literal', 'value': token[1], 'dataType': 'float'}
        
        elif token[0] == 'STRING':
            self.eat('STRING')
            return {'type': 'Literal', 'value': token[1], 'dataType': 'string'}
        
        elif token[0] == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            return {'type': 'Identifier', 'name': token[1]}
        
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            expr = self.expression()
            self.eat('RPAREN')
            return expr
        
        else:
            raise SyntaxError(f"Unexpected token: {token}")

class CodeGenerator:
    """
    A code generator that converts an AST into executable code.
    In this simple implementation, we'll generate Python code.
    """
    def __init__(self, ast):
        self.ast = ast
        self.output = []
        self.indent_level = 0
    
    def indent(self):
        """Add indentation to the output."""
        return '    ' * self.indent_level
    
    def generate(self):
        """Generate code from the AST."""
        self.visit(self.ast)
        return '\n'.join(self.output)
    
    def visit(self, node):
        """Visit a node in the AST."""
        method_name = f"visit_{node['type']}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Generic visitor for any node without a specific visitor."""
        raise NotImplementedError(f"No visit method for {node['type']}")
    
    def visit_Program(self, node):
        """Visit a Program node."""
        self.output.append("# Generated by SimpleCompiler")
        self.output.append("")
        
        for statement in node['body']:
            self.visit(statement)
    
    def visit_PrintStatement(self, node):
        """Visit a PrintStatement node."""
        expr = self.visit(node['expression'])
        self.output.append(f"{self.indent()}print({expr})")
    
    def visit_AssignmentStatement(self, node):
        """Visit an AssignmentStatement node."""
        name = node['name']
        value = self.visit(node['value'])
        self.output.append(f"{self.indent()}{name} = {value}")
    
    def visit_Block(self, node):
        """Visit a Block node."""
        self.indent_level += 1
        
        for statement in node['body']:
            self.visit(statement)
        
        self.indent_level -= 1
    
    def visit_BinaryExpression(self, node):
        """Visit a BinaryExpression node."""
        left = self.visit(node['left'])
        right = self.visit(node['right'])
        operator = node['operator']
        
        return f"({left} {operator} {right})"
    
    def visit_Literal(self, node):
        """Visit a Literal node."""
        value = node['value']
        data_type = node['dataType']
        
        if data_type == 'string':
            return f'"{value}"'
        else:
            return str(value)
    
    def visit_Identifier(self, node):
        """Visit an Identifier node."""
        return node['name']

class Compiler:
    """
    A simple compiler that orchestrates the compilation process.
    """
    def __init__(self):
        pass
    
    def compile(self, source_code, output_file=None):
        """Compile the source code."""
        # Lexical analysis
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Code generation
        code_generator = CodeGenerator(ast)
        target_code = code_generator.generate()
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(target_code)
        
        return target_code

def main():
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source_file> [output_file]")
        return
    
    source_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        with open(source_file, 'r') as f:
            source_code = f.read()
        
        compiler = Compiler()
        target_code = compiler.compile(source_code, output_file)
        
        if not output_file:
            print(target_code)
        else:
            print(f"Compilation successful. Output written to {output_file}")
    
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
    except Exception as e:
        print(f"Compilation error: {e}")

if __name__ == "__main__":
    main()