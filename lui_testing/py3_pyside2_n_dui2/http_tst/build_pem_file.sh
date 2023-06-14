# creating .key and .csr files
openssl req -new -newkey rsa:4096 -nodes -keyout tmp_dummy.key -out tmp_dummy.csr

# creating .pem file
openssl x509 -req -sha256 -days 365 -in tmp_dummy.csr -signkey tmp_dummy.key -out tmp_dummy.pem
