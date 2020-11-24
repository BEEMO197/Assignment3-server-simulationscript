import random
import requests
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json

clients_lock = threading.Lock()

players = []
OutLiarHighPlayers = []
OutLiarLowPlayers = []

gameLobbies = {'NumberOfLobbies' : 0, 'Lobbies' : []}

def GameSimulations(sock):
    playerCount = 0
    count = 0

    while True:
        data, addr = sock.recvfrom(8192)

        data = json.loads(data)
        
        if 'NumberOfGames' in data:
            count = data['NumberOfGames']

        else :
            if(data not in players):
                playerCount += 1
                players.append(data)

            else :
                playerCount = len(players)

            if(len(players) >= 3 or playerCount >= 3 or len(OutLiarHighPlayers) >= 3 or len(OutLiarLowPlayers) >= 3): 

                if(len(players) >= 3):
                    temp = 1
                    maxPlayer = len(players)
                    for player in players:
                        if ((int(player['EloPoints']) - int(players.__getitem__(temp)['EloPoints'])) > 100):
                            OutLiarHighPlayers.append(player)
                            players.remove(player)
                            maxPlayer -= 1

                        elif ((int(player['EloPoints']) - int(players.__getitem__(temp)['EloPoints'])) < -100):
                            OutLiarLowPlayers.append(player)
                            players.remove(player)
                            maxPlayer -= 1

                        else :
                            print("ok")
                            temp += 1
                        
                        if temp >= maxPlayer:
                            temp = 0
                            
                print(players)
                print(OutLiarHighPlayers)
                print(OutLiarLowPlayers)
                
                if(len(players) >= 3):
                    gameLobbies['Lobbies'].append({'GameID' : len(gameLobbies['Lobbies']) + 1, 'PlayersInLobby' : players, 'WinningPlayer' : {}})

                elif(playerCount >= 3):
                    gameLobbies['Lobbies'].append({'GameID' : len(gameLobbies['Lobbies']) + 1, 'PlayersInLobby' : players, 'WinningPlayer' : {}})

                elif(len(OutLiarHighPlayers) >= 3):
                    gameLobbies['Lobbies'].append({'GameID' : len(gameLobbies['Lobbies']) + 1, 'PlayersInLobby' : OutLiarHighPlayers, 'WinningPlayer' : {}})
                
                elif(len(OutLiarLowPlayers) >= 3):
                    gameLobbies['Lobbies'].append({'GameID' : len(gameLobbies['Lobbies']) + 1, 'PlayersInLobby' : OutLiarLowPlayers, 'WinningPlayer' : {}})

                gameLobbies['NumberOfLobbies'] = len(gameLobbies['Lobbies'])
                playerCount = 0

                # Decide Winner Randomly
                for i in range(count):
                    #print(gameLobbies)
                    # Send Winner to Client
                    print(i)
                    UpdatePlayerUrl = "https://ciupendb77.execute-api.us-east-1.amazonaws.com/default/UpdatePlayer?EloPointsUpdate="

                    #print(gameLobbies['Lobbies'].__getitem__(gameLobbies['NumberOfLobbies']  - 1))
                
                    winningPlayer = random.choice(random.choice(gameLobbies['Lobbies'])['PlayersInLobby'])

                    for item in gameLobbies['Lobbies'].__getitem__(gameLobbies['NumberOfLobbies']  - 1)['PlayersInLobby']:
                        print(item)
                        if(item is not winningPlayer):
                            item['EloPoints'] = str(int(item['EloPoints']) - 5)
                            requests.get(UpdatePlayerUrl + item['EloPoints'] + "&UserToUpdate=" + item['User_ID'])

                        else :
                            item['EloPoints'] = str(int(item['EloPoints']) + 15)
                            requests.get(UpdatePlayerUrl + item['EloPoints'] + "&UserToUpdate=" + item['User_ID'])
                            winningPlayer = item

                    gameLobbies['Lobbies'].__getitem__(gameLobbies['NumberOfLobbies']  - 1)['WinningPlayer'] = winningPlayer
                    sock.sendto(bytes(str(gameLobbies['Lobbies'].__getitem__(gameLobbies['NumberOfLobbies']  - 1)), "utf-8"), addr)

                players.clear()


def main():
   port = 12345
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.bind(('', port))

   start_new_thread(GameSimulations, (s,))
   while True:
      time.sleep(1)

if __name__ == '__main__':
   main()
