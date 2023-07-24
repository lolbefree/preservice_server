import os
import socket
import time

import requests
from datetime import datetime

today = datetime.now().strftime("%Y_%m_%d")

err_log_file = os.path.join("c:\\temp", f"err_preservice{today}.log")
attempt_log_file = os.path.join("c:\\temp", f"attempts_preservice{today}.log")

if not os.path.exists(err_log_file):
    with open(err_log_file, "w") as f:
        pass

if not os.path.exists(attempt_log_file):
    with open(attempt_log_file, "w") as f:
        pass

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 1234)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

sock.listen(1)


def start():
    max_retries = 3
    retry_delay = 2  # seconds

    while True:
        connection, client_address = sock.accept()
        try:
            data = connection.recv(1024)
            if not data:
                break

            # Use 'str.strip()' to remove leading/trailing whitespaces from the received data
            tel, gsalid = map(str, data.decode("utf-8").strip().split())
            print(tel, gsalid)  # Print the arguments (optional)

            retries = 0
            while retries < max_retries:
                try:
                    get = requests.get(
                        f"http://localhost:4059/execsvcscript?name=webcall&startparam1={tel}&startparam2={gsalid}",
                        timeout=10)
                    get.raise_for_status()  # Raise an exception for unsuccessful HTTP response (status code >= 400)

                    # Use 'with' statement to open files for writing
                    with open(attempt_log_file, "a") as f_with_attempts:
                        f_with_attempts.write(f"tel = {tel}; gsalid = {gsalid}; status_code = {get.status_code}; \n")
                    break  # If successful, break out of the retry loop

                except requests.exceptions.RequestException as err:
                    with open(err_log_file, "a") as f_with_errors:
                        f_with_errors.write(f"HTTP request failed (Retry {retries + 1}/{max_retries}): {err}\n")
                    retries += 1
                    time.sleep(retry_delay)

            if retries == max_retries:
                with open(err_log_file, "a") as f_with_errors:
                    f_with_errors.write(f"Maximum retries reached. Unable to perform HTTP request.\n")
                # Proceed with the next iteration of the loop after maximum retries reached
                continue

        except Exception as err:
            with open(err_log_file, "a") as f:
                f.write(str(err) + "\n")

        finally:
            connection.close()


try:
    start()
except Exception as err:
    with open(err_log_file, "a") as f:
        f.write(str(err) + "\n")
    start()
