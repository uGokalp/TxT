
"""
Object of the program: to update the configuration parameters using REST API POST command of a number devices identified by IP addresses listed a text file
 
Input file_1(text)             :               {IP address_1}; { IP address_2} ;…
Input file_2 (text)            :               API command in JSON
Output file (text)             :               {IP address_1    OK};  {IP address_2   OK}; …
 
Script file exec:
 
Read Input file_1
                Number_of_devices = number of rows                        
For i= 1 to Number_of_devices do
http POST Input  JSON commands in Input file_2
if return code= “successful” then
print Output file { IP address -- OK}
else
Notify print Output file { IP address -- NOT OK}
next i
                          finish          
"""


import requests
import os
import logging
import json
import sys


def read_file(file, single=False):
    with open(file) as f:
        data = f.read()
    if single:
        return data
    return data.split()


def read_json(file):
    with open(file) as f:
        data = json.load(f)
    return data


if __name__ == "__main__":

    # Arg 0: method
    # Arg 1: ip adresses
    # Arg 2: Json
    # Arg 3: log file

    args = [i for i in sys.argv[1:]]  # first one is name
    if os.path.isfile(args[3]):
        os.remove(args[3])

    logging.basicConfig(filename=args[3], level=logging.INFO)
    logger = logging.getLogger(__name__)

    method = read_file(args[0], single=True)
    ip_addresses = read_file(args[1])
    json_to_post = read_json(args[2])

    for ip in ip_addresses:
        new_ip = f'http://{ip}/{method}'
        print(ip)
        post = requests.post(url=new_ip, json=json_to_post)
        status = post.status_code
        if status == 200:
            status = "OK"
        else:
            status = "NOT OKAY"
        logger.info("{0}    {1}".format(ip, post.status_code))
