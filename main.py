import OpenSSL
import ssl, socket
import sqlite3

conn = sqlite3.connect('ssl_hosts.db')
f = open("ssl-list.csv", "a")

c = conn.cursor()

c.execute(''' SELECT count(ip) FROM sqlite_master WHERE type='table' AND name='host' ''')

if c.fetchone()[0]:
    print('table exists')
else:
    c.execute('''CREATE TABLE hosts (date text, trans text, symbol text, qty real, price real)''')


with open("hostnames.txt", "r") as fr:
    for ip in fr:
        print(f'checking {ip}')

        try:
            cert = ssl.get_server_certificate((ip.rstrip(), 443))
        except TimeoutError:
            print("SSL not OPEN (TimeoutError)")
            f.write("%s,NO SSL FOUND,\n" % (ip.rstrip()))
            continue
        except Exception as ex:
            print(ex)

        if cert:
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            print(f'{ip.rstrip()},{x509.get_subject().CN},{x509.get_notAfter()}')
            f.write("%s,%s,%s\n" % (ip.rstrip(), x509.get_subject().CN, x509.get_notAfter()))
            del cert