from ast import keyword
import re
import string
from turtle import position
from wsgiref import validate

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
Plus_Minus = '+-'
Mul_Div_Mod = '*/%'
Increment_Decrement = ['++', '--']
Compound = ['+=', '*=', '-=', '/=', '%=']
Relational_Operation = ['<', '>', '<=', '>=', '!=', '==']
And_Logical = '&&'
OR_Logical = '||'
Brackets = ['(', ')', '{', '}', '[', ']']
Key_words = ['VAR',
             'AND',
             'OR',
             'NOT',
             'if',
             'elseif',
             'else',
             'for',
             'to',
             'while',
             'do',
             'END',
             'return',
             'continue',
             'break',
             'bool',
             'accept',
             'decline',
             'khali',
             'constant',
             'open',
             'close',
             'define',
             'def',
             'func',
             'int',
             'char',
             'String',
             'float',
             'Array']
OOP = ['class', 'private', 'public', 'protected', 'void', 'extends',
       'implements', 'import', 'new', 'return', 'interface', 'this', 'super', 'final', 'static']
ERROR = ['try',
         'catch', 'finally']
bool_const = ['True', 'False']
id = r'^[A-Za-z_]+[A-Za-z0-9_]*'
# word_break = ['+', '-', '*', '/', '%', '=', '!', '<', '>', '&', '|',
#               '(', ')', '{', '}', '[', ']', ':', ',', ';', ' ', '.', '"', '\n', "'"]
word_break1 = [' ', ',', ':', '!', '<', '>', '&', '|', ';', '\n']

# Error reporting


class Error:
    def __init__(self, error_name, details, line):
        self.error_name = error_name
        self.details = details
        self.line = line

    # return error as string

    def asString(self):
        result = f'{self.error_name}: {self.details} line:{self.line}\n'
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        f.write(
            f'({self.error_name},{self.details},{self.line})\n')
        return result

    # for not allowed characters


class IllegalCharError(Error):
    def __init__(self, details, line):
        super().__init__('Illegal Character', details, line)


class ExpectedCharError(Error):
    def __init__(self, details, line):
        super().__init__('Expected Character', details, line)


class InvalidSyntaxError(Error):
    def __init__(self, line, details=''):
        super().__init__('Invalid Syntax', details, line)

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
            # print('aaaa', self.line)
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
tokens = []


class Lexer:
    # constructor
    def __init__(self, file_name, text, line_no):
        self.line_no = line_no
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

        # open('../Token/token.txt', 'w').close()
        while(self.current_char != None):
            position_start = self.position.copy()
            char = self.current_char

            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '#':
                tokens.append(self.isComment())
                # self.advance()
            elif self.current_char == '\n':
                tokens.append(Token('New Line', self.line_no))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.isNumber())
                # self.advance()
            elif self.current_char in re.findall(id, self.current_char):
                tokens.append(self.isIdentifier())
                # self.advance()
            elif self.current_char == '"':
                tokens.append(self.isString())
                # self.advance()
            elif self.current_char == "'":
                tokens.append(self.isChar())
                # self.advance()
            elif self.current_char == '=':
                tokens.append(self.isEqual())
                # self.advance()
            elif self.current_char == '!':
                tokens.append(self.isNotEqual())
                # self.advance()
            elif self.current_char in Plus_Minus:
                tokens.append(self.isPlusMinus())
                # self.advance()
            elif self.current_char in Mul_Div_Mod:
                tokens.append(self.isMultiplicationDivideModulus())
                # self.advance()
            elif self.current_char == '^':
                tokens.append(self.isPower())
                # self.advance()
            elif self.current_char in Brackets:
                tokens.append(self.isBracket())
                self.advance()
            elif self.current_char == ';':
                tokens.append(self.isSemicolon())
                # tokens.append(
                #     Token(self.current_char, self.current_char, self.line_no))
                self.advance()
            elif self.current_char in Relational_Operation:
                tokens.append(self.isRelationalOperator())
                # self.advance()
            elif self.current_char in And_Logical:
                tokens.append(self.isAND())
                # self.advance()
            elif self.current_char in OR_Logical:
                tokens.append(self.isOR())
                # self.advance()
            elif self.current_char == ',':
                # tokens.append(
                #     Token(self.current_char, self.current_char, self.line_no))
                # self.advance()
                tokens.append(self.isComma())
            elif self.current_char == ':':
                tokens.append(
                    Token(self.current_char, self.current_char, self.line_no))
                self.advance()
            elif self.current_char == '.':
                tokens.append(self.isDot())
            elif self.current_char == 'True' or self.current_char == 'False':
                tokens.append(self.isBool())
                # self.advance()
            else:
                self.advance()
                return [], IllegalCharError("'" + char + "'", self.line_no)

        return tokens, None

    def isBool(self):
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        bool = ''
        while self.current_char != None and (self.current_char == 'True' or
                                             self.current_char == 'False'):
            if (self.current_char == 'True' or
                    self.current_char == 'False'):
                bool += self.current_char
                self.advance()
            token_type = 'bool_const'
        f.write(f'({token_type},{self.current_char},{self.line_no})\n')
        return Token(token_type, self.current_char, self.line_no)

    def isComma(self):
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        comma = ''
        while self.current_char != None and self.current_char == ',':
            if self.current_char == ',':
                comma += self.current_char
                self.advance()
            token_type = 'comma'
        f.write(f'({token_type},{token_type},{self.line_no})\n')
        return Token(token_type, token_type, self.line_no)

    def isDot(self):
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        dot = ''
        while self.current_char != None and self.current_char == '.':
            if self.current_char == '.':
                dot += self.current_char
                self.advance()
            token_type = '.'
        f.write(f'({token_type},{self.current_char},{self.line_no})\n')
        return Token(token_type, self.current_char, self.line_no)

    def isOR(self):
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        OR = ''
        while self.current_char != None and self.current_char in OR_Logical:
            if self.current_char == '|':
                OR += self.current_char
                self.advance()
                if self.current_char == '|':
                    OR += self.current_char
            token_type = 'OR'
        f.write(f'({token_type},{self.current_char},{self.line_no})\n')
        return Token(token_type, self.current_char, self.line_no)

    def isAND(self):
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')

        while self.current_char != None and self.current_char in And_Logical:
            AND = ''
            if self.current_char == '&':
                AND += self.current_char
                self.advance()
                if self.current_char == '&':
                    AND += self.current_char
            token_type = 'AND'
        f.write(f'({token_type},{self.current_char},{self.line_no})\n')
        return Token(token_type, self.current_char, self.line_no)

    def isPower(self):
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')

        while self.current_char != '^' and self.current_char != None:
            power = ''
            power += self.current_char
            self.advance()
        f.write(f'(Power,{self.current_char},{self.line_no})\n')
        return Token('Power', self.current_char, self.line_no)

    def isNotEqual(self):
        isneq = ''
        isneq += self.current_char
        position_start = self.position.copy()
        char = self.current_char
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        self.advance()

        if self.current_char == '=':
            isneq += self.current_char
            self.advance()
            f.write(f'(NEQ,{isneq},{self.line_no})\n')
            return Token('NEQ', isneq, self.line_no)
        elif self.current_char == '!':
            isneq += self.current_char
            self.advance()
            f.write(
                f'(ExpectedCharError after,{isneq},{self.line_no})\n')
            return ExpectedCharError(" = (after !)", self.line_no)
        self.advance()
        f.write(f'(NOT,{isneq},{self.line_no})\n')
        return Token('NOT', isneq, self.line_no)

    def isEqual(self):
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        token_type = 'EQ'
        self.advance()

        if self.current_char == '=':
            token_type = 'RO'
            self.advance()
        f.write(f'({token_type},{token_type},{self.line_no})\n')
        return Token(token_type, token_type, self.line_no)

    def isComment(self):
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        self.advance()

        while self.current_char != '\n' or self.current_char != '#':
            self.advance()

        self.advance()
        f.write(f'(Comment,{self.current_char},{self.line_no})\n')
        return Token('Comment', self.current_char, self.line_no)

    def isIdentifier(self):
        # writing tokens
        token_type = ''
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        id_str = ''
        position_start = self.position.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()
        #     if self.current_char == '.':
        #         token_type = 'Identifier can not have .'
        #         # f.write(f'({token_type},{id_str},{self.line_no})\n')
        #         break
        #     elif self.current_char == '-':
        #         token_type = 'Identifiers can not have -'
        #         break
        #     # return Token(token_type, id_str, self.line_no)
        # else:
        if id_str in Key_words:
            token_type = id_str
        elif id_str in OOP:
            token_type = id_str
        elif id_str in ERROR:
            token_type = id_str
        elif id_str in bool_const:
            token_type = 'bool_const'
        else:
            token_type = 'Identifier'

        f.write(f'({token_type},{id_str},{self.line_no})\n')
        return Token(token_type, id_str, self.line_no)

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
        f.write(f'(string_const,{string},{self.line_no})\n')
        return Token('string_const', string, self.line_no)

    def isChar(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        char = ''
        count = 0
        position_start = self.position.copy()
        escape_character = False
        self.advance()

        # escape_characters = {
        #     'n': '\n',
        #     't': '\t'
        # }
        while self.current_char != None and self.current_char not in "'":
            # if escape_character:
            #     char += escape_characters.get(self.current_char,
            #                                   self.current_char)
            # else:
            # if self.current_char == '\\':
            #     escape_character = True
            # else:
            char += self.current_char
            count += 1
            self.advance()
            # escape_character = False

        self.advance()
        if count > 1:
            f.write(
                f'(char can not be more than one character,{char},{self.line_no})\n')
            return Token('char can not be more than one character', char, self.line_no)
        else:
            f.write(f'(char_const,{char},{self.line_no})\n')
            return Token('char_const', char, self.line_no)

    # def isString(self):
    #     # writing tokens
    #     f = open(
    #         r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
    #     string = ''
    #     position_start = self.position.copy()
    #     escape_character = False
    #     self.advance()

    #     escape_characters = {
    #         'n': '\n',
    #         't': '\t'
    #     }
    #     while self.current_char != None and (self.current_char != '"' or escape_character):
    #         if escape_character:
    #             string += escape_characters.get(self.current_char,
    #                                             self.current_char)
    #         else:
    #             if self.current_char == '\\':
    #                 escape_character = True
    #             else:
    #                 string += self.current_char
    #             self.advance()
    #             escape_character = False

    #     self.advance()
    #     f.write(f'(String,{string},{self.line_no})\n')
    #     return Token('String', string, self.line_no)

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

            f.write(f'(int_const,{int(num_str)},{self.line_no})\n')
            return Token('int_const', int(num_str), self.line_no)
        else:
            f.write(f'(float_const,{float(num_str)},{self.line_no})\n')
            return Token('float_const', float(num_str), self.line_no)

    def isPlusMinus(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')

        position_start = self.position.copy()
        token_type = ''
        while self.current_char != None and self.current_char in Plus_Minus:
            comp_str = ''
            if self.current_char == '+':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                elif self.current_char == '+':
                    comp_str += self.current_char
                if comp_str in Compound:
                    token_type = 'Compound'
                elif comp_str in Increment_Decrement:
                    token_type = 'Inc-Dec'
                else:
                    token_type = 'PM'
                f.write(f'({token_type},{comp_str},{self.line_no})\n')
                self.advance()
                return Token(token_type, comp_str, self.line_no)

            else:
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                elif self.current_char == '-':
                    comp_str += self.current_char
                if comp_str in Compound:
                    token_type = 'Compound'
                elif comp_str in Increment_Decrement:
                    token_type = 'Inc-Dec'
                else:
                    token_type = 'PM'
                f.write(f'({token_type},{comp_str},{self.line_no})\n')
                self.advance()
                return Token(token_type, comp_str, self.line_no)

    def isMultiplicationDivideModulus(self):
        # writing tokens

        position_start = self.position.copy()
        token_type = ''
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        while self.current_char != None and self.current_char in Mul_Div_Mod:
            comp_str = ''
            if self.current_char == '*':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'Compound' if comp_str in Compound else 'MDM'
                f.write(f'({token_type},{comp_str},{self.line_no})\n')
                return Token(token_type, comp_str, self.line_no)
            elif self.current_char == '/':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'Compound' if comp_str in Compound else 'MDM'
                f.write(f'({token_type},{comp_str},{self.line_no})\n')
                return Token(token_type, comp_str, self.line_no)
            else:
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'Compound' if comp_str in Compound else 'MDM'
                f.write(f'({token_type},{comp_str},{self.line_no})\n')
                return Token(token_type, comp_str, self.line_no)

    def isRelationalOperator(self):
        # writing tokens
        position_start = self.position.copy()
        token_type = ''
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        while self.current_char != None and self.current_char in Relational_Operation:
            comp_str = ''
            if self.current_char == '<':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'RO'
                f.write(f'({token_type},{comp_str},{self.line_no})\n')
                return Token(token_type, comp_str, self.line_no)
            elif self.current_char == '>':
                comp_str += self.current_char
                self.advance()
                if self.current_char == '=':
                    comp_str += self.current_char
                token_type = 'RO'
                f.write(f'({token_type},{comp_str},{self.line_no})\n')
                return Token(token_type, comp_str, self.line_no)
            # elif self.current_char == '!':
            #     comp_str += self.current_char
            #     self.advance()
            #     if self.current_char == '=':
            #         comp_str += self.current_char
            #     token_type = 'RO'
            #     f.write(f'({token_type},{comp_str},{self.position.line+1})\n')
            #     return Token(token_type, comp_str, self.position.line+1)
            else:
                comp_str += self.current_char
                self.advance()
                # if self.current_char == '=':
                #     comp_str += self.current_char
                token_type = 'RO'
                f.write(f'({token_type},{comp_str},{self.line_no})\n')
                return Token(token_type, comp_str, self.line_no)

    def isBracket(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        while self.current_char != None and self.current_char in Brackets:
            f.write(
                f'({self.current_char},{self.current_char},{self.line_no})\n')
            return Token(self.current_char, self.current_char, self.line_no)

    def isSemicolon(self):
        # writing tokens
        f = open(
            r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
        while self.current_char != None and self.current_char == ';':
            f.write(
                f'({self.current_char},{self.current_char},{self.line_no})\n')
            return Token(self.current_char, self.current_char, self.line_no)

# semantic structure


class MDT:
    def __init__(self, Name, Type, TypeModifier, Extends, Implements):
        self.Name = Name
        self.Type = Type
        self.TypeModifier = TypeModifier
        self.Extends = Extends
        self.Implements = Implements


class CDT:
    def __init__(self, Name, Type, AccessModifier, Static, Final, RefofCT):
        self.Name = Name
        self.Type = Type
        self.AccessModifier = AccessModifier
        self.Static = Static
        self.Final = Final
        self.RefofCT = RefofCT


class FDT:
    def __init__(self, Name, Type, Scope, Final):
        self.Name = Name
        self.Type = Type
        self.Scope = Scope
        self.Final = Final


MDTA = []
FDTA = []
CDTA = []
Scope_Stack = []


class Semantic_Analyzer:
    def __init__(self):
        pass

    def insertMDT(self, Name, Type, TypeModifier, Extends, Implements):

        MDTA.append(MDT(Name, Type, TypeModifier, Extends, Implements))

    def insertCDT(self, Name, Type, AccessModifier, Static, Final, RefofCT):
        CDTA.append(CDT(Name, Type, AccessModifier, Static, Final, RefofCT))

    def insertFDT(self, Name, Type, Scope, Final):
        FDTA.append(FDT(Name, Type, Scope, Final))

    def lookupMDT(self, Name, Type):
        for obj in MDTA:
            if(obj.Name == Name and obj.Type == Type):
                if(obj.Type != 'class'):
                    print("wrong type")
                elif(obj.TypeModifier == 'final'):
                    print("can't be extended")
                else:
                    return obj.Name + ' ' + obj.Type + ' ' + obj.TypeModifier + ' ' + obj.Extends + ' ' + obj.Implements
            return None

    def lookupCDT(self, Name, RefofCT):
        for obj in CDTA:
            if(obj.Name == Name and obj.RefofCT == RefofCT):
                return obj.Name + ' ' + obj.Type + ' ' + obj.AccessModifier + ' ' + obj.Static + ' ' + obj.Final + ' ' + obj.RefofCT
            return False

    def lookupCDTF(self, Name, RefofCT, Parameters):
        for obj in CDTA:
            if(obj.Name == Name and obj.RefofCT == RefofCT and obj.Type == Parameters):
                return obj.Name + ' ' + obj.Type + ' ' + obj.AccessModifier + ' ' + obj.Static + ' ' + obj.Final + ' ' + obj.RefofCT
            return False

    def lookupFDT(self, Name, Scope_Stack):
        for obj in FDTA:
            if(obj.Name == Name):
                for sc in Scope_Stack:
                    if(obj.Scope == sc):
                        return obj.Name + ' ' + obj.Type + ' ' + obj.Scope + ' ' + obj.Final
            return False

    def CreateScope(self, scope):
        Scope_Stack.append(scope)

    def DestroyScope(self):
        Scope_Stack.pop()

    def Print_Tables(self):
        print("Main Table")
        for obj in MDTA:
            print('Name: '+obj.Name + ' ' + 'Type: '+obj.Type + ' ' + 'TM: '+obj.TypeModifier +
                  ' ' + 'Ext: '+obj.Extends + ' ' +'Impl: ' +obj.Implements + '\n')
        print("Class Table")
        for obj in CDTA:
            print('Name: '+obj.Name + ' ' + 'Type: '+obj.Type + ' ' + 'AM: '+obj.AccessModifier +
                  ' ' + 'Static: '+obj.Static + ' ' + 'Final: '+obj.Final + ' ' + 'Class Ref: '+obj.RefofCT + '\n')
        print("Function Table")
        for obj in FDTA:
            print('Name: '+obj.Name + ' ' + 'Type: '+obj.Type + ' ' +
                  'Scope: '+obj.Scope + ' ' + 'Final: '+obj.Final + '\n')

    def CheckCompatibility(self, left_type, right_type, operator):
        return None

    def CheckCompatibilityOT(self, operand_type, operator):
        return None


token_index = 0
Sem = Semantic_Analyzer()
# global A,F,S,T,N,TM,E,I

A = ''
F = ''
ST = ''
T = ''
N = ''
TM = ''
E = ''
I = ''
AM = ''
RefofCT = ''
TF = ''
TFT = ''
SC = 0
class SyntaxAnalyzer:
    global token_index
    global A, F, ST, T, N, TM, E, I, AM, RefofCT, TF, TFT, SC
    # global semantic

    def __init__(self, token, value):
        self.token = token
        self.value = value
        self.token_index = token_index
        self.token_index = 0
        self.SC = SC
        self.SC = 0
        self.A = A
        self.A = ''
        self.TF = TF
        self.TF = ''
        self.TFT = TFT
        self.TFT = ''
        self.RefofCT = RefofCT
        self.RefofCT = ''
        self.AM = AM
        self.AM = ''
        self.F = F
        self.F = ''
        self.ST = ST
        self.ST = ''
        self.T = T
        self.T = ''
        self.N = N
        self.N = ''
        self.TM = TM
        self.TM = ''
        self.E = E
        self.E = ''
        self.I = I
        self.I = ''
        print(self.Validate())
        # self.semantic = semantic
        # self.semantic = Semantic_Analyzer()
        # self.semantic.Print_Tables()

    def Validate(self):
        if(self.S()):
            if(self.token[self.token_index] == "$"):
                Sem.Print_Tables()
                return True
        return False

    def S(self):
        if(self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or self.token[self.token_index] == 'while' or
           self.token[self.token_index] == 'int' or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or self.token[self.token_index] == 'float' or
           self.token[self.token_index] == 'char' or self.token[self.token_index] == 'public' or self.token[self.
                                                                                                            token_index] == 'private' or self.token[self.token_index] == 'protected' or
           self.token[self.token_index] == 'final' or self.token[self.token_index] == 'this' or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break' or
           self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func' or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec' or
           self.token[self.token_index] == 'Inc-Dec' or self.token[self.token_index] == '' or
           self.token[self.token_index] == 'try' or self.token[self.token_index] == 'Array' or self.token[self.token_index] == '$'):

            if(self.SST()):
                print("SST passed")
                print(self.token[self.token_index])
                if(self.S()):
                    print(self.token[self.token_index])
                    print("S passed")
                    return True
                elif(self.token[self.token_index] == '$'):
                    print("S passed")
                    return True
        return False

    def SST(self):
        if(self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or self.token[self.token_index] == 'while' or
           self.token[self.token_index] == 'int' or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or self.token[self.token_index] == 'float' or
           self.token[self.token_index] == 'char' or self.token[self.token_index] == 'public' or self.token[self.
                                                                                                            token_index] == 'private' or self.token[self.token_index] == "protected" or
           self.token[self.token_index] == 'final' or self.token[self.token_index] == 'this' or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break' or
           self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func' or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec' or
           self.token[self.token_index] == 'Inc-Dec' or self.token[self.token_index] == 'try' or self.token[self.token_index] == 'Array'):
            if(self.FST()):
                print("For passed")
                return True
            elif(self.IfElse()):
                return True
            elif(self.WST()):
                return True
            elif(self.Try()):
                return True
            elif(self.DecST()):
                print(True)
                return True
            elif(self.ClassDef()):
                return True
            # elif(self.ClassBody2()):
            #     return True
            elif(self.AssignST()):
                return True
            elif(self.Cont()):
                if(self.token[self.token_index] == ";"):
                    self.token_index += 1
                    return True
                return False
            elif(self.Break()):
                if(self.token[self.token_index] == ";"):
                    self.token_index += 1
                    return True
                return False
            elif(self.token[self.token_index] == 'return'):
                self.token_index += 1
                if(self.OE()):
                    if(self.token[self.token_index] == ";"):
                        self.token_index += 1
                        return True
                return False
            elif(self.Dict()):
                return True
            elif(self.FuncDef()):
                return True
            elif(self.token[self.token_index] == 'Identifier'):
                self.token_index += 1
                if(self.ObjectDef()):
                    if(self.token[self.token_index] == ";"):
                        self.token_index += 1
                        return True
                return False
            elif(self.token[self.token_index] == "this"):
                self.token_index += 1
                if(self.token[self.token_index] == "."):
                    self.token_index += 1
                    if(self.token[self.token_index] == 'Identifier'):
                        self.token_index += 1
                        if(self.K()):
                            if(self.token[self.token_index] == ";"):
                                self.token_index += 1
                                return True
                return False
            elif(self.IncDec()):
                if(self.This()):
                    if(self.token[self.token_index] == 'Identifier'):
                        self.token_index += 1
                        if(self.Z2() == True):
                            if(self.token[self.token_index] == ";"):
                                self.token_index += 1
                                return True
                return False
            elif(self.Array()):
                return True
        return False

    def Array(self):
        if(self.token[self.token_index] == 'Array'):
            if(self.token[self.token_index] == 'Array'):
                self.token_index += 1
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    if(self.token[self.token_index] == 'EQ'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '['):
                            self.token_index += 1
                            if(self.AValues()):
                                if(self.token[self.token_index] == ']'):
                                    self.token_index += 1
                                    if(self.token[self.token_index] == ';'):
                                        self.token_index += 1
                                        return True
        return False

    def AValues(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
           or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == 'this' or self.token[self.token_index] == '['
           or self.token[self.token_index] == '' or self.token[self.token_index] == ']'):
            if(self.token[self.token_index] == ']'):
                return True
            elif(self.OE()):
                if(self.AValues2()):
                    return True
            elif(self.token[self.token_index] == '['):
                self.token_index += 1
                if(self.ArrayPos()):
                    if(self.token[self.token_index] == ']'):
                        self.token_index += 1
                        if(self.AValues2()):
                            return True
        return False

    def AValues2(self):
        if(self.token[self.token_index] == ',' or self.token[self.token_index] == ''
           or self.token[self.token_index] == ']'):
            if(self.token[self.token_index] == ']'):
                return True
            elif(self.token[self.token_index] == ','):
                self.token_index += 1
                if(self.OE()):
                    if(self.AValues2()):
                        return True
            elif(self.token[self.token_index] == ','):
                self.token_index += 1
                if(self.token[self.token_index] == '['):
                    self.token_index += 1
                    if(self.ArrayPos()):
                        if(self.token[self.token_index] == ']'):
                            self.token_index += 1
                            if(self.AValues2()):
                                return True
        return False

    def ArrayPos(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
           or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == 'this' or self.token[self.token_index] == ']'
           or self.token[self.token_index] == ''):
            if(self.token[self.token_index] == ']'):
                if(self.token[self.token_index] == ']'):
                    return True
                elif(self.OE()):
                    if(self.ArrayPos2()):
                        return True
        return False

    def ArrayPos2(self):
        if(self.token[self.token_index] == ',' or self.token[self.token_index] == ''
           or self.token[self.token_index] == ']'):
            if(self.token[self.token_index] == ']'):
                return True
            elif(self.token[self.token_index] == ','):
                self.token_index += 1
                if(self.OE()):
                    if(self.ArrayPos2()):
                        return True
        return False

    def K(self):
        if(self.token[self.token_index] == '.' or self.token[self.token_index] == '{' or
           self.token[self.token_index] == '(' or self.token[self.token_index] == 'EQ' or
           self.token[self.token_index] == ';' or self.token[self.token_index] == ''):
            if(self.Z2()):
                return True
            elif(self.token[self.token_index] == 'EQ'):
                self.token_index += 1
                if(self.OE()):
                    return True
        return False

    def ObjectDef(self):
        if(self.token[self.token_index] == '.' or
           self.token[self.token_index] == 'EQ' or self.token[self.token_index] == 'Compound' or
           self.token[self.token_index] == '[' or self.token[self.token_index] == '(' or
           self.token[self.token_index] == 'Inc-Dec'):
            if(self.token[self.token_index] == 'EQ'):
                self.token_index += 1
                if(self.token[self.token_index] == 'new'):
                    self.token_index += 1
                    if(self.CName()):
                        if(self.token[self.token_index] == '('):
                            self.token_index += 1
                            if(self.token[self.token_index] == ')'):
                                self.token_index += 1
                                return True
                elif(self.Z()):
                    return True
        return False

    def Z(self):
        if(self.token[self.token_index] == '.' or self.token[self.token_index] == 'EQ' or
           self.token[self.token_index] == 'Compound' or self.token[self.token_index] == '[' or
           self.token[self.token_index] == '(' or
           self.token[self.token_index] == 'Inc-Dec'):
            if(self.token[self.token_index] == '.'):
                self.token_index += 1
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    if(self.R1()):
                        return True
            elif(self.token[self.token_index] == '['):
                self.token_index += 1
                if(self.token[self.token_index] == 'int_const'):
                    self.token_index += 1
                    if(self.token[self.token_index] == ']'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.R1()):
                                    return True
            elif(self.token[self.token_index] == '('):
                self.token_index += 1
                if(self.Parameter()):
                    if(self.token[self.token_index] == ')'):
                        self.token_index += 1
                        if(self.R2()):
                            return True
            elif(self.XColon()):
                return True
            return False

    def R1(self):
        if(self.token[self.token_index] == '.' or self.token[self.token_index] == '[' or
           self.token[self.token_index] == '(' or self.token[self.token_index] == '' or
           self.token[self.token_index] == ';' or self.token[self.token_index] == 'AND' or
           self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'OR' or
           self.token[self.token_index] == 'MDM' or self.token[self.token_index] == 'PM' or
           self.token[self.token_index] == ',' or self.token[self.token_index] == ')'):
            if(self.token[self.token_index] == '.'):
                self.token_index += 1
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    if(self.Z()):
                        return True
            elif(self.token[self.token_index] == '['):
                self.token_index += 1
                if(self.token[self.token_index] == 'int_const'):
                    self.token_index += 1
                    if(self.token[self.token_index] == ']'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.Z()):
                                    return True
            elif(self.token[self.token_index] == '('):
                self.token_index += 1
                if(self.Parameter()):
                    if(self.token[self.token_index] == ')'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.Z()):
                                    return True
            elif(self.token[self.token_index] == ';' or self.token[self.token_index] == 'AND' or
                 self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'OR' or
                 self.token[self.token_index] == 'MDM' or self.token[self.token_index] == 'PM' or
                 self.token[self.token_index] == ',' or self.token[self.token_index] == ')'):
                return True
        return False

    def R2(self):
        if(self.token[self.token_index] == '.' or self.token[self.token_index] == '' or
           self.token[self.token_index] == ';' or self.token[self.token_index] == 'AND' or
           self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'OR' or
           self.token[self.token_index] == 'MDM' or self.token[self.token_index] == 'PM' or
           self.token[self.token_index] == ',' or self.token[self.token_index] == ')'):
            if(self.token[self.token_index] == '.'):
                self.token_index += 1
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    if(self.B()):
                        return True
            elif(self.token[self.token_index] == ';' or self.token[self.token_index] == 'AND' or
                 self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'OR' or
                 self.token[self.token_index] == 'MDM' or self.token[self.token_index] == 'PM' or
                 self.token[self.token_index] == ',' or self.token[self.token_index] == ')'):
                return True
        return False

    def B(self):
        if(self.token[self.token_index] == '.' or self.token[self.token_index] == '(' or
           self.token[self.token_index] == '[' or self.token[self.token_index] == 'EQ' or
           self.token[self.token_index] == 'Compound' or self.token[self.token_index] == 'Inc-Dec'):
            if(self.Z2()):
                return True
            elif(self.XColon()):
                return True
        return False

    def XColon(self):
        if(self.token[self.token_index] == 'EQ' or self.token[self.token_index] == 'Compound' or
           self.token[self.token_index] == 'Inc-Dec'):
            if(self.AssignOP()):
                if(self.OE()):
                    return True
            elif(self.IncDec()):
                return True
        return False

    def Z2(self):
        if(self.token[self.token_index] == '.' or self.token[self.token_index] == '[' or
           self.token[self.token_index] == '(' or self.token[self.token_index] == '' or
           self.token[self.token_index] == 'MDM' or self.token[self.token_index] == 'PM'
           or self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'AND'
           or self.token[self.token_index] == 'OR' or self.token[self.token_index] == ','
           or self.token[self.token_index] == ')' or self.token[self.token_index] == ';'):
            if(self.token[self.token_index] == '.'):
                self.token_index += 1
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    if(self.R1Colon()):
                        return True
            elif(self.token[self.token_index] == '['):
                self.token_index += 1
                if(self.token[self.token_index] == 'int_const'):
                    self.token_index += 1
                    if(self.token[self.token_index] == ']'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.R1Colon()):
                                    return True
            elif(self.token[self.token_index] == '('):
                self.token_index += 1
                if(self.Parameter()):
                    if(self.token[self.token_index] == ')'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.R1Colon()):
                                    return True
            elif(self.token[self.token_index] == 'MDM' or self.token[self.token_index] == 'PM'
                 or self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'AND'
                 or self.token[self.token_index] == 'OR' or self.token[self.token_index] == ','
                 or self.token[self.token_index] == ')' or self.token[self.token_index] == ';'):
                return True
            return False

    def R1Colon(self):
        if(self.token[self.token_index] == '.' or self.token[self.token_index] == '[' or
           self.token[self.token_index] == '(' or self.token[self.token_index] == '' or
           self.token[self.token_index] == 'MDM' or self.token[self.token_index] == 'PM'
           or self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'AND'
           or self.token[self.token_index] == 'OR' or self.token[self.token_index] == ','
           or self.token[self.token_index] == ')' or self.token[self.token_index] == ';'):
            if(self.token[self.token_index] == '.'):
                self.token_index += 1
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    if(self.Z2()):
                        return True
            elif(self.token[self.token_index] == '['):
                self.token_index += 1
                if(self.token[self.token_index] == 'int_const'):
                    self.token_index += 1
                    if(self.token[self.token_index] == ']'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.Z2()):
                                    return True
            elif(self.token[self.token_index] == '('):
                self.token_index += 1
                if(self.Parameter()):
                    if(self.token[self.token_index] == ')'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.Z2()):
                                    return True
            elif(self.token[self.token_index] == 'MDM' or self.token[self.token_index] == 'PM'
                 or self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'AND'
                 or self.token[self.token_index] == 'OR' or self.token[self.token_index] == ','
                 or self.token[self.token_index] == ')' or self.token[self.token_index] == ';'):
                return True
            return False

    def WST(self):
        if(self.token[self.token_index] == 'while'):
            if(self.token[self.token_index] == 'while'):
                self.N = self.value[self.token_index]
                self.token_index += 1
                if(self.token[self.token_index] == '('):
                    self.SC = self.SC+1
                    Sem.CreateScope(self.SC)
                    self.token_index += 1
                    if(self.OE()):
                        Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                        if(self.token[self.token_index] == ')'):
                            self.token_index += 1
                            if(self.token[self.token_index] == '{'):
                                self.token_index += 1
                                if(self.Body1()):
                                    Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                                    return True
            return False

    def FST(self):
        if(self.token[self.token_index] == 'for'):
            if(self.token[self.token_index] == 'for'):
                self.N = self.value[self.token_index]
                self.token_index += 1
                if(self.token[self.token_index] == '('):
                    self.SC = self.SC+1
                    Sem.CreateScope(self.SC)
                    self.token_index += 1
                    if(self.C1()):
                        Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                        print("c1 passed")
                        if(self.C2()):
                            if(self.token[self.token_index] == ';'):
                                Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                                self.token_index += 1
                                print("c2 passed")
                                if(self.C3()):
                                    Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                                    print("c3 passed")
                                    print(self.token[token_index+1])
                                    if(self.token[token_index] == ')'):
                                        self.token_index += 1
                                        print("c3 passed 1")
                                        if(self.token[self.token_index] == '{'):
                                            self.token_index += 1
                                            if(self.Body1()):
                                                Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                                                print("body1 passed")
                                                return True
        return False

    def C1(self):
        if(self.token[self.token_index] == ';' or self.token[self.token_index] == 'int' or self.token[self.token_index] == 'char' or
           self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float' or
           self.token[self.token_index] == 'bool' or self.token[self.token_index] == 'this' or self.token[self.token_index] == 'Identifier'):
            if(self.token[self.token_index] == ';'):
                self.token_index += 1
                return True
            elif(self.DecST()):
                return True
            elif(self.AssignST()):
                return True
        return False

    def C2(self):
        if(self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'int_const'
           or self.token[self.token_index] == 'string_const' or self.token[self.token_index] == 'float_const' or
           self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '(' or self.token[self.token_index] == 'NOT' or
           self.token[self.token_index] == 'Inc-Dec' or self.token[self.token_index] == 'this' or self.token[self.token_index] == '' or
           self.token[self.token_index] == ';'):
            if(self.OE()):
                return True
            elif(self.token[self.token_index] == ';'):
                return True
        return False

    def C3(self):
        if(self.token[self.token_index] == 'this' or
           self.token[self.token_index] == '' or self.token[self.token_index] == ')'
           or self.token[self.token_index] == 'Identifier'):
            print("in c3")
            if(self.This()):
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    print("This passed")
                    if(self.IncDec()):
                        print("incdec passed")
                        print(self.token[self.token_index])
                        return True
            elif(self.This()):
                print("incdec passed 1")
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    if(self.AssignOP()):
                        if(self.OE()):
                            return True
                return False
            elif(self.token[self.token_index] == ')'):
                return True
        return False

    def X1(self):
        if(self.token[self.token_index] == '.' or self.token[self.token_index] == '[' or
           self.token[self.token_index] == '('):
            if(self.token[self.token_index] == '.'):
                self.token_index += 1
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    if(self.X()):
                        return True
            elif(self.token[self.token_index] == '['):
                self.token_index += 1
                if(self.token[self.token_index] == 'int_const'):
                    self.token_index += 1
                    if(self.token[self.token_index] == ']'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.X()):
                                    return True
            elif(self.token[self.token_index] == '('):
                self.token_index += 1
                if(self.Parameter()):
                    if(self.token[self.token_index] == ')'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.X()):
                                    return True
            return False

    def X(self):
        if(self.token[self.token_index] == '.' or self.token[self.token_index] == '(' or
           self.token[self.token_index] == '[' or self.token[self.token_index] == 'EQ' or
           self.token[self.token_index] == 'Compound' or self.token[self.token_index] == 'Inc-Dec'):
            if(self.token[self.token_index] == '.'):
                self.token_index += 1
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    if(self.X()):
                        return True
            elif(self.AssignOP()):
                if(self.OE()):
                    return True
            elif(self.token[self.token_index] == '('):
                self.token_index += 1
                if(self.Parameter()):
                    if(self.token[self.token_index] == ')'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.X()):
                                    return True
            elif(self.IncDec()):
                return True
            elif(self.token[self.token_index] == '['):
                self.token_index += 1
                if(self.token[self.token_index] == 'int_const'):
                    self.token_index += 1
                    if(self.token[self.token_index] == ']'):
                        self.token_index += 1
                        if(self.token[self.token_index] == '.'):
                            self.token_index += 1
                            if(self.token[self.token_index] == 'Identifier'):
                                self.token_index += 1
                                if(self.X()):
                                    return True
        return False

    def IfElse(self):
        if(self.token[self.token_index] == 'if'):
            if(self.token[self.token_index] == 'if'):
                self.N = self.value[self.token_index]
                self.token_index += 1
                if(self.token[self.token_index] == '('):
                    self.SC = self.SC+1
                    Sem.CreateScope(self.SC)
                    self.token_index += 1
                    if(self.OE()):
                        if(self.token[self.token_index] == ')'):
                            Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                            self.token_index += 1
                            if(self.token[self.token_index] == '{'):
                                self.token_index += 1
                                print("if oe passed")
                                if(self.Body1()):
                                    print("Body 1 passed")
                                    print(self.token[self.token_index])
                                    if(self.Else()):
                                        print("else passed")
                                        return True
        return False

    def Else(self):
        if(self.token[self.token_index] == 'else' or
           self.token[self.token_index] == '' or self.token[self.token_index] == 'while'
           or self.token[self.token_index] == 'for' or
           self.token[self.token_index] == 'if' or self.token[self.token_index] == 'continue' or
           self.token[self.token_index] == 'break' or self.token[self.token_index] == 'return' or
            self.token[self.token_index] == 'Identifier' or
           self.token[self.token_index] == 'this' or self.token[self.token_index] == 'Inc-Dec' or
           self.token[self.token_index] == 'int' or self.token[self.token_index] == 'String' or
           self.token[self.token_index] == 'bool' or self.token[self.token_index] == 'public' or
           self.token[self.token_index] == 'private' or self.token[self.token_index] == 'protected' or
           self.token[self.token_index] == 'final' or self.token[self.token_index] == 'func' or
           self.token[self.token_index] == '$' or
           self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char' or
            self.token[self.token_index] == 'try'
           or self.token[self.token_index] == 'Array' or self.token[self.token_index] == 'except'
           or self.token[self.token_index] == 'finally'):
            if(self.token[self.token_index] == 'else'):
                self.N = self.value[self.token_index]
                self.token_index += 1
                if(self.token[self.token_index] == '{'):
                    self.SC = self.SC+1
                    Sem.CreateScope(self.SC)
                    self.token_index += 1
                    if(self.Body1()):
                        Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                        return True
            elif(self.token[self.token_index] == 'while'
                 or self.token[self.token_index] == 'for' or
                 self.token[self.token_index] == 'if' or self.token[self.token_index] == 'continue' or
                 self.token[self.token_index] == 'break' or self.token[self.token_index] == 'return' or
                 self.token[self.token_index] == 'Identifier' or
                 self.token[self.token_index] == 'this' or self.token[self.token_index] == 'Inc-Dec' or
                 self.token[self.token_index] == 'int' or self.token[self.token_index] == 'String' or
                 self.token[self.token_index] == 'bool' or self.token[self.token_index] == 'public' or
                 self.token[self.token_index] == 'private' or self.token[self.token_index] == 'protected' or
                 self.token[self.token_index] == 'final' or self.token[self.token_index] == 'func' or
                 self.token[self.token_index] == '$' or
                 self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char' or
                 self.token[self.token_index] == 'try'
                 or self.token[self.token_index] == 'Array' or self.token[self.token_index] == 'except'
                 or self.token[self.token_index] == 'finally'):
                return True
        return False

    def FuncDef(self):
        if(self.token[self.token_index] == "func"):
            if(self.token[self.token_index] == "func"):
                self.token_index += 1
                if(self.RetType()):
                    if(self.token[self.token_index] == "Identifier"):
                        self.token_index += 1
                        if(self.token[self.token_index] == "("):
                            self.SC = self.SC+1
                            print(self.SC)
                            Sem.CreateScope(self.SC)
                            self.token_index += 1
                            if(self.Parameter()):
                                if(self.token[self.token_index] == ")"):
                                    self.token_index += 1
                                    if(self.token[self.token_index] == '{'):
                                        self.token_index += 1
                                        if(self.Body1()):
                                            print("func body 1 passed")
                                            Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                                            return True
        return False

    # def Body(self):
    #     if(self.token[self.token_index] == ";" or self.token[self.token_index] == "{"):
    #         if(self.MST()):
    #             if(self.token[self.token_index] == '}'):
    #                 self.token_index += 1
    #                 return True
    #     return False

    def Body1(self):
        if(self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or
           self.token[self.token_index] == 'while' or self.token[self.token_index] == 'int' or
           self.token[self.token_index] == 'try' or
           self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or
           self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char'
           or self.token[self.token_index] == 'Array' or self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
           or self.token[self.token_index] == 'protected' or self.token[self.token_index] == 'final'
           or self.token[self.token_index] == 'this' or self.token[self.token_index] == '}'
           or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break'
           or self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == '' or self.token[self.token_index] == 'except'
           or self.token[self.token_index] == 'finally' or self.token[self.token_index] == '$'):
            if(self.MST()):
                if(self.token[self.token_index] == '}'):

                    # Sem.DestroyScope()
                    self.token_index += 1
                    return True
        return False

    def MST(self):
        if(self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or
           self.token[self.token_index] == 'while' or self.token[self.token_index] == 'try' or self.token[self.token_index] == 'int' or
           self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or
           self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char' or self.token[self.token_index] == 'Array'
           or self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
           or self.token[self.token_index] == 'protected'
           or self.token[self.token_index] == 'this'
           or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break'
           or self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == '' or self.token[self.token_index] == '}'):
            if(self.SST()):
                if(self.MST()):
                    return True
            elif(self.token[self.token_index] == '}'):
                return True

    def ClassDef(self):
        if(self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
           or self.token[self.token_index] == 'protected'):
            if(self.AccessModifier1()):
                if(self.ClassModifier()):
                    if(self.token[self.token_index] == "class"):
                        self.T = self.value[self.token_index]
                        self.token_index += 1
                        if(self.token[self.token_index] == "Identifier"):
                            self.N = self.value[self.token_index]
                            self.RefofCT = self.value[self.token_index]
                            self.token_index += 1
                            if(self.Inheritance()):
                                # Sem.insertMDT(
                                #     self.N, self.T, self.TM, self.E, self.I)
                                return True
            # elif(self.AccessModifier1()):
            #     if(self.ClassModifier()):
            #         if(self.token[self.token_index] == "class"):
            #             self.token_index += 1
            #             if(self.token[self.token_index] == "Identifier"):
            #                 self.token_index += 1
            #                 if(self.Inheritance()):
            #                     if(self.token[self.token_index] == "{"):
            #                         self.token_index += 1
            #                         if(self.ClassBody()):
            #                             if(self.token[self.token_index] == "}"):
            #                                 self.token_index += 1
            #                                 return True
        return False

    def ClassBody(self):
        if(self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
           or self.token[self.token_index] == 'protected'
           or self.token[self.token_index] == 'int' or
           self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or
           self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char' or
           self.token[self.token_index] == 'void' or
           self.token[self.token_index] == 'class' or self.token[self.token_index] == 'Identifier' or
           self.token[self.token_index] == '' or self.token[self.token_index] == '}'):
            print("class body")
            # self.AM = self.value[self.token_index]
            if(self.DT()):
                if(self.token[self.token_index] == "Identifier"):
                    self.N = self.value[self.token_index]
                    self.token_index += 1
                    if(self.ClassBody1()):
                        if(self.ClassBody()):
                            Sem.insertCDT(self.N, self.T, self.AM, self.ST, self.F, self.RefofCT)
                            # Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                            return True
            elif(self.AccessModifier()):
                print("func am passed")
                if(self.token[self.token_index] == "func"):
                    self.token_index += 1
                    if(self.ClassModifier()):
                        print("func cm passed")
                        if(self.ClassBody2()):
                            Sem.insertCDT(self.N, self.TF, self.AM, self.ST, self.F, self.RefofCT)
                            print(self.token[self.token_index])
                            if(self.ClassBody()):
                                print("in class body func")
                                # Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                                return True
            elif(self.AccessModifier1()):
                if(self.ClassModifier()):
                    if(self.token[self.token_index] == "class"):
                        self.T = self.value[self.token_index]
                        self.token_index += 1
                        if(self.token[self.token_index] == "Identifier"):
                            self.N = self.value[self.token_index]
                            Sem.insertCDT(self.N, self.T, self.AM, self.ST, self.F, self.RefofCT)
                            self.token_index += 1
                            if(self.Inheritance()):
                                # if(self.token[self.token_index] == "{"):
                                #     self.token_index += 1
                                #     if(self.ClassBody()):
                                #         if(self.token[self.token_index] == "}"):
                                #             self.token_index += 1
                                return True
            elif(self.token[self.token_index] == "Identifier"):
                self.token_index += 1
                if(self.ClassBody1()):
                    if(self.ClassBody()):
                        Sem.insertCDT(self.N, self.T, self.AM, self.ST, self.F, self.RefofCT)
                        return True
            elif(self.token[self.token_index] == "}"):
                return True
        print("class body")
        return False

    def ClassBody1(self):
        if(self.token[self.token_index] == 'EQ' or self.token[self.token_index] == ';'
           or self.token[self.token_index] == '('):
            if(self.Initialize()):
                if(self.List()):
                    return True
            elif(self.token[self.token_index] == '('):
                self.SC = self.SC+1
                print("func param start")
                self.token_index += 1
                if(self.Parameter()):
                    if(self.token[self.token_index] == ")"):
                        self.token_index += 1
                        if(self.token[self.token_index] == "{"):
                            self.token_index += 1
                            if(self.Body1()):
                                Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                                # if(self.token[self.token_index] == "}"):
                                #     self.token_index += 1
                                return True
        return False

    def ClassBody2(self):
        if(self.token[self.token_index] == 'void' or self.token[self.token_index] == 'int'
           or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float'
           or self.token[self.token_index] == 'char' or self.token[self.token_index] == 'bool'):
            if(self.RetType()):
                print("func ret passed")
                # self.token_index += 1
                if(self.token[self.token_index] == "Identifier"):
                    self.N = self.value[self.token_index]
                    self.token_index += 1
                    if(self.ClassBody1()):
                        print("func class body1 passed")
                        print(self.token[self.token_index])
                        return True
            # elif(self.token[self.token_index] == 'class'):
            #     self.token_index += 1
            #     if(self.token[self.token_index] == "Identifier"):
            #         self.token_index += 1
            #         if(self.Inheritance()):
            #             if(self.token[self.token_index] == "{"):
            #                 self.token_index += 1
            #                 if(self.ClassBody()):
            #                     if(self.token[self.token_index] == "}"):
            #                         self.token_index += 1
            #                         return True
        return False

    def AccessModifier(self):
        if(self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
           or self.token[self.token_index] == 'protected' or self.token[self.token_index] == '' or self.token[self.token_index] == 'void'
           or self.token[self.token_index] == 'int'
           or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float'
           or self.token[self.token_index] == 'char' or self.token[self.token_index] == 'bool'
           or self.token[self.token_index] == 'static' or self.token[self.token_index] == 'final'):
            if(self.token[self.token_index] == "public"):
                self.A = self.value[self.token_index]
                self.AM = self.value[self.token_index]
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == "private"):
                self.A = self.value[self.token_index]
                self.AM = self.value[self.token_index]
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == "protected"):
                self.A = self.value[self.token_index]
                self.AM = self.value[self.token_index]
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == 'void'
                 or self.token[self.token_index] == 'int'
                 or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float'
                 or self.token[self.token_index] == 'char' or self.token[self.token_index] == 'bool'
                 or self.token[self.token_index] == 'static' or self.token[self.token_index] == 'final'):
                return True
        return False

    def AccessModifier1(self):
        if(self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
           or self.token[self.token_index] == 'protected'):
            if(self.token[self.token_index] == "public"):
                # self.A = self.value[self.token_index]
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == "private"):
                # self.A = self.value[self.token_index]
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == "protected"):
                # self.A = self.value[self.token_index]
                self.token_index += 1
                return True
        return False

    def ClassModifier(self):
        if(self.token[self.token_index] == 'abstract' or self.token[self.token_index] == 'final'
           or self.token[self.token_index] == '' or self.token[self.token_index] == 'class'
           or self.token[self.token_index] == 'void' or self.token[self.token_index] == 'static'
           or self.token[self.token_index] == 'int'
           or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float'
           or self.token[self.token_index] == 'char' or self.token[self.token_index] == 'bool'):
            if(self.token[self.token_index] == "static"):
                self.ST = self.value[self.token_index]
                self.token_index += 1
                return True
            # elif(self.token[self.token_index] == "abstract"):
            #     self.token_index += 1
            #     return True
            elif(self.token[self.token_index] == "final"):
                self.TM = self.value[self.token_index]
                self.F = self.value[self.token_index]
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == "class" or self.token[self.token_index] == "void"
                 or self.token[self.token_index] == 'int'
                 or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float'
                 or self.token[self.token_index] == 'char' or self.token[self.token_index] == 'bool'):
                return True
        return False

    def ClassModifier1(self):
        if(self.token[self.token_index] == 'final'
           or self.token[self.token_index] == '' or self.token[self.token_index] == 'class'
           or self.token[self.token_index] == 'void' or self.token[self.token_index] == 'int'
           or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float'
           or self.token[self.token_index] == 'char' or self.token[self.token_index] == 'bool'):
            # if(self.token[self.token_index] == "abstract"):
            #     self.token_index += 1
            #     return True
            if(self.token[self.token_index] == "final"):
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == "class" or self.token[self.token_index] == "void"
                 or self.token[self.token_index] == 'int'
                 or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float'
                 or self.token[self.token_index] == 'char' or self.token[self.token_index] == 'bool'):
                return True
        return False

    def RetType(self):
        if(self.token[self.token_index] == 'int' or self.token[self.token_index] == 'char'
           or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float'
           or self.token[self.token_index] == 'void' or self.token[self.token_index] == 'bool'):
            if(self.token[self.token_index] == "void"):
                self.T = self.value[self.token_index]
                self.token_index += 1
                return True
            elif(self.DT()):
                return True
        return False

    def DT(self):
        if(self.token[self.token_index] == 'int' or self.token[self.token_index] == 'char'
           or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float'
           or self.token[self.token_index] == 'bool'):
            if(self.token[self.token_index] == "String"):
                self.T = self.value[self.token_index]
                self.TF += self.value[self.token_index]
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == "int"):
                self.T = self.value[self.token_index]
                self.TF += self.value[self.token_index]
                self.token_index += 1
                # print(True)
                return True
            elif(self.token[self.token_index] == "char"):
                self.T = self.value[self.token_index]
                self.TF += self.value[self.token_index]
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == "float"):
                self.T = self.value[self.token_index]
                self.TF += self.value[self.token_index]
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == "bool"):
                self.T = self.value[self.token_index]
                self.TF += self.value[self.token_index]
                self.token_index += 1
                return True
        else:
            return False
    # def RetType(self):
    #     # not complete
    #     return False

    def Inheritance(self):
        if(self.token[self.token_index] == 'extends' or self.token[self.token_index] == '{'):
            if(self.token[self.token_index] == "extends"):

                self.token_index += 1
                if(self.token[self.token_index] == "Identifier"):
                    self.E = self.value[self.token_index]
                    self.token_index += 1
                    if(self.ext1()):
                        RMT = Sem.lookupMDT(self.E, self.T)
                        if(RMT == None):
                            print("Undeclared ID")
                        # else:
                            # if(RMT.Type != 'class'):
                                # print("Wrong type")
                            # elif(RMT.TypeModifier == 'final'):
                                # print("can't be extended")
                            # else:
                        else:
                            Sem.insertMDT(
                                    self.N, self.T, self.TM, self.E, self.I)
                        return True
            elif(self.token[self.token_index] == "{"):
                Sem.insertMDT(
                    self.N, self.T, self.TM, self.E, self.I)
                self.token_index += 1
                if(self.ClassBody()):
                    if(self.token[self.token_index] == "}"):
                        self.RefofCT = ''
                        self.token_index += 1
                        return True
        return False

    def ext1(self):
        if(self.token[self.token_index] == ',' or self.token[self.token_index] == '{'):
            if(self.token[self.token_index] == ","):
                self.token_index += 1
                if(self.token[self.token_index] == "Identifier"):
                    self.token_index += 1
                    if(self.ext1()):
                        return True
            elif(self.token[self.token_index] == "{"):
                self.token_index += 1
                if(self.ClassBody()):
                    if(self.token[self.token_index] == "}"):
                        self.token_index += 1
                        return True
        return False

    def Parameter(self):
        if(self.token[self.token_index] == 'int' or self.token[self.token_index] == 'char'
           or self.token[self.token_index] == 'String' or self.token[self.token_index] == 'float'
           or self.token[self.token_index] == 'bool' or self.token[self.token_index] == ''
           or self.token[self.token_index] == ')'):
            if(self.DT()):
                if(self.token[self.token_index] == "Identifier"):
                    self.N = self.value[self.token_index]
                    self.token_index += 1
                    Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                    print("param1 passed")
                    if(self.P1()):
                        print("param2 passed")
                        Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                        return True
            elif(self.token[self.token_index] == ")"):
                return True
        return False

    def P1(self):
        if(self.token[self.token_index] == 'EQ' or self.token[self.token_index] == 'comma'
           or self.token[self.token_index] == '' or self.token[self.token_index] == ')'):
            if(self.token[self.token_index] == "EQ"):
                self.token_index += 1
                if(self.OE()):
                    if(self.P2()):
                        # Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                        return True
            elif(self.P2()):
                # Sem.insertFDT(self.N, self.T, str(self.SC), self.F)
                return True
            elif(self.token[self.token_index] == ")"):
                self.TF += '->'
                return True
        return False

    def P2(self):
        print(self.token[self.token_index])
        if(self.token[self.token_index] == 'comma' or self.token[self.token_index] == ''
           or self.token[self.token_index] == ')'):
            print("in param 2")
            if(self.token[self.token_index] == "comma"):
                self.TF += ','
                self.token_index += 1
                if(self.DT()):
                    if(self.token[self.token_index] == "Identifier"):
                        self.N = self.value[self.token_index]
                        self.token_index += 1
                        if(self.P1()):
                            return True
            elif(self.token[self.token_index] == ")"):
                return True
        return False

    def This(self):
        if(self.token[self.token_index] == 'this' or self.token[self.token_index] == ''
           or self.token[self.token_index] == 'Identifier'):
            if(self.token[self.token_index] == "this"):
                self.token_index += 1
                if(self.token[self.token_index] == "."):
                    self.token_index += 1
                    return True
            elif(self.token[self.token_index] == "Identifier"):
                return True
        return False

    def OE(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
           or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == 'this'):
            if(self.AE()):
                if(self.OEColon()):
                    print("OE")
                    return True
        return False

    def OEColon(self):
        if(self.token[self.token_index] == 'OR' or self.token[self.token_index] == ')'
                or self.token[self.token_index] == ';' or self.token[self.token_index] == ','
                or self.token[self.token_index] == ''):
            if(self.token[self.token_index] == "OR"):
                self.token_index += 1
                if(self.AE()):
                    if(self.OEColon()):
                        return True
            elif(self.token[self.token_index] == ')' or self.token[self.token_index] == ';'
                 or self.token[self.token_index] == ','):
                return True
        return False

    def AE(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
           or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == 'this'):
            if(self.RE()):
                if(self.AEColon()):
                    return True
        return False

    def AEColon(self):
        if(self.token[self.token_index] == 'AND' or self.token[self.token_index] == ')'
                or self.token[self.token_index] == ';' or self.token[self.token_index] == ','
                or self.token[self.token_index] == '' or self.token[self.token_index] == 'OR'):
            if(self.token[self.token_index] == "AND"):
                self.token_index += 1
                if(self.RE()):
                    if(self.AEColon()):
                        return True
            elif(self.token[self.token_index] == ')'
                 or self.token[self.token_index] == ';' or self.token[self.token_index] == ','
                 or self.token[self.token_index] == 'OR'):
                return True
        return False

    def RE(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
           or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == 'this'):
            if(self.E()):
                if(self.REColon()):
                    return True
        return False

    def REColon(self):
        if(self.token[self.token_index] == 'RO' or self.token[self.token_index] == ''
                or self.token[self.token_index] == 'AND' or self.token[self.token_index] == 'OR'
                or self.token[self.token_index] == ',' or self.token[self.token_index] == ')'
                or self.token[self.token_index] == ';'):
            if(self.token[self.token_index] == "RO"):
                self.token_index += 1
                if(self.E()):
                    if(self.REColon()):
                        return True
            elif(self.token[self.token_index] == 'AND' or self.token[self.token_index] == 'OR'
                 or self.token[self.token_index] == ',' or self.token[self.token_index] == ')'
                 or self.token[self.token_index] == ';'):
                return True
        return False

    def E(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
           or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == 'this'):
            if(self.T()):
                if(self.EColon()):
                    return True
        return False

    def EColon(self):
        if(self.token[self.token_index] == 'PM' or self.token[self.token_index] == ''
           or self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'AND'
           or self.token[self.token_index] == 'OR' or self.token[self.token_index] == ','
           or self.token[self.token_index] == ')' or self.token[self.token_index] == ';'):
            if(self.token[self.token_index] == "PM"):
                self.token_index += 1
                if(self.T()):
                    if(self.EColon()):
                        return True
            elif(self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'AND' or self.token[self.token_index] == 'OR'
                 or self.token[self.token_index] == ',' or self.token[self.token_index] == ')'
                 or self.token[self.token_index] == ';'):
                return True
        return False

    def T(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
           or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == 'this'):
            if(self.F()):
                if(self.TColon()):
                    return True
        return False

    def TColon(self):
        if(self.token[self.token_index] == 'MDM' or self.token[self.token_index] == ''
           or self.token[self.token_index] == 'PM' or self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'AND'
           or self.token[self.token_index] == 'OR' or self.token[self.token_index] == ','
           or self.token[self.token_index] == ')' or self.token[self.token_index] == ';'
           or self.token[self.token_index] == '}'):
            if(self.token[self.token_index] == "MDM"):
                self.token_index += 1
                if(self.F()):
                    if(self.TColon()):
                        return True
            elif(self.token[self.token_index] == 'PM' or self.token[self.token_index] == 'RO' or self.token[self.token_index] == 'AND' or self.token[self.token_index] == 'OR'
                 or self.token[self.token_index] == ',' or self.token[self.token_index] == ')'
                 or self.token[self.token_index] == ';' or self.token[self.token_index] == '}'):
                return True
        return False

    def F(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
           or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == 'this'):
            if(self.token[self.token_index] == 'Identifier'):
                self.token_index += 1
                if(self.FColon()):
                    print("fcolon passed")
                    return True
            elif(self.Const()):
                return True
            elif(self.token[self.token_index] == '('):
                self.token_index += 1
                if(self.OE()):
                    if(self.token[self.token_index] == ')'):
                        self.token_index += 1
                        return True
            elif(self.token[self.token_index] == 'NOT'):
                self.token_index += 1
                if(self.F()):
                    return True
            elif(self.IncDec()):
                if(self.This()):
                    if(self.token[self.token_index] == 'Identifier'):
                        self.token_index += 1
                        if(self.Z2()):
                            return True
            elif(self.token[self.token_index] == 'this'):
                self.token_index += 1
                if(self.token[self.token_index] == '.'):
                    self.token_index += 1
                    if(self.token[self.token_index] == 'Identifier'):
                        self.token_index += 1
                        if(self.Z()):
                            return True
        return False

    def FColon(self):
        if(self.token[self.token_index] == '.' or self.token[self.token_index] == 'EQ'
           or self.token[self.token_index] == 'Compound' or self.token[self.token_index] == '['
           or self.token[self.token_index] == '(' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == '' or self.token[self.token_index] == '{' or self.token[self.token_index] == 'MDM'
           or self.token[self.token_index] == 'PM' or self.token[self.token_index] == 'RO'
           or self.token[self.token_index] == 'AND' or self.token[self.token_index] == 'OR'
           or self.token[self.token_index] == ',' or self.token[self.token_index] == ')'
           or self.token[self.token_index] == ';'):
            if(self.Z()):
                if(self.token[self.token_index] == ';'):
                    self.token_index += 1
                    return True
            elif(self.token[self.token_index] == 'MDM'
                 or self.token[self.token_index] == 'PM' or self.token[self.token_index] == 'RO'
                 or self.token[self.token_index] == 'AND' or self.token[self.token_index] == 'OR'
                 or self.token[self.token_index] == ',' or self.token[self.token_index] == ')'
                 or self.token[self.token_index] == ';' or self.token[self.token_index] == '{'):
                return True
        return False

    def Const(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const'):
            if(self.token[self.token_index] == 'int_const'):
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == 'string_const'):
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == 'float_const'):
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == 'bool_const'):
                self.token_index += 1
                return True
        return False

    def Break(self):
        if(self.token[self.token_index] == 'break'):
            if(self.token[self.token_index] == 'break'):
                self.token_index += 1
                # if(self.token[self.token_index] == ';'):
                #     self.token_index += 1
                return True
        return False

    def Cont(self):
        if(self.token[self.token_index] == 'continue'):
            if(self.token[self.token_index] == 'continue'):
                self.token_index += 1
                # if(self.token[self.token_index] == ';'):
                #     self.token_index += 1
                return True
        return False

    def DecST(self):
        if(self.token[self.token_index] == 'int' or self.token[self.token_index] == 'String'
           or self.token[self.token_index] == 'float'
           or self.token[self.token_index] == 'bool' or self.token[self.token_index] == 'char'):
            print("in decst")
            if(self.DT()):
                print(self.DT())
                print(self.token[self.token_index])
                if(self.token[self.token_index] == 'Identifier'):
                    self.N = self.value[self.token_index]
                    print(True)
                    self.token_index += 1
                    print(self.token[self.token_index])
                    if(self.Initialize()):
                        print(self.token[self.token_index])
                        if(self.List()):
                            print(self.token[self.token_index])
                            return True
        return False

    def Initialize(self):
        if(self.token[self.token_index] == 'EQ' or self.token[self.token_index] == ''
           or self.token[self.token_index] == ','
           or self.token[self.token_index] == ';'):
            if(self.token[self.token_index] == 'EQ'):
                print(self.token[self.token_index])
                self.token_index += 1
                if(self.OE()):
                    return True
            elif(self.token[self.token_index] == ','
                 or self.token[self.token_index] == ';'):
                print(True)
                return True
        return False

    def List(self):
        if(self.token[self.token_index] == ','
           or self.token[self.token_index] == ';'):
            if(self.token[self.token_index] == ';'):
                print(self.token[self.token_index])
                print(True)
                self.token_index += 1
                return True
            elif(self.token[self.token_index] == ','):
                self.token_index += 1
                if(self.token[self.token_index] == 'Identifier'):
                    self.N = self.value[self.token_index]
                    self.token_index += 1
                    if(self.Initialize()):
                        if(self.List()):
                            return True
        return False

    def AssignST(self):
        if(self.token[self.token_index] == 'this' or self.token[self.token_index] == 'Identifier'):
            if(self.This()):
                if(self.token[self.token_index] == 'Identifier'):
                    self.token_index += 1
                    if(self.X1()):
                        if(self.Initialize()):
                            if(self.List()):
                                return True
        return False

    def AssignOP(self):
        if(self.token[self.token_index] == 'EQ'
           or self.token[self.token_index] == 'Compound'):
            if(self.token[self.token_index] == 'EQ'):
                self.token_index += 1
                return True
            elif(self.CAssign()):
                return True
        return False

    def CAssign(self):
        if(self.token[self.token_index] == 'Compound'):
            if(self.token[self.token_index] == 'Compound'):
                self.token_index += 1
                return True
        return False

    def IncDec(self):
        if(self.token[self.token_index] == 'Inc-Dec'):
            if(self.token[self.token_index] == 'Inc-Dec'):
                self.token_index += 1
                # print(self.token[self.token_index])
                return True
        return False

    # def ObjectDef(self):
    #     # not complete
    #     return False

    def CName(self):
        if(self.token[self.token_index] == 'Identifier'):
            # if(self.token[self.token_index] == 'EQ'):
            #     self.token_index += 1
            if(self.token[self.token_index] == 'Identifier'):
                self.token_index += 1
                return True
        return False

    # def A(self):
    #     if(self.token[self.token_index] == 'EQ'):
    #         if(self.token[self.token_index] == 'EQ'):
    #             self.token_index += 1
    #             if(self.AColon()):
    #                 return True
    #     return False

    # def AColon(self):
    #     if(self.token[self.token_index] == 'new' or self.token[self.token_index] == '{'):
    #         if(self.C()):
    #             return True
    #         elif(self.token[self.token_index] == 'new'):
    #             self.token_index += 1
    #             if(self.DT()):
    #                 if(self.token[self.token_index] == '['):
    #                     self.token_index += 1
    #                     if(self.N()):
    #                         if(self.C1s()):
    #                             return True
    #     return False

    # def C(self):
    #     if(self.token[self.token_index] == '{'):
    #         if(self.token[self.token_index] == '{'):
    #             self.token_index += 1
    #             if(self.D()):
    #                 return True
    #     return False

    # def C1s(self):
    #     if(self.token[self.token_index] == '{' or self.token[self.token_index] == ''
    #        or self.token[self.token_index] == ';'):
    #         if(self.token[self.token_index] == '{'):
    #             self.token_index += 1
    #             if(self.D()):
    #                 return True
    #         elif(self.token[self.token_index] == ';'):
    #             return True
    #     return False

    # def N(self):
    #     if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == ','
    #        or self.token[self.token_index] == ']'):
    #         if(self.token[self.token_index] == 'int_const'):
    #             self.token_index += 1
    #             if(self.IColon()):
    #                 return True
    #         elif(self.token[self.token_index] == ','):
    #             self.token_index += 1
    #             if(self.I2()):
    #                 return True
    #         elif(self.token[self.token_index] == ']'):
    #             self.token_index += 1
    #             return True
    #     return False

    # def D(self):
    #     if(self.token[self.token_index] == '{'):
    #         if(self.token[self.token_index] == '{'):
    #             self.token_index += 1
    #             if(self.M()):
    #                 if(self.DColon()):
    #                     return True
    #     return False

    # def DColon(self):
    #     if(self.token[self.token_index] == ',' or self.token[self.token_index] == '}'):
    #         if(self.token[self.token_index] == ','):
    #             self.token_index += 1
    #             if(self.D()):
    #                 return True
    #         elif(self.token[self.token_index] == '}'):
    #             self.token_index += 1
    #             return True
    #     return False

    # def M(self):
    #     if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
    #        or self.token[self.token_index] == 'float_const'
    #        or self.token[self.token_index] == 'bool_const'):
    #         if(self.Const()):
    #             if(self.MColon()):
    #                 return True
    #     return False

    # def MColon(self):
    #     if(self.token[self.token_index] == ',' or self.token[self.token_index] == '}'):
    #         if(self.token[self.token_index] == ','):
    #             self.token_index += 1
    #             if(self.M()):
    #                 return True
    #         elif(self.token[self.token_index] == '}'):
    #             self.token_index += 1
    #             return True
    #     return False

    # def I2(self):
    #     if(self.token[self.token_index] == ',' or self.token[self.token_index] == ']'):
    #         if(self.token[self.token_index] == ','):
    #             self.token_index += 1
    #             if(self.I2()):
    #                 return True
    #         elif(self.token[self.token_index] == ']'):
    #             self.token_index += 1
    #             return True
    #     return False

    # def I(self):
    #     if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
    #        or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
    #        or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
    #        or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
    #        or self.token[self.token_index] == 'this' or self.token[self.token_index] == ','
    #        or self.token[self.token_index] == ']'):
    #         if(self.OE()):
    #             if(self.IColon()):
    #                 return True
    #         elif(self.token[self.token_index] == ','):
    #             self.token_index += 1
    #             if(self.I2()):
    #                 return True
    #         elif(self.token[self.token_index] == ']'):
    #             self.token_index += 1
    #             return True
    #     return False

    # def IColon(self):
    #     if(self.token[self.token_index] == ']'):
    #         if(self.token[self.token_index] == ']'):
    #             self.token_index += 1
    #             return True
    #     return False

    def Try(self):
        if(self.token[self.token_index] == 'try'):
            if(self.token[self.token_index] == 'try'):
                self.token_index += 1
                if(self.token[self.token_index] == '{'):
                    self.token_index += 1
                    if(self.BodyT()):
                        if(self.Except()):
                            if(self.Finally()):
                                return True
        return False

    def BodyT(self):
        if(self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or
           self.token[self.token_index] == 'while' or self.token[self.token_index] == 'int' or
           self.token[self.token_index] == 'try' or
           self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or
           self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char'
           or self.token[self.token_index] == 'Array' or self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
           or self.token[self.token_index] == 'protected' or self.token[self.token_index] == 'final'
           or self.token[self.token_index] == 'this'
           or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break'
           or self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == '' or self.token[self.token_index] == 'except'
           or self.token[self.token_index] == 'finally' or self.token[self.token_index] == '$'):
            if(self.BodyT()):
                if(self.TTry()):
                    return True
        return False

    def TTry(self):
        if(self.token[self.token_index] == 'try' or self.token[self.token_index] == ''
           or self.token[self.token_index] == 'except'):
            if(self.Try()):
                return True
            elif(self.token[self.token_index] == 'except'):
                return True
        return False

    def Except(self):
        if(self.token[self.token_index] == 'except'):
            if(self.token[self.token_index] == 'except'):
                self.token_index += 1
                if(self.token[self.token_index] == '{'):
                    self.token_index += 1
                    if(self.Body1()):
                        if(self.EExcept()):
                            return True
        return False

    def EExcept(self):
        if(self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or
           self.token[self.token_index] == 'while' or self.token[self.token_index] == 'int' or
           self.token[self.token_index] == 'try' or
           self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or
           self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char'
           or self.token[self.token_index] == 'Array' or self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
           or self.token[self.token_index] == 'protected' or self.token[self.token_index] == 'final'
           or self.token[self.token_index] == 'this'
           or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break'
           or self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == '' or self.token[self.token_index] == 'except'
           or self.token[self.token_index] == 'finally' or self.token[self.token_index] == '$'
           or self.token[self.token_index] == 'except' or self.token[self.token_index] == ''):

            if(self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or
               self.token[self.token_index] == 'while' or self.token[self.token_index] == 'int' or
               self.token[self.token_index] == 'try' or
               self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or
               self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char'
               or self.token[self.token_index] == 'Array' or self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
               or self.token[self.token_index] == 'protected' or self.token[self.token_index] == 'final'
               or self.token[self.token_index] == 'this'
               or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break'
               or self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func'
               or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec'
               or self.token[self.token_index] == '' or self.token[self.token_index] == 'except'
               or self.token[self.token_index] == 'finally' or self.token[self.token_index] == '$'):
                return True
            elif(self.Except()):
                return True
        return False

    def Finally(self):
        if(self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or
           self.token[self.token_index] == 'while' or self.token[self.token_index] == 'int' or
           self.token[self.token_index] == 'try' or
           self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or
           self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char'
           or self.token[self.token_index] == 'Array' or self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
           or self.token[self.token_index] == 'protected' or self.token[self.token_index] == 'final'
           or self.token[self.token_index] == 'this'
           or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break'
           or self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == '' or self.token[self.token_index] == 'except'
           or self.token[self.token_index] == 'finally' or self.token[self.token_index] == '$'
           or self.token[self.token_index] == ''):
            if(self.token[self.token_index] == 'finally'):
                self.token_index += 1
                if(self.token[self.token_index] == '{'):
                    self.token_index += 1
                    if(self.Body1()):
                        return True
            elif(self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or
                 self.token[self.token_index] == 'while' or self.token[self.token_index] == 'int' or
                 self.token[self.token_index] == 'try' or
                 self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or
                 self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char'
                 or self.token[self.token_index] == 'Array' or self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
                 or self.token[self.token_index] == 'protected' or self.token[self.token_index] == 'final'
                 or self.token[self.token_index] == 'this'
                 or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break'
                 or self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func'
                 or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec'
                 or self.token[self.token_index] == '' or self.token[self.token_index] == 'except'
                 or self.token[self.token_index] == 'finally' or self.token[self.token_index] == '$'):
                return True
        return False

    def Dict(self):
        if(self.token[self.token_index] == 'Identifier'):
            if(self.token[self.token_index] == 'Identifier'):
                self.token_index += 1
                if(self.token[self.token_index] == 'EQ'):
                    self.token_index += 1
                    if(self.BodyDict()):
                        return True
        return False

    def BodyDict(self):
        if(self.token[self.token_index] == '{'):
            if(self.token[self.token_index] == '{'):
                self.token_index += 1
                if(self.BodyIn()):
                    return True
        return False

    def BodyIn(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
           or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == 'this'):
            if(self.Key()):
                if(self.token[self.token_index] == ':'):
                    self.token_index += 1
                    if(self.Value()):
                        return True
        return False

    def Key(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
           or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
           or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
           or self.token[self.token_index] == 'this'):
            if(self.OE()):
                return True
        return False

    def Value(self):
        if(self.token[self.token_index] == 'int_const' or self.token[self.token_index] == 'string_const'
           or self.token[self.token_index] == 'char_const'
                or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'float_const'
                or self.token[self.token_index] == 'bool_const' or self.token[self.token_index] == '('
                or self.token[self.token_index] == 'NOT' or self.token[self.token_index] == 'Inc-Dec'
                or self.token[self.token_index] == 'this' or self.token[self.token_index] == 'Array'
                or self.token[self.token_index] == '{' or self.token[self.token_index] == '' or
                self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or
                self.token[self.token_index] == 'while' or self.token[self.token_index] == 'int' or
                self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or
                self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char'
                or self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
                or self.token[self.token_index] == 'protected'
                or self.token[self.token_index] == 'final' or self.token[self.token_index] == 'this'
                or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break'
                or self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func'
                or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec'
                or self.token[self.token_index] == ',' or self.token[self.token_index] == '$'):
            if(self.BodyDict()):
                if(self.Comma()):
                    return True
            elif(self.OE()):
                if(self.Comma()):
                    return True
            if(self.Array()):
                if(self.Comma()):
                    return True
            elif(self.token[self.token_index] == 'if' or self.token[self.token_index] == 'for' or
                 self.token[self.token_index] == 'while' or self.token[self.token_index] == 'int' or
                 self.token[self.token_index] == 'String' or self.token[self.token_index] == 'bool' or
                 self.token[self.token_index] == 'float' or self.token[self.token_index] == 'char'
                 or self.token[self.token_index] == 'public' or self.token[self.token_index] == 'private'
                 or self.token[self.token_index] == 'protected'
                 or self.token[self.token_index] == 'final' or self.token[self.token_index] == 'this'
                 or self.token[self.token_index] == 'continue' or self.token[self.token_index] == 'break'
                 or self.token[self.token_index] == 'return' or self.token[self.token_index] == 'func'
                 or self.token[self.token_index] == 'Identifier' or self.token[self.token_index] == 'Inc-Dec'
                 or self.token[self.token_index] == ',' or self.token[self.token_index] == '$'):
                return True
        return False

    def Comma(self):
        if(self.token[self.token_index] == ',' or self.token[self.token_index] == '}'):
            if(self.token[self.token_index] == ','):
                self.token_index += 1
                if(self.BodyIn()):
                    return True
            elif(self.token[self.token_index] == '}'):
                self.token_index += 1
                return True
        return False


# driver class


def run(file_name, text, line_no):
    lexer = Lexer(file_name, text, line_no)
    tokens, error = lexer.makeTokens()
    if error:
        print(error.asString())
    else:
        print(tokens)
    # return tokens, error


def chadBreak(file_name, String, line_no):
    temp_str = ''
    String += '\n'
    for x in String:
        if x not in word_break1:
            temp_str += x
        else:
            run(file_name, temp_str, line_no)
            temp_str = ''
            temp_str += x
