import requests
import time


command = None
if __name__ == "__main__":

    r_g = requests.get('http://localhost:8080/', stream = True, params = "a")

    full_file = ''
    line_str = ''
    while True:
        tmp_dat = r_g.raw.read(1)
        single_char = str(tmp_dat.decode('utf-8'))
        line_str += single_char
        if single_char == '\n':
            full_file += line_str
            line_str = ''

        elif line_str[-7:] == '/*EOF*/':
            print('/*EOF*/ received')
            break

    print('full_file: \n', full_file)





