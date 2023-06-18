import requests
import time

command = str(input(">> "))
print('entered:', command)

cmd = {'command': [command]}

r_g = requests.get(
    'https://localhost:8080/', stream = True,
    #params = cmd, verify = "../httpS_test_01/testeando.key"
    #params = cmd, verify = "../httpS_test_01/testeando.csr"
    params = cmd, verify = "../httpS_test_01/testeando.pem"
    #params = cmd, verify = False
)

line_str = ''
while True:
    tmp_dat = r_g.raw.read(1)
    single_char = str(tmp_dat.decode('utf-8'))
    line_str += single_char
    if single_char == '\n':
        print('receiving <<', line_str, '>>')
        line_str = ''

    elif line_str[-7:] == '/*EOF*/':
        print('/*EOF*/ received')
        break

    print('#', end = '')
