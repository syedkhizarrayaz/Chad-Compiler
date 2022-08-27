import json
import re
import numpy as np
from sre_parse import DIGITS

DIGITS = '0123456789'
Plus_Minus = '+-'
Mul_Div_Mod = '*/%'
Compound = ['+=', 'x=', '-=', '/=', '%=']
Relational_Operation = ['<', '>', '<=', '>=', '!=', '==']
And_Logical = ['&&']
OR_Logical = ['||']

# Error reporting


class Error:
    def __init__(self, position_start, position_end, error_name, details):
        self.position_start = position_start
        self.position_end = position_end
        self.error_name = error_name
        self.details = details

    # return error as string

    def asString(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.position_start.file_name}, line {self.position_start.line + 1}'
        return result

    # for not allowed characters


class IllegalCharError(Error):
    def __init__(self, position_start, position_end, details):
        super().__init__(position_start, position_end, 'Illegal Character', details)

# position of error


class Position:
    def __init__(self, index, line, column, file_name, file_text):
        self.index = index
        self.line = line
        self.column = column
        self.file_name = file_name
        self.file_text = file_text

    def advance(self, current_char):
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.line += 1
            self.column = 0

        return self

    def copy(self):
        return Position(self.index, self.line, self.column, self.file_name, self.file_text)

# Token generation

# token constants


TT_INT = 'int'
TT_FLOAT = 'float'
TT_CHAR = 'char'
TT_STR = 'String'
TT_PLUS = 'Plus'
TT_MINUS = 'Minus'
TT_DIV = 'Div'
TT_MUL = 'Mul'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'


class Token:
    # constructor
    def __init__(self, type_, value=None, line=None):
        self.type = type_
        self.value = value
        self.line = line

    # for returning token
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}:line {self.line}'
        return f'{self.type}:line {self.line}'

# lexer class


class Lexer:
    # constructor
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.position = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    # moving to next character
    def advance(self):
        self.position.advance(self.current_char)
        self.current_char = self.text[self.position.index] if self.position.index < len(
            self.text) else None

    # creating tokens
    def makeTokens(self):
        tokens = []
        # open('../Token/token.txt', 'w').close()

        while(self.current_char != None):
            position_start = self.position.copy()
            char = self.current_char
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in re.findall('\d', self.current_char):
                tokens.append(self.isNumber())
            elif self.current_char in Plus_Minus:
                tokens.append(self.isPlusMinus())
                self.advance()
            elif self.current_char in Mul_Div_Mod:
                tokens.append(self.isMultiplicationDivideModulus())
                self.advance()
            # elif self.current_char == '/':
            #     tokens.append(Token('Div'))
            #     self.advance()
            elif self.current_char == '(':
                tokens.append(Token('LPAREN'))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token('RPAREN'))
                self.advance()
            else:
                self.advance()
                # tokens.append(IllegalCharError(
                # position_start, self.position, "'" + char + "'"))
                return [], IllegalCharError(position_start, self.position, "'" + char + "'")

        return tokens, None

    def isNumber(self):

        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:

            f.write(f'(int,{int(num_str)},{self.position.line})\n')
            return Token('int', int(num_str), self.position.line)
        else:
            f.write(f'(int,{float(num_str)},{self.position.line})\n')
            return Token('float', float(num_str), self.position.line)

    def isPlusMinus(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        while self.current_char != None and self.current_char in Plus_Minus:
            if self.current_char == '+':
                f.write(f'(int,{self.current_char},{self.position.line})\n')
                return Token('PM', self.current_char, self.position.line)
                break
            else:
                f.write(f'(int,{self.current_char},{self.position.line})\n')
                return Token('PM', self.current_char, self.position.line)
                break

    def isMultiplicationDivideModulus(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        while self.current_char != None and self.current_char in Mul_Div_Mod:
            if self.current_char == '*':
                f.write(f'(int,{self.current_char},{self.position.line})\n')
                return Token('MDM', self.current_char, self.position.line)
                break
            elif self.current_char == '/':
                f.write(f'(int,{self.current_char},{self.position.line})\n')
                return Token('MDM', self.current_char, self.position.line)
                break
            else:
                f.write(f'(int,{self.current_char},{self.position.line})\n')
                return Token('MDM', self.current_char, self.position.line)
                break


# driver class

def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.makeTokens()

    return tokens, error
