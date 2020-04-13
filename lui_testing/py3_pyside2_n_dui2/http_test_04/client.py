import requests
#import time

r = requests.get('http://localhost:8080/', stream=True)

line_str = ''

while True:
    #time.sleep(0.1)
    tmp_dat = r.raw.read(1)
    single_char = str(tmp_dat.decode('utf-8'))
    line_str += single_char
    if single_char == '\n':
        print('receiving <<', line_str, '>>')
        line_str = ''

    elif line_str[-7:] == '/*EOF*/':
        print('/*EOF*/ received')
        break

    print('#', end = '')

