import requests, time, sqlite3, pathlib, platform

#personal authentication data stored in auth.py file present in .gitignore, consider to use that file instead
try:
   from auth import client_id, client_secret 
except:
   client_id = "guest_id"
   client_secret = "guest_secret"
   
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

f_out = open('game_id.csv', 'wt')
f_err = open('game_err.csv', 'wt')

with open('game.csv') as file:
    for line in file:
        game=line.rstrip()
        response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=f'fields name; search "{game}";')
        data = response.json()
        
        try:
           #if more than 1 element is available a prompt is presented to the user to make a choice
           if len(data) > 1:
              i = 1
              games = list(data)
              for el in games:
                 print(f'{i} | {el["name"]}')
                 i += 1
           
              x = input('Choose a version: ')
              try:
                 y = int(x)
                 if y > len(data):
                    raise ValueError('Input outside the range')
              except ValueError as e:
                 print(f'Input not valid: {e}')
              f_out.write(f'{(games[y-1])['id']}; {(games[y-1])['name']}\n')
           else:
              f_out.write(f'{data['id']}; {data['name']}\n')
        except:
           print(f'Game {game} not found')
           f_err.write(f'{game}\n')
           
f_out.close()
f_err.close()


# POST request to backloggd section

try:
   from auth import py_session_token, py_user_token, py_csrf_token, py_userid
except:
   py_session_token = 'guest_session_token'
   py_user_token = 'guest_user_token'
   py_csrf_token = 'guest_csrf_token'
   py_userid = 'guest_userid'
   py_username='guest_username'

#on linux environment try to catch cookie information from firefox default path
if platform.system() == 'Linux':
   for p in pathlib.Path(f'{pathlib.Path.home()}/.mozilla/firefox').rglob("cookies.sqlite"):
      try:
         dbfile = p.resolve()
         #print(dbfile)
         con = sqlite3.connect(dbfile)
         cur = con.cursor()
         cur.execute("select * from moz_cookies where host = '.backloggd.com'")
         results = (cur.fetchall())[0]
         cookie = dict(zip(results[::2], results[1::2]))
         py_user_token = cookie['remember_user_token']
         print(cookie['remember_user_token'])
         con.close()
      except:
         continue
else:
   print('Not already available on Windows and MacOS')


with open('game_id.csv') as file:
   for line in file:
      game=line.rstrip()
      py_gameid, py_name = game.split(';')

      py_url = f'https://www.backloggd.com/api/user/{py_userid}/log/{py_gameid}'
      #notice is_backlog%5D=true field, next action is to customize with played/rank
      py_dataraw = f'game_id={py_gameid}&log%5Bis_play%5D=false&log%5Bis_playing%5D=false&log%5Bis_backlog%5D=true&log%5Bis_wishlist%5D=false&log%5Bstatus%5D=completed&log%5Bid%5D=&modal_type=quick'
      #py_dataraw = f'type=backlog&game_id={py_gameid}'

      py_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0', 'Accept': '*/*', 'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Referer': f'https://www.backloggd.com/u/{py_username}/', 'Origin': 'https://www.backloggd.com', 'Connection': 'keep-alive', 'Cookie': f'_backloggd_session={py_session_token}; ne_cookies_consent=true; remember_user_token={py_user_token}', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'no-cors', 'Sec-Fetch-Site': 'same-origin', 'X-CSRF-Token': py_csrf_token, 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'Priority': 'u=4', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
      
      response = requests.post(py_url, data=py_dataraw, headers=py_headers)
      print(response)
      time.sleep(1)













        
   
