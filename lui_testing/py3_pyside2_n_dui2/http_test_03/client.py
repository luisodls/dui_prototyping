import requests
old_stable = '''
r = requests.get('http://localhost:8080/')
print(r.headers['content-type'])
print(r.text, "\n")
print(dir(r))
'''

import requests
r = requests.get('http://localhost:8080/', stream=True)

for line in r.iter_lines():
    if line:
        print("tst")
        decoded_line = line.decode('utf-8')
        print(str(decoded_line))
