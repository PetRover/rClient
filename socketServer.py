__author__ = 'brycecarter'

import socket
import threading
import select
import Queue
import time


class Client(threading.Thread):

    def __init__(self, connection, addr, queues):
        super(Client, self).__init__()
        self.address = addr
        self.connection = connection
        self.size = 1024
        self.queues = queues

    def run(self):
        running = 1
        while running:
            inputReady, outputReady, errorReady = select.select([self.connection], [self.connection], [])
            for soc in inputReady:
                receivedData = soc.recv(self.size)
                if receivedData:
                    self.handleReceivedData(receivedData)
            for soc in outputReady:
                dataToSend = self.getDataToSend()
                if dataToSend:
                    soc.send(dataToSend)
            time.sleep(1)

    def handleReceivedData(self, data):
        self.queues['receiveQueue'].put(data)

    def getDataToSend(self):
        if not self.queues['sendQueue'].empty():
            result = self.queues['sendQueue'].get()
        else:
            result = None
        return result


class SocketServer(object):
    def __init__(self, ip, port):
        print 'New server created on port {0}'.format(port)
        self.newConnectionsQueue = Queue.Queue()

        self.clientIds = []
        self.clientsThreads = {}
        self.clientQueues = {}
        self.port = port
        self.ip = ip
        self.listenerThread = None

    @staticmethod
    def listenForConnections_thread_(newConnectionQueue, ip, port):
        serverSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            serverSoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serverSoc.bind((ip, port))
            serverSoc.listen(5)
            while True:
                newConnectionQueue.put(serverSoc.accept())
        finally:
            serverSoc.close()

    def startListening(self):
        print 'Server is now listening...'
        self.listenerThread = threading.Thread(target=self.listenForConnections_thread_, args=(self.newConnectionsQueue, self.ip, self.port))
        self.listenerThread.daemon = True
        self.listenerThread.start()

    def checkForNewConnections(self):
        while not self.newConnectionsQueue.empty():
            print 'Found {0} new connection'.format(self.newConnectionsQueue.qsize())
            connection, addr = self.newConnectionsQueue.get()
            clientId = 0 if len(self.clientIds) == 0 else max(self.clientIds) + 1
            self.clientIds.append(clientId)
            queues = {'sendQueue': Queue.Queue(),
                      'receiveQueue': Queue.Queue()}
            self.clientQueues[clientId] = queues
            client = Client(connection, addr, queues)
            client.daemon = True
            self.clientsThreads[clientId] = client
            client.start()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', default=None)
    parser.add_argument('-i', '--ip', default='localhost')
    parser.add_argument('-p', '--port', default=1024)
    args = parser.parse_args()

    ss = SocketServer(args.ip, args.port)
    ss.startListening()
    while True:
        ss.checkForNewConnections()
        for queueDict in ss.clientQueues.values():
            if not queueDict['receiveQueue'].empty():
                d = queueDict['receiveQueue'].get()
                with open('readData.file', 'a') as f:
                    f.write(d)
                print 'Read: {0}'.format(d)
            if args.data is not None:
                print 'Sending: {0}'.format(args.data)
                queueDict['sendQueue'].put(args.data)
            time.sleep(2)
