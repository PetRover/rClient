__author__ = 'brycecarter'

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', 1024))

while 1:
    data = raw_input('enter data to send:')

    dataList = data.split(',')
    processedDataList = []
    for d in dataList:
        try:
            processedDataList.append(str(unichr(int(d, 16))))
        except ValueError:
            processedDataList.append(d)
    dataToSend = ''.join(processedDataList)
    s.send(dataToSend)
