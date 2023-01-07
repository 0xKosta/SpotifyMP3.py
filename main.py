import spotipy as sf
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl as yt
import json
import os
import time as t

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def intro():
    print(r'''  _____ ____   ___   ______  ____  _____  __ __  ___ ___  ____    ____  __ __ 
 / ___/|    \ /   \ |      ||    ||     ||  |  ||   |   ||    \  |    \|  |  |
(   \_ |  o  )     ||      | |  | |   __||  |  || _   _ ||  o  ) |  o  )  |  |
 \__  ||   _/|  O  ||_|  |_| |  | |  |_  |  ~  ||  \_/  ||   _/  |   _/|  ~  |
 /  \ ||  |  |     |  |  |   |  | |   _] |___, ||   |   ||  | __ |  |  |___, |
 \    ||  |  |     |  |  |   |  | |  |   |     ||   |   ||  ||  ||  |  |     |
  \___||__|   \___/   |__|  |____||__|   |____/ |___|___||__||__||__|  |____/      github.com/Buxx0
                                                                              ''')
    t.sleep(3)
def youtube_download(song):
    ydl = yt.YoutubeDL(
        {
        'outtmpl': f'/downloads/%(title)s.mp3',
        'format': 'bestaudio'
        }
    )
    with ydl:
        video = ydl.extract_info(f"ytsearch:{song}",
                                  download=False)
        result = video["entries"][0]
        clear()
        userResponse = input(f'''Found song: {result['title']}
Download this song? [Y/N]\n''')\
            .upper()
        while userResponse not in ["Y", "N"]:
            userResponse = input("Unknown option, please type Y or N.")\
                .upper()
        if userResponse == "N":
            return
        print("Downloading song!")
        ydl.extract_info(f"ytsearch:{song}",
                         download=True)
        clear()
        print("Song downloaded!")


def spotifySearch(client, track):
    client_credentials_manager = SpotifyClientCredentials(client_id=client['cid'], client_secret=client['secret'])
    sp = sf.Spotify(client_credentials_manager=client_credentials_manager)
    clear()
    track = sp.track(track)
    song = f"{track['artists'][0]['name']} - {track['name']}"
    print(f"Loaded track {track['name']} by {track['artists'][0]['name']}, searching YouTube.")
    youtube_download(song)


def saveClient(cid, secret):
    with open('user.json', 'w') as user_save:
        json.dump({"cid": cid, "secret": secret}, user_save)

def loadClient():
    if os.stat('user.json').st_size == 0:
        return None
    with open('user.json') as user_save:
        parsed_json = json.load(user_save)
    return parsed_json


def authorization():
    cid = input("Please input your Client ID:\n")
    secret = input("Please input your Client Secret:\n")
    save = input("Would you like to save these credentials? [Y/N]\n")\
        .upper()
    while save not in ["Y", "N"]:
        save = input("Unknown option, please input Y or N.\n")\
            .upper()
    if save == "Y":
        saveClient(cid, secret)
    return {"cid":cid,"secret":secret}

def exitChoice():
    choice = input("Would you like to download another track? [Y/N]\n")\
        .upper()
    while choice not in ["Y", "N"]:
        choice = input("Unknown option, please input Y or N.\n")\
            .upper()
    if choice == "Y":
        return False
    return True

def main():
    intro()
    savedClient = loadClient()
    if savedClient == None:
        savedClient = authorization()
    else:
        print(f"Loaded Client ID: {savedClient['cid']} and Secret: {savedClient['secret']}")
    exit = False
    while not exit:
        track = input("Please paste the URL of the track you'd like to download.\n")
        spotifySearch(savedClient, track)
        exit = exitChoice()
        clear()
    print("Exiting in 3 seconds...")
    t.sleep(3)


main()
