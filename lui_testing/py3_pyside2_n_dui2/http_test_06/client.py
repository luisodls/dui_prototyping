import requests
import time

command = str(input(">> "))
print('entered:', command)


cmd = {'command': [command]}

r_g = requests.get('http://localhost:8080/', stream = True, params = cmd)

line_str = ''
while True:
    tmp_dat = r_g.raw.read(1)
    single_char = str(tmp_dat.decode('utf-8'))
    line_str += single_char
    if single_char == '\n':
        print('>>', line_str[:-1])
        line_str = ''

    elif line_str[-7:] == '/*EOF*/':
        print('/*EOF*/ received')
        break


