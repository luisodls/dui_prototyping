
import requests
#r = requests.get('http://localhost:8080/', stream=True)

with requests.get('http://localhost:8080/', stream=False) as r:
    print(r.headers)
    '''
    for line in r.iter_lines():
        if line:
            print("\\n")
            print(str(line.decode('utf-8')))

    '''
    lines = r.iter_content()
    # Save the first line for later or just skip it
    first_line = next(lines)
    print(str(first_line.decode('utf-8')))
    for line in lines:
        print(str(line.decode('utf-8')))

