from unittest import result
import Chad

# for scripting in shell
# cleaning tokens
f = open(
    r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'w').close()
# read char by char
test = open(
    r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Test\test1.txt', 'r')
while 1:
    # read by character
    char = test.read(1)
    result1, error = Chad.run('test', char)
    if error:
        print(error.asString())
    else:
        print(result1)
    if not char:
        break


# while True:
#     # text = input('Chad > ')
#     result1, error = Chad.runFile(test)

#     if error:
#         print(error.asString())
#     else:
#         print(result1)
