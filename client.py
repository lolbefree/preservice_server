import os

import pyodbc
import socket
import subprocess
import sys
import getpass
from datetime import datetime

today = datetime.now().strftime("%d.%m.%y - %H:%M")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if not os.path.exists(f"c:\\temp\\{getpass.getuser()}_presservice.log"):
    f= open(f"c:\\temp\\{getpass.getuser()}_presservice.log", "w")
    f.close()
if not os.path.exists(f"c:\\temp\\{getpass.getuser()}_presservice_err.log"):
    f= open(f"c:\\temp\\{getpass.getuser()}_presservice_err.log", "w")
    f.close()

def m1(gsalid):
    def conserv(ip):
        server_address = (f'{ip}', 1234)
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)

        self.server = not_for_git.db_server
        self.database = not_for_git.db_name
        self.username = not_for_git.db_user
        self.password = not_for_git.db_pw
        self.driver = '{ODBC Driver 17 for SQL Server}'  # Driver you need to connect to the database '{SQL Server}'  #
        self.numpad_mod = ""
        self.cnn = pyodbc.connect(
            'DRIVER=' + self.driver + ';PORT=port;SERVER=' + self.server + ';PORT=1443;DATABASE=' + self.database +
            ';UID=' + self.username +
            ';PWD=' + self.password)
        self.cursor = self.cnn.cursor()


    cursor = cnn.cursor()
    tel = list(cursor.execute("select uwtel from gsals01 where gsalid={}".format(gsalid)))[0][0]
    tel = "".join([i for i in tel if i.isdigit()])
    try:
        p = subprocess.Popen(["powershell.exe",
                              f"""import-module activedirectory\n
                              $user =  $env:username\n
                              $comp = Get-ADUser $user  -properties labelcomputer | select -ExpandProperty labelcomputer\n
                              $comp"""],
                             stdout=subprocess.PIPE)
        result = str(p.communicate()[0])
        ip = (result[2:-5])
        if "." in ip:
            name = ip.index(".")
            ip = (ip[:name])
        try:
            conserv(ip)
        except:
            conserv(ip + ".stoik.local")
        message = bytes(f'{tel+ " " + str(gsalid)}', encoding='utf8')
        sock.sendall(message)
    except Exception as err:
        with open(f"c:\\temp\\{getpass.getuser()}_presservice_err.log", "a") as err_file:
            err_file.write(f"time: {today};" + str(err)+"\n")
    finally:
        print('closing socket')
        with open(f"c:\\temp\\{getpass.getuser()}_presservice.log", "a") as filelog:
            filelog.write(f"time: {today}; ip: {ip}; gsalid: {gsalid}; tel: {tel};\n")
        sock.close()


if __name__ == "__main__":
    args = sys.argv[1]
    get_gsalid = m1(args)
