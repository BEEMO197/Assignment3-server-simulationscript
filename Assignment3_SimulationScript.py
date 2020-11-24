import random
import requests
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json

players = {"Players" : []}

def GetGameResults(sock):

    while True:
        data, addr = sock.recvfrom(1024)

        print(str(data))

def main():
    addr = "52.203.158.53"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((addr, port))

    start_new_thread(GetGameResults, (s,))

    numPlayers = int(input("How Manny Players : "))
    
    numGames = int(input("How Many Games? : "))

    GetPlayersUrl = "https://ciupendb77.execute-api.us-east-1.amazonaws.com/default/GetTableItems"
    AddPersonUrl = "https://ciupendb77.execute-api.us-east-1.amazonaws.com/default/AddTableItem"
    
    PlayerTable = requests.get(GetPlayersUrl)
    PlayerTableBody = json.loads(PlayerTable.content)

    print(len(PlayerTableBody['Items']))

    toSend = {"NumberOfGames" : 0, "Players" : []}
    toSend['NumberOfGames'] = numGames

    if ( numPlayers > len(PlayerTableBody['Items']) ):

        if len(PlayerTableBody['Items']) > 0:
            for item in PlayerTableBody['Items']:
                toSend['Players'].append(item)

        else :
            for count in range(numPlayers - len(PlayerTableBody['Items'])):
                newPerson = requests.get(AddPersonUrl)
                newPersonBody = json.loads(newPerson.content)

                player = newPersonBody['Item']
                print("New Player Created: " + str(player))
                toSend["Players"].append(player)

    else:
        itemCount = 0
        for item in PlayerTableBody['Items']:
            if(itemCount >= numPlayers):
                break
            toSend['Players'].append(item)
            itemCount += 1

        s.send(bytes(json.dumps(toSend), "utf-8"))

    for item in toSend['Players']:
        s.send(bytes(json.dumps(item), "utf-8"))
        time.sleep(0.5)

    while True:
        time.sleep(0)

main()