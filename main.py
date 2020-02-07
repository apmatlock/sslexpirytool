import OpenSSL
import ssl, socket
import sqlite3

#sql junk ...needs to be moved into it's own file
sql_create_hosts_table = """ CREATE TABLE IF NOT EXISTS hosts (
                                        id integer PRIMARY KEY,
                                        subject_name text,
                                        dated_added text,
                                        expiry_date text
                                    ); """


conn = sqlite3.connect('ssl_hosts.db')
c = conn.cursor()
c.execute(sql_create_hosts_table)

f = open("ssl-list.csv", "a")

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