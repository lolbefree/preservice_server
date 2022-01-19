import os
import socket
import requests as requests
from datetime import datetime

today = datetime.now().strftime("%Y_%m_%d")
if not os.path.exists(f"c:\\temp\\err_preservice{today}.log"):
    f = open(f"c:\\temp\\err_preservice{today}.log", "w")
    f.close()
    f = open(f"c:\\temp\\attempts_preservice{today}.log", "w")
    f.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 1234)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

sock.listen(1)


def start():
    while True:
        connection, client_address = sock.accept()
        # print(connection.recv(1024).decode("utf-8"))
        data = connection.recv(1024)
        # print('received {!r}'.format(data))
        tel, gsalid = map(str, data.decode("utf-8").split())
        print(tel, gsalid)
        get = requests.get(f"http://localhost:4059/execsvcscript?name=webcall&startparam1={tel}&startparam2={gsalid}")
        print(get.status_code)
        with open(f"c:\\temp\\attempts_preservice{today}.log", "a") as f_with_attempts:
            f_with_attempts.write(f"tel = {tel}; gsalid = {gsalid}; status_code = {get.status_code}; \n")
        print(data)
        connection.close()


try:
    start()
except Exception as err:
    if os.path.exists(f"c:\\temp\\err_preservice{today}.log"):
        with open(f"c:\\temp\\err_preservice{today}.log", "a") as f:
            f.write(str(err) + "\n")
    start()


