import http.client

conn = http.client.HTTPSConnection("localhost", 8080)
conn.request("GET", "/")

'''
conn.request("GET", "/")
r1 = conn.getresponse()
print("r1.status, r1.reason", r1.status, r1.reason)
#200 OK
'''

copied = '''
conn = http.client.HTTPSConnection("www.python.org")
conn.request("GET", "/")
r1 = conn.getresponse()
print(r1.status, r1.reason)
'''

test_later = '''
data1 = r1.read()  # This will return entire content.
# The following example demonstrates reading data in chunks.
conn.request("GET", "/")
r1 = conn.getresponse()
while chunk := r1.read(200):
p    rint(repr(chunk))
'''

