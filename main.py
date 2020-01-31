import OpenSSL
import ssl, socket

f = open("ssl-list.csv", "a")

with open("hostnames.txt", "r") as fr:
    for ip in fr:
        print(f'checking {ip}')

        try:
            cert = ssl.get_server_certificate((ip.rstrip(), 443))
        except TimeoutError:
            print("SSL not OPEN (TimeoutError)")
            f.write("%s,NO SSL FOUND,\n" % (ip))
            continue
        except Exception as ex:
            print(ex)

        if cert:
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            print(f'{ip},{x509.get_subject().CN},{x509.get_notAfter()}')
            f.write("%s,%s,%s\n" % (ip, x509.get_subject().CN, x509.get_notAfter()))
            del cert