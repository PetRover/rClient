# rClient
Client side application for the Rover pet-bot

 All python code in rClient should be designed to use the rPyEnv virtual python environment. This will allow maximum cross-compatibility of the python code  
 The virtual environment can be enabled using the following command
 ```
 source rPyEnv/bin/activate
 ```

## Usage socketServer.py

 For standalone usage of the socketServer, start the server using:
 ```
 python socketServer.py -p<port> -d<data>
 ```
 Note that the 'port' and 'data' arguments are optional and default to 1024 and None respectively.
 This will start the server and it will begin listening for connection at localhost:port. Once a connection has been established, the server will refresh every second and display the data that has been received from the connection. At the same time, if the data argument was provided, the server will send the data to the connection.

## Usage socketClient.py
The socketClient can be started with the following command:
 ```
 python clientServer.py
 ```
 This will start the client and provide a looping prompt to end data that will then be sent to socket
 
