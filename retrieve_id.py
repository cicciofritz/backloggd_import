import requests, time

#personal authentication data stored in auth.py file present in .gitignore, consider to use that file instead
try:
   from auth import client_id, client_secret 
except:
   client_id = "host_id"
   client_secret = "host_secret"
   
#Authenticate using Twitch credential
response = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials")
data = response.json()

#check authentication procedure
try:
   if data['access_token']:
      print("Authentication OK")
except:
   raise ValueError("Authentication Failed") #exit on error

headers = {'Client-ID': client_id, 'Authorization': f'Bearer {data["access_token"]}'}

with open('game.csv') as file:
    for line in file:
        game=line.rstrip()
        response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=f'fields name; search "{game}";')
        data = response.json()
        print(data)
        time.sleep(1)
        
   
