from socket import *
import threading
from threading import *
from random import randint 
import json

def isJson(j):
    try:
        json.loads(j)
        return True
    except TypeError:
        return False

def isInt(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('192.168.0.2', serverPort))
serverSocket.listen(5)
print('Server is ready to listen')

class ClientInputs:
    def __init__(self, function, num1, num2, result=0):
        self.function = function
        self.num1 = num1
        self.num2 = num2
        self.result = result

    def __str__(self):
        return f"function: {self.function}, num1: {self.num1}, num2: {self.num2}, result: {self.result}"

def handleClient(connectionSocket, adress):
   
    while True:

        try: 
            clientJson = connectionSocket.recv(1024).decode()
            print(f"Client: {adress} sent: {clientJson}")

            if not clientJson:
                break
            if isJson(clientJson) == True:
                response = "Input Valid"
            else:
                response = "Invalid Input, Try again"
                break
            connectionSocket.send(response.encode())        
            
            clientDict = json.loads(clientJson)
            clientFunction = clientDict["function"]
            clientNum1 = clientDict["num1"]
            clientNum2 = clientDict["num2"]

            if not clientNum1 or not clientNum2:
                break

            if isInt(clientNum1) == False:
                num1 = float(clientNum1)
            else:
                num1 = int(clientNum1)

            if isInt(clientNum2) == False:
                num2 = float(clientNum2)
            else:
                num2 = int(clientNum2)
               
            str(clientFunction)
            

            def calculateInputs(function, num1, num2):

                if function.lower() == "random":

                    if num1 < num2:
                        randResult = randint(num1, num2)
                        return randResult
                    else:
                        randResult = randint(num2, num1)
                        return randResult
                elif function.lower() == "subtract":
                    if num1 < num2:
                        subResult = num2 - num1
                        return subResult
                    else:
                        subResult = num1 - num2
                        return subResult
                elif function.lower() == "add":
                    addResult = num1 + num2
                    return addResult
                else:
                    return "invalid function input"

            resultObject = ClientInputs(clientFunction, clientNum1, clientNum2, calculateInputs(clientFunction, num1, num2))
            print("sending:(", resultObject, f") to {adress}")
            finishedResult = json.dumps(resultObject.__dict__)
            connectionSocket.send(finishedResult.encode())
            
        except ConnectionAbortedError:
                   
            break

        except ConnectionResetError:
            
            
            break

    connectionSocket.close()
    print(f"Connection with {adress} closed")
       
while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target = handleClient,args = (connectionSocket, addr)).start()
    print(f"Client Connected: {addr}")
