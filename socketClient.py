__author__ = 'brycecarter'

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', 1024))

while 1:
    data = raw_input('enter data to send:')
    try:
        d = ''.join([str(unichr(int(val, 16))) for val in data.split(',')])
    except ValueError:
        d = data
    s.send(d)
