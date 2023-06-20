import requests
import time

cmd_in = str(input(">> "))
print('entered:', cmd_in)

cmd = {
    'command': [cmd_in]
}

r_g = requests.get(
    'https://localhost:8080/', stream = True,
    params = cmd, verify = "../tmp_dummy.pem"
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
