from unittest import result
import Chad

# for scripting in shell
# cleaning tokens
f1 = open(
r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'w').close()
# read char by char
test = open(
    r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Test\test1.txt', 'r')
token_file = open(
    r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'r')
f = open(
    r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'a')
token_array = []
token_array_value = []
line_no = 1
while True:
    # read by character
    Str = test.readline()

    # print(Str)
    Chad.chadBreak('test', Str, line_no)
    line_no += 1
    if not Str:
        f.write(f'($,$,{line_no})\n')
        f.close()
        test.close()
        break
line_no1 = 1
while True:
    Str1 = token_file.readline()
    Str1 = Str1[1:-2]
    # print("str1 ", Str1)
    Str2 = Str1.split(",")
    Str3 = Str1.split(",")
    Str2 = Str2[:-2]
    Str3 = Str3[1:-1]
    # print("Str2 ", Str2)
    # print("Str3 ", Str3)
    for item in Str2:
        # print(item)
        token_array.append(item)
    for item in Str3:
        # print(item)
        token_array_value.append(item)
    # print(token_array);

    line_no1 += 1
    if not Str2:
        break
    elif not Str3:
        break

token_array1 = ['int', 'Identifier', ';', '$']
print(token_array)
print(token_array_value)
Chad.SyntaxAnalyzer(token_array,token_array_value)

# Sa = Chad.SyntaxAnalyzer("ja")
# Sa.Validate()
# line = 0
# while True:
#     text = input('Chad > ')
#     Chad.chadBreak('file', text, line)
#     line += 1
