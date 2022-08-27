from unittest import result
import Chad

# for scripting in shell
# cleaning tokens
f = open(
    r'D:\uni\Sem VI\Compiler Construction\Project\Chad-Compiler\Token\token.txt', 'w').close()
while True:
    text = input('Chad > ')
    result1, error = Chad.run('<stdin>', text)

    if error:
        print(error.asString())
    else:
        print(result1)
