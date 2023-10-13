from socket import *
import json

serverName = "192.168.0.2"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def checkInt(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def checkFloat(num):
    try: 
        float(num)
        return True
    except ValueError:
        return False
    
class ClientInputs:
    def __init__(self, function, num1, num2, result=0):
        self.function = function
        self.num1 = num1
        self.num2 = num2
        self.result = result

    def __str__(self):
        return f"function: {self.function}, num1: {self.num1}, num2: {self.num2}, result: {self.result}"

while True:

    while True:
        functionInput = input("Choose your function (Add, Subtract, Random): ")
        if functionInput.lower() == "add" or functionInput.lower() == "subtract" or functionInput.lower() == "random":
           break
        else:
            print("Enter a valid function input")
            

    while True:
        num1 = input("Enter the first number: ")
        if checkInt(num1) or checkFloat(num1):
            num1 = int(num1)
            break
        else:
            print("Please enter a number, int or float")
            
    while True:
        num2 = input("Now enter the second number: ")

        if checkInt(num2) or checkFloat(num2):
            num2 = int(num2)
            break
        else:
            print("Please enter a number, int or float")

    inputObject = ClientInputs(functionInput, num1, num2)
    finishedInputs = json.dumps(inputObject.__dict__)

    clientSocket.send(finishedInputs.encode())
    response = clientSocket.recv(1024)
    print(response.decode())
    print("Result: ")
    resultFromServer = clientSocket.recv(1024)
    result = json.loads(resultFromServer)
    resultClassObject = ClientInputs(result["function"], result["num1"], result["num2"], result["result"])
    if resultClassObject.function.lower() == "add":
        print(f"{resultClassObject.num1} + {resultClassObject.num2} = {resultClassObject.result}")
    elif resultClassObject.function.lower() == "subtract":
        if resultClassObject.num1 < resultClassObject.num2:
            print(f"{resultClassObject.num2} - {resultClassObject.num1} = {resultClassObject.result}")
        else:
            print(f"{resultClassObject.num1} - {resultClassObject.num2} = {resultClassObject.result}")
    elif resultClassObject.function.lower() == "random":
        if resultClassObject.num1 < resultClassObject.num2:
            print(f"Random range from {resultClassObject.num1} to {resultClassObject.num2} = {resultClassObject.result}")
        else:
            print(f"Random range from {resultClassObject.num2} to {resultClassObject.num1} = {resultClassObject.result}")
    else:
        print("Something terrible has happened")

   
    while True:
        redo = input("Would you like to try again? y/n: ")
        if redo.lower() == "n":
            print("Goodbye Then")
            exit()
        elif redo.lower() == "y":
            break
        else:
            print("Please enter y for yes or n for no")

