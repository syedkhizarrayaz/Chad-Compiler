from ast import keyword
import re
import string

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
Plus_Minus = '+-'
Mul_Div_Mod = '*/%'
Compound = ['+=', '*=', '-=', '/=', '%=']
Relational_Operation = ['<', '>', '<=', '>=', '!=', '==']
And_Logical = ['&&']
OR_Logical = ['||']
Brackets = ['(', ')', '{', '}', '[', ']']
Key_words = ['bool', 'byte', 'char', 'int', 'long', 'short', 'float', 'double', 'private', 'protected', 'public', 'abstract', 'final', 'try', 'catch', 'finally', 'throw', 'break', 'case', 'continue', 'do', 'while', 'range', 'switch',
             "elseif", 'if', 'else', 'page,extends', 'implements', 'import', 'instanceOf', 'new', 'return', 'interface', 'this', 'throws', 'void', 'super', 'accept', 'decline', "null", 'constant', 'define', 'func', 'open', 'close', 'const', 'goto']
id = r'^[A-Za-z_]+[A-Za-z0-9_]*'

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
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        f.write(
            f'({self.error_name},{self.details},{self.position_start.line})\n')
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
            elif self.current_char in re.findall('\w', self.current_char):
                tokens.append(self.isIdentifier())
            elif self.current_char == "'":
                tokens.append(self.isChar())
            elif self.current_char == '"':
                tokens.append(self.isString())
            elif self.current_char in re.findall('\d', self.current_char):
                tokens.append(self.isNumber())
            elif self.current_char in Compound:
                tokens.append(self.isCompound())
                self.advance()
            elif self.current_char in Plus_Minus:
                tokens.append(self.isPlusMinus())
                self.advance()
            elif self.current_char in Mul_Div_Mod:
                tokens.append(self.isMultiplicationDivideModulus())
                self.advance()
            elif self.current_char in Brackets:
                tokens.append(self.isBracket())
                self.advance()
            elif self.current_char in Relational_Operation:
                tokens.append(self.isRelationalOperator())
                self.advance()
            else:
                self.advance()
                return [], IllegalCharError(position_start, self.position, "'" + char + "'")

        return tokens, None

    def isIdentifier(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        id_str = ''
        position_start = self.position.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        token_type = 'Keyword' if id_str in Key_words else 'Identifier'
        f.write(f'({token_type},{id_str},{self.position.line+1})\n')
        return Token(token_type, id_str, self.position.line+1)

    def isString(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        string = ''
        position_start = self.position.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }
        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char,
                                                self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
                self.advance()
                escape_character = False

        self.advance()
        f.write(f'(String,{string},{self.position.line+1})\n')
        return Token('String', string, self.position.line+1)

    def isChar(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        char = ''
        position_start = self.position.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }
        while self.current_char != None and (self.current_char != "'" or escape_character):
            if escape_character:
                char += escape_characters.get(self.current_char,
                                              self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    char += self.current_char
                self.advance()
                escape_character = False

        self.advance()
        f.write(f'(Char,{char},{self.position.line+1})\n')
        return Token('Char', char, self.position.line+1)

    def isString(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        string = ''
        position_start = self.position.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }
        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char,
                                                self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
                self.advance()
                escape_character = False

        self.advance()
        f.write(f'(String,{string},{self.position.line+1})\n')
        return Token('String', string, self.position.line+1)

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
            f.write(f'(int,{float(num_str)},{self.position.line+1})\n')
            return Token('float', float(num_str), self.position.line+1)

    def isPlusMinus(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        comp_str = ''
        position_start = self.position.copy()
        token_type = ''
        while self.current_char != None and self.current_char in Plus_Minus:
            if self.current_char == '+':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'Compound' if comp_str in Compound else 'PM'
                f.write(f'({token_type},{comp_str},{self.position.line+1})\n')
                return Token(token_type, comp_str, self.position.line+1)
            else:
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'Compound' if comp_str in Compound else 'PM'
                f.write(f'({token_type},{comp_str},{self.position.line+1})\n')
                return Token(token_type, comp_str, self.position.line+1)

    def isMultiplicationDivideModulus(self):
        # writing tokens
        comp_str = ''
        position_start = self.position.copy()
        token_type = ''
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        while self.current_char != None and self.current_char in Mul_Div_Mod:
            if self.current_char == '*':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'Compound' if comp_str in Compound else 'MDM'
                f.write(f'({token_type},{comp_str},{self.position.line+1})\n')
                return Token(token_type, comp_str, self.position.line+1)
            elif self.current_char == '/':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'Compound' if comp_str in Compound else 'MDM'
                f.write(f'({token_type},{comp_str},{self.position.line+1})\n')
                return Token(token_type, comp_str, self.position.line+1)
            else:
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'Compound' if comp_str in Compound else 'MDM'
                f.write(f'({token_type},{comp_str},{self.position.line+1})\n')
                return Token(token_type, comp_str, self.position.line+1)

    def isRelationalOperator(self):
        # writing tokens
        comp_str = ''
        position_start = self.position.copy()
        token_type = ''
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        while self.current_char != None and self.current_char in Relational_Operation:
            if self.current_char == '<':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'RO'
                f.write(f'({token_type},{comp_str},{self.position.line+1})\n')
                return Token(token_type, comp_str, self.position.line+1)
            elif self.current_char == '>':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'RO'
                f.write(f'({token_type},{comp_str},{self.position.line+1})\n')
                return Token(token_type, comp_str, self.position.line+1)
            elif self.current_char == '!':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'RO'
                f.write(f'({token_type},{comp_str},{self.position.line+1})\n')
                return Token(token_type, comp_str, self.position.line+1)
            else:
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'RO'
                f.write(f'({token_type},{comp_str},{self.position.line+1})\n')
                return Token(token_type, comp_str, self.position.line+1)

    def isBracket(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        while self.current_char != None and self.current_char in Brackets:
            f.write(f'({self.current_char}, ,{self.position.line+1})\n')
            return Token(self.current_char, ' ', self.position.line+1)
# driver class


def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.makeTokens()

    return tokens, error


def runFile(file_name):
    while 1:
    # read by character
        char = file_name.read(1)
        run(file_name, char)         
        if not char:
            break
