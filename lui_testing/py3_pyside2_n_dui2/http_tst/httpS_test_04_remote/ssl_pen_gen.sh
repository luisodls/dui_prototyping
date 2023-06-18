# creating .key and .csr files
openssl req -new -newkey rsa:4096 -nodes -keyout tmp_cimav.key -out tmp_cimav.csr

# creating .pem file
openssl x509 -req -sha256 -days 365 -in tmp_cimav.csr -signkey tmp_cimav.key -out tmp_cimav.pem
